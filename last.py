import tkinter as tk
from tkinter import Label, Entry, Button, Text, Scrollbar, END, filedialog
from googletrans import Translator
from PyPDF2 import PdfReader
from translate import Translator as PDFTranslator
import speech_recognition as sr
from langdetect import detect
from gtts import gTTS
import pygame

# Initialize the speech recognition
recognizer = sr.Recognizer()

class LanguageTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translator")

        self.label = Label(root, text="Enter Text:")
        self.label.pack()

        self.input_entry = Entry(root, width=40)
        self.input_entry.pack()

        self.language_label = Label(root, text="Select Target Language:")
        self.language_label.pack()

        # Dropdown menu for selecting the target language
        self.languages = ["Gujarati","Hindi","Kannada","Malayalam","Marathi","Nepali","Punjabi","Tamil","Telugu","Sindhi","Urdu"]  # Add more languages as needed
        self.language_var = tk.StringVar(root)
        self.language_var.set(self.languages[0])  # Set default language
        self.language_dropdown = tk.OptionMenu(root, self.language_var, *self.languages)
        self.language_dropdown.pack()

        self.translate_button = Button(root, text="Translate", command=self.translate)
        self.translate_button.pack()

        self.output_label = Label(root, text="Translated Text:")
        self.output_label.pack()

        self.output_text = Text(root, width=40, height=4)
        self.output_text.pack()

        self.scrollbar = Scrollbar(root, command=self.output_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=self.scrollbar.set)

    def translate(self):
        source_text = self.input_entry.get()
        target_language = self.language_var.get().lower()  # Get the selected target language

        translated_text = self.translate_to_language(source_text, target_language)

        self.output_text.delete(1.0, END)
        self.output_text.insert(END, translated_text)

    def translate_to_language(self, source_text, target_language):
        translator = Translator()
        translation = translator.translate(source_text, src='en', dest=target_language)
        translated_text = translation.text

        return translated_text

class SpeechTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Recognition and Translation")

        self.translation_label = Label(root, text="")
        self.translation_label.pack()

        self.recognize_button = Button(root, text="Start Speech Recognition", command=self.recognize_and_translate)
        self.recognize_button.pack()

    def translate_to_indian_language(self, text, target_language):
        translator = Translator()
        translation = translator.translate(text, src='auto', dest=target_language)
        translated_text = translation.text
        return translated_text

    def play_audio(self, audio_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def recognize_and_translate(self):
        try:
            with sr.Microphone() as source:
                print("Speak something:")
                audio = recognizer.listen(source)

            spoken_text = recognizer.recognize_google(audio)
            print("You said:", spoken_text)

            detected_language = detect(spoken_text)
            print("Detected Language:", detected_language)

            if detected_language != "en":
                translated_text = self.translate_to_indian_language(spoken_text, "en")  # Translate to Hindi as an example
                print("Translation:", translated_text)
            else:
                translated_text = spoken_text

            tts = gTTS(translated_text, lang='en')
            tts.save("translation.mp3")

            self.play_audio("translation.mp3")

            # Update the label to display the translated text
            self.translation_label.config(text="Translation: " + translated_text)

        except sr.UnknownValueError:
            print("AVA's Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from AVA's Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

class PDFTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Translator")

        self.upload_button = Button(root, text="Upload PDF", command=self.translate_pdf)
        self.upload_button.pack(pady=10)

        self.languages = ["hi", "gu", "ta", "te", "ml"]  # Add more languages as needed
        self.target_language_var = tk.StringVar()
        self.target_language_var.set(self.languages[0])  # Set the default language

        self.language_label = Label(root, text="Select Target Language:")
        self.language_label.pack()
        self.language_dropdown = tk.OptionMenu(root, self.target_language_var, *self.languages)
        self.language_dropdown.pack()

        self.result_text = Text(root, height=10, width=40)
        self.result_text.pack(pady=10)

    def extract_text_from_pdf(self, pdf_file):
        text = ""
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

    def translate_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

        if not pdf_path:
            return

        target_language_code = self.target_language_var.get()
        extracted_text = self.extract_text_from_pdf(pdf_path)
        translator = PDFTranslator(to_lang=target_language_code)
        translated_text = translator.translate(extracted_text)

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, translated_text)

if __name__ == "__main__":
    root = tk.Tk()

    # Create instances of the three applications
    app1 = LanguageTranslatorApp(root)
    app2 = SpeechTranslatorApp(root)
    app3 = PDFTranslatorApp(root)

    root.mainloop()
