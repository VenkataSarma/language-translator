import speech_recognition as sr
from langdetect import detect
from googletrans import Translator
from gtts import gTTS  # Import gTTS library
import pygame
import time

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

try:
    # Capture audio input
    with sr.Microphone() as source:
        print("Speak something:")
        audio = recognizer.listen(source)

    # Recognize the speech
    spoken_text = recognizer.recognize_google(audio)
    print("You said:", spoken_text)

    # Detect the language of the spoken text
    detected_language = detect(spoken_text)
    print("Detected Language:", detected_language)

    # Translate the speech to Indian regional languages
    if detected_language!= "en":
        translated_text = translate_to_indian_language(spoken_text, "en")  # Translate to Hindi as an example
        print("Translation:", translated_text)
    else:
        translated_text = spoken_text

    # Convert translated text to speech
    tts = gTTS(translated_text, lang='en')  # Use Hindi for the translation
    tts.save("translation.mp3")

    # Play the translated speech
    play_audio("translation.mp3")
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
except Exception as e:
    print(f"An error occurred: {e}")
