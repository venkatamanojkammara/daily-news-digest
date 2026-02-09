"""
backend/news/fetcher.py
------------------------
Responsible for collecting the news articles from the RSS feeds of truested sources.

This module:
- Uses topic -> Sources -> RSS mapping from backend/news/sources.py
- Fetches structured articles metadata.
- Do not extracts full article content. This will be handled in backend/news/extractor.py
- Do not summarize. This will be handled in 'ai/'.

Output of this module is the RAW article list used by the AI pipeline.
"""


#-------------------------------------------------------
# Imports
#-------------------------------------------------------
import feedparser
from typing import List, Dict
from backend.news.sources import NEWS_SOURCES
from backend.config import MAX_ARTICLES_PER_SOURCE
from backend.utils.logger import get_logger

logger = get_logger(__name__)


#-------------------------------------------------------
# Fetch Articles for sinlge topic
#-------------------------------------------------------
def fetch_articles_for_topic(topic: str) -> List[Dict]:
    """
    Fetches articles for a single topic from all trusted news sources.

    - Iterates through every trusted publisher. Checks if the publisher had the RSS feed for the particular topic.
    - Extracts the limited number of articles from each sources. 
    - Returns a list of articles metadata.

    Returns:
        A list of article dictionaries. Each dictionary contains:
        {
            'title': str,
            'url': str,
            'published': str,
            'source': str,
            'topic': str,
        }
    """
    articles = []

    for source_name, topics_map in NEWS_SOURCES.items():
        feed_url = topics_map.get(topic)
        if not feed_url:
            continue

        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
                articles.append({
                    "title": entry.get("title", "").strip(),
                    "url": entry.get("link", "").strip(),
                    "published": entry.get("published", ""),
                    "source": source_name,
                    "topic": topic 
                })
        except Exception as e:
            logger.error(f"Failed to fetch {source_name} feed for {topic}: {e}")


    return articles


#-------------------------------------------------------
# Fetch articles for multiple topics
#-------------------------------------------------------
def fetch_articles_for_topics(topics: str) -> List[Dict]:
    """
    Fetches articles for multiple topics.

    This function acts as a wrapper over 'fetch_articles_for_topic()' and 
    is designed to support user personalization, where user can select multiple topics.

    - Loops through each selected topics.
    - Calls the single topic fetcher -> fetch_articles_for_topic()
    - Combines all results into one unified list.

    Example:
    topics = ["Technology", "Business", "Politics"]
    Returns a list containing articles from both categories.
      
    """

    all_articles = []

    for topic in topics:
        all_articles.extend(fetch_articles_for_topic(topic))
    
    return all_articles