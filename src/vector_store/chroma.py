import chromadb
from chromadb.config import Settings
from src import setup_logger
from typing import List, Optional
from .base import VectorStoreInterface

log = setup_logger(__name__)

class ChromaVectorStore(VectorStoreInterface):
    def __init__(self, path: str = "./data/chroma_db"):
        try:
            # TODO: Further investigation into these settings is needed.
            # Set up ChromaDB for persistent storage on disk
            self.client = chromadb.PersistentClient(path=path, settings=Settings(anonymized_telemetry=False))
            # Get or create a collection, similar to a table in a database
            # Note: If using Gemini embedding, the dimension might be 768 or 1024 (needs confirmation)
            # ChromaDB usually handles dimension automatically, but specifying embedding_function is more reliable
            # metadata={"hnsw:space": "cosine"} indicates using cosine similarity
            self.collection = self.client.get_or_create_collection(
                name="user_memories",
                metadata={"hnsw:space": "cosine"} # Use cosine similarity
                # embedding_function=chromadb.utils.embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key="YOUR_GEMINI_API_KEY")
                # Note: If specifying the embedding function here, you don't need to pass embedding during add
            )
            log.info(f"ChromaDB client initialized. Collection 'user_memories' loaded/created at {path}.")
        except Exception as e:
            log.error(f"Failed to initialize ChromaDB: {e}")
            raise

    async def add_memory(self, user_id: str, text: str, embedding: List[float]):
        """add a memory to the vector database"""
        if not embedding:
            log.warning(f"Skipping adding memory for user {user_id} due to missing embedding.")
            return
        try:
            # TODO: Consider using a better ID generation method in the future (low priority for personal use).
            # Use user_id and a unique identifier (e.g., text hash or timestamp) as the ID.
            # Here we simply use the text hash, but note that collisions are possible; a better approach is to use a UUID.
            doc_id = f"{user_id}_{hash(text)}"
            self.collection.add(
                embeddings=[embedding],
                documents=[text],
                metadatas=[{"user_id": user_id}],
                ids=[doc_id]
            )
            log.debug(f"Memory added for user {user_id}: {text[:50]}...")
        except Exception as e:
            log.error(f"Error adding memory to ChromaDB for user {user_id}: {e}")

    async def search_memory(self, user_id: str, query_embedding: List[float], n_results: int = 3) -> List[str]:
        """Search relevant memories based on the query embedding"""
        if not query_embedding:
            log.warning(f"Skipping memory search for user {user_id} due to missing query embedding.")
            return []
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where={"user_id": user_id} # Only search memories for a specific user
            )
            # log.debug(f"Memory search results for user {user_id}: {results}")
            # results['documents'] is a list of lists, we need the first list
            return results['documents'][0] if results and results['documents'] else []
        except Exception as e:
            log.error(f"Error searching memory in ChromaDB for user {user_id}: {e}")
            return []