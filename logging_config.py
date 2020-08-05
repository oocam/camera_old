import os
import logging
from logging.config import dictConfig

log_path = "system.logs"

if os.environ.get("OOCAM_LOGS") is not None:
    log_path = os.environ["OOCAM_LOGS"]

print(f"Log files will be generated at: {log_path}")

logging_config = dict(
    version=1,
    formatters={
        "formatter": {"format": "%(asctime)s %(name)-s:%(levelname)-s: %(message)s"},
    },
    handlers={
        "handler": {
            "class": "logging.FileHandler",
            "formatter": "formatter",
            "level": logging.DEBUG,
            "filename": log_path,
        }
    },
    root={"handlers": ["handler"], "level": logging.DEBUG},
)

dictConfig(logging_config)
