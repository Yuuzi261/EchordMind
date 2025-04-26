# src/utils/i18n.py
import yaml
from pathlib import Path
import os

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
