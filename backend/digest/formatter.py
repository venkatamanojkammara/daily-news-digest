"""
backend/digest/formatter.py
---------------------------

Converts structured digest into HTML email content.
"""


#-----------------------------------------------------------------
# Imports
#-----------------------------------------------------------------
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from backend.config import APP_BASE_URL
from backend.email.unsubscribe import generate_unsubscribe_token

TEMPLATE_DIR = Path(__file__).parent / "templates"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


#-----------------------------------------------------------------
# Render to HTML
#-----------------------------------------------------------------
def render_digest_html(digest: dict) -> str:
    """
    Render digest into HTML using Jinja template.
    """

    template = env.get_template("digest.html")

    unsubscribe_token = generate_unsubscribe_token(digest["user_email"])
    unsubscribe_url = f"{APP_BASE_URL}/unsubscribe?token={unsubscribe_token}"

    return template.render(
        date=digest["date"],
        sections=digest["sections"],
        unsubscribe_url=unsubscribe_url
    )
