import winsound
import os

def play(sound_name):
    path = os.path.join("assets", "sounds", f"{sound_name}.wav")
    if os.path.exists(path):
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
