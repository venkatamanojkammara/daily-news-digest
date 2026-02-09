"""
backend/email/tracker.py
-------------------------

Future features for:
- Open tracking.
- Click tracking.

Currently contains placeholders for future implementations.
"""


#------------------------------------------------------------------------
# Add Tracking Pixel
#------------------------------------------------------------------------
def add_tracking_pixel(html: str, user_id: int, message_id: str) -> str:
    """
    Add invisible tracking pixel to email HTML.
    (Implement later with an API endpoint that logs opens).

    """
    pixel_url = f"https://yourdomain.com/track/open/{user_id}"
    tracking_img = f'<img src="{pixel_url}" width="1" height="1" style="display:none;"/>'
    return html + tracking_img


#------------------------------------------------------------------------
# Rewrite Links for Click Tracking
#------------------------------------------------------------------------
def rewrite_links_for_click_tracking(html: str, user_id: int) -> str:
    """
    Rewrite links to track clicks before redirecting.
    Placeholder for future implementation.

    """
    return html