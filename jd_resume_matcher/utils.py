from pdfminer.high_level import extract_text

def extract_text_from_file(path):
    """Extract full text from .pdf or .txt files."""
    if path.lower().endswith('.pdf'):
        return extract_text(path)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()