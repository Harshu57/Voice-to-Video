from __future__ import annotations

import logging

from .config import CONFIG


def setup_logger(name: str) -> logging.Logger:
    level = logging.DEBUG if CONFIG.debug else logging.INFO
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    for noisy in ["urllib3", "moviepy", "PIL"]:
        logging.getLogger(noisy).setLevel(logging.WARNING)
    return logger
