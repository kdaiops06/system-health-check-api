import logging
import sys

from app.config import get_settings

_FORMAT = "%(asctime)s | %(levelname)s | %(component)s | %(message)s"


def configure_logging() -> None:
    settings = get_settings()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))


def get_logger(component: str) -> logging.LoggerAdapter:
    return logging.LoggerAdapter(
        logging.getLogger(component),
        {"component": component},
    )
