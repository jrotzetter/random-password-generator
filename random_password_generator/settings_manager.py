import os
import json

class SettingsManager:
    def __init__(self):
        self.settings = None

    def save_settings(self):
        if self.settings:
            with open("settings.json", "w") as f:
                json.dump(self.settings, f)

    def load_settings(self):
        if not os.path.isfile("settings.json"):
            with open("settings.json", "w") as f:
                json.dump({
                    "exclude_chars": "",
                    "appearance_mode": "System",
                    "scaling": "100%"
                    }, f)

        with open("settings.json", "r") as f:
            self.settings = json.load(f)
