from src import setup_logger
from collections import deque
from typing import List, Dict, Optional, Tuple
from src import AppConfig
from src.llm import LLMServiceInterface
from src.embedding import EmbeddingServiceInterface
from src.vector_store import VectorStoreInterface

from src.utils.i18n import get_translator
from src.utils.core_utils import insert_timestamp, create_system_message

log = setup_logger(__name__)

class MemoryService:
    def __init__(self, llm_service: LLMServiceInterface, embedding_service: EmbeddingServiceInterface, vector_store: VectorStoreInterface, config: AppConfig):
        self.llm_service = llm_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        # Use a dictionary to store short-term memory for each user {user_id: deque}
        self.short_term_memory: Dict[str, deque] = {}
        self.temporary_chat_memory: Dict[str, deque] = {}   # for temporary chat mode
        # Set the maximum length of short-term memory (number of conversation turns)
        # TODO The triggering mechanism needs further adjustment.
        self.max_history_length = 20  # For example, keep the last 10 conversation turns (user+bot)
        # Set the conversation length threshold to trigger summarization
        self.summarization_threshold = 16  # Trigger summarization when the conversation reaches 8 turns
        # Number of memories to retrieve for RAG
        self.rag_n_results = 3

        # load config settings
        self.summarization_prompt = config.summarization_prompt
        self.rag_prompt_prefix = config.rag_prompt_prefix
        
        self.lang = config.model_lang
        self.tr = get_translator()
        
        # dynamic settings
        self.use_temporary_chat: Dict[str, bool] = {}


    def _get_user_memory(self, user_id: str) -> deque:
        """get or create the specified user's short-term memory deque"""
        is_temporary_chat = self.use_temporary_chat.get(user_id, False)
        user_memory = self.temporary_chat_memory if is_temporary_chat else self.short_term_memory

        if user_id not in user_memory:
            user_memory[user_id] = deque(maxlen=self.max_history_length)
            kind = "short-term" if not is_temporary_chat else "temporary"
            log.info(f"Initialized {kind} memory for user {user_id}.")
        return user_memory[user_id]

    async def add_message(self, user_id: str, role: str, content: str, timestamp: str = None):
        """add a message to the short-term memory and trigger summarization check"""
        user_memory = self._get_user_memory(user_id)
        user_memory.append({"role": role, "content": content, "timestamp": timestamp})
        log.debug(f"Added message to short-term memory for user {user_id}. New length: {len(user_memory)}")
        if not self.use_temporary_chat.get(user_id, False):
            await self.check_and_summarize(user_id) # Check if summarization is needed after adding the message

    def get_history(self, user_id: str) -> List[Dict[str, str]]:
        """get the current short-term history record of the user"""
        user_memory = self._get_user_memory(user_id)
        return list(user_memory)

    # TODO This function's mechanism still needs significant optimization
    async def check_and_summarize(self, user_id: str):
        """check the conversation length and summarize if needed"""
        user_memory = list(self._get_user_memory(user_id))
        if len(user_memory) >= self.summarization_threshold:
            log.info(f"Summarization threshold reached for user {user_id}. Current length: {len(user_memory)}")

            # Extract the part that needs summarizing (e.g., all dialogue except the most recent turns)
            # This simply summarizes the entire current deque and then replaces the old one.
            # A more optimized method would be to only summarize the oldest part.
            history_to_summarize = insert_timestamp(user_memory, self.tr.t(self.lang, 'prompt.timestamp_format'))
            history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history_to_summarize])

            summary = await self.llm_service.summarize_conversation(history_text, self.summarization_prompt)

            if summary:
                log.info(f"Generated summary for user {user_id}: {summary[:100]}...")
                # 1. Store the summary in long-term memory (vector database)
                summary_embedding = await self.embedding_service.get_embedding(summary)
                if summary_embedding:
                    await self.vector_store.add_memory(user_id, self.tr.t(self.lang, 'prompt.conversation_summary', summary=summary), summary_embedding)
                    log.debug(f"Summary stored in vector store for user {user_id}.")

                # 2. Update short-term memory: Keep the summary and the most recent turns
                # For example, keep the summary and the most recent 4 turns of conversation
                keep_recent_n = 4
                new_memory = deque(maxlen=self.max_history_length)
                # TODO: Re-evaluate the use of summary as mid-term memory.
                # TODO: The current approach conflicts with the insert_timestamp function.
                # TODO: Exception handling could solve this timestamp conflict.
                # TODO: However, adding a system role prompt to the history is not a wise choice.
                # TODO: Therefore, the original intention is temporarily commented out.
                # new_memory.append(create_system_message(f"Previous conversation summary: {summary}"))  # Add the summary as a system message
                if len(user_memory) > keep_recent_n:
                    for msg in user_memory[-keep_recent_n:]:
                        new_memory.append(msg)
                else: # If history length is less than keep_recent_n, keep all
                     for msg in user_memory:
                        new_memory.append(msg)


                self.short_term_memory[user_id] = new_memory
                log.info(f"Short-term memory updated with summary for user {user_id}. New length: {len(new_memory)}")
            else:
                log.warning(f"Failed to generate summary for user {user_id}. Short-term memory not modified by summarization.")


    async def retrieve_relevant_memories(self, user_id: str, query: str) -> Optional[str]:
        """retrieve and format the relevant memories based on the current query"""
        log.debug(f"Retrieving relevant memories for user {user_id} based on query: {query[:50]}...")
        query_embedding = await self.embedding_service.get_embedding(query)
        if not query_embedding:
            log.warning(f"Could not get embedding for query for user {user_id}.")
            return None

        relevant_docs = await self.vector_store.search_memory(user_id, query_embedding, n_results=self.rag_n_results)

        if relevant_docs:
            # log.info(f"Found {len(relevant_docs)} relevant memories for user {user_id}.")
            # Format the retrieved documents as RAG context
            context = "\n".join([f"- {doc}" for doc in relevant_docs])
            formatted_rag_context = self.rag_prompt_prefix.format(relevant_memories=context)
            log.debug(f"Formatted RAG context for user {user_id}: {formatted_rag_context[:100]}...")
            return formatted_rag_context
        else:
            # log.info(f"No relevant memories found for user {user_id}.")
            return None
        
    def temporary_chat_mode(self, user_id: str, state: bool):
        """set the temporary chat mode state for a specific user and clear temporary history if exiting"""
        log.info(f"Setting temporary chat mode for user {user_id} to {state}")
        self.use_temporary_chat[user_id] = state # Update the user's state
        
        if not state:
            if user_id in self.temporary_chat_memory:
                del self.temporary_chat_memory[user_id] # Clear the temporary chat memory
                log.info(f"Cleared temporary chat memory for user {user_id}")
            else:
                log.debug(f"User {user_id} exited temporary mode, but no temporary history was found to clear.")
    