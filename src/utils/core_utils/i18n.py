# src/utils/i18n.py
import yaml
from pathlib import Path
import os
import threading
from typing import Dict, Any, Optional
from src import setup_logger

log = setup_logger(__name__)

_translator_instance = None
_translator_lock = threading.Lock()

class Translator:
    def __init__(self, locales_dir: Path = None):
        if locales_dir is None:
            locales_dir = Path(os.getcwd()) / "locales"
            
        self.translations: Dict[str, Dict[str, Any]] = {}
        
        if not locales_dir.is_dir():
            log.warning(f"Locales directory not found: {locales_dir}")
            return
        
        for lang_file in locales_dir.glob("*.yaml"):
            lang_code = lang_file.stem.lower()      # Get language code from filename (e.g., zh-tw)
            try:
                data = yaml.safe_load(lang_file.read_text(encoding="utf-8"))
                
                if isinstance(data, dict) and lang_code in data:
                    self.translations[lang_code] = data.get(lang_code, {}) # Use data[lang_code]
                elif isinstance(data, dict):
                    self.translations[lang_code] = data
                else:
                    print(f"Warning: Could not load translation data from {lang_file}. Unexpected format.")
                
            except FileNotFoundError:
                 print(f"Error: Language file not found: {lang_file}")
            except yaml.YAMLError as e:
                print(f"Error loading YAML file {lang_file}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred loading {lang_file}: {e}")

    def t(self, lang: str, key: str, **kwargs) -> str:
        # key is like "system.startup"
        lang_code = lang.lower()
        lang_data = self.translations.get(lang_code)
        
        if not isinstance(lang_data, dict):
            log.debug(f"Language data not found for {lang}. Using default English translations.")
            lang_data = self.translations.get("en-us", {})
        
        parts = key.split(".")
        value: Any = lang_data
        
        for part in parts:
            if not isinstance(value, dict):
                # Path leads to a non-dictionary value before reaching the end
                log.warning(f"Key path '{key}' invalid at part '{part}' for lang '{lang}'. Expected dict, got {type(value)}.")
                return key
            
            value = value.get(part)
            
            if value is None:
                # Key part not found
                log.warning(f"Key part '{part}' not found in path '{'.'.join(parts[:parts.index(part) + 1])}' for lang '{lang}'.")
                return key
            
        if not isinstance(value, str):
            log.warning(f"Value for key '{key}' in lang '{lang}' is not a string. Got {type(value)}.")
            return key
        
        if kwargs:
            try:
                return value.format(**kwargs)
            except (KeyError, ValueError) as e:
                return value
        else:
            return value

def get_translator(locales_dir: Path = None):
    """
    Get the unique Translator instance.
    If the instance does not exist, create a new one.
    Read the language setting from the environment variable LANG.
    """
    global _translator_instance
    
    with _translator_lock:
        if _translator_instance is None:
            _translator_instance = Translator(locales_dir=locales_dir)
            
    return _translator_instance
