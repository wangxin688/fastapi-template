import contextvars
import logging
import logging.config
import os
import random
import string
from datetime import datetime

from app.core.config import settings

log_id_context = contextvars.ContextVar("log_id")


class LogIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        tags = getattr(record, "tag", None)
        if tags:
            setattr(record, "tags", {})
        log_id = get_context_log_id()
        getattr(record, "tags", {})["_logid"] = log_id
        record._logid = log_id
        return True


def get_context_log_id():
    log_id = log_id_context.get(None)
    if log_id:
        return log_id
    time_id = datetime.now().strftime("%Y%m%d%H%M%S")
    ip_id = "010010010010"
    random_id = str(
        "".join([random.choice(string.hexdigits).capitalize() for s in range(6)])
    )
    new_log_id = time_id + ip_id + random_id
    log_id_context.set(new_log_id)
    return new_log_id


_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s %(_logid)s"
            "[%(filename)s][%(funcName)s][%(lineno)d]> %(message)"
        },
        "json": {
            "class": "app.utils.json_loggers.CustomJsonFormatter",
            "format": "%(message)s",
        },
        "filters": {
            "logid_filter": {
                "()": LogIdFilter,
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "default",
            },
            "file": {
                "class": "logging.handlers.TimeRotatingFileHandler",
                "level": "DEBUG",
                "filename": os.path.join(settings.LOG_DIR, "app.log"),
                "when": "W6",
                "encoding": "utf-8",
                "formatter": "default",
                "backupCount": 7,
                "filters": ["logid_filter"],
            },
            "json": {
                "class": "logging.handlers.TimeRotatingFileHandler",
                "level": "DEBUG",
                "filename": os.path.join(settings.LOG_DIR, "app.log"),
                "when": "W6",
                "encoding": "utf-8",
                "formatter": "json",
                "backupCount": 7,
                "filters": ["logid_filter"],
            },
        },
        "loggers": {
            "app": {"handlers": ["console", "file"], "level": "DEBUG"},
            "audit": {"handlers": ["console", "json"], "level": "DEBUG"},
        },
    },
}

logging.config.dictConfig(_config)
app_logger = logging.getLogger("app")
json_logger = logging.getLogger("audit")
