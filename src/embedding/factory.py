import os

from .gemini_service import GeminiEmbeddingService
from .base import EmbeddingServiceInterface

def get_embedding_service(service_name: str, **kwargs) -> EmbeddingServiceInterface:
    embedding_model_name = kwargs["embedding_model_name"]
    match service_name:
        case "gemini":
            return GeminiEmbeddingService(api_key=os.getenv("GEMINI_API_KEY"), embedding_model_name=embedding_model_name)
        case _:
            raise ValueError(f"Unknown Embedding name: {service_name}")