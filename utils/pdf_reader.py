import pdfplumber

def extract_text_from_pdf(file):
    """
    Extracts text from a PDF file with error handling and validation.
    """
    try:
        # 1. Basic Validation: Check if it's really a PDF
        if file.type != "application/pdf":
            return "Error: Uploaded file is not a standard PDF."

        # 2. Extract Text
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        
        # 3. Check for Empty PDFs (Scanned images or corrupted files)
        if not text.strip():
            return "Error: No text found. This PDF might be an image or scanned document."
            
        return text

    except Exception as e:
        return f"Error reading PDF: {str(e)}"