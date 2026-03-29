import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))

    # File handler (with rotation)
    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(logging.Formatter(log_format))

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)