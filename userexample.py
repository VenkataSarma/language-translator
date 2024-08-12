import speech_recognition as sr
from langdetect import detect
from googletrans import Translator
from gtts import gTTS
import pygame
import tkinter as tk
from tkinter import Button, Label

# Initialize the speech recognition
recognizer = sr.Recognizer()

# Function to perform translation to Indian regional languages
def translate_to_indian_language(text, target_language):
    translator = Translator()
    translation = translator.translate(text, src='auto', dest=target_language)
    translated_text = translation.text
    return translated_text

# Function to play audio
def play_audio(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
# Function to handle the speech recognition and translation process
def recognize_and_translate():
    try:
        with sr.Microphone() as source:
            print("Speak something:")
            audio = recognizer.listen(source)

        spoken_text = recognizer.recognize_google(audio)
        print("You said:", spoken_text)

        detected_language = detect(spoken_text)
        print("Detected Language:", detected_language)

        if detected_language != "en":
            translated_text = translate_to_indian_language(spoken_text, "en")  # Translate to Hindi as an example
            print("Translation:", translated_text)
        else:
            translated_text = spoken_text

        tts = gTTS(translated_text, lang='en')
        tts.save("translation.mp3")

        play_audio("translation.mp3")

        # Update the label to display the translated text
        translation_label.config(text="Translation: " + translated_text)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from AVA's Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Create the Tkinter window
root = tk.Tk()
root.title("Speech Recognition and Translation")

# Create a label for displaying translation
translation_label = Label(root, text="")
translation_label.pack()

# Create a button to trigger the speech recognition and translation
recognize_button = Button(root, text="Start Speech Recognition", command=recognize_and_translate)
recognize_button.pack()

root.mainloop()
