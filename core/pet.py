"""nibble's state and evolution"""
from config import STAGE_THRESHOLD
class Nibble: 
    STAGES = ['egg', 'baby', 'child', 'teen', 'adult', 'elder']

    def __init__(self, stage='egg', xp=0):
        if stage not in self.STAGES:
            raise ValueError(f"Invalid stage: {stage}. Must be one of {self.STAGES}.")
        self.stage = stage
        self.xp = xp
        self.history = []

    def apply_signals(self, signals: dict):
        """update nibble's state based on external signals"""
        xp = signals.get('xp_gained', 0)
        self.xp += xp
        # simple history log
        self.history.append({
            'xp_gained': xp,
            'new_total_xp': self.xp,
            'stage': self.stage,
            'signals': signals
        })

    def evolve(self):
        """checks if XP threshold met and evolves nibble to next stage"""
        if self.stage == 'egg': 
            if self.xp >= STAGE_THRESHOLD.get('baby', float('inf')):
                self.stage = 'baby'
        elif self.stage == 'baby':
            if self.xp >= STAGE_THRESHOLD.get('child', float('inf')):
                self.stage = 'child'
        elif self.stage == 'child':
            if self.xp >= STAGE_THRESHOLD.get('teen', float('inf')):
                self.stage = 'teen'
        elif self.stage == 'teen':
            if self.xp >= STAGE_THRESHOLD.get('adult', float('inf')):
                self.stage = 'adult'
        elif self.stage == 'adult':
            if self.xp >= STAGE_THRESHOLD.get('elder', float('inf')):
                self.stage = 'elder'

    def status(self) -> dict: 
        """return nibble's current status"""
        return {
            'stage': self.stage,
            'xp': self.xp,
            'history_length': len(self.history)
        }