# mediaControl.py (Linux Version)
import subprocess

def play_media():
    subprocess.run(["playerctl", "play-pause"])
    print("Toggled media play/pause.")

def pause_media():
    subprocess.run(["playerctl", "pause"])
    print("Media paused.")

def fast_forward_media():
    subprocess.run(["playerctl", "next"])
    print("Next track.")

def rewind_media():
    subprocess.run(["playerctl", "previous"])
    print("Previous track.")