"""
Structured application logger using loguru.

Import this module's ``logger`` object anywhere in the codebase
instead of using the standard ``logging`` module.

The format includes timestamp, level, module name, and the message,
which makes log lines easy to filter in tools like Kibana or Datadog.
"""

import sys

from loguru import logger

# Remove the default loguru handler
logger.remove()

# ── Console handler ────────────────────────────────────────────────────────────
logger.add(
    sys.stdout,
    level="DEBUG",
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> — "
        "<level>{message}</level>"
    ),
    colorize=True,
)

# ── File handler (rotating) ────────────────────────────────────────────────────
logger.add(
    "logs/saathi_{time:YYYY-MM-DD}.log",
    level="INFO",
    rotation="00:00",    # New file at midnight
    retention="30 days",
    compression="gz",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} — {message}",
    enqueue=True,        # Thread-safe async logging
)

__all__ = ["logger"]
