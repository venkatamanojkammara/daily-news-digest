"""
backend/news/dedup.py
----------------------

Simple duplicate removal based on normalized text.

"""

from typing import List, Dict

#-------------------------------------------------------
# DeDuplicate Articles
#-------------------------------------------------------
def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
    """
    This function removes duplicate articles based on normalized text.
    """
    seen = set()
    unique_articles = []

    for article in articles:
        key = article["title"].lower().strip()

        if key not in seen:
            unique_articles.append(article)
            seen.add(key)

    return unique_articles