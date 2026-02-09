"""
backend/news/cleaner.py
------------------------

Cleans article text before AI processing.

"""


#-------------------------------------------------------
# Imports
#-------------------------------------------------------
import re 


#-------------------------------------------------------
# Clean text
#-------------------------------------------------------
def clean_text(text: str) -> str:
    """
    This function removes extra spaces and junk lines.
    """
    text = re.sub(r"\s+", " ", text)
    text = text.replace("Advertisement", "")
    
    return text.strip()