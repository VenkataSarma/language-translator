import tkinter as tk
from tkinter import Label, Entry, Button, Text, Scrollbar, END
from googletrans import Translator

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

if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageTranslatorApp(root)
    root.mainloop()

