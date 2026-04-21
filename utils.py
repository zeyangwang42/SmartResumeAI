import pdfplumber
import re


def extract_text_from_pdf(uploaded_file) -> str:
    text = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()