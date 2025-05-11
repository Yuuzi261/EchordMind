import asyncio
from google import genai
from google.genai import types, errors
from google.genai.types import Tool, GoogleSearch
from src import setup_logger
from src.utils.i18n import get_translator
from src.utils.core_utils import insert_timestamp, create_system_message
from src.utils.integrations import weather_period_reporter
from src import AppConfig
from typing import List, Dict, Optional
from .base import LLMServiceInterface

log = setup_logger(__name__)

class GeminiAssistant(LLMServiceInterface):
    DEFAULT_GENERATION_MODEL = "gemini-2.0-flash"
    
    def __init__(self, api_key: str, model_name: str, config: AppConfig):
        try:
            self.client = genai.Client(api_key=api_key)
            log.info("Google Generative AI configured successfully.")
        except Exception as e:
            log.error(f"Failed to configure Google Generative AI: {e}")
            raise
        
        self.generation_model = self._validate_model(model_name, "generation", self.DEFAULT_GENERATION_MODEL)
        
        self.lang = config.model_lang
        self.enable_timestamp_prompt = config.enable_timestamp_prompt
        self.enable_weather_period_prompt = config.enable_weather_period_prompt
        
        self.content_moderation_error = config.content_moderation_error
        self.unknown_response_error = config.unknown_response_error
        self.service_error = config.service_error
        
        self.google_search_tool = Tool(google_search=GoogleSearch())
        
        self.tr = get_translator()
        

    async def generate_response(self, system_prompt: str, history: List[Dict[str, str]], user_input: str, rag_context: Optional[str] = None, temperature: float = 1.0, use_search: bool = False) -> Optional[str]:
        try:
            # Construct the complete context
            full_history = [create_system_message(system_prompt)]
            if rag_context:
                rag_msg = self.tr.t(self.lang, 'prompt.long_term_memory', rag_context=rag_context)
                full_history.append(create_system_message(rag_msg)) # Inject RAG context as a system message
            
            sep = self.tr.t(self.lang, 'prompt.history_separator')
            full_history.append(create_system_message(sep))
           
            if self.enable_timestamp_prompt:
                timestamped_history = insert_timestamp(history, self.tr.t(self.lang, 'prompt.timestamp_format'))    # Insert timestamp to the history record
                full_history.extend(timestamped_history)                                                            # Insert the conversation history after the RAG context (if present)
            else:
                full_history.extend(history)
            
            if self.enable_weather_period_prompt:
                date, period, weather = await weather_period_reporter('Asia/Taipei', lang=self.lang, location='Taipei') # TODO: time zone and location should be configurable
                full_history.append(create_system_message(self.tr.t(self.lang, 'prompt.weather_period_info_format', date=date, period=period, weather=weather)))

            system_instruction = self._format_history(full_history)
            log.debug(f"system instruction: {system_instruction}")
            
            # Configure generation
            gemini_config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature
            )
            if use_search:
                gemini_config.tools = [self.google_search_tool]
                gemini_config.response_modalities = ["TEXT"]

            max_retries = 3
            retry_delay_seconds = 5
            
            for attempt in range(max_retries):
                try:
                    # Call the Gemini API to generate response
                    response = await self.client.aio.models.generate_content(
                        model=self.generation_model,
                        config=gemini_config,
                        contents=user_input
                    )

                    # check if response is empty
                    if response.text:
                        return response.text
                    elif response.prompt_feedback:
                        log.warning(f"Gemini call blocked or failed. Feedback: {response.prompt_feedback}")
                        return self.content_moderation_error
                    else:
                        log.error(f"Gemini returned an empty response or unexpected format: {response}")
                        return self.unknown_response_error
                except errors.ServerError as e:
                    # catch ServerError and retry if necessary
                    log.warning(f"ServerError on attempt {attempt + 1}: {e}")
                    if e.code == 503 and attempt < max_retries - 1:
                        log.info(f"Retrying in {retry_delay_seconds} seconds...")
                        await asyncio.sleep(retry_delay_seconds)
                    elif e.code == 503 and attempt == max_retries - 1:
                        log.error(f"Max retries reached for 503 ServerError: {e}", exc_info=True)
                        return self.service_error
                    else:
                        log.error(f"Non-retryable ServerError on attempt {attempt + 1}: {e}", exc_info=True)
                        return self.service_error

        except Exception as e:
            log.error(f"Error generating response from Gemini: {e}", exc_info=True)
            # TODO consider more fine-grained error handling, e.g., API rate limit
            return self.service_error

    async def summarize_conversation(self, conversation_history: str, summarization_prompt: str) -> Optional[str]:
        """use the LLM to summarize the conversation content"""
        log.debug(f"Summarizing conversation history: {conversation_history}")
        try:
            response = await self.client.aio.models.generate_content(
                model=self.generation_model,
                config=types.GenerateContentConfig(
                    system_instruction=summarization_prompt,
                    temperature=0.1
                ),
                contents=conversation_history
            )
            if response.text:
                log.info("Summarization successful.")
                log.info(f"Summarization result: {response.text}...")
                return response.text
            elif response.prompt_feedback:
                log.warning(f"Gemini summarization blocked. Feedback: {response.prompt_feedback}")
                return None # or return an error message
            else:
                log.error(f"Gemini summarization returned empty response: {response}")
                return None
        except Exception as e:
            log.error(f"Error summarizing conversation with Gemini: {e}", exc_info=True)
            return None
        
    def _validate_model(self, model_name: str, model_type: str, default_model: str) -> str:
        """check if the specified model is available, otherwise use the default model"""
        try:
            self.client.models.get(model=model_name)
            log.info(f"{model_type.capitalize()} model '{model_name}' validated successfully.")
            return model_name
        except:
            log.warning(
                f"{model_type.capitalize()} model '{model_name}' is not available. "
                f"Using default model '{default_model}'."
            )
            return default_model
        
    def _format_history(self, history: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """transform internal history record to the format accepted by the Gemini API"""
        formatted = []
        for item in history:
            if item['role'] == 'system':
                formatted.append(item['content'])
            else:
                formatted.append(f"{item['role']}: {item['content']}")
        return formatted