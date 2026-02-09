"""
backend/db/crud.py
------------------

CRUD operations (Create, Read, Update, Delete) for database operations.

Rule:
- All Database access should be here.
- Streamlit pages and jobs should never write raw SQL queries.

This module contains functions used by:
- Streamlit UI (subscribe, update preferences, manage subscription).
- Scheduler/Worker (get subscribers, update statuses, email logs).

"""


#-------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------
from __future__ import annotations

from datetime import date
from typing import Optional, List, Any, Dict

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from backend.db.models import Subscriber, EmailLog


#------------------------------------------------------------------------
# CRUD operations for Subscriber
#------------------------------------------------------------------------
def create_subscriber(db: Session, email: str) -> Subscriber:
    """
    Create a new Subscriber if not exists, otherwise return existing.

    Default behaviour:
    - is_verified = False
    - is_active = True
    - preffered_time = "08:00"
    - time_zone = "Asia/Kolkata"
    - topics = []

    """

    email = email.strip().lower()

    existing = db.scalar(select(Subscriber).where(Subscriber.email == email))
    if existing: 
        return existing
    
    sub = Subscriber(email=email)
    db.add(sub)
    db.flush()
    return sub


#-----------------------------------------------------------------------------
# Get subscriber by email
#-----------------------------------------------------------------------------
def get_subscriber_by_email(db: Session, email: str) -> Optional[Subscriber]:
    """
    Return subscriber by email or None if not found.
    """
    email = email.strip().lower()

    return db.scalar(select(Subscriber).where(Subscriber.email == email))


#-----------------------------------------------------------------------------
# Get subscriber by id
#-----------------------------------------------------------------------------
def get_subscriber_by_id(db: Session, subscriber_id: int) -> Optional[Subscriber]:
    """
    Return subscriber by ID
    """
    return db.scalar(select(Subscriber).where(Subscriber.id == subscriber_id))


#-----------------------------------------------------------------------------
# Update preferences
#-----------------------------------------------------------------------------
def update_preferences(
    db: Session,
    email: str,
    topics: List[str],
    preffered_time: str,
    time_zone: str = "Asia/Kolkata"
) -> Subscriber:
    """
    Update subscriber preferences.
    - Topics must be List[str].
    - preffered_time format must be in HH:MM (e.g., 08:00).

    """
    sub = get_subscriber_by_email(db, email)
    if not sub:
        raise ValueError(f"Subscriber not found for email: {email}.")
    
    topics_clean = sorted({t.strip() for t in topics if t and t.strip()})

    sub.topics = topics_clean
    sub.preffered_time = preffered_time
    sub.time_zone = time_zone

    db.add(sub)
    db.flush()
    return sub


#-----------------------------------------------------------------------------
# Subscriber Verification
#-----------------------------------------------------------------------------
def set_verified(db: Session, email: str, verified: bool = True) -> Subscriber:
    """
    Mark subscriber as email verified/unverified.

    """
    sub = get_subscriber_by_email(db, email)
    if not sub:
        raise ValueError(f"Subscriber not found for email: {email}.")
    
    sub.is_verified = verified
    db.add(sub)
    db.flush()
    return sub


#-----------------------------------------------------------------------------
# Pause Digest
#-----------------------------------------------------------------------------
def pause_subscription(db: Session, email: str) -> Subscriber:
    """
    Pause daily sending of digest to the subscriber.
    """
    sub = get_subscriber_by_email(db, email)
    if not sub:
        raise ValueError(f"Subscriber not found for email: {email}")

    sub.is_active = False
    db.add(sub)
    db.flush()
    return sub
    

#-----------------------------------------------------------------------------
# Resume Digest
#-----------------------------------------------------------------------------
def resume_subscription(db: Session, email: str) -> Subscriber:
    """
    Resume daily emails to the subscribers.
    """
    sub = get_subscriber_by_email(db, email)
    if not sub:
        raise ValueError(f"Subscriber not found for email: {email}")
        
    sub.is_active = True
    db.add(sub)
    db.flush()

    return sub


#----------------------------------------------------------------------------
# Unsubscribe
#----------------------------------------------------------------------------
def unsubscribe(db: Session, email: str) -> Subscriber:
    """
    Unsubscribe user from emails.
    We keep subscriber row for audit/history but deactivete them.
    """
    sub = get_subscriber_by_email(db, email)
    if not sub:
        raise ValueError(f"Subscriber not found for email: {email}")
    
    sub.is_active = False
    db.add(sub)
    db.flush()

    return sub


#----------------------------------------------------------------------------
# Get Active Verified Subscribers
#----------------------------------------------------------------------------
def get_active_verified_subscribers(db: Session) -> List[Subscriber]:
    """
    Return all subscribers eligible for sending emails
    - is_active = True
    - is_verified = True
    """
    stmt = select(Subscriber).where(
        Subscriber.is_active.is_(True),
        Subscriber.is_verified.is_(True)
    )

    return list(db.scalars(stmt).all())


#----------------------------------------------------------------------------
# EmailLog CRUD
#----------------------------------------------------------------------------
def log_email_status(
    db: Session,
    subscriber_id: int,
    digest_date: date,
    subject: str,
    status: str,
    provider: Optional[str] = None,
    provider_message_id: Optional[str] = None,
    error_message: Optional[str] = None
) -> EmailLog:
    """
    Create an EmailLog row for each email send attempt.
    """
    log = EmailLog(
        subscriber_id = subscriber_id,
        digest_date = digest_date,
        subject = subject, 
        status = status,
        provider = provider,
        provider_message_id = provider_message_id,
        error_message = error_message
    )
    db.add(log)
    db.flush()

    return log


#----------------------------------------------------------------------------
# Check digest status
#----------------------------------------------------------------------------
def has_digest_been_sent(db: Session, subscriber_id: int, digest_date: date) -> bool:
    """
    Prevent duplicate emails on the same day.
    Returns True if digest has been sent to the subscriber on the same day.
    """
    stmt = select(EmailLog).where(
        EmailLog.subscriber_id == subscriber_id,
        EmailLog.digest_date == digest_date,
        EmailLog.status == "sent"
    )

    return db.scalar(stmt) is not None
