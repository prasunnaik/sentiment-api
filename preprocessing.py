import re

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and punctuation
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Remove extra spaces
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    
    return text
