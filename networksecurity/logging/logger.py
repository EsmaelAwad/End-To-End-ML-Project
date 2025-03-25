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
    """
    # Format timestamp for filenames
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    
    # Ensure logs directory exists
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Define full log file path
    log_file_path = os.path.join(logs_dir, log_filename)

    # Configure logging to log INFO and above
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Silence noisy loggers
    logging.getLogger("pymongo").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)

    # Return a logger configured for this module
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info(msg)

    return logger

# Usage:
logger = setup_logging()
