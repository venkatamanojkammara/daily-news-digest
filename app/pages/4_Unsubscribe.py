import streamlit as st

from backend.db.connection import get_session
from backend.db import crud
from backend.email.unsubscribe import verify_unsubscribe_token
from app.components.alerts import success, error, info

st.title("❌ Unsubscribe")

token = st.query_params.get("token")

if not token:
    error(
        "This unsubscribe page is accessed via a special link.\n\n"
        "Please use the unsubscribe link provided in the email you received."
    )
else:
    email = verify_unsubscribe_token(token)

    if not email:
        error("This unsubscribe link is invalid or has expired.")
    else:
        with get_session() as db:
            crud.unsubscribe(db, email)

        success("You have been unsubscribed successfully.")
        info("You will no longer receive daily news digests.")
