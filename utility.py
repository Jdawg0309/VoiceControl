import webbrowser
import datetime
import requests
import random

def search_google(command):
    query = command.split("search google for ")[-1]
    webbrowser.open(f"https://www.google.com/search?q={query}")
    print(f"Searching Google for: {query}")

def search_youtube(command):
    query = command.split("search youtube for ")[-1]
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    print(f"Searching YouTube for: {query}")

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
    api_key = "your_openweather_api_key"
    city = "New York"
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