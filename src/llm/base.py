from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any

class LLMServiceInterface(ABC):
    """
    Abstract base class, defines the common interface for LLM services.
    Classes implementing this interface can integrate with different LLM providers, such as Gemini, Claude, GPT, etc.
    """
    
    @abstractmethod
    def __init__(self, api_key: str):
        """
        Initialize the LLM service.
        
        Args:
            api_key: Access token for the LLM API.
        """
        pass
    
    @abstractmethod
    async def generate_response(self, system_prompt: str, history: List[Dict[str, str]], user_input: str, rag_context: Optional[str] = None, temperature: float = 1.0, use_search: bool = False) -> Optional[str]:
        """
        Generate a response to a conversation.
        
        Args:
            system_prompt: System prompt, defining the behavior and limitations of the AI assistant.
            history: Conversation history list, each item contains 'role' and 'content'.
            user_input: The current user input.
            rag_context: Optional context for search-enhanced generation.
            
        Returns:
            The generated response text, or None or an error message if failed.
        """
        pass
    
    @abstractmethod
    async def summarize_conversation(self, conversation_history: str, summarization_prompt: str) -> Optional[str]:
        """
        Use the LLM to summarize the conversation content.
        
        Args:
            conversation_history: The text of the conversation to be summarized.
            summarization_prompt: The prompt template for guiding the LLM on how to summarize.
            
        Returns:
            The summarized conversation content, or None if failed.
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
    
    @abstractmethod
    def _format_history(self, history: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Format the internal history record to the specific format accepted by the LLM API.
        
        Args:
            history: The standard format of the conversation history record.
            
        Returns:
            The formatted history record for the specific LLM API format.
        """
        pass
