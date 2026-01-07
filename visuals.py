"""Visual representation of Nibble's state"""

from logging import root
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk # type: ignore
import os
from config import STAGE_THRESHOLD

def show_nibble(nibble, xp=0, next_xp=50): 
    root = tk.Tk()
    root.title("Nibble 🐾")
    root.geometry("400x500")
    
    title = ttk.Label(root, text="Meet Nibble 🐾", font=("Segoe UI", 18, "bold"))
    title.pack(pady=(10,5))

    image_frame = ttk.Frame(root)
    image_frame.pack(pady=10)

    stats_frame = ttk.Frame(root)
    stats_frame.pack(pady=10)

    progress_frame = ttk.Frame(root)
    progress_frame.pack(pady=10)


    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    pet_frame = tk.Frame(main_frame)
    pet_frame.pack(pady=5)

    stats_frame = tk.Frame(main_frame)
    stats_frame.pack(pady=5)

    progress_frame = tk.Frame(main_frame)
    progress_frame.pack(pady=5)
 
    STAGE_COLORS = {
        "egg": "#FFF7CC",
        "baby": "#E8F7FF",
        "child": "#E9FFE8",
        "teen": "#F0E8FF",
        "adult": "#FFE8EC",
        "elder": "#EFEFEF"
    }
    root.configure(bg=STAGE_COLORS.get(nibble.stage, "#FFFFFF"))

    # image path based on stage
    img = Image.open(f"assets/{nibble.stage}.png")
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    img_label = ttk.Label(image_frame, image=photo)
    img_label.image = photo
    img_label.pack()

    # stats
    """stage_label = tk.Label(stats_frame, text=f"Stage: {nibble.stage.capitalize()}", font=("Arial", 16, "bold"))
    stage_label.pack(pady=10)

    xp_label = tk.Label(stats_frame, text=f"XP: {nibble.xp}", font=("Arial", 14))
    xp_label.pack(pady=5)"""

    ttk.Label(stats_frame, text=f"Stage: {nibble.stage}", font=("Segoe UI", 14)).pack()
    ttk.Label(stats_frame, text=f"XP: {nibble.xp}", font=("Segoe UI", 12)).pack()


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
    # Progress bar
    progress_label = tk.Label(progress_frame, text="Progress loading...", font=("Arial", 11), fg="gray")
    progress_label.pack()


    if nibble.stage != "elder":
        stages = list(STAGE_THRESHOLD.keys())
        current_stage = nibble.stage
        next_stage = stages[stages.index(current_stage) + 1]

        current_xp = nibble.xp
        current_threshold = STAGE_THRESHOLD[current_stage]
        next_threshold = STAGE_THRESHOLD[next_stage]

        xp_needed = max(0, next_threshold - current_xp)
        progress_text = f"{xp_needed} XP to reach {next_stage.capitalize()}"
        # Progress within this stage (0–100)
        progress_value = (current_xp - current_threshold) / (next_threshold - current_threshold)
        progress_value = max(0, min(progress_value, 1)) * 100

        progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=220, mode="determinate")
        progress_bar["value"] = progress_value
        progress_bar.pack(pady=5)

    else:
        progress_text = "Final stage reached 🌟"

        progress_label.config(text=progress_text)

    root.mainloop()