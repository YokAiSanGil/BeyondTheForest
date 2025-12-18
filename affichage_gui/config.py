import json
import os

SETTINGS_FILE = "settings.json"

class GameConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameConfig, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
        
        # Valeurs par défaut
        self.enable_scanlines = True
        self.enable_flicker = False
        self.debug_force_hermit = False
        
        self.load()
        self.initialized = True

    def to_dict(self):
        return {
            "enable_scanlines": self.enable_scanlines,
            "enable_flicker": self.enable_flicker,
            "debug_force_hermit": self.debug_force_hermit
        }

    def save(self):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.to_dict(), f, indent=4)
        except Exception as e:
            print(f"Erreur sauvegarde settings: {e}")

    def load(self):
        if not os.path.exists(SETTINGS_FILE):
            return
        
        try:
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                self.enable_scanlines = data.get("enable_scanlines", True)
                self.enable_flicker = data.get("enable_flicker", True)
                self.debug_force_hermit = data.get("debug_force_hermit", False)
        except Exception as e:
            print(f"Erreur chargement settings: {e}")

    def toggle(self, setting_name):
        if hasattr(self, setting_name):
            setattr(self, setting_name, not getattr(self, setting_name))
            self.save()
