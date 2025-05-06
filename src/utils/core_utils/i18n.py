# src/utils/i18n.py
import yaml
from pathlib import Path
import os
import threading

_translator_instance = None
_translator_lock = threading.Lock()

class Translator:
    def __init__(self, lang: str, locales_dir: Path = None):
        if locales_dir is None:
            locales_dir = Path(os.getcwd()) / "locales"
        data = yaml.safe_load((locales_dir / f"{lang}.yaml").read_text(encoding="utf-8"))
        self.strings = data.get(lang, data)

    def t(self, key: str, **kwargs) -> str:
        # key is like "system.startup"
        template = self.strings
        for part in key.split("."):
            template = template.get(part, {})
        if not isinstance(template, str):
            return key
        if kwargs:
            return template.format(**kwargs)
        else:
            return template

def get_translator(locales_dir: Path = None):
    """
    Get the unique Translator instance.
    If the instance does not exist, create a new one.
    Read the language setting from the environment variable LANG.
    """
    global _translator_instance
    
    with _translator_lock:
        if _translator_instance is None:
            lang = os.getenv("LANG", "en")
            _translator_instance = Translator(lang=lang, locales_dir=locales_dir)
            
    return _translator_instance
