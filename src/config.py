import yaml
import logging
import os

from .log import setup_logger

log = setup_logger(__name__)

class AppConfig:
    """
    Loads application configuration from YAML files.
    """
    def __init__(
        self,
        base_setting_config_path: str = "configs/base_setting.yaml",
        personality_config_path: str = "configs/personality.yaml",
        exception_message_config_path: str = "configs/exception_message.yaml",
        role_settings_config_path: str = "configs/role_settings.yaml"
    ):
        self._base_setting_config_path = base_setting_config_path
        self._personality_config_path = personality_config_path
        self._exception_message_config_path = exception_message_config_path
        self._role_settings_config_path = role_settings_config_path
        
        # base setting default settings
        self.enable_timestamp_prompt: bool = True
        self.enable_weather_period_prompt: bool = True
        self.model_default_temperature: float = 1.0

        # personality default settings
        self.system_prompt: str = "You are a friendly AI assistant."
        self.summarization_prompt: str = "Please summarize the following conversation:\n"
        self.rag_prompt_prefix: str = "Relevant memories:\n{relevant_memories}\n---\n"
        
        # exception message default settings
        # conversation
        self.no_response_exception: str = "Sorry, I'm having trouble processing your request at the moment. Please try again later."
        self.unknown_exception: str = "Oops, an unexpected error occurred while processing your message. I've logged the details."
        
        # gemini service
        self.content_moderation_error: str = "Sorry, I cannot process this request, it may have triggered safety restrictions."
        self.unknown_response_error: str = "Sorry, an error occurred and I could not generate a response."
        self.service_error: str = "Sorry, I'm having a little trouble thinking, please try again later."
        
        # role settings
        self.user_role: str = "user"
        self.model_role: str = "model"

        self._load_configs()

    def _load_yaml_config(self, file_path: str, config_name: str) -> dict:
        """Helper to load a single YAML file with error handling."""
        config_data = {}
        if not os.path.exists(file_path):
            log.warning(f"{config_name} config file not found at {file_path}. Using default settings.")
            return config_data # Return empty dict if file doesn't exist
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                if config_data is None:
                    log.warning(f"{config_name} config file at {file_path} is empty. Using default settings.")
                    return {} # Return empty dict if file is empty
            log.info(f"{config_name} config loaded successfully from {file_path}.")
            return config_data
        except yaml.YAMLError as e:
            log.error(f"Error decoding YAML from {file_path} for {config_name}: {e}. Using default settings.")
            return {} # Return empty dict on YAML error

    def _load_configs(self):
        """Loads all necessary configuration files."""
        # Load base config
        self.base_setting_data = self._load_yaml_config(self._base_setting_config_path, "Base setting")
        self.enable_timestamp_prompt = self.base_setting_data.get("enable_timestamp_prompt", self.enable_timestamp_prompt)
        self.enable_weather_period_prompt = self.base_setting_data.get("enable_weather_period_prompt", self.enable_weather_period_prompt)
        self.model_default_temperature = self.base_setting_data.get("model_default_temperature", self.model_default_temperature)
        
        # Load personality config
        personality_data = self._load_yaml_config(self._personality_config_path, "Personality")
        self.system_prompt = personality_data.get("system_prompt", self.system_prompt)
        self.summarization_prompt = personality_data.get("summarization_prompt", self.summarization_prompt)
        self.rag_prompt_prefix = personality_data.get("rag_prompt_prefix", self.rag_prompt_prefix)

        # Load exception message config
        exception_message_data = self._load_yaml_config(self._exception_message_config_path, "Exception message")
        # conversation
        conversation_data = exception_message_data.get("conversation", {})
        self.no_response_exception = conversation_data.get("NO_RESPONSE_EXCEPTION", self.no_response_exception)
        self.unknown_exception = conversation_data.get("UNKNOWN_EXCEPTION", self.unknown_exception)
        
        # gemini service
        gemini_service_data = exception_message_data.get("gemini_service", {})
        self.content_moderation_error = gemini_service_data.get("CONTENT_MODERATION_ERROR", self.content_moderation_error)
        self.unknown_response_error = gemini_service_data.get("UNKNOWN_RESPONSE_ERROR", self.unknown_response_error)
        self.service_error = gemini_service_data.get("SERVICE_ERROR", self.service_error)
        
        # role settings
        role_settings_data = self._load_yaml_config(self._role_settings_config_path, "Role settings")
        self.user_role = role_settings_data.get("user_role", self.user_role)
        self.model_role = role_settings_data.get("model_role", self.model_role)
