import pdfplumber
import re
from typing import List
from io import BytesIO


def extract_words_from_pdf(file_content: bytes) -> List[str]:
    """
    Extract words from a PDF file.
    Returns a list of unique words (cleaned and deduplicated).
    """
    words = set()
    
    try:
        with pdfplumber.open(BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Extract words using regex (alphabetical, 4+ characters)
                    # This filters out common short words and numbers
                    word_pattern = r'\b[A-Za-z]{4,}\b'
                    found_words = re.findall(word_pattern, text)
                    
                    # Clean words: lowercase, remove duplicates
                    for word in found_words:
                        cleaned = word.lower().strip()
                        # Filter out common words and ensure it's a valid word
                        if len(cleaned) >= 4 and cleaned.isalpha():
                            words.add(cleaned)
    
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        raise
    
    return sorted(list(words))
