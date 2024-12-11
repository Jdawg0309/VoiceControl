# application_control.py
import subprocess
import os
import webbrowser
import datetime
import requests
import random
import openai
from dotenv import load_dotenv
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
import keyboard  # For media control
import signal

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_command():
    """Continuously listen for commands and execute system tasks."""
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("System is on and waiting for activation. Say 'Sally' to activate.")

    while True:
        try:
            with mic as source:
                print("Listening for the wake word 'Sally'...")
                audio = recognizer.listen(source)

            wake_word = recognizer.recognize_google(audio).lower()
            print(f"Wake word received: {wake_word}")

            if "sally" in wake_word:
                print("Sally is active! Listening for your command...")
                with mic as source:
                    print("Listening for a command...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio).lower()
                    print(f"Command received: {command}")

                    # Process individual commands
                    if "shutdown" in command:
                        shutdown_system()
                    if "reboot" in command or "restart" in command:
                        reboot_system()
                    if "sleep" in command:
                        sleep_system()
                    if "volume up" in command:
                        volume_up()
                    if "volume down" in command:
                        volume_down()
                    if "mute" in command:
                        mute_system()
                    if "play" in command:
                        play_media()
                    if "pause" in command:
                        pause_media()
                    if "fast forward" in command:
                        fast_forward_media()
                    if "rewind" in command:
                        rewind_media()
                    if "open" in command:
                        open_application(command)
                    if "close" in command:
                        close_application(command)
                    if "search google" in command or "google" in command:
                        search_google(command)
                    if "search youtube" in command or "youtube" in command:
                        search_youtube(command)
                    if "tell me a joke" in command or "joke" in command:
                        tell_joke()
                    if "what time is it" in command or "time" in command:
                        tell_time()
                    if "weather update" in command or "weather" in command:
                        fetch_weather()
                    if "exit" in command:
                        print("Exiting program...")
                        break
            else:
                print("Wake word 'Sally' not detected. Listening again...")
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

# System Control Functions
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
    interface = devices.Activate(IAudioEndpointVolume._iid_, cast, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def volume_up():
    volume = get_volume_control()
    volume.SetMasterVolumeLevelScalar(min(1.0, volume.GetMasterVolumeLevelScalar() + 0.1), None)
    print("Volume increased.")

def volume_down():
    volume = get_volume_control()
    volume.SetMasterVolumeLevelScalar(max(0.0, volume.GetMasterVolumeLevelScalar() - 0.1), None)
    print("Volume decreased.")

def mute_system():
    volume = get_volume_control()
    volume.SetMute(1, None)
    print("System muted.")

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

# Other Helper Functions
app_pids = {}

def open_application(command):
    """Open an application and store its PID."""
    try:
        app_name = command.split("open ")[1]
        app_paths = {
            "browser": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "spotify": "C:\\Users\\User\\AppData\\Roaming\\Spotify\\Spotify.exe",
            "notepad": "C:\\Windows\\system32\\notepad.exe",
            "calculator": "C:\\Windows\\System32\\calc.exe"
        }
        app_path = app_paths.get(app_name.lower())
        if app_path:
            if os.path.exists(app_path):
                # Open the application and store the PID
                process = subprocess.Popen(app_path)
                app_pids[app_name.lower()] = process.pid
                print(f"Opened {app_name} with PID {process.pid}")
            else:
                print(f"Error: The path for {app_name} does not exist: {app_path}")
        else:
            print(f"Error: Application {app_name} not found in app_paths.")
    except IndexError:
        print("Please specify the application to open (e.g., 'open spotify').")
    except Exception as e:
        print(f"An error occurred while trying to open the application: {e}")


import psutil
import subprocess
import signal

def close_application(command):
    """Close an application using its PID or process name."""
    try:
        app_name = command.split("close ")[1].lower()
        pid = app_pids.get(app_name)
        
        if pid and psutil.pid_exists(pid):
            # Use taskkill to terminate the process by PID
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=True, capture_output=True, text=True)
            print(f"Closed {app_name} with PID {pid}")
            del app_pids[app_name]  # Remove the PID from the dictionary
        else:
            print(f"PID for {app_name} not found. Attempting to locate by process name...")
            # Search for the process by name
            process_found = False
            for process in psutil.process_iter(['pid', 'name']):
                if app_name in process.info['name'].lower():
                    print(f"Found {app_name} with PID {process.info['pid']}. Terminating...")
                    os.kill(process.info['pid'], signal.SIGTERM)
                    process_found = True
            if process_found:
                print(f"Successfully closed all running instances of {app_name}.")
            else:
                print(f"Error: No running process found for {app_name}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to close the application: {e.stderr.strip()}")
    except IndexError:
        print("Please specify the application to close (e.g., 'close browser').")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def shutdown_system():
    print("Shutting down the computer...")
    os.system("shutdown /s /f /t 0")

def restart_system():
    print("Restarting the computer...")
    os.system("shutdown /r /f /t 0")

def search_google(command):
    if "search google for" in command:
        search_query = command.split("search google for ")[1]
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    else:
        print("Please provide a valid Google search command.")

def search_youtube(command):
    if "search youtube for" in command:
        search_query = command.split("search youtube for ")[1]
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
    else:
        print("Please provide a valid YouTube search command.")

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts."
    ]
    print(random.choice(jokes))

def tell_time():
    now = datetime.datetime.now()
    print(f"The current time is {now.strftime('%H:%M')}.")

def fetch_weather():
    api_key = "your_openweather_api_key"  # Replace with your API key
    city = "New York"  # Replace with your city
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        data = response.json()
        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            print(f"Weather in {city}: {weather}, {temp} °C.")
        else:
            print("Failed to fetch weather updates.")
    except Exception as e:
        print(f"Error fetching weather: {e}")

def ask_chatgpt(command):
    """
    Processes the 'ask ChatGPT' command and fetches a response from OpenAI's API.
    """
    if "ask chatgpt" in command or "ask ai" in command:
        try:
            # Extract the query from the command
            query = command.split("ask chatgpt")[-1].strip()
            print(f"Querying ChatGPT: {query}")

            # Call the OpenAI ChatGPT API
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  # Model name
                messages=[{"role": "user", "content": query}],
            )

            # Extract and print the response
            chatgpt_response = response.choices[0].message.content
            print(f"ChatGPT Response: {chatgpt_response}")
        except Exception as e:
            print(f"Error communicating with ChatGPT: {e}")
    else:
        print("Please provide a valid ChatGPT query command.")