from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import subprocess
import os

def shutdown_system():
    print("Shutting down the system...")
    os.system("shutdown /s /f /t 0")

def reboot_system():
    print("Rebooting the system...")
    os.system("shutdown /r /f /t 0")

def sleep_system():
    print("Putting the system to sleep...")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

# Volume Control Functions
def get_volume_control():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def volume_up():
    volume = get_volume_control()
    current_volume = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(min(1.0, current_volume + 0.1), None)
    print("Volume increased.")

def volume_down():
    volume = get_volume_control()
    current_volume = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(max(0.0, current_volume - 0.1), None)
    print("Volume decreased.")

def mute_system():
    volume = get_volume_control()
    volume.SetMute(1, None)
    print("System muted.")
