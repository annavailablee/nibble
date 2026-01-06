"""Evaluator for nibble's behavior and decision making"""
from config import (
    XP_PER_5MINUTES,
    XP_ERROR_FIXED,
    XP_REFLECTION,
)

class Evaluator:

    def evaluate(self, metrics: dict) -> dict:
        """
        Input: 
            metrics = {
                "session_minutes": int,
                "errors_before": int
                "errors_after": int,
                "lines_added": int,
                "lines_deleted": int,
                "reflections_done": bool
                }
        Output:
            signals = {
                "xp_gained": int,
                "fixed_error": bool,
                "long_session": bool
                }
        """

        signals={
            "xp_gained": 0,
            "fixed_error": False,
            "long_session": False
        }
        
        # XP from session duration
        minutes = metrics.get("session_minutes", 0)
        xp_from_time = (minutes // 5) * XP_PER_5MINUTES
        signals["xp_gained"] += xp_from_time

        if minutes >= 25: 
            signals["long_session"] = True

        # XP from fixing errors
        if metrics.get("errors_before", 0) > metrics.get("errors_after", 0):
            signals["fixed_error"] = True
            signals["xp_gained"] += XP_ERROR_FIXED

        # XP from reflections
        if metrics.get("reflections_done", False):
            signals["xp_gained"] += XP_REFLECTION
            
        return signals