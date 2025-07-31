"""Logging configuration for the auth backend."""

import logging
import sys
from typing import Dict, Any


def setup_logging(level: str = "INFO") -> None:
    """Setup application logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
