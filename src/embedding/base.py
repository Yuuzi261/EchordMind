from abc import ABC, abstractmethod
from typing import List, Optional

class EmbeddingServiceInterface(ABC):
    """
    Abstract base class, defines the common interface for Embedding Services.
    Classes implementing this interface can integrate with different Embedding Model Providers, such as Gemini, Claude, GPT, etc.
    """
    
    @abstractmethod
    def __init__(self, api_key: str):
        """
        Initialize the Embedding Service.
        
        Args:
            api_key: Access token for the Embedding Model API.
        """
        pass
    
    @abstractmethod
    async def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get the embedding vector of the text.
        
        Args:
            text: The text to be converted to an embedding vector.
            
        Returns:
            The embedding vector (list of floats), or None if failed.
        """
        pass
    
    @abstractmethod
    def _validate_model(self, model_name: str, model_type: str, default_model: str) -> str:
        """
        Checks if the specified model is available and returns the default model if not.
        
        Args:
            model_name: The name of the model to validate.
            model_type: The type of the model (e.g., 'generation', 'embedding'), used for logging or validation context.
            default_model: The default model to use if the specified model is unavailable.
        Returns:
            The available model name. Returns `model_name` if it is valid, otherwise returns `default_model`.
        Raises:
            NotImplementedError: This method must be implemented by concrete subclasses.
        """
        pass
