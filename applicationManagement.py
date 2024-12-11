import psutil
import signal
import subprocess
import os

# Dictionary to store application PIDs
app_pids = {}


def open_application(command):
    try:
        app_name = command.split("open ")[1]
        app_paths = {
            "browser": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "spotify": "C:\\Users\\User\\AppData\\Roaming\\Spotify\\Spotify.exe",
            "notepad": "C:\\Windows\\system32\\notepad.exe",
            "calculator": "C:\\Windows\\System32\\calc.exe"
        }
        app_path = app_paths.get(app_name.lower())
        if app_path and os.path.exists(app_path):
            process = subprocess.Popen(app_path)
            app_pids[app_name.lower()] = process.pid
            print(f"Opened {app_name} with PID {process.pid}")
        else:
            print(f"Error: Application {app_name} not found or invalid path.")
    except IndexError:
        print("Please specify the application to open (e.g., 'open spotify').")
    except Exception as e:
        print(f"An error occurred while trying to open the application: {e}")

def close_application(command):
    try:
        app_name = command.split("close ")[1].lower()
        pid = app_pids.get(app_name)
        if pid and psutil.pid_exists(pid):
            os.kill(pid, signal.SIGTERM)
            print(f"Closed {app_name} with PID {pid}")
            del app_pids[app_name]
        else:
            print(f"No active process found for {app_name}.")
    except IndexError:
        print("Please specify the application to close (e.g., 'close browser').")
    except Exception as e:
        print(f"An error occurred while trying to close the application: {e}")