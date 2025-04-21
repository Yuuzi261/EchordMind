from abc import ABC, abstractmethod
from typing import List, Optional

class VectorStoreInterface(ABC):
    """
    Vector store interface, defining core functionalities for a vector database.
    Any class implementing this interface must provide methods for initialization, adding memories, and searching memories.
    """
    
    @abstractmethod
    def __init__(self, path: str):
        """
        initialize the vector store
        
        parameters:
            path: vector store path
        """
        pass
    
    @abstractmethod
    async def add_memory(self, user_id: str, text: str, embedding: List[float]):
        """
        Add a memory to the vector database.

        Parameters:
            user_id: User identifier.
            text: Memory text content.
            embedding: Vector embedding representation of the text.
        """
        pass
    
    @abstractmethod
    async def search_memory(self, user_id: str, query_embedding: List[float], n_results: int = 3) -> List[str]:
        """
        Search for relevant memories based on the query embedding.

        Parameters:
            user_id: User identifier.
            query_embedding: Vector embedding representation of the query text.
            n_results: Number of results to return.

        Returns:
            A list of relevant memory texts.
        """
        pass