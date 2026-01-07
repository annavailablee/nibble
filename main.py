"""entry point for the application"""
from core.pet import Nibble
from core.evaluator import Evaluator
from visuals import show_nibble
def simulate_session(): 
    #Create pet and evaluator
    nibble = Nibble(stage='baby', xp=0)
    evaluator = Evaluator()
    nibble, history = nibble.load_state()
    nibble.history = history
 
    #fake session metrics
    session_metrics = {
        "session_minutes": 30,
        "errors_before": 5,
        "errors_after": 2,
        "lines_added": 50,
        "lines_deleted": 10,
        "reflections_done": True
    }
    nibble.save_state()

    #Evaluate session to get signals
    signals = evaluator.evaluate(session_metrics)

    nibble.update_stage()

    #Apply signals to nibble
    nibble.apply_signals(signals)

    old_stage = nibble.history[-1]["stage_before"]
    new_stage = nibble.stage

    if old_stage != new_stage:
        print(f"✨ Nibble evolved into {new_stage.capitalize()}!")

    #Print nibble status
    print("\n 🐾Nibble Status After Session: ")
    status = nibble.status()

    print("\n 📜History\n")
    for entry in nibble.history:
        print(entry, "\n")

    #Explain nibble state
    explanation = nibble.explain_state()
    print("\n 🐾Nibble State Explanation: ")
    print(explanation)

    # Show the nibble stage visualizer
    next_stage = nibble.get_next_stage()
    show_nibble(nibble)


if __name__ == "__main__":
    simulate_session()