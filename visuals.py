"""Visual representation of Nibble's state"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # type: ignore
from config import STAGE_THRESHOLD

BG_COLOR = "#D6BAFA" 

def show_nibble(nibble, notification=None):
    root = tk.Tk()
    root.title("Nibble 🐾")
    root.configure(bg=BG_COLOR)

    # notification
    if notification:
        tk.Label(root, text=notification, font=("Arial", 11, "italic"), fg="#2E7D32", bg=BG_COLOR).pack(pady=5)

    # title
    tk.Label(root, text="Meet Nibble 🐾", font=("Segoe UI", 18, "bold"), bg=BG_COLOR).pack(pady=(10, 5))

    # main container
    main_frame = tk.Frame(root, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    # image
    image_frame = tk.Frame(main_frame, bg=BG_COLOR)
    image_frame.pack(pady=5)

    img = Image.open(f"assets/{nibble.stage}.png")
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    img_label = tk.Label(image_frame, image=photo, bg=BG_COLOR)
    img_label.image = photo
    img_label.pack()

    # stats
    stats_frame = tk.Frame(main_frame, bg=BG_COLOR)
    stats_frame.pack(pady=5)

    tk.Label(stats_frame, text=f"Stage: {nibble.stage.capitalize()}", font=("Segoe UI", 14), bg=BG_COLOR).pack()
    tk.Label(stats_frame, text=f"XP: {nibble.xp}", font=("Segoe UI", 12), bg=BG_COLOR).pack()

    #stage message
    message = nibble.get_stage_message()
    tk.Label(main_frame, text=message, font=("Arial", 11, "italic"), fg="#444", bg=BG_COLOR).pack(pady=5)

    # XP needed for next stage
    if nibble.stage != "elder":
        stages = list(STAGE_THRESHOLD.keys())
        next_stage = stages[stages.index(nibble.stage) + 1]
        xp_needed = STAGE_THRESHOLD[next_stage] - nibble.xp

        tk.Label(main_frame, text=f"{xp_needed} XP needed for next stage {next_stage.capitalize()}", font=("Arial", 12), bg=BG_COLOR).pack(pady=5)
    else:
        tk.Label(main_frame, text="Nibble has reached the final stage!", font=("Arial", 12), bg=BG_COLOR).pack(pady=5)

    #history
    tk.Label(main_frame, text=f"Sessions logged: {len(nibble.history)}", font=("Arial", 12), bg=BG_COLOR).pack(pady=8)

    #progress bar
    progress_frame = tk.Frame(main_frame, bg=BG_COLOR)
    progress_frame.pack(pady=5)

    if nibble.stage != "elder":
        current_stage = nibble.stage
        stages = list(STAGE_THRESHOLD.keys())
        next_stage = stages[stages.index(current_stage) + 1]

        current_xp = nibble.xp
        current_threshold = STAGE_THRESHOLD[current_stage]
        next_threshold = STAGE_THRESHOLD[next_stage]

        progress_value = ((current_xp - current_threshold) / (next_threshold - current_threshold))
        progress_value = max(0, min(progress_value, 1)) * 100

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Nibble.Horizontal.TProgressbar", troughcolor=BG_COLOR, background="#381270")

        ttk.Progressbar( progress_frame, style="Nibble.Horizontal.TProgressbar", orient="horizontal", length=220, mode="determinate", value=progress_value).pack()
    else:
        tk.Label(progress_frame, text="Final stage reached 🌟", font=("Arial", 11), bg=BG_COLOR).pack()

    root.mainloop()
    STAGE_COLORS = {
        "baby": "#FFD700",
        "child": "#FFB14E",
        "teen": "#FF7F50",
        "adult": "#6A5ACD",
        "elder": "#A2DFFF"
    }