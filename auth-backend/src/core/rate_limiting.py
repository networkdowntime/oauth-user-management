"""Rate limiting configuration for the application."""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


# Create rate limiter instance
limiter = Limiter(key_func=get_remote_address)
