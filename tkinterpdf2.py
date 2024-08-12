import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
from translate import Translator

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to handle the translation
def translate_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    if not pdf_path:
        return

    target_language_code = target_language_var.get()
    extracted_text = extract_text_from_pdf(pdf_path)
    translator = Translator(to_lang=target_language_code)
    translated_text = translator.translate(extracted_text)

    # Display the translated text
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, translated_text)

# Create the tkinter window
root = tk.Tk()
root.title("PDF Translator")

# Create a button to upload a PDF
upload_button = tk.Button(root, text="Upload PDF", command=translate_pdf)
upload_button.pack(pady=10)

# Create a dropdown for selecting the target language
languages = ["hi", "gu", "ta", "te", "ml"]  # Add more languages as needed
target_language_var = tk.StringVar()
target_language_var.set(languages[0])  # Set the default language

language_label = tk.Label(root, text="Select Target Language:")
language_label.pack()
language_dropdown = tk.OptionMenu(root, target_language_var, *languages)
language_dropdown.pack()

# Create a text widget to display the translated text
result_text = tk.Text(root, height=10, width=40)
result_text.pack(pady=10)

root.mainloop()
