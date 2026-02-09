"""
backend/news/sources.py
------------------------

Top trusted news sources based on the preference topics.
Only reputed publishers are included.

"""
NEWS_SOURCES = {
    "The Hindu": {
        "Technology": "https://www.thehindu.com/sci-tech/technology/feeder/default.rss",
        "Business": "https://www.thehindu.com/business/feeder/default.rss",
        "Politics": "https://www.thehindu.com/news/national/feeder/default.rss",
        "Sports": "https://www.thehindu.com/sport/feeder/default.rss",
        "World": "https://www.thehindu.com/news/international/feeder/default.rss",
    },

    "Times of India": {
        "Technology": "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms",
        "Business": "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
        "Politics": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
        "Sports": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
        "World": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    },

    "Deccan Chronicle": {
        "Technology": "https://www.deccanchronicle.com/rss/technology.xml",
        "Business": "https://www.deccanchronicle.com/rss/business.xml",
        "Politics": "https://www.deccanchronicle.com/rss/nation.xml",
        "Sports": "https://www.deccanchronicle.com/rss/sports.xml",
        "World": "https://www.deccanchronicle.com/rss/world.xml",
    },

    "Indian Express": {
        "Technology": "https://indianexpress.com/section/technology/feed/",
        "Business": "https://indianexpress.com/section/business/feed/",
        "Politics": "https://indianexpress.com/section/india/feed/",
        "Sports": "https://indianexpress.com/section/sports/feed/",
        "World": "https://indianexpress.com/section/world/feed/",
    },

    "Hindustan Times": {
        "Technology": "https://www.hindustantimes.com/feeds/rss/technology/rssfeed.xml",
        "Business": "https://www.hindustantimes.com/feeds/rss/business/rssfeed.xml",
        "Politics": "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",
        "Sports": "https://www.hindustantimes.com/feeds/rss/sports/rssfeed.xml",
        "World": "https://www.hindustantimes.com/feeds/rss/world-news/rssfeed.xml",
    },
}