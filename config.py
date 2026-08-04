import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULT_CONFIG = {
    "lm_studio": {
        "url": "http://localhost:1234/v1",
        "selected_model": "",
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "wordpress": {
        "url": "",
        "username": "",
        "application_password": "",
        "default_status": "draft"  # 'draft' or 'publish'
    },
    "social_accounts": {
        "facebook": {"enabled": False, "page_id": "", "access_token": ""},
        "instagram": {"enabled": False, "account_id": "", "access_token": ""},
        "twitter": {"enabled": False, "api_key": "", "api_secret": "", "access_token": "", "access_secret": ""},
        "linkedin": {"enabled": False, "author_urn": "", "access_token": ""}
    },
    "trend_watcher": {
        "keywords": ["Intelligence Artificielle", "Réseaux Sociaux", "Marketing Digital", "Technologie"],
        "rss_feeds": [
            "https://news.google.com/rss?hl=fr&gl=FR&ceid=FR:fr",
            "https://www.presse-citron.net/feed/"
        ]
    }
}

class ConfigManager:
    def __init__(self, filepath=CONFIG_FILE):
        self.filepath = filepath
        self.data = self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            self.save(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return self._merge_defaults(data, DEFAULT_CONFIG)
        except Exception as e:
            print(f"[ConfigManager] Erreur chargement config ({e}), utilisation des paramètres par défaut.")
            return DEFAULT_CONFIG.copy()

    def _merge_defaults(self, target, source):
        merged = target.copy()
        for key, value in source.items():
            if key not in merged:
                merged[key] = value
            elif isinstance(value, dict) and isinstance(merged[key], dict):
                merged[key] = self._merge_defaults(merged[key], value)
        return merged

    def save(self, data=None):
        if data is not None:
            self.data = data
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            print(f"[ConfigManager] Configuration sauvegardée dans {self.filepath}")
        except Exception as e:
            print(f"[ConfigManager] Erreur sauvegarde: {e}")

    def get(self, section, key=None, default=None):
        section_data = self.data.get(section, {})
        if key is None:
            return section_data
        return section_data.get(key, default)

    def set(self, section, key, value):
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
        self.save()
