from dataclasses import dataclass
from rich.syntax import Syntax


@dataclass
class TokenErrorReport:
    message: str
    error_code: int
    token_index: int


@dataclass
class ErrorType:
    message: str
    description: str


@dataclass
class LexerErrorReport:
    error: ErrorType
    code: Syntax
    line_number: int


class ErrorTypeNotFound(Exception):
    """
    This error is raised when using the 'get_error' method in 'ErrorRegistry'
    class and 'ErrorType' matching 'error_code' doesn't exist.
    """
    pass


class ErrorRegistry:
    """
    A Registry to hold different types of error types.
    Stores 'ErrorType' classes in a dict.
    """

    def __init__(self) -> None:
        self.errors: dict[int, ErrorType] = {}

    def add_error(self, error_code: int, error: ErrorType) -> None:
        """
        Adds an ErrorType to the registry

        :param error_code: The code of the error.
        :type error_code: Integer.
        :param error: The Error Class containing information about the error
        :type error: class 'ErrorType'
        """
        self.errors[error_code] = error

    def get_error(self, error_code: int) -> ErrorType:
        """
        Gets the ErrorType from the error_code given

        :param error_code: The code of the error.
        :return: The error type matching the error code.
        :rtype: ErrorType
        """
        if error_code not in self.errors:
            raise ValueError(f'Error code: "{error_code}" was not found.')
        return self.errors[error_code]
