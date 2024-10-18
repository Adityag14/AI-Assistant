import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
import os
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key from .env file
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Initialize pyttsx3 engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Speaking function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Listening to voice command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Command: {query}")
    except Exception as e:
        print(e)
        speak("Sorry, I didn't catch that. Could you repeat?")
        return "None"
    return query

# Gemini AI integration using google.generativeai
def queryGeminiAI(prompt):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()  # Ensure we return a trimmed response
    except Exception as e:
        print(f"Error querying Gemini AI: {str(e)}")
        return None

# Dictionary of known applications
known_apps = {
    "notepad": "notepad.exe",
    "microsoft edge": "msedge.exe",
    "google chrome": "chrome.exe",
    "microsoft word": "winword.exe",
    "microsoft excel": "excel.exe",
    "powershell": "powershell.exe",
    "command prompt": "cmd.exe",
}

# Dynamic system command execution (Windows-specific)
def executeDynamicCommand(command):
    command = command.lower().strip()  # Convert command to lower case and remove extra spaces
    if command in known_apps:
        app_name = known_apps[command]
        try:
            subprocess.run(f'start {app_name}', shell=True)
            speak(f"Opening {command}.")
        except Exception as e:
            speak(f"Failed to open {command}: {str(e)}")
    else:
        # If command is not a known app, attempt to run it as a command
        try:
            subprocess.run(command, shell=True)
            speak(f"Executing: {command}.")
        except Exception as e:
            speak(f"An error occurred while executing the command: {str(e)}")

# Main query handling loop
def Take_query():
    speak("Hello! I am your assistant. What would you like to do?")
    while True:
        query = takeCommand().lower()

        if "open wikipedia" in query:
            speak("Searching Wikipedia.")
            query = query.replace("open wikipedia", "")
            result = wikipedia.summary(query, sentences=3)
            speak(f"According to Wikipedia: {result}")

        elif "bye" in query:
            speak("Goodbye!")
            exit()

        else:
            speak("Let me generate a command.")
            dynamic_command = queryGeminiAI(query)  # Send prompt to Gemini
            if dynamic_command:
                executeDynamicCommand(dynamic_command)  # Execute generated command
            else:
                speak("I couldn't generate a command.")

if __name__ == '__main__':
    Take_query()
