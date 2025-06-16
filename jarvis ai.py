import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import requests
import json

class JARVIS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200)
        self.engine.setProperty('volume', 1)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        print("JARVIS initialized successfully!")
        self.speak("Hello! I am JARVIS, your personal assistant. How can I help you today?")

    def speak(self, text):
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that. Could you please repeat?")
            return ""
        except sr.RequestError:
            self.speak("Sorry, there's an issue with the speech recognition service.")
            return ""
        except sr.WaitTimeoutError:
            return ""

    def get_time(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        self.speak(f"The current time is {time_str}")

    def get_date(self):
        today = datetime.date.today()
        date_str = today.strftime("%B %d, %Y")
        self.speak(f"Today's date is {date_str}")

    def search_wikipedia(self, query):
        try:
            self.speak("Searching Wikipedia...")
            result = wikipedia.summary(query, sentences=2)
            self.speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            self.speak(f"Multiple results found. Here's information about {e.options[0]}")
            result = wikipedia.summary(e.options[0], sentences=2)
            self.speak(result)
        except wikipedia.exceptions.PageError:
            self.speak("Sorry, I couldn't find any information about that topic.")
        except Exception:
            self.speak("Sorry, there was an error searching Wikipedia.")

    def open_website(self, website):
        websites = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'github': 'https://www.github.com',
            'stackoverflow': 'https://stackoverflow.com',
            'reddit': 'https://www.reddit.com'
        }
        if website in websites:
            self.speak(f"Opening {website}")
            webbrowser.open(websites[website])
        else:
            self.speak(f"Opening {website}")
            webbrowser.open(f"https://www.{website}.com")

    def open_whatsapp(self):
        """Open WhatsApp Web in the default browser"""
        try:
            self.speak("Opening WhatsApp Web")
            webbrowser.open('https://web.whatsapp.com')
        except Exception:
            self.speak("Sorry, I couldn't open WhatsApp Web.")

    def open_application(self, app_name):
        try:
            if 'notepad' in app_name:
                os.system('notepad')
            elif 'calculator' in app_name:
                os.system('calc')
            elif 'browser' in app_name:
                webbrowser.open('https://www.google.com')
            elif 'file explorer' in app_name or 'files' in app_name:
                os.system('explorer')
            else:
                self.speak("Sorry, I don't know how to open that application.")
                return
            self.speak(f"Opening {app_name}")
        except Exception:
            self.speak("Sorry, I couldn't open that application.")

    def tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the computer go to the doctor? Because it had a virus!",
            "Why don't programmers like nature? It has too many bugs!",
            "How do you organize a space party? You planet!",
            "Why did the robot go on a diet? It had a byte problem!"
        ]
        joke = random.choice(jokes)
        self.speak(joke)

    def get_weather(self, city="delhi"):
        api_key = "421e0d856377bacec5e269f3733578b8"
        if not city:
            city = "Delhi"
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            if data.get("cod") == 200:
                weather = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                weather_info = f"The weather in {city} is {weather} with a temperature of {temperature}°C. It feels like {feels_like}°C with {humidity}% humidity."
                self.speak(weather_info)
            elif data.get("cod") == "404":
                self.speak("City not found. Please check the city name.")
            else:
                self.speak(f"Weather service error: {data.get('message', 'Unknown error')}")
        except requests.exceptions.RequestException:
            self.speak("Sorry, I couldn't connect to the weather service. Please check your internet connection.")
        except KeyError:
            self.speak("Sorry, I received incomplete weather data.")
        except Exception:
            self.speak("Sorry, there was an error getting the weather information.")

    def shutdown_system(self):
        self.speak("Are you sure you want to shutdown the system? Say yes to confirm.")
        command = self.listen()
        if 'yes' in command:
            self.speak("Shutting down the system. Goodbye!")
            os.system("shutdown /s /t 1")
        else:
            self.speak("Shutdown cancelled.")

    def reboot_system(self):
        self.speak("Are you sure you want to restart the system? Say yes to confirm.")
        command = self.listen()
        if 'yes' in command:
            self.speak("Rebooting the system. See you soon!")
            os.system("shutdown /r /t 1")
        else:
            self.speak("Restart cancelled.")

    def process_command(self, command):
        if 'time' in command:
            self.get_time()
        elif 'date' in command:
            self.get_date()
        elif 'wikipedia' in command or 'search' in command:
            query = command.replace('wikipedia', '').replace('search', '').strip()
            if query:
                self.search_wikipedia(query)
            else:
                self.speak("What would you like me to search for?")
        elif 'whatsapp' in command:
            self.open_whatsapp()
        elif 'open' in command:
            if 'website' in command or any(site in command for site in ['google', 'youtube', 'github']):
                site = command.replace('open', '').replace('website', '').strip()
                self.open_website(site)
            else:
                app = command.replace('open', '').strip()
                self.open_application(app)
        elif 'joke' in command:
            self.tell_joke()
        elif 'weather' in command:
            city = command.replace('weather', '').replace('in', '').strip()
            self.get_weather(city)
        elif any(keyword in command for keyword in ['shutdown', 'turn off', 'band hoo jaa']):
            self.shutdown_system()
        elif any(keyword in command for keyword in ['restart', 'reboot', 'gadhda hai tu']):
            self.reboot_system()
        elif any(keyword in command for keyword in ['stop', 'exit', 'quit', 'bye', 'ruk ja']):
            self.speak("Goodbye! Have a great day!")
            return False
        elif 'hello' in command or 'hi' in command:
            responses = [
                "Hello! How can I assist you?",
                "Hi there! What can I do for you?",
                "Greetings! How may I help you today?"
            ]
            self.speak(random.choice(responses))
        elif 'who are you' in command or 'what are you' in command:
            self.speak("I am JARVIS, your personal AI assistant. I can help you with various tasks like telling time, searching information, opening applications, and much more!")
        elif 'thank you' in command or 'thanks' in command:
            self.speak("You're welcome! I'm always here to help.")
        else:
            self.speak("I'm sorry, I don't understand that command.")
        return True

    def run(self):
        running = True
        while running:
            command = self.listen()
            if command:
                running = self.process_command(command)

def main():
    try:
        jarvis = JARVIS()
        jarvis.run()
    except KeyboardInterrupt:
        print("\nJARVIS shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
