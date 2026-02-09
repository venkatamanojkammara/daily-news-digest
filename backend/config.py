"""
backend/config.py
-----------------

Central configuration for the AI News Digest product.

This module is the single source of truth for:
- Environment variables (.env)
- Database connection URL
- Newsletter topics and default sources
- News fetch limits
- Gemini API settings (LLM layer)
- Email settings (simple SMTP: email + password)
- Security settings (token signing)
- Logging settings

"""


#-------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------
from __future__ import annotations
import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv


#------------------------------------------------------------------------
# Load envirornment variables from .env file from project root directory
#------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOTENV_PATH = PROJECT_ROOT

if DOTENV_PATH.exists():
    load_dotenv()


#------------------------------------------------------------------------
# General Application Settings
#------------------------------------------------------------------------
APP_NAME: str = os.getenv("APP_NAME", "AI News Digest")
APP_ENV: str = os.getenv("APP_ENV", "development")
APP_BASE_URL: str = os.getenv("APP_BASE_URL", "http://localhost:8501")
DEFAULT_TIMEZONE: str = os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")
DEFAULT_PREFFERED_TIME = os.getenv("DEFAULT_PREFFERED_TIME", "08:00")


#------------------------------------------------------------------------
# Database Configuration Settings
# - SQLite (MVP/local): sqlite:///data/app.db
# - PostgreSQL (prod): postgresql+psycopg2://user:pass@host:5432/db
#------------------------------------------------------------------------
# DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{PROJECT_ROOT / 'data' / 'app.db'}")

DB_PATH = PROJECT_ROOT / "data" / "app.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH.as_posix()}")

if DATABASE_URL.startswith("sqllite"):
    (PROJECT_ROOT / 'data').mkdir(parents=True, exist_ok=True)



#------------------------------------------------------------------------
# Gemini API Settings (LLM Layer)
#------------------------------------------------------------------------
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_OUTPUT_TOKENS: int = int(os.getenv("LLM_MAX_OUTPUT_TOKENS", "512"))

# digest and summary preferences
SUMMARY_BULLETS_COUNT: int = int(os.getenv("SUMMARY_BULLETS_COUNT", "3"))
DIGEST_MAX_ARTCLES_PER_TOPIC: int = int(os.getenv("DIGEST_MAX_ARTCLES_PER_TOPIC", "5"))
DIGEST_TOTAL_MAX_ARTICLES: int = int(os.getenv("DIGEST_TOTAL_MAX_ARTICLES", "12")) 


#------------------------------------------------------------------------
# Email Settings
#------------------------------------------------------------------------
EMAIL_PROVIDER: str = os.getenv("EMAIL_PROVIDER", "smtp").lower()

FROM_EMAIL: str = os.getenv("FROM_EMAIL", "")
REPLY_TO_EMAIL: str = os.getenv("REPLY_TO_EMAIL", FROM_EMAIL).strip()

SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL: str = os.getenv("SMTP_EMAIL", FROM_EMAIL).strip()
SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "true").lower() == "true"


#------------------------------------------------------------------------
# Security Settings 
#------------------------------------------------------------------------

SECRET_KEY: str = os.getenv("SECRET_KEY", "change-the-key-leter")


#------------------------------------------------------------------------
# Topics and Sources Settings
#------------------------------------------------------------------------

TOPICS: List[str] = [
    "Technology",  
    "Business", 
    "Politics",
    "Sports",
    "World"
]

DEFAULT_SOURCES: List[str] = [
    "India Today", 
    "Hindistan Times",
    "The Hindu",
    "Indian Express", 
    "Times of India"
]


#------------------------------------------------------------------------
# News Fetch Limits
#------------------------------------------------------------------------

MAX_ARTICLES_PER_SOURCE: int = int(os.getenv("MAX_ARTICLES_PER_SOURCE", "5"))
MAX_ARTICLES_TEXT_CHARS: int = int(os.getenv("MAX_ARTICLES_TEXT_CHARS", "12000"))


#------------------------------------------------------------------------
# Logging Settings
#------------------------------------------------------------------------

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR: Path = os.getenv("LOG_DIR", (PROJECT_ROOT / "logs"))
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)


#------------------------------------------------------------------------
# Config Validation Helpers
#------------------------------------------------------------------------

def validate_config() -> None:
    """
    Validate critical validation values.
    Recommended usage:
        from backend.config import validate_config
        validate_config()
    Returns:
        RuntimeError if any critical config values are missing or invalid.
    """

    if APP_ENV in ("production", "staging"):
        if not SECRET_KEY or SECRET_KEY.startswith("dev-"):
            raise RuntimeError("SECRET_KEY must be surely set in production/stating envirornments.")
    
    if LLM_PROVIDER != "gemini":
        raise RuntimeError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}. Currently only gemini is supported.")
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY must be set for LLM_PROVIDER 'gemini'.")
    
    if EMAIL_PROVIDER != "smtp":
        raise RuntimeError(f"Unsuppoted EMAIL_PROVIDER: {EMAIL_PROVIDER}. Currently only smtp is suppoted.")
    if not FROM_EMAIL:
        raise RuntimeError("From email must be set.")
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise RuntimeError("SMTP_EMAIL and SMTP_PASSWORD must be set for email sending.")
    


#------------------------------------------------------------------------
# Print Config Summary
#------------------------------------------------------------------------
def print_config_summary() -> None:
    """
    Print a summary of critical configuration values.
    Useful for debugging and verification during application startup.
    """
    safe = {
        "APP_NAME": APP_NAME,
        "APP_ENV": APP_ENV,
        "APP_BASE_URL": APP_BASE_URL,
        "DATABASE_URL": DATABASE_URL,
        "LLM_PROVIDER": LLM_PROVIDER,
        "GEMINI_MODEL": GEMINI_MODEL,
        "EMAIL_PROVIDER": EMAIL_PROVIDER,
        "SMTP_HOST": SMTP_HOST,
        "SMTP_PORT": SMTP_PORT,
        "SMTP_EMAIL": SMTP_EMAIL,
        "FROM_EMAIL": FROM_EMAIL,
        "DEFAULT_TIMEZONE": DEFAULT_TIMEZONE
    }

    for key, value in safe.items():
        print(f"{key} = {value}")