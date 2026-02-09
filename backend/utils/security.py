"""
backend/utils/security.py
-------------------------

Security helps for hashing and token-safe operations.
"""


#-------------------------------------------------------
# Imports
#-------------------------------------------------------
import hashlib
import hmac
from backend.config import SECRET_KEY


#-------------------------------------------------------
# Hash Email
#-------------------------------------------------------
def hash_email(email: str) -> str:
    """
    Hashes an email using HMAC with SHA256. (for logging/anonymization)
    """
    return hashlib.sha256(email.encode()).hexdigest()


#-------------------------------------------------------
# Sign Data
#-------------------------------------------------------
def sign_data(data: str) -> str:
    """
    Create HMAC signature using SECRET_KEY.
    """
    return hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()