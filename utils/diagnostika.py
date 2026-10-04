"""Configuration for local, bounded game diagnostics."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import user_data_dir


def configure_logging():
    log_dir = user_data_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = (log_dir / "harem_debug.log").resolve()
    logger = logging.getLogger()
    if not any(
        isinstance(handler, RotatingFileHandler)
        and Path(handler.baseFilename).resolve() == log_path
        for handler in logger.handlers
    ):
        handler = RotatingFileHandler(
            log_path,
            maxBytes=1_000_000,
            backupCount=2,
            encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s"
        ))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return log_path
