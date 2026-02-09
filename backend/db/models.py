"""
backend/db/models.py
---------------------
SQL Alchemy ORM models (database tables).

This file defines the database schema used by the application. It should contain:
- Base declarative class for model definitions.
- Table models (Subscribers, Email-log, Digest, etc.)

Note:
- Not keeping CRUD operations here, only the models.

"""


#-------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------
from __future__ import annotations

from datetime import datetime, date
from typing import Any, Optional, List

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer, 
    String, 
    Text,
    func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import JSON


#------------------------------------------------------------------------
# Base class for all ORM models
#------------------------------------------------------------------------
class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    """
    pass


#------------------------------------------------------------------------
# Subscriber Model
#------------------------------------------------------------------------
class Subscriber(Base):
    """
    Stores newsletter subscribers and their preferences.
    
    Fields:
        - email: Unique identifier for the subscriber.
        - topics: List of interested topics (JSON array).
        - preffered_time: Local time in the format HH:MM (eg: 08:00).
        - time_zone: e.g., 'Asia/Kolkota'.
        - is_active: Pause/Resume digest.
        - is_verified: email verification status (recommanded).
    """
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)

    topics: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    preffered_time: Mapped[str] = mapped_column(String(5), nullable=False, default="08:00")
    time_zone: Mapped[str] = mapped_column(String(64), nullable=False, default="Asia/Kolkota")

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())

    email_logs: Mapped[list['EmailLog']] = relationship("EmailLog", back_populates="subscriber", cascade="all, delete-orphan")


    def __repr__(self) -> str:
        return f"<Subscriber id={self.id}, email={self.email} active={self.is_active} verified={self.is_verified}>"


#------------------------------------------------------------------------
# Email Log model
#------------------------------------------------------------------------
class EmailLog(Base):
    """
    Logs/Stores every email sent to subscribers.

    Why this matter:
    - Lets you debus deliverability issues.
    - Helps you build admin analytics later.
    - Makes your scheduler pipeline reliable.

    Fields:
    - status: 'sent', 'failed', 'bounced'.capitalize
    - provider: 'sendgrid', 'ses', etc.
    - provider_message_id: useful for debugging with email provider.
    
    """
    __tablename__ = "email_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    subscriber_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscribers.id", ondelete="CASCADE"), nullable=False, index=True)

    digest_date: Mapped[date] = mapped_column(Date, nullable=False)
    subject: Mapped[str] = mapped_column(String(256), nullable=False, default="Daily News Digest")

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="sent")
    provider: Mapped[str] = mapped_column(String(32), nullable=True)
    provider_message_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    subscriber: Mapped["Subscriber"] = relationship("Subscriber", back_populates="email_logs")


    def __repr__(self) -> str:
        return f"<EmailLog id={self.id}, subscriber_id={self.subscriber_id}, date={self.digest_date}, status={self.status}>"
        
