# customLogger.py
import logging
import sys

COLORS = {
    'DEBUG': '\033[92m',
    'INFO': '\033[94m',
    'WARNING': '\033[93m',
    'ERROR': '\033[91m',
    'CRITICAL': '\033[91m'
}
RESET_COLOR = '\033[0m'

class CustomFormatter(logging.Formatter):
    def format(self, record):
        levelname_color = COLORS.get(record.levelname, RESET_COLOR) + record.levelname + RESET_COLOR
        record.levelname = levelname_color
        log_format = '\n[%(levelname)s]: FILE[%(filename)s] =====>>> %(message)s'
        formatter = logging.Formatter(log_format)
        return formatter.format(record)

def setup_logger():
    logger = logging.getLogger('custom_logger')  # Use a unique name for the logger
    logger.propagate = False  # Prevent duplicate logs
    if not logger.hasHandlers():  # Avoid adding multiple handlers
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(CustomFormatter())
        logger.addHandler(console_handler)
    return logger

def set_log_level(log_level):
    logging.getLogger('custom_logger').setLevel(log_level)

def get_custom_logger():
    return logging.getLogger('custom_logger')

# Initialize the logger at module level
setup_logger()
