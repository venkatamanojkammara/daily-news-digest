"""
backend/email/validators.py
---------------------------

Utility function for validating email.
"""

import re


EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


#------------------------------------------------------------------------
# Email Validation
#------------------------------------------------------------------------
def is_valid_email(email: str) -> bool:
    """
    Validate email address using regex
    Returns True if email is valid, else False.
    """
    if not email:
        return False
    return bool(EMAIL_REGEX.match(email.strip()))