import tkinter as tk
import speech_recognition as sr
from langdetect import detect
from googletrans import Translator
from gtts import gTTS
import pygame

# Initialize the speech recognition
recognizer = sr.Recognizer()

# Function to perform translation to Indian regional languages
def translate_to_indian_language(text, target_language):
    translator = Translator()
    translation = translator.translate(text, src='auto', dest=target_language)
    translated_text = translation.text
    return translated_text

# Function to capture and process speech
def capture_and_translate():
    try:
        # Capture audio input
        with sr.Microphone() as source:
            status_label.config(text="Listening...")
            window.update()
            audio = recognizer.listen(source)
            status_label.config(text="Processing...")

        # Recognize the speech
        spoken_text = recognizer.recognize_google(audio)
        input_text.delete(1.0, tk.END)
        input_text.insert(tk.END, spoken_text)

        # Detect the language of the spoken text
        detected_language = detect(spoken_text)
        detected_language_label.config(text="Detected Language: " + detected_language)

        # Translate the speech to Indian regional languages
        if detected_language != "en":
            translated_text = translate_to_indian_language(spoken_text, "en")  # Translate to Hindi as an example
        else:
            translated_text = spoken_text

        # Update the translated text
        translation_text.delete(1.0, tk.END)
        translation_text.insert(tk.END, translated_text)

        # Convert translated text to speech
        tts = gTTS(translated_text, lang='en')  # Use Hindi for the translation
        tts.save("translation.mp3")

        # Play the translated speech
        play_audio("translation.mp3")

        status_label.config(text="Translation Complete")
    except sr.UnknownValueError:
        status_label.config(text="Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        status_label.config(text=f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        status_label.config(text=f"An error occurred: {e}")

# Function to play audio
def play_audio(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Create the main application window
window = tk.Tk()
window.title("Speech Translator")

# Create labels and text widgets
input_label = tk.Label(window, text="Spoken Text:")
input_text = tk.Text(window, height=3, width=40)
detected_language_label = tk.Label(window, text="")
translation_label = tk.Label(window, text="Translation:")
translation_text = tk.Text(window, height=3, width=40)
status_label = tk.Label(window, text="")

# Create the Capture and Translate button
capture_button = tk.Button(window, text="Capture and Translate", command=capture_and_translate)

# Pack widgets
input_label.pack()
input_text.pack()
detected_language_label.pack()
translation_label.pack()
translation_text.pack()
status_label.pack()
capture_button.pack()

# Start the Tkinter main loop
window.mainloop()
