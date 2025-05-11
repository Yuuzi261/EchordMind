import os

from .gemini_service import GeminiAssistant
from .grok_service import GrokAssistant
from .base import LLMServiceInterface

def get_llm_service(service_name: str, **kwargs) -> LLMServiceInterface:
    model_name = kwargs["model_name"]
    config = kwargs["config"]
    match service_name:
        case "gemini":
            # system_instruction = kwargs["system_instruction"]
            return GeminiAssistant(api_key=os.getenv("GEMINI_API_KEY"), model_name=model_name, config=config)
        case "grok":
            return GrokAssistant(api_key=os.getenv("GROK_API_KEY"), model_name=model_name, config=config)
        case _:
            raise ValueError(f"Unknown LLM name: {service_name}")
        