from dataclasses import dataclass


@dataclass
class TokenErrorReport:
    message: str
    error_code: int
    token_index: int


@dataclass
class Error:
    message: str
    description: str


class ErrorRegistry:
    """
    A Registry to hold different types of errors.
    Stores 'Error' classes in a dict.
    """
    def __init__(self) -> None:
        self.errors: dict[int, Error] = {}

    def add_error(self, error_code: int, error: Error) -> None:
        """
        Adds an Error to the registry

        :param error_code: The code of the error.
        :type error_code: Integer.
        :param error: The Error Class containing information about the error
        :type error: class 'Error'
        """
        self.errors[error_code] = error

    def get_error(self, error_code: int) -> Error:
        """
        Gets the 
        """
        return self.errors[error_code]


error_registry = ErrorRegistry()

error_registry.add_error(-1, Error('Exception Occurred.', 'An exception, can be caused by different reasons.'))
error_registry.add_error(1, Error('Invalid Syntax.', 'Caused by improper syntax.'))
error_registry.add_error(2, Error('Invalid Syntax.', 'Caused if there is more than 2 equal sign in the expression.'))
error_registry.add_error(3, Error('Invalid Syntax.', 'Caused if there is more than 1 dot found in a floating number.'))
error_registry.add_error(4, Error('Invalid Syntax.', 'Caused if the ending qoute was not found.'))

print(help(ErrorRegistry))
