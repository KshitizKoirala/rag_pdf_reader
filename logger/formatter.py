import logging

from typing import ClassVar


class CustomFormatter(logging.Formatter):
    grey: ClassVar[str] = "\x1b[38;20m"
    yellow: ClassVar[str] = "\x1b[33;20m"
    red: ClassVar[str] = "\x1b[31;20m"
    bold_red: ClassVar[str] = "\x1b[31;1m"
    reset: ClassVar[str] = "\x1b[0m"
    format: ClassVar[str] = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS: ClassVar[dict[int, str]] = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
