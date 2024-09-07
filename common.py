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
    def __init__(self):
        self.errors = {}

    def add_error(self, error_code: int, error: Error):
        self.errors[error_code] = error

    def get_error(self, error_code: int) -> Error:
        return self.errors[error_code]


def get_last_five_lines(text: str):
    lines = text.splitlines()
    if len(lines) > 5:
        return '\n'.join(lines[-5:])
    else:
        return text


error_registry = ErrorRegistry()

error_registry.add_error(-1, Error('Exception Occurred.', 'An exception, can be caused by different reasons.'))
error_registry.add_error(1, Error('Invalid Syntax.', 'Caused by improper syntax.'))
error_registry.add_error(2, Error('Invalid Syntax.', 'Caused if there is more than 2 equal sign in the expression.'))
error_registry.add_error(3, Error('Invalid Syntax.', 'Caused if there is more than 1 dot found in a floating number.'))
error_registry.add_error(4, Error('Invalid Syntax.', 'Caused if the ending qoute was not found.'))
