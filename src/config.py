import yaml
import logging
import os

from .log import setup_logger

log = setup_logger(__name__)

class AppConfig:
    """
    Loads application configuration from YAML files.
    """
    def __init__(self, personality_config_path: str = "configs/personality.yaml", exception_message_config_path: str = "configs/exception_message.yaml"):
        self._personality_config_path = personality_config_path
        self._exception_message_config_path = exception_message_config_path

        # personality default settings
        self.system_prompt: str = "You are a friendly AI assistant."
        self.summarization_prompt: str = "Please summarize the following conversation:\n"
        self.rag_prompt_prefix: str = "Relevant memories:\n{relevant_memories}\n---\n"
        
        # exception message default settings
        self.no_response_exception: str = "Sorry, I'm having trouble processing your request at the moment. Please try again later."
        self.unknown_exception: str = "Oops, an unexpected error occurred while processing your message. I've logged the details."

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
        # Load personality config
        personality_data = self._load_yaml_config(self._personality_config_path, "Personality")
        self.system_prompt = personality_data.get("system_prompt", self.system_prompt)
        self.summarization_prompt = personality_data.get("summarization_prompt", self.summarization_prompt)
        self.rag_prompt_prefix = personality_data.get("rag_prompt_prefix", self.rag_prompt_prefix)

        # Load exception message config
        exception_message_data = self._load_yaml_config(self._exception_message_config_path, "Exception message")
        self.no_response_exception = exception_message_data.get("NO_RESPONSE_EXCEPTION", self.no_response_exception)
        self.unknown_exception = exception_message_data.get("UNKNOWN_EXCEPTION", self.unknown_exception)
