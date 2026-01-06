"""Evaluator for nibble's behavior and decision making"""
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
                "meaningful_edit": bool,
                "long_session": bool
                }
        """

        signals={}
        #logic

        return signals