"""nibble's state and evolution"""
import time
from config import STAGE_THRESHOLD
import json

class Nibble: 
    def get_next_stage(self):
        if self.stage == "elder":
           return None

        current_index = self.STAGES.index(self.stage)
        return self.STAGES[current_index + 1]
    
    STAGES = ['baby', 'child', 'teen', 'adult', 'elder']

    def __init__(self, stage='baby', xp=0, dev_mode=False):
        if stage not in self.STAGES:
            raise ValueError(f"Invalid stage: {stage}. Must be one of {self.STAGES}.")
        self.stage = stage
        self.xp = xp
        self.history = []
        self.dev_mode = dev_mode
        self.last_session_time = None
    
    def update_stage(self):
        for stage, threshold in STAGE_THRESHOLD.items():
            if self.xp >= threshold:
                self.stage = stage

    def apply_signals(self, signals: dict):
        """update nibble's state based on external signals"""
        xp = signals.get('xp_gained', 0)
        self.xp += xp

        old_stage = self.stage
        self.update_stage()

        # simple history log
        self.history.append({
            'xp_gained': xp,
            'new_total_xp': self.xp,
            'stage_before': old_stage,
            'stage_after': self.stage,
            'signals': signals
        })
        STAGE_XP_MODIFIER = {
            "baby": 1.0,
            "child": 0.6,
            "teen": 0.4,
            "adult": 0.25,
            "elder": 0.0
        }   
        xp = int(signals.get("xp_gained", 0) * STAGE_XP_MODIFIER[self.stage])
        self.xp += xp


    def status(self) -> dict: 
        """return nibble's current status"""
        return {
            'stage': self.stage,
            'xp': self.xp,
            'history_length': len(self.history)
        }
    def explain_state(self) -> str:
        """explain nibble's current state"""
        explanation = f"Nibble is currently at stage '{self.stage}' with {self.xp} XP."
        if self.stage != 'elder':
            next_stage = self.STAGES[self.STAGES.index(self.stage) + 1]
            next_threshold = STAGE_THRESHOLD.get(next_stage, 'N/A')
            explanation += f" Needs {next_threshold - self.xp} more XP to evolve to '{next_stage}'."
        else:
            explanation += " Nibble has reached the final stage."
        return explanation
    
    def save_state(self, filepath= "data/nibble_state.json"):
        """save nibble's state to a file"""
        data = {
            "stage": self.stage,
            "xp": self.xp,
            "history": self.history,
            "last_active": time.time(),
            "last_session_time": self.last_session_time,
            "dev_mode": self.dev_mode
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4) 
    
    def get_stage_message(self):
        messages = {
            "baby": "Nibble is curious and learning every day 🐣",
            "child": "Nibble is playful and full of energy 🐾",
            "teen": "Nibble is figuring things out and testing limits 😼",
            "adult": "Nibble is confident and focused 💼🐕",
            "elder": "Nibble is wise and content 🌟"
        }
        return messages.get(self.stage, "")

    @classmethod
    def load_state(cls, filepath="data/nibble_state.json"):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            nibble = cls(
                stage=data.get("stage", "baby"),
                xp=data.get("xp", 0),
                dev_mode=data.get("dev_mode", False)
            )
            nibble.history = data.get("history", [])
            nibble.last_active = data.get("last_active", None)
            nibble.last_session_time = data.get("last_session_time", None)

            return nibble, nibble.history

        except FileNotFoundError:
            print("DEBUG: No saved state found. Creating new Nibble.")
            nibble = cls()
            return nibble, []

        except Exception as e:
            print("DEBUG: Failed to load state:", e)
            nibble = cls()
            return nibble, []

    def get_stage_progress(self, stage_thresholds):
        next_stage = self.get_next_stage()
        if next_stage is None:
            return None, None

        current_threshold = stage_thresholds[self.stage]
        next_threshold = stage_thresholds[next_stage]
        return current_threshold, next_threshold