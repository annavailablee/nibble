"""entry point for the application"""

import time
from core.pet import Nibble
from core.evaluator import Evaluator
from visuals import show_nibble


DEV_MODE = True

if DEV_MODE:
    XP_COOLDOWN = 0          # no cooldown
    XP_MULTIPLIER = 1.0
    RETURN_THRESHOLD = 1     # seconds (testing)
    BONUS_XP = 5
else:
    XP_COOLDOWN = 10 * 60    # 10 minutes
    XP_MULTIPLIER = 0.25
    RETURN_THRESHOLD = 6 * 60 * 60  # 6 hours
    BONUS_XP = 1



def simulate_session():
    evaluator = Evaluator()

    nibble, history = Nibble.load_state()
    nibble.history = history

    if DEV_MODE:
        print("🧪 DEV MODE ENABLED")

    now = time.time()
    notification = None

    last_active = getattr(nibble, "last_active", None)
    if last_active and now - last_active > RETURN_THRESHOLD:
        nibble.xp += BONUS_XP
        notification = f"🐾 Welcome back! Nibble gained +{BONUS_XP} XP"

    last_xp_time = getattr(nibble, "last_xp_time", 0)
    can_gain_xp = DEV_MODE or (now - last_xp_time >= XP_COOLDOWN)

    session_metrics = {
        "session_minutes": 30,
        "errors_before": 5,
        "errors_after": 2,
        "lines_added": 50,
        "lines_deleted": 10,
        "reflections_done": True
    }

    stage_before = nibble.stage

    if can_gain_xp:
        signals = evaluator.evaluate(session_metrics)
        signals["xp_gained"] = int(signals.get("xp_gained", 0) * XP_MULTIPLIER)
        nibble.apply_signals(signals)
        nibble.last_xp_time = now
    else:
        print("⏳ Session too short. No XP gained.")

    stage_after = nibble.stage

    if stage_before != stage_after:
        print(f"✨ Nibble evolved into {stage_after.capitalize()}!")

    nibble.last_active = now
    nibble.save_state()

    print("\n 🐾 Nibble Status After Session:")
    print(nibble.status())

    print("\n 📜 History\n")
    for entry in reversed(nibble.history):
        print(entry, "\n")

    print("\n 🐾 Nibble State Explanation:")
    print(nibble.explain_state())

    show_nibble(nibble, notification=notification)


if __name__ == "__main__":
    simulate_session()
