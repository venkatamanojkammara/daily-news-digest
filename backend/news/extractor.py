"""
backend/news/extractor.py
-------------------------

Extracts the full article content from a given news URL.

This module:
- Downloads article HTML
- Extracts main textual content
- Truncates text to a safe maximum length
- Fails gracefully on errors
"""

# -------------------------------------------------------
# Imports
# -------------------------------------------------------
from newspaper import Article

from backend.config import MAX_ARTICLES_TEXT_CHARS
from backend.utils.logger import get_logger

logger = get_logger(__name__)


# -------------------------------------------------------
# Extract single article text
# -------------------------------------------------------
def extract_article_text(url: str) -> str:
    """
    Extract full article text from a URL.

    Steps:
    1. Download article using newspaper3k
    2. Parse main body text
    3. Apply NLP processing (when available)
    4. Truncate to MAX_ARTICLES_TEXT_CHARS

    Parameters
    ----------
    url : str
        News article URL

    Returns
    -------
    str
        Cleaned article text (possibly truncated),
        or empty string if extraction fails.
    """
    try:
        article = Article(url, request_timeout=10)
        article.download()
        article.parse()

        # Improves content extraction for many sites
        try:
            article.nlp()
        except Exception:
            pass  # NLP is optional

        text = article.text.strip()

        if not text:
            logger.warning(f"No extractable text found for URL: {url}")
            return ""

        return text[:MAX_ARTICLES_TEXT_CHARS]

    except Exception as e:
        logger.error(f"Failed to extract article from {url}: {e}")
        return ""
