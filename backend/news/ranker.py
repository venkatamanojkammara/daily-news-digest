"""
backend/news/ranker.py
----------------------

Rank artilces by simple heuristics.
"""
from typing import List, Dict

#-------------------------------------------------------
# Rank Articles
#-------------------------------------------------------
def rank_articles(articles: List[Dict], top_n: int = 15):
    """
    Basic Ranking:
    - Longer Titles slightly prioritized.
    - Can later includes recency, source weight etc.
    """
    return sorted(articles, key=lambda x: len(x["title"]), reverse=True)[: top_n]