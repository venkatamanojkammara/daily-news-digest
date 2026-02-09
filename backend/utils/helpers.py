"""
backend/utils/helpers.py
-------------------------

General purpose helper functions used across the project.
"""


#-------------------------------------------------------
# Imports
#-------------------------------------------------------
from typing import List, Dict


#-------------------------------------------------------
# Chunk List
#-------------------------------------------------------
def chunk_list(list: List, chunk_size: int) -> List[List]:
    """
    Splits a list into chunks of given size.
    """
    return [list[i : i + chunk_size] for i in range(0, len(list), chunk_size)]


#-------------------------------------------------------
# Safe Get
#-------------------------------------------------------
def safe_get(data: Dict, key: str, default=None):
    """
    Safely retrieves a value from a dictionary.
    """
    return data.get(key, default)


#-------------------------------------------------------
# Truncate Text
#-------------------------------------------------------
def truncate_text(text: str, max_chars: int) -> str:
    """
    Truncates a string to a maximum length.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "..."