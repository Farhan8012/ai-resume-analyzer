import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[^\w\s\n]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
