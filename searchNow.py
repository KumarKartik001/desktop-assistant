import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser

recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')

# Set speech rate
engine.setProperty('rate', 175)

def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            recognizer.adjust_for_ambient_noise(source,duration=0.5)
            try:
                command = recognizer.recognize_google(audio, language="en-in")
                return command.lower()
            except sr.UnknownValueError:
                speak("Sorry, I could not understand the audio. Please try again.")
            except sr.RequestError:
                speak("There was an issue with the Google Speech Recognition service. Please try again.")

def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("google search","")
        query = query.replace("google","")
        
        speak("sir, this is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query,1)
            speak(result)

        except:
            speak("Sorry sir, I am unable to found anything to speak about it...")

def searchYoutube(query):
    if "youtube" in query.lower():
        speak("This is what I found on youtube, for your search!")
        query = query.replace("youtube search","")
        query = query.replace("youtube","")

        web = "https://www.youtube.com/results?search_query=" + query

        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, sir")

def searchWikipedia(query):
    if "wikipedia" in query.lower():
        speak("Searching from wikipedia....")
        query = query.replace("search wikipedia","")
        query = query.replace("wikipedia","")
        results = wikipedia.summary(query,sentences = 2)
        speak("According to wikipedia...")
        print(results)
        speak(results)