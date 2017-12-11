"""
Application specific errors to throw.
"""

class DataBaseException(Exception):
    """Exception raised for errors in the database.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        """
        Database error message initializer.
        """
        self.message = message
