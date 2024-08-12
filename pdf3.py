import PyPDF2
from translate import Translator

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to translate text to a regional language
def translate_to_regional_language(text, target_language_code):
    translator = Translator(to_lang=target_language_code)
    translated_text = translator.translate(text)
    return translated_text

# PDF file to process
pdf_file = r"C:\K1\intro.pdf"  # Replace with the actual path to your PDF file

# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_file)

# Target language code (e.g., 'hi' for Hindi)
target_language_code = 'hi'

# Translate the extracted text to the regional language
translated_text = translate_to_regional_language(extracted_text, target_language_code)

# Print the translated text
print(translated_text)
