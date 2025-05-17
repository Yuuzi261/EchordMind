import discord
from discord.ext import commands
from discord import app_commands
from src import setup_logger
import os
from datetime import datetime
from core import Cog_Extension
from src import AppConfig
from src.llm import LLMServiceInterface
from src.memory_service import MemoryService
from src.utils.core_utils import get_localized_choices, get_localized_name_from_value
from src import split_markdown_message
from src.llm.factory import get_llm_service
from src.embedding.factory import get_embedding_service
from src.vector_store.factory import get_vector_store

log = setup_logger(__name__)

BINARY_STATES = ['enable', 'disable']
TEMPERATURE_LEVELS = [
    "ultra_stable", "very_stable", "stable", "moderate", "slightly_flexible",
    "balanced", "creative", "highly_creative", "extremely_creative",
    "beyond_imagination", "crazy_mode"
]

BINARY_STATES_CALCULATOR = lambda i, val: 1 - i                     # enable --> 1, disable --> 0
TEMPERATURE_LEVELS_CALCULATOR = lambda i, val: round(i * 0.2, 1)    # 0.2 is the step size


class ConversationCog(Cog_Extension):
    def __init__(self, bot: commands.Bot, llm_service: LLMServiceInterface, memory_service: MemoryService, config: AppConfig):
        super().__init__(bot)                
        self.llm_service = llm_service
        self.memory_service = memory_service
        self.system_prompt = config.system_prompt           # load AI personality settings
        
        # load exception message settings
        self.no_response_exception = config.no_response_exception
        self.unknown_exception = config.unknown_exception
        
        # load role settings
        self.user_role = config.user_role
        self.model_role = config.model_role
        
        # dynamic settings
        # TODO: In the future, these values ​​should be made into dictionaries to support multi-user scenarios
        self.temperature = config.model_default_temperature
        self.use_search = False
        

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is not None:
            return                                          # Currently only supports private messages

        if message.author.bot:
            return

        if not message.content:
            log.info(f"Ignoring message from {message.author.id} because it has no text content.")
            # await message.author.send("Please enter text message and chat with me.")
            return


        user_id = str(message.author.id)
        user_input = message.content
        user_input_timestamp = datetime.now().isoformat()

        log.info(f"Received DM from user {user_id}: {user_input[:50]}...")

        async with message.channel.typing(): # show "typing..."
            try:
                # --- memory processing ---
                # 1. retrieve relevant memories (RAG)
                relevant_memories = await self.memory_service.retrieve_relevant_memories(user_id, user_input)
                if relevant_memories is not None: log.info(f"Retrieved relevant memories for user {user_id}: {relevant_memories[:100]}...")

                # 2. get short-term history
                short_term_history = self.memory_service.get_history(user_id)
                log.info(f"Retrieved short-term history for user {user_id}. Length: {len(short_term_history)}")
                

                # --- LLM API calling ---
                bot_response = await self.llm_service.generate_response(
                    system_prompt=self.system_prompt,
                    history=short_term_history,
                    user_input=user_input,
                    rag_context=relevant_memories,
                    temperature=self.temperature,
                    use_search=self.use_search
                )

                # --- response and memory update ---
                if bot_response:
                    # send response
                    chunk_size = 2000   # Discord message limit is 2000 characters
                    if len(bot_response) > 2000:
                        chunks = split_markdown_message(bot_response, chunk_size)
                        for chunk in chunks:
                            await message.author.send(chunk)
                    else:
                        await message.author.send(bot_response)
                    
                    bot_response_timestamp = datetime.now().isoformat()
                    log.info(f"Sent response to user {user_id}: {bot_response[:50]}...")

                    # update short-term memory (user input + bot response)
                    await self.memory_service.add_message(user_id, self.user_role, user_input, user_input_timestamp)
                    await self.memory_service.add_message(user_id, self.model_role, bot_response, bot_response_timestamp)

                else:
                    # if LLM API returns no valid response
                    await message.author.send(self.no_response_exception)
                    log.warning(f"LLMService returned None or empty response for user {user_id}.")

            except Exception as e:
                log.error(f"Error processing message from user {user_id}: {e}", exc_info=True)
                try:
                    await message.author.send(self.unknown_exception)
                except discord.errors.Forbidden:
                     log.error(f"Cannot send error message to user {user_id} (DM closed or blocked).")

    toggle_group = app_commands.Group(name='toggle', description='Toggle something')

    @toggle_group.command(name='search')
    async def toggle_search(self, itn: discord.Interaction, state: int):
        """Toggle search functionality

        Parameters
        -----------
        state: int
            Whether to enable or disable search functionality.
        """
        self.use_search = bool(state)
        
        choice_name = get_localized_name_from_value(itn, state, BINARY_STATES, 'binary_state', BINARY_STATES_CALCULATOR)
        await itn.response.send_message(f"Search functionality {choice_name}.", ephemeral=True)
        
    temporary_subgroup = app_commands.Group(name="temporary", description="Subgroup of toggle group", parent=toggle_group)
    
    @temporary_subgroup.command(name='chat')
    async def toggle_temporary_chat(self, itn: discord.Interaction, state: int):
        """Toggle temporary chat functionality

        Parameters
        -----------
        state: int
            Whether to enable or disable temporary chat functionality.
        """
        self.memory_service.temporary_chat_mode(str(itn.user.id), bool(state))
        
        choice_name = get_localized_name_from_value(itn, state, BINARY_STATES, 'binary_state', BINARY_STATES_CALCULATOR)
        await itn.response.send_message(f"Temporary chat functionality {choice_name}.", ephemeral=True)
        
    @toggle_group.command(name='temperature')
    @app_commands.rename(temperature="level")
    async def toggle_temperature(self, itn: discord.Interaction, temperature: float):
        """Toggle the creativity level of LLM's response

        Parameters
        -----------
        temperature: float
            The temperature level of LLM's response.
        """
        self.temperature = temperature
        
        choice_name = get_localized_name_from_value(itn, temperature, TEMPERATURE_LEVELS, 'temperature_level', TEMPERATURE_LEVELS_CALCULATOR)
        await itn.response.send_message(f"Temperature level set to {choice_name}.", ephemeral=True)
    
    @toggle_search.autocomplete('state')
    @toggle_temporary_chat.autocomplete('state')
    async def autocomplete_toggle_state(self, itn: discord.Interaction, current: str):
        return get_localized_choices(itn, current, BINARY_STATES, 'binary_state', BINARY_STATES_CALCULATOR)
        
    @toggle_temperature.autocomplete('temperature')
    async def autocomplete_temperature_level(self, itn: discord.Interaction, current: str):
        return get_localized_choices(itn, current, TEMPERATURE_LEVELS, 'temperature_level', TEMPERATURE_LEVELS_CALCULATOR)


async def setup(bot: commands.Bot):
    """Cog's entry point, used for loading the Cog"""

    config = AppConfig()

    vector_db_path = os.getenv("VECTOR_DB_PATH") or "data/"                    # set the path to the ChromaDB persistence path

    try:
        use_llm_service = config.default_llm_service
        use_embedding_service = config.default_embedding_service
        llm_service = get_llm_service(service_name=use_llm_service, model_name=config.default_model[use_llm_service], config=config)
        embedding_service = get_embedding_service(service_name=use_embedding_service, embedding_model_name=config.default_embedding_model[use_embedding_service])
        vector_store = get_vector_store(vector_store_name="chroma", path=vector_db_path)
        memory_service = MemoryService(llm_service, embedding_service, vector_store, config)
        await bot.add_cog(ConversationCog(bot, llm_service, memory_service, config))
        log.info("ConversationCog added successfully.")
    except Exception as e:
        log.error(f"Failed to initialize services or add ConversationCog: {e}", exc_info=True)