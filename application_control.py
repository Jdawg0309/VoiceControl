import os
import openai
from dotenv import load_dotenv
from applicationManagement import *
from mediaControl import *
from systemControl import *
from utility import *

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to process voice commands
def process_command():
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
                    if "ask chatgpt" in command or "ask ai" in command:
                        ask_chatgpt(command)
                    if "exit" in command:
                        print("Exiting program...")
                        break
            else:
                print("Wake word 'Sally' not detected. Listening again...")
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")



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