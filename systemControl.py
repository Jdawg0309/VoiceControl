# systemControl.py (Linux Version)
import alsaaudio
import subprocess
import os

def shutdown_system():
    print("Shutting down the system...")
    subprocess.run(["sudo", "shutdown", "-h", "now"])

def reboot_system():
    print("Rebooting the system...")
    subprocess.run(["sudo", "reboot"])

def sleep_system():
    print("Putting the system to sleep...")
    subprocess.run(["sudo", "systemctl", "suspend"])

# ALSA Volume Control
def get_mixer():
    return alsaaudio.Mixer()

def volume_up():
    mixer = get_mixer()
    current = mixer.getvolume()[0]
    mixer.setvolume(min(100, current + 10))
    print("Volume increased.")

def volume_down():
    mixer = get_mixer()
    current = mixer.getvolume()[0]
    mixer.setvolume(max(0, current - 10))
    print("Volume decreased.")

def mute_system():
    mixer = get_mixer()
    mixer.setmute(not mixer.getmute()[0])  # Toggle mute
    print("System muted.")