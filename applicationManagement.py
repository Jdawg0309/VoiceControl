# applicationManagement.py (Linux Version)
import psutil
import signal
import subprocess
import os

app_pids = {}

def open_application(command):
    try:
        app_name = command.split("open ")[1]
        app_paths = {
            "browser": "/usr/bin/chromium-browser",
            "spotify": "spotify",
            "notepad": "mousepad",
            "calculator": "galculator"
        }
        app_cmd = app_paths.get(app_name.lower())
        if app_cmd:
            process = subprocess.Popen(app_cmd.split())
            app_pids[app_name.lower()] = process.pid
            print(f"Opened {app_name} with PID {process.pid}")
        else:
            print(f"Error: Application {app_name} not configured.")
    except IndexError:
        print("Specify application (e.g., 'open browser').")

def close_application(command):
    try:
        app_name = command.split("close ")[1].lower()
        pid = app_pids.get(app_name)
        if pid and psutil.pid_exists(pid):
            os.kill(pid, signal.SIGTERM)
            del app_pids[app_name]
            print(f"Closed {app_name}")
        else:
            print(f"No active process for {app_name}.")
    except Exception as e:
        print(f"Error closing app: {e}")