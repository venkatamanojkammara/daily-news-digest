"""
backend/digest/builder.py
-------------------------

Builds a structured news digest for a specific user
based on their topic preferences and AI-summarized articles.
"""


#-----------------------------------------------------------------
# Imports
#-----------------------------------------------------------------
from datetime import datetime
from collections import defaultdict
from typing import List, Dict

from backend.config import DIGEST_TOTAL_MAX_ARTICLES


#-----------------------------------------------------------------
# Build Digest
#-----------------------------------------------------------------
def build_digest_for_user(user, summarized_articles: List[Dict]) -> Dict:
    """
    Build a digest structure for a user.

    Parameters
    ----------
    user : Subscriber object
           Contains user preferences like topics.
    summarized_articles : List[Dict]
        Articles already processed by AI summarizer.
    Returns: Dict
        Structured digest object.
    """

    sections = defaultdict(list)
    user_topics = set(user.topics)

    for article in summarized_articles:
        if article["topic"] in user_topics:
            sections[article["topic"]].append(article)

    total = sum(len(v) for v in sections.values())
    if total > DIGEST_TOTAL_MAX_ARTICLES:
        trimmed = 0
        for topic in sections:
            sections[topic] = sections[topic][:2]
            trimmed += len(sections[topic])
            if trimmed >= DIGEST_TOTAL_MAX_ARTICLES:
                break

    return {
        "date": datetime.now().strftime("%d %b %Y"),
        "user_email": user.email,
        "sections": sections
    }
