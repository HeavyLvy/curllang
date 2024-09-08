from dataclasses import dataclass


@dataclass
class TokenErrorReport:
    message: str
    error_code: int
    token_index: int


@dataclass
class ErrorType:
    message: str
    description: str


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
            raise ErrorTypeNotFound(f'Error code: "{error_code}" was not found.')
        return self.errors[error_code]


error_registry = ErrorRegistry()

error_registry.add_error(-1, ErrorType('Exception Occurred.', 'An exception, can be caused by different reasons.'))
error_registry.add_error(1, ErrorType('Invalid Syntax.', 'Caused by improper syntax.'))
error_registry.add_error(2,
                         ErrorType('Invalid Syntax.', 'Caused if there is more than 2 equal sign in the expression.'))
error_registry.add_error(3,
                         ErrorType('Invalid Syntax.', 'Caused if there is more than 1 dot found in a floating number.'))
error_registry.add_error(4, ErrorType('Invalid Syntax.', 'Caused if the ending qoute was not found.'))
