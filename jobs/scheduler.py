"""
jobs/scheduler.py
-----------------

Time-based scheduler for running the daily news digest pipeline.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import time
from datetime import date

from backend.db.connection import get_session
from backend.db import crud
from backend.utils.time_utils import is_send_time
from backend.utils.logger import get_logger

from jobs.daily_pipeline import run_daily_pipeline

logger = get_logger(__name__)

CHECK_INTERVAL_SECONDS = 60  # check every minute


def run_scheduler() -> None:
    """
    Continuously monitor users and trigger daily pipeline
    when at least one user reaches their preferred time.
    """
    logger.info("Scheduler started")

    while True:
        try:
            today = date.today()
            trigger_pipeline = False

            with get_session() as db:
                users = crud.get_active_verified_subscribers(db)

                for user in users:
                    if crud.has_digest_been_sent(db, user.id, today):
                        continue

                    if is_send_time(user.preffered_time, user.time_zone):
                        logger.info(
                            f"Triggering digest pipeline at "
                            f"{user.preffered_time} ({user.time_zone})"
                        )
                        trigger_pipeline = True
                        break  # only decide trigger, not process users

            if trigger_pipeline:
                run_daily_pipeline()

        except Exception as e:
            logger.exception(f"Scheduler error: {e}")

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_scheduler()
