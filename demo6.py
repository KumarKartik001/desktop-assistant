import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import subprocess
import datetime
import screen_brightness_control as sbc  # Import for brightness control
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL



# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Set speech rate
engine.setProperty('rate', 175)

def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.energy_threshold = 300
            audio = recognizer.listen(source)
            recognizer.adjust_for_ambient_noise(source,duration=0.5)
            try:
                command = recognizer.recognize_google(audio, language="en-in")
                return command.lower()
            except sr.UnknownValueError:
                speak("Sorry, I could not understand the audio. Please try again.")
            except sr.RequestError:
                speak("There was an issue with the Google Speech Recognition service. Please try again.")


def greet():
    speak("Hello! I am your voice-based AI assistant. How can I assist you today?")


def open_website(query):
    sites = [ 
        ["google", "https://www.google.com/"],
        ["amazon", "https://www.amazon.in"],
        ["flipkart", "https://www.flipkart.com"],
        ["it saso", "https://itsasoo.com/"],
        ["classroom", "https://classroom.google.com/?pli=1"],
        ["instagram", "https://www.instagram.com/"]
    ]
    for site in sites:
        if f"open {site[0]}".lower() in query:
            speak(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])


def tell_time():
    time = datetime.datetime.now().strftime("%H hours and %M minutes and %S seconds")
    speak(f"Sir, the time is {time}")


def control_brightness(level):
    try:
        sbc.set_brightness(level)
        speak(f"Setting brightness to {level} percent.")
    except Exception as e:
        speak("Sorry, I couldn't adjust the brightness.")


# Function to get the current volume level
def get_current_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)  # Get the correct interface
    return volume.GetMasterVolumeLevelScalar() * 100  # Returns volume in the range [0.0, 1.0]


# Function to set the volume level
def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)  # Get the correct interface
    # Ensure the volume level is between 0 and 100
    level = max(0, min(level, 100))
    speak(f"Setting volume to {level} percent.")
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)
    speak("This is how loud I will talk to you.")




def run_assistant():
    greet()
    while True:
        query = listen()

        if "open" in query:
            open_website(query)


        elif "the time" in query:
            tell_time()


        elif "set brightness to" in query:
            try:
                level_str = query.split("set brightness to ")[-1].strip()
                if "%" in level_str:
                    level = int(level_str.replace("%", "").strip())
                else:
                    level = int(level_str)
                control_brightness(level)
            except ValueError:
                speak("I didn't understand the brightness level. Please try again.")


        elif "set volume to" in query:
            try:
                level_str = query.split("set volume to ")[-1].strip()
                if "%" in level_str:
                    level = int(level_str.replace("%", "").strip())
                else:
                    level = int(level_str)
                set_volume(level)
            except ValueError:
                speak("I didn't understand the volume level. Please try again.")


        elif "current volume" in query:
            current_volume = get_current_volume()
            speak(f"The current volume is {current_volume} percent.")


        elif "exit" in query.lower() or "quit" in query.lower() or "bye" in query.lower():
            speak("Goodbye! Have a great day.")
            break


        elif "your name" in query.lower():
            speak("My name is Max, and I am your Voice Assistant")

        elif "how are you" in query.lower() or "how r u" in query.lower():
            speak("I am great sir..., thanks for asking....")
            speak("what you want to do today.....")

        elif "hello" in query:
            speak("Hello sir, How are you ?")
                
        elif "i am fine" in query or "i am good" in query or "i am great" in query:
            speak("That's Great Sir")
                
        elif "how are you" in query or "what about you" in query:
            speak("I am good sir, and eagerly waiting to help you !")

        elif "thankyou" in query or "thanks" in query:
            speak("My peasure sir!")

        elif "thankyou" in query or "thanks" in query:
            speak("My pleasure sir!")

        elif "google" in query.lower():
            from searchNow import searchGoogle
            searchGoogle(query)
        elif "youtube" in query.lower():
            from searchNow import searchYoutube
            searchYoutube(query)
        elif "wikipedia" in query.lower():
            from searchNow import searchWikipedia
            searchWikipedia(query)

        # elif "the date" in query or "today's day" in query:
        #     tell_date_and_day()

        else:
            print(f"You said: {query}. I don't know how to do that yet.")
            speak(f"You said: {query}. I don't know how to do that yet.")


if __name__ == "__main__":
    run_assistant()