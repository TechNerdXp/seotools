import logging
import os

if not os.path.exists('logs'):
    os.makedirs('logs')


class LoggingLevelFilter(logging.Filter):
    def __init__(self, logging_level: int):
        super().__init__()
        self.logging_level = logging_level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == self.logging_level
    

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')

critical_handler = logging.FileHandler('logs/critical.log')
critical_handler.setLevel(logging.CRITICAL)
critical_handler.setFormatter(formatter)
critical_handler.addFilter(LoggingLevelFilter(logging.CRITICAL))

debug_handler = logging.FileHandler('logs/debug.log')
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)
debug_handler.addFilter(LoggingLevelFilter(logging.DEBUG))

error_handler = logging.FileHandler('logs/error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
error_handler.addFilter(LoggingLevelFilter(logging.ERROR))

info_handler = logging.FileHandler('logs/info.log')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)
info_handler.addFilter(LoggingLevelFilter(logging.INFO))

warning_handler = logging.FileHandler('logs/warning.log')
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(formatter)
warning_handler.addFilter(LoggingLevelFilter(logging.WARNING))

logger.addHandler(critical_handler)
logger.addHandler(debug_handler)
logger.addHandler(error_handler)
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
