import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRANSLATIONS_PATH = BASE_DIR / 'resources' / 'translations.json'


class LanguageManager:
    """Load translations and print text by message id."""

    def __init__(self, language='pl', enabled=True):
        self.language = language
        self.enabled = enabled
        self.translations_path =  TRANSLATIONS_PATH
        self._messages = {}
        self._load_translations()

    def _load_translations(self):
        """Load translations from JSON and keep only id -> text mapping."""
        try:
            with open(self.translations_path, encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self._messages = {}
            return

        language_list = data.get(self.language, [])
        self._messages = {
            item['id']: item['text']
            for item in language_list
            if 'id' in item and 'text' in item
        }

    def set_enabled(self, enabled: bool):
        """Enable or disable printing of messages."""
        self.enabled = enabled

    def get_text(self, message_id):
        """Return text for a message id or None if not found."""
        return self._messages.get(message_id)

    def print_by_id(self, message_id, **kwargs):
        """Print the text for a message id, formatted by kwargs, if printing is enabled."""
        if not self.enabled:
            return None

        text = self.get_text(message_id)
        if text is None:
            return None

        try:
            text = text.format(**kwargs)
        except Exception:
            pass

        print(text)
        return text

    def input_by_id(self, prompt_id, **kwargs):
        """Read user input after printing a prompt from translations by prompt id."""
        if not self.enabled:
            return None

        prompt_text = self.get_text(prompt_id)
        if prompt_text is None:
            prompt_text = ""

        try:
            prompt_text = prompt_text.format(**kwargs)
        except Exception:
            pass

        return input(prompt_text)

