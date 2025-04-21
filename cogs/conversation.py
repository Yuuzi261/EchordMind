# cogs/conversation.py
import discord
from discord.ext import commands
from src import setup_logger
import os
from src import AppConfig
from src.llm import LLMServiceInterface
from src.memory_service import MemoryService
from src.llm.factory import get_llm_service
from src.vector_store.factory import get_vector_store

log = setup_logger(__name__)

class ConversationCog(commands.Cog):
    def __init__(self, bot: commands.Bot, llm_service: LLMServiceInterface, memory_service: MemoryService, config: AppConfig):
        self.bot = bot
        self.llm_service = llm_service
        self.memory_service = memory_service
        self.system_prompt = config.system_prompt           # load AI personality settings
        # load exception message settings
        self.no_response_exception = config.no_response_exception
        self.unknown_exception = config.unknown_exception
        

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
                    rag_context=relevant_memories
                )

                # --- response and memory update ---
                if bot_response:
                    # send response
                    await message.author.send(bot_response)
                    log.info(f"Sent response to user {user_id}: {bot_response[:50]}...")

                    # update short-term memory (user input + bot response)
                    await self.memory_service.add_message(user_id, "user", user_input)
                    await self.memory_service.add_message(user_id, "model", bot_response) # Gemini 的角色是 model

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


async def setup(bot: commands.Bot):
    """Cog's entry point, used for loading the Cog"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        log.error("GEMINI_API_KEY not found in environment variables!")
        raise ValueError("GEMINI_API_KEY is required.")

    config = AppConfig(
        personality_config_path="configs/personality.yaml",
        exception_message_config_path="configs/exception_message.yaml"
    )

    vector_db_path = "data/"                    # set the path to the ChromaDB persistence path

    try:
        llm_service = get_llm_service(llm_name="gemini", api_key=api_key, model_name="gemini-2.5-flash-preview-04-17", embedding_model_name="gemini-embedding-exp-03-07", config=config)
        vector_store = get_vector_store(vector_store_name="chroma", path=vector_db_path)
        memory_service = MemoryService(llm_service, vector_store, config)
        await bot.add_cog(ConversationCog(bot, llm_service, memory_service, config))
        log.info("ConversationCog added successfully.")
    except Exception as e:
        log.error(f"Failed to initialize services or add ConversationCog: {e}", exc_info=True)