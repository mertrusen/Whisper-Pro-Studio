import json
import os

class PresetManager:
    def __init__(self):
        self.preset_file = os.path.join(os.path.expanduser("~"), "whisper_presets.json")
        self.config_file = os.path.join(os.path.expanduser("~"), "whisper_config.json")
        self.presets = self.load_presets()
        
    def load_presets(self):
        if os.path.exists(self.preset_file):
            try:
                with open(self.preset_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except: pass
        return {"Standart (Türkçe)": {"model": "large-v3", "lang": "tr - Türkçe", "format": "srt", "word_ts": True}}

    def save_presets(self):
        try:
            with open(self.preset_file, "w", encoding="utf-8") as f:
                json.dump(self.presets, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving presets: {e}")

    def add_preset(self, name, config):
        self.presets[name] = config
        self.save_presets()

    def delete_preset(self, name):
        if name in self.presets:
            del self.presets[name]
            self.save_presets()
            
    def load_last_session(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except: pass
        return {}

    def save_last_session(self, config):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving session: {e}")
