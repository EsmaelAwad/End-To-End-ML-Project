class NetworkSecurityException(Exception):
    def __init__(self, message, error_details, error_code):
        """
        Custom exception class for handling errors within the NetworkSecurity module.

        This exception extracts traceback details such as file name, line number, and function
        where the exception occurred, and provides a formatted message for better debugging.

        Attributes:
            message (str): A custom error message.
            error_code (int): A custom error code representing the type of failure.
            file_name (str): The name of the file where the exception was raised.
            line_number (int): The line number where the exception was raised.
            error_type (str): The name of the function or method where the exception was raised.

        Args:
            message (str): Description of the error.
            error_details (tuple): Tuple from sys.exc_info() containing exception metadata.
            error_code (int): Custom error code for categorizing the error.

        Example:
            ```python
            import sys
            from networksecurity.exceptions.exception import NetworkSecurityException

            try:
                result = 10 / 0
            except Exception:
                raise NetworkSecurityException("Division failed", sys.exc_info(), 500)
            ```

        Output:
            Error occurred in file: main.py at line 12 in function: <module>,
            with code: 500 and message: Division failed
        """
        super().__init__(message)
        self.message = message
        _, _, tb = error_details  # unpack the tuple
        self.error_code = error_code
        self.line_number = tb.tb_lineno
        self.file_name = tb.tb_frame.f_code.co_filename
        self.error_type = tb.tb_frame.f_code.co_name

    def __str__(self):
        return (
            f"Error occurred in file: {self.file_name} at line {self.line_number} "
            f"in function: {self.error_type}, with code: {self.error_code} "
            f"and message: {self.message}"
        )