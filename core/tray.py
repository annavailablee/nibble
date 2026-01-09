# core/tray.py
import threading
import os
import pystray
from pystray import MenuItem as item
from PIL import Image
from visuals import show_nibble

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def start_tray(nibble):
    def open_nibble(icon, _):
        threading.Thread(
            target=show_nibble,
            args=(nibble,),
            daemon=True
        ).start()

    def quit_app(icon, _):
        icon.stop()

    image_path = os.path.join(ASSETS_DIR, "tray.png")
    image = Image.open(image_path)

    menu = (
        item("Open Nibble", open_nibble, default=True),
        item("Quit", quit_app),
    )

    icon = pystray.Icon("Nibble", image, "Nibble 🐾", menu)
    icon.run()
