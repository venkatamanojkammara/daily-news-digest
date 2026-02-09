"""
backend/utils/time_utils.py
---------------------------

Handles time related operations. (TimeZone, Sheduling logic)
"""


#-------------------------------------------------------
# Imports
#-------------------------------------------------------
from datetime import datetime
import pytz


#-------------------------------------------------------
# Get Time in TimeZone
#-------------------------------------------------------
def get_current_time_in_timezone(timezone: str) -> datetime:
    """
    Returns current datetime in given timezone.
    """
    tz = pytz.timezone(timezone)
    return datetime.now(tz)


#-------------------------------------------------------
# Check if time matches user preffered time
#-------------------------------------------------------
def is_send_time(preffered_time: str, timezone: str) -> bool:
    """
    Check if current time matches user's preffered time.
    preffered_time format: 'HH:MM'
    """

    now = get_current_time_in_timezone(timezone)
    current_time = now.strftime('%H:%M')

    return (current_time == preffered_time)