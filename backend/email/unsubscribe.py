"""
backend/email/unsubscribe.py
-----------------------------

Generate and verify secure unsubscribe tokens

"""


#--------------------------------------------------------------------------------
# Imports
#--------------------------------------------------------------------------------
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from backend.config import SECRET_KEY
TOKEN_MAX_AGE = 60 * 60 * 24 * 7

serializer = URLSafeTimedSerializer(SECRET_KEY)



#---------------------------------------------------------------------
# Generate Unsubscribe Token
#---------------------------------------------------------------------
def generate_unsubscribe_token(email: str) -> str:
    """
    Generate a signed unsubscribe token for an email.
    """

    return serializer.dumps(email, salt="unsubscribe-token")


#---------------------------------------------------------------------
# Verify Unsubscribe Token
#---------------------------------------------------------------------
def verify_unsubscribe_token(token: str) -> str | None:
    """
    Verify token and return email if valid.
    Returns None if token is invalid or expired.
    """
    try:
        email = serializer.loads(token, salt="unsubscribe-token", max_age=TOKEN_MAX_AGE)
        return email
    except (BadSignature, SignatureExpired):
        return None