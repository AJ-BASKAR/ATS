import pdfplumber
import spacy
import re
import nltk
from nltk.corpus import stopwords

# Ensure stopwords are available
try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))

# Load SpaCy NLP model (can be used later for entity extraction, etc.)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    """
    Extracts all readable text from a PDF file using pdfplumber.
    """
    with pdfplumber.open(pdf_file) as pdf:
        pages = [page.extract_text() for page in pdf.pages if page.extract_text()]
        text = "\n".join(pages)
    return text if text.strip() else "No readable text found."

def remove_unwanted_sections(text):
    """
    Removes emails, phone numbers, URLs, and common irrelevant phrases.
    """
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)  # Remove emails
    text = re.sub(r'\b\d{10}\b', '', text)  # 10-digit phone numbers
    text = re.sub(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', '', text)  # formatted phone numbers
    text = re.sub(r'(references available upon request|soft skills:.*)', '', text, flags=re.IGNORECASE)
    return text

def clean_text(text):
    """
    Lowercases, removes special characters, and filters out stopwords.
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)  # Only letters and whitespace
    words = [word for word in text.split() if word not in stop_words]
    return " ".join(words)

def process_resume(pdf_file):
    """
    Full pipeline to extract and clean resume text.
    """
    raw_text = extract_text_from_pdf(pdf_file)
    cleaned = clean_text(remove_unwanted_sections(raw_text))
    return cleaned
