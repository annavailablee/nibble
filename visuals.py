"""Visual representation of Nibble's state"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk # type: ignore
import os
from config import STAGE_THRESHOLD

def show_nibble(nibble): 
    root = tk.Tk()
    root.title("Nibble 🐾")
    root.geometry("400x480")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    pet_frame = tk.Frame(main_frame)
    pet_frame.pack(pady=5)

    stats_frame = tk.Frame(main_frame)
    stats_frame.pack(pady=5)

    progress_frame = tk.Frame(main_frame)
    progress_frame.pack(pady=5)
 

    # image path based on stage
    img_path = os.path.join("assets", f"{nibble.stage}.png")
    img = Image.open(img_path)
    img = img.resize((300, 300), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    img_label = tk.Label(pet_frame, image=tk_img)
    img_label.image = tk_img
    img_label.pack(pady=10)
    # stats
    stage_label = tk.Label(stats_frame, text=f"Stage: {nibble.stage.capitalize()}", font=("Arial", 16, "bold"))
    stage_label.pack(pady=10)

    xp_label = tk.Label(stats_frame, text=f"XP: {nibble.xp}", font=("Arial", 14))
    xp_label.pack(pady=5)

    if nibble.stage != "elder":
        stages = list(STAGE_THRESHOLD.keys())
        next_stage = stages[stages.index(nibble.stage) + 1]
        xp_needed = STAGE_THRESHOLD[next_stage] - nibble.xp
        next_label = tk.Label(root, text=f" {xp_needed} XP needed for next stage {next_stage.capitalize()}", font=("Arial", 12))
        next_label.pack(pady=5)
    else:
        final_label = tk.Label(root, text="Nibble has reached the final stage!", font=("Arial", 12))
        final_label.pack(pady=5)

    history_label = tk.Label(root, text=f"Sessions logged: {len(nibble.history)}", font=("Arial", 12))
    history_label.pack(pady=10)

    progress_label = tk.Label(progress_frame, text="Progress loading...", font=("Arial", 12), fg="gray")
    if nibble.stage != "elder":
        next_stage = list(STAGE_THRESHOLD.keys())[list(STAGE_THRESHOLD.keys()).index(nibble.stage) + 1]
        xp_needed = STAGE_THRESHOLD[next_stage] - nibble.xp
        progress_text = f"{xp_needed} XP to reach {next_stage.capitalize()}"
    else:
        progress_text = "Final stage reached 🌟"

    if nibble.stage != "elder":
        stages = list(STAGE_THRESHOLD.keys())
        current_stage = nibble.stage
        next_stage = stages[stages.index(current_stage) + 1]

        current_xp = nibble.xp
        current_threshold = STAGE_THRESHOLD[current_stage]
        next_threshold = STAGE_THRESHOLD[next_stage]

        progress_value = (current_xp - current_threshold) / (next_threshold - current_threshold)
        progress_value = max(0, min(progress_value, 1)) * 100  # clamp 0–100

        progress_bar = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            length=200,
            mode="determinate"
        )
        progress_bar["value"] = progress_value
        progress_bar.pack(pady=5)


    progress_label.config(text=progress_text)

    root.mainloop()