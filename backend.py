from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

app = Flask(__name__)

# Initialize the recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

@app.route('/recognize_and_translate', methods=['POST'])
def recognize_and_translate():
    try:
        # Receive audio file and language from the client
        audio_file = request.files['audio']
        target_language = request.form['language']

        # Save the received audio file temporarily
        audio_file.save("temp_audio.wav")

        with sr.AudioFile("temp_audio.wav") as source:
            audio = recognizer.record(source)

        spoken_text = recognizer.recognize_google(audio)
        print("You said:", spoken_text)

        detected_language = translator.detect(spoken_text).lang
        print("Detected Language:", detected_language)

        if detected_language != target_language:
            translated_text = translator.translate(spoken_text, src=detected_language, dest=target_language).text
            print("Translation:", translated_text)
        else:
            translated_text = spoken_text

        tts = gTTS(translated_text, lang=target_language)
        tts.save("translation.mp3")

        # Play the translation audio (you need to implement play_audio function)
        play_audio("translation.mp3")

        # Update the label to display the translated text
        return jsonify({"translation": translated_text})

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return jsonify({"error": "Speech recognition error"})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"})

if __name__ == '__main__':
    app.run(debug=True)
