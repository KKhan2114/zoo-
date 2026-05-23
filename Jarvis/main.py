import speech_recognition as sr
import webbrowser
import customtkinter as ctk
from tkinter import END
import threading
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# ------------------ AI CONFIG ------------------

client = OpenAI(
    api_key="YOUR_OPENAI_API_KEY"
)

newsapi = "YOUR_NEWS_API_KEY"

# ------------------ SPEAK FUNCTION ------------------

def speak(text):
    chat_box.insert(END, f"Jarvis: {text}\n\n")
    chat_box.see(END)

    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# ------------------ AI PROCESS ------------------

def aiProcess(command):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a smart AI assistant named Jarvis. Give short and useful responses."
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content

# ------------------ COMMAND PROCESS ------------------

def processCommand(command):

    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")

    elif command.startswith("play"):

        try:
            song = command.split(" ")[1]
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")

        except:
            speak("Song not found")

    elif "news" in command:

        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )

        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])

            for article in articles[:5]:
                speak(article["title"])

    else:
        output = aiProcess(command)
        speak(output)

# ------------------ VOICE LISTENER ------------------

def listenCommand():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        status_label.configure(text="Adjusting for noise...")

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)

        status_label.configure(text="Listening... Speak now!")

        try:
            # Listen with longer timeout and phrase timeout
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            status_label.configure(text="Processing speech...")

            # Try to recognize speech
            command = recognizer.recognize_google(audio, language='en-US')

            # Convert to lowercase for processing
            command = command.lower()

            chat_box.insert(END, f"You: {command}\n\n")
            chat_box.see(END)

            processCommand(command)

        except sr.WaitTimeoutError:
            speak("No speech detected. Please try again.")
            chat_box.insert(END, "Error: No speech detected within timeout.\n\n")
            chat_box.see(END)

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that. Please speak clearly.")
            chat_box.insert(END, "Error: Speech not recognized. Please speak more clearly.\n\n")
            chat_box.see(END)

        except sr.RequestError as e:
            speak("Speech recognition service unavailable. Check your internet connection.")
            chat_box.insert(END, f"Error: Speech service unavailable - {e}\n\n")
            chat_box.see(END)

        except Exception as e:
            speak("An error occurred with speech recognition.")
            chat_box.insert(END, f"Error: {str(e)}\n\n")
            chat_box.see(END)

        status_label.configure(text="Idle")

# ------------------ THREADING ------------------

def startListening():
    thread = threading.Thread(target=listenCommand)
    thread.start()

# ------------------ GUI ------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("800x600")
app.title("Jarvis AI Assistant")

# Title

title = ctk.CTkLabel(
    app,
    text="JARVIS AI ASSISTANT",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)

# Chat Box

chat_box = ctk.CTkTextbox(
    app,
    width=700,
    height=350,
    font=("Arial", 16)
)

chat_box.pack(pady=20)

# Status Label

status_label = ctk.CTkLabel(
    app,
    text="Idle",
    font=("Arial", 18)
)

status_label.pack(pady=10)

# Listen Button

listen_button = ctk.CTkButton(
    app,
    text="🎤 Speak",
    width=200,
    height=50,
    font=("Arial", 20),
    command=startListening
)

listen_button.pack(pady=20)

# Welcome Message

speak("Hello, I am Jarvis. How can I help you?")

app.mainloop()
