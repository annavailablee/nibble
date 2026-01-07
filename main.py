"""entry point for the application"""
from core.pet import Nibble
from core.evaluator import Evaluator
from visuals import show_nibble
from core.pet import Nibble
import time
signals = {}
def simulate_session(): 
    #Create pet and evaluator
    evaluator = Evaluator()
    nibble, history = Nibble.load_state()
    nibble.history = history
    MIN_SESSION_GAP = 5 * 60  # 5 minutes

    can_gain_xp = True

    if hasattr(nibble, "last_active") and nibble.last_active:
        time_since_last = time.time() - nibble.last_active
        if time_since_last < MIN_SESSION_GAP:
            can_gain_xp = False

    BONUS_XP = 1    
    RETURN_THRESHOLD = 60 * 60 * 6  # 6 hours

    notification = None

    if hasattr(nibble, "last_active") and nibble.last_active:
        time_away = time.time() - nibble.last_active
        if time_away > RETURN_THRESHOLD:
            nibble.xp += BONUS_XP
            notification = "🐾 Welcome back! Nibble gained +1 XP"

    #fake session metrics
    session_metrics = {
        "session_minutes": 30,
        "errors_before": 5,
        "errors_after": 2,
        "lines_added": 50,
        "lines_deleted": 10,
        "reflections_done": True
    }
    

    #Evaluate session to get signals
    if can_gain_xp:
        signals = evaluator.evaluate(session_metrics)
        nibble.apply_signals(signals)
    else:
        print("⏳ Session too short. No XP gained.")

    nibble.save_state()

    stage_before = nibble.stage
    stage_after = nibble.stage

    if stage_before != stage_after:
        print(f"✨ Nibble evolved into {stage_after.capitalize()}!")


    #Print nibble status
    print("\n 🐾Nibble Status After Session: ")
    status = nibble.status()

    print("\n 📜History\n")
    for entry in reversed(nibble.history):
        print(entry, "\n")

    #Explain nibble state
    explanation = nibble.explain_state()
    print("\n 🐾 Nibble State Explanation: ")
    print(explanation)

    # Show the nibble stage visualizer
    next_stage = nibble.get_next_stage()
    show_nibble(nibble, notification=notification)

    nibble.save_state()
if __name__ == "__main__":
    simulate_session()