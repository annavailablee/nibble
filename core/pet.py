"""nibble's state and evolution"""

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
        pass

    def evolve(self):
        """checks if XP threshold met and evolves nibble to next stage"""
        pass

    def status(self) -> dict: 
        """return nibble's current status"""
        return {
            'stage': self.stage,
            'xp': self.xp,
            'history': self.history
        }