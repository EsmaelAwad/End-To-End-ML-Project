import sys
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import setup_logging

logger = setup_logging(__name__)

def divide_numbers(a, b):
    return a / b

if __name__ == "__main__":
    try:
        result = divide_numbers(5, 0)
    except Exception:
        err = NetworkSecurityException("Failed to divide numbers", sys.exc_info(), 500, logger=logger)
