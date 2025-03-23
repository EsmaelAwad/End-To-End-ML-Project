import logging
import os
from datetime import datetime

def setup_logging(msg: str = "Logging started...") -> logging.Logger:
    """
    Configures and returns a logger that logs messages to a timestamped file in the 'logs/' directory.

    Logs are saved in the format:
    `logs/YYYY-MM-DD_HH-MM-SS.log`

    The logger will output logs in the following format:
    `[timestamp] - [module_name] - [level] - [message]`

    Args:
        msg (str): Initial info message to log after logger is set up. Default is "Logging started..."

    Returns:
        logging.Logger: A configured logger instance.

    Example:
        ```python
        from networksecurity.logging.logger import setup_logging

        logger = setup_logging("App started")
        logger.info("Something happened")
        # In case of an exception, use logger.exception(err) and pass an exception object like so:
        logger.error("An exception occurred:")
        logger.exception(err)
        ```

    Output:
        2025-03-23 19:30:01,123 - __main__ - INFO - App started
        2025-03-23 19:30:02,456 - __main__ - INFO - Something happened
        2025-03-23 19:30:03,789 - __main__ - ERROR - An exception occurred:
        Traceback (most recent call last):
          File "main.py", line 12, in <module>
            result = divide_numbers(5, 0)
          File "main.py", line 8, in divide_numbers
            return a / b 
    """
    # Format timestamp for filenames
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    
    # Ensure logs directory exists
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Define full log file path
    log_file_path = os.path.join(logs_dir, log_filename)

    # Configure logging
    logging.basicConfig(
        filename=log_file_path,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.info(msg=msg)

    return logger

# Usage:
logger = setup_logging()
