from .gemini_service import GeminiAssistant
from .grok_service import GrokAssistant
from .base import LLMService

def get_llm_service(llm_name: str, **kwargs) -> LLMService:
    api_key = kwargs["api_key"]
    model_name = kwargs["model_name"]
    embedding_model_name = kwargs["embedding_model_name"]
    config = kwargs["config"]
    match llm_name:
        case "gemini":
            # system_instruction = kwargs["system_instruction"]
            return GeminiAssistant(api_key=api_key, model_name=model_name, embedding_model_name=embedding_model_name, config=config)
        case "grok":
            return GrokAssistant(api_key=api_key, model_name=model_name, embedding_model_name=embedding_model_name, config=config)
        case _:
            raise ValueError(f"Unknown LLM name: {llm_name}")
        