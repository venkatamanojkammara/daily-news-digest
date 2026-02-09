"""
jobs/daily_pipeline.py
----------------------

End-to-end daily news digest pipeline.

This script:
1. Fetches active + verified subscribers
2. Fetches news based on user topic preferences
3. Extracts and cleans article text
4. Summarizes articles using Gemini (LangChain)
5. Deduplicates and ranks articles
6. Builds personalized digest
7. Renders HTML email
8. Sends email
9. Logs email status

This file is the HEART of the product.
If this works → the product works.
"""

from datetime import date

from backend.db.connection import get_session
from backend.db import crud

from backend.news.fetcher import fetch_articles_for_topics
from backend.news.extractor import extract_article_text
from backend.news.cleaner import clean_text
from backend.news.dedup import deduplicate_articles
from backend.news.ranker import rank_articles

from backend.ai.summarizer import summarize_article

from backend.digest.builder import build_digest_for_user
from backend.digest.formatter import render_digest_html

from backend.email.sender import send_email
from backend.config import APP_NAME
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def run_daily_pipeline() -> None:
    """
    Run the daily news digest pipeline for all eligible users.
    """

    logger.info("Starting daily news pipeline")

    today = date.today()

    with get_session() as db:
        users = crud.get_active_verified_subscribers(db)

        if not users:
            logger.info("No active verified subscribers found.")
            return

        logger.info(f"Found {len(users)} active subscribers")

        for user in users:
            logger.info(f"Processing user: {user.email}")

            # Prevent duplicate emails for same day
            if crud.has_digest_been_sent(db, user.id, today):
                logger.info(f"Digest already sent today for {user.email}")
                continue

            try:
                # --------------------------------------------------
                # 1. Fetch raw articles based on user topics
                # --------------------------------------------------
                raw_articles = fetch_articles_for_topics(user.topics)

                if not raw_articles:
                    logger.warning(f"No articles found for user {user.email}")
                    continue

                # --------------------------------------------------
                # 2. Extract + clean + summarize articles
                # --------------------------------------------------
                summarized_articles = []

                for article in raw_articles:
                    text = extract_article_text(article["url"])
                    if not text:
                        continue

                    cleaned = clean_text(text)
                    if not cleaned:
                        continue

                    ai_result = summarize_article(cleaned)

                    summarized_articles.append({
                        "title": article["title"],
                        "url": article["url"],
                        "source": article["source"],
                        "topic": article["topic"],

                        # AI output
                        "bullets": ai_result.get("bullets", []),
                        "summary": ai_result.get("summary", ""),
                        "category": ai_result.get("category", article["topic"]),
                        "importance_score": ai_result.get("importance_score", 3),
                    })

                if not summarized_articles:
                    logger.warning(f"No summarized articles for {user.email}")
                    continue

                # --------------------------------------------------
                # 3. Deduplicate & rank articles
                # --------------------------------------------------
                summarized_articles = deduplicate_articles(summarized_articles)
                summarized_articles = rank_articles(summarized_articles)

                # --------------------------------------------------
                # 4. Build digest for user
                # --------------------------------------------------
                digest = build_digest_for_user(user, summarized_articles)

                if not digest["sections"]:
                    logger.warning(f"Empty digest for {user.email}")
                    continue

                # --------------------------------------------------
                # 5. Render HTML email
                # --------------------------------------------------
                html_body = render_digest_html(digest)

                subject = f"🗞️ {APP_NAME} — Daily News Digest"

                # --------------------------------------------------
                # 6. Send email
                # --------------------------------------------------
                success = send_email(
                    to_email=user.email,
                    subject=subject,
                    html_body=html_body,
                )

                # --------------------------------------------------
                # 7. Log email status
                # --------------------------------------------------
                if success:
                    crud.log_email_status(
                        db=db,
                        subscriber_id=user.id,
                        digest_date=today,
                        subject=subject,
                        status="sent",
                        provider="smtp",
                    )
                    logger.info(f"Email sent successfully to {user.email}")
                else:
                    crud.log_email_status(
                        db=db,
                        subscriber_id=user.id,
                        digest_date=today,
                        subject=subject,
                        status="failed",
                        provider="smtp",
                        error_message="SMTP send failed",
                    )
                    logger.error(f"Email send failed for {user.email}")

            except Exception as e:
                logger.exception(f"Pipeline error for user {user.email}: {e}")

    logger.info("Daily news pipeline finished")


if __name__ == "__main__":
    run_daily_pipeline()
