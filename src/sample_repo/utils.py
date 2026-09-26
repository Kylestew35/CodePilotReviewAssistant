"""Utility functions."""

import re
import time
import logging

logger = logging.getLogger(__name__)


def validate_email(email):
    """Validate email address."""
    # Overly permissive regex
    return re.match(r".+@.+", email) is not None


def retry(func, retries=3):
    """Retry a function call."""
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(1)


def flatten(nested_list):
    """Flatten a nested list."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def chunk(lst, size):
    """Split list into chunks."""
    # Off-by-one possible if size is 0
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def sanitize_input(value):
    """Sanitize user input."""
    # Incomplete sanitization — only strips whitespace
    return str(value).strip()


# Dead code — never called anywhere
def _legacy_format_price(price):
    return "$" + str(round(price, 2))
