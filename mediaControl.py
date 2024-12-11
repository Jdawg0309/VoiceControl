import keyboard  # For media control
# Media Control Functions
def play_media():
    keyboard.press_and_release('play/pause')
    print("Playing media...")

def pause_media():
    keyboard.press_and_release('play/pause')
    print("Pausing media...")

def fast_forward_media():
    keyboard.press_and_release('next track')
    print("Fast forwarding media...")

def rewind_media():
    keyboard.press_and_release('previous track')
    print("Rewinding media...")