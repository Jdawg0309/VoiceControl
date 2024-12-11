# application_control.py
import subprocess
import os
import webbrowser
import datetime
import requests
import random
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_command():
    """Continuously listen for wake word and process commands."""
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("System is on and waiting for activation. Say 'Sally' to activate.")

    while True:
        try:
            with mic as source:
                # Reduce ambience adjustment to once initially
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for the wake word 'Sally'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)  # Adjust timings for responsiveness

            wake_word = recognizer.recognize_google(audio).lower()
            print(f"Wake word received: {wake_word}")

            if "sally" in wake_word:
                print("Sally is active! Listening for your command...")
                try:
                    with mic as source:
                        print("Listening for a command...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Shorter delays
                        command = recognizer.recognize_google(audio).lower()
                        print(f"Command received: {command}")

                        # Handle commands
                        if "open" in command:
                            open_application(command)
                        if "close" in command:
                            close_application(command)
                        if "shutdown" in command:
                            shutdown_system()
                        if "restart" in command:
                            restart_system()
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
                        if "search ai" in command or "ai" in command or "chatgpt" in command:
                            ask_chatgpt(command)
                        if "exit" in command:
                            print("Exiting program...")
                            break
                        else:
                            print(f"Command '{command}' not recognized.")
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand the command.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
            else:
                print("Wake word 'Sally' not detected. Listening again...")
        except sr.UnknownValueError:
            print("Listening again...")
        except sr.WaitTimeoutError:
            print("Listening timed out, restarting...")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

def open_application(command):
    try:
        app_name = command.split("open ")[1]
        app_paths = {
            "browser": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "spotify": "C:\\Users\\Junaet Mahbub\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\spotify.exe",
            "notepad": "C:\\Windows\\system32\\notepad.exe",
            "calculator": "C:\\Windows\\System32\\calc.exe"
        }
        app_path = app_paths.get(app_name.lower())
        if app_path:
            subprocess.Popen(app_path)
            print(f"Opening {app_name}...")
        else:
            print(f"{app_name} not found.")
    except IndexError:
        print("Please specify the application to open (e.g., 'open spotify').")

def close_application(command):
    try:
        app_name = command.split("close ")[1]
        app_processes = {
            "browser": "chrome.exe",
            "spotify": "Spotify.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe"
        }
        process_name = app_processes.get(app_name.lower())
        if process_name:
            subprocess.call(f"taskkill /f /im {process_name}", shell=True)
            print(f"Closing {app_name}...")
        else:
            print(f"{app_name} not found.")
    except IndexError:
        print("Please specify the application to close (e.g., 'close spotify').")

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