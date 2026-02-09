"""
backend/email/sender.py
------------------------

Handles all email sending logic using SMTP using credentials from config.py

Supports:
- HTML Emails
- TLS encryption
- Error handling

"""


#----------------------------------------------------------------------------
# Imports
#----------------------------------------------------------------------------
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_EMAIL,
    SMTP_PASSWORD,
    SMTP_USE_TLS,
    FROM_EMAIL,
    REPLY_TO_EMAIL
)
from backend.utils.logger import get_logger

logger = get_logger(__name__)


#------------------------------------------------------------------------
# Send Email
#------------------------------------------------------------------------
def send_email(to_email: str, subject: str, html_body: str) -> bool:
    """
    Send an email using SMTP.
    
    Args:
        to_email: Receipent email address.
        subject: Subject of an email.
        html_body: HTML view of email.

    Returns:
        True if email sent successfully, False otherwise.
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg["Reply-To"] = REPLY_TO_EMAIL

        msg.attach(MIMEText(html_body, "html"))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        if SMTP_USE_TLS:
            server.starttls()

        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        server.quit()

        logger.info(f"Email sent sucessfully to {to_email}.")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}. Error: {e}.")
        return False

    
