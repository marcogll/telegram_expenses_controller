"""
Handles user permissions and access control.

Defines who is allowed to perform certain actions, such as uploading
or querying expense data.
"""

from app.config import config

def is_user_allowed(user_id: str) -> bool:
    """
    Checks if a given user ID is allowed to use the bot.

    For now, this is a stub. A real implementation could check against
    a database of users or a predefined list in the config.
    """
    # For example, you could have a comma-separated list of allowed IDs
    # ALLOWED_USERS = config.ALLOWED_USER_IDS.split(',')
    # return user_id in ALLOWED_USERS
    return True # Allow all users for now
