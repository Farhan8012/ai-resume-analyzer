import re

def clean_text(text):
    """
    Cleans text but PRESERVES newlines so structure is kept.
    """
    # 1. Convert to lowercase
    text = text.lower()
    
    # 2. Remove special characters (keep letters, numbers, spaces, AND newlines)
    # [^...] means "not in this list". \w=words, \s=whitespace (includes \n)
    text = re.sub(r'[^\w\s]', '', text)
    
    # 3. Replace multiple spaces/tabs with a single space
    # We use [ \t]+ instead of \s+ to avoid grabbing newlines
    text = re.sub(r'[ \t]+', ' ', text)
    
    # 4. Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    return text.strip()