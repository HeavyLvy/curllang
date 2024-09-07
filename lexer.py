import string
from rich.console import Console
from rich.syntax import Syntax
from dataclasses import dataclass

console = Console()


@dataclass
class Token:
	token: str
	value: str


@dataclass
class TokenErrorReport:
	message: str
	error_code: int
	token_index: int


@dataclass
class ErrorCode:
	message: str
	description: str


ERROR_CODES = {
	-1: ErrorCode(
     'Exception Occurred.',
    'An exception, can be caused by different reasons.'
    ),
	1: ErrorCode(
     'Invalid Syntax.',
     'Caused by improper syntax.'
     ),
	2: ErrorCode(
		'Invalid Syntax.',
		'Caused if there is more than 2 equal sign in the expression.',
	),
	3: ErrorCode(
     'Invalid Syntax.',
     'Caused if there is more than 1 dot found in a floating number.'
     ),
	4: ErrorCode(
     'Invalid Syntax.',
     'Caused if the ending qoute was not found.'
     ),
}

BASE_ARITHMETIC_OPERATIONS = ['addition', 'subtraction', 'multiplication', 'division']


def lex_line(line: str):
	result = {}
	error_found = False
	parsed_tokens = []
	token_sequence = []
	token_type = None

	def raise_parse_error(message: str, token_index, error_code=-1):
		nonlocal error_found
		error_found = True
		result['error'] = TokenErrorReport(
			message=message, error_code=error_code, token_index=token_index - 1
		)

	found_end_of_string = False
	for i, char in enumerate(line):
		if error_found:
			break

		def append_token():
			nonlocal token_sequence, token_type
			value = ''.join(token_sequence)
			parsed_tokens.append(Token(token_type, value))
			token_type = None
			token_sequence = []

		# Set Flags
		if not token_type:
			if char in string.ascii_letters:
				token_type = 'identifier'
			if char in string.digits:
				token_type = 'integer'
			if char == '+':
				token_type = 'addition'
			if char == '-':
				token_type = 'subtraction'
			if char == '*':
				token_type = 'multiplication'
			if char == '/':
				token_type = 'division'
			if char == '=':
				token_type = 'assignment'
			if char == '"':
				token_type = 'string_start'

		# Handle Flags
		if token_type == 'identifier':
			if char not in string.ascii_letters + '_' and char not in string.digits:
				append_token()
			else:
				token_sequence.append(char)
		if token_type == 'integer':
			if char not in string.digits or char == '.':
				if char == '.':
					token_type = 'float'
				else:
					append_token()
			else:
				token_sequence.append(char)
		if token_type == 'float':
			if token_sequence.count('.') > 1:
				raise_parse_error('No such data type with more than 1 dot.', i, 3)
			if char not in string.digits and char != '.':
				append_token()
			else:
				token_sequence.append(char)
		if token_type in BASE_ARITHMETIC_OPERATIONS:
			token_sequence.append(char)
			append_token()
		if token_type == 'assignment':  # Handles both assignment and comparison
			if char != '=':
				if len(token_sequence) == 2:
					token_type = 'comparison'
				elif len(token_sequence) > 2:
					raise_parse_error('No such operation for more than 2 equal signs', i, 2)

				append_token()
			else:
				token_sequence.append(char)
		if token_type == 'string':
			if char != '"':
				token_sequence.append(char)
			else:
				found_end_of_string = True
				append_token()
		if token_type == 'string_start':
			if char != '"':
				token_type = 'string'
				token_sequence.append(char)

	if token_type:
		if token_type == 'string' and not found_end_of_string:
			raise_parse_error(
				'Expected an ending qoute',
				i + 2,
				4,  # we add 2 to i because we expect the qoute to be on the next index/char
			)
			append_token()
		append_token()

	result['tokens'] = parsed_tokens
	return result


def get_last_five_lines(text: str):
	lines = text.splitlines()
	if len(lines) > 5:
		return '\n'.join(lines[-5:])
	else:
		return text


def output_parsing_errors(errors, verbose: int):
	print(errors)
	console.print(
		f"[white on red bold]{len(errors)} parsing error{'s' if len(errors) > 1 else ''} raised.",
		highlight=False,
	)
	for error_index, error in enumerate(errors):
		token_index = error['error'].token_index
		error_code = error['error'].error_code

		console.print(
			f'[[white]{error_index}[red]] {ERROR_CODES[error_code].message} Error Code: {error_code}',
			style='bold red',
			highlight=False,
		)
		if verbose > 0:
			console.print(
				f"    {error['error'].message}",
				style='bold red',
				highlight=False,
			)
		if verbose > 1:
			console.print(
				f'    {ERROR_CODES[error_code].description}',
				style='bold red',
				highlight=False,
			)
		console.print(error['code'])
		console.print(
			' ' * (token_index + 3 + len(str(error['line']))) + '^',
			style='bold yellow',
		)


def lex_code(input_code: str, verbose: int = 0):
	processed_code = ''
	found_errors = []

	# Go through each line of the code and parse and put any errors into the found errors list
	for line_number, line_content in enumerate(input_code.splitlines()):
		processed_code += line_content + '\n'
		parsed_line = lex_line(line_content)

		if parsed_line.get('error'):
			syntax = Syntax(
				get_last_five_lines(processed_code[1:-1]),
				'lua',
				theme='monokai',
				line_numbers=True,
				highlight_lines=[line_number],  # NOQA
				start_line=len(processed_code.splitlines()) - 5
				if len(processed_code.splitlines()) > 5
				else 1,
			)
			found_errors.append(
				{'error': parsed_line['error'], 'code': syntax, 'line': line_number}
			)
		elif parsed_line['tokens']:
			console.print(parsed_line['tokens'])

	# Output the errors
	if found_errors:
		output_parsing_errors(found_errors, verbose)
