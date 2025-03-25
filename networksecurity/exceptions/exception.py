class NetworkSecurityException(Exception):
    """
    Custom exception class for handling and logging structured errors in the NetworkSecurity pipeline.

    This class extracts detailed traceback information including the file name, line number, and 
    function where the exception occurred. If a logger is provided, it will automatically log 
    the error message and the full traceback for easier debugging.

    Attributes:
        message (str): Description of the error.
        error_code (int): Custom error code for categorizing the error.
        file_name (str): The name of the file where the exception was raised.
        line_number (int): The exact line number where the error occurred.
        error_type (str): The function or method name where the exception occurred.

    Args:
        message (str): A human-readable message describing the error.
        error_details (tuple): Output from `sys.exc_info()` to extract traceback.
        error_code (int): A custom code representing the failure context.
        logger (logging.Logger, optional): Logger to automatically log the error and traceback.

    Example:
        ```python
        try:
            risky_operation()
        except Exception as e:
            raise NetworkSecurityException("Operation failed", sys.exc_info(), 501, logger)
        ```

    Log Output:
        2025-03-25 22:10:23,045 - __main__ - ERROR - Error occurred in file: main.py at line 27 in function: process_data, with code: 501 and message: Operation failed
        2025-03-25 22:10:23,046 - __main__ - ERROR - Traceback (most recent call last):
          File "main.py", line 26, in process_data
            risky_operation()
          ...
    """

    def __init__(self, message, error_details, error_code, logger=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

        # Extract traceback info from sys.exc_info()
        _, _, tb = error_details
        self.line_number = tb.tb_lineno
        self.file_name = tb.tb_frame.f_code.co_filename
        self.error_type = tb.tb_frame.f_code.co_name

        # Optional logging: log both the formatted message and full traceback
        if logger:
            logger.error(self.__str__())           # Logs custom structured error message
            logger.exception(message)              # Logs full traceback automatically

    def __str__(self):
        return (
            f"Error occurred in file: {self.file_name} "
            f"at line {self.line_number} "
            f"in function: {self.error_type}, "
            f"with code: {self.error_code} "
            f"and message: {self.message}"
        )