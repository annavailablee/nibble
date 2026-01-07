"""nibble's state and evolution"""
from config import STAGE_THRESHOLD
import json
class Nibble: 
    STAGES = ['baby', 'child', 'teen', 'adult', 'elder']

    def __init__(self, stage='baby', xp=0):
        if stage not in self.STAGES:
            raise ValueError(f"Invalid stage: {stage}. Must be one of {self.STAGES}.")
        self.stage = stage
        self.xp = xp
        self.history = []
    
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
            'stage': self.stage,
            'xp': self.xp,
            'history': self.history
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4) 
    
    @classmethod
    def load_state(cls, filepath= "data/nibble_state.json"):
        """load nibble's state from a file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return cls( 
                stage=data.get('stage', 'baby'),
                xp=data.get('xp', 0)
            ), data.get('history', [])
        except FileNotFoundError:
            return cls(), []