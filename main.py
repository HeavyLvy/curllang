import string
from rich.console import Console
from rich.syntax import Syntax

# install(show_locals=True)
console = Console()


def parse_line(line: str):
    result = {}
    error_found = False
    parsed_tokens = []
    token_sequence = []
    flag = None

    def raise_parse_error(message: str, token_index, error_code=-1):
        nonlocal error_found
        error_found = True
        result["error"] = {
            "message": message,
            "code": error_code,
            "token_index": token_index - 1,
            # We subtract one because the char still gets proccsed after the error is called, incrementing the index by one. (which would be the next index, that we dont want).
        }
        error_code = error_code

    for i, char in enumerate(line):
        if error_found:
            break

        def append_token():
            nonlocal token_sequence, flag

            parsed_tokens.append({"flag": flag, "value": "".join(token_sequence)})
            flag = None
            token_sequence = []

        # Set Flags
        if not flag:
            if char in string.ascii_letters:
                flag = "identifier"
            if char in string.digits:
                flag = "integer"
            if char == "+":
                flag = "addition"
            if char == "-":
                flag = "subtraction"
            if char == "*":
                flag = "multiplication"
            if char == "/":
                flag = "division"
            if char == "=":
                flag = "assignment"

        # Handle Flags
        if flag == "identifier":
            if char not in string.ascii_letters + "_" and char not in string.digits:
                append_token()
            else:
                token_sequence.append(char)
        if flag == "integer":
            if char not in string.digits or char == ".":
                if char == ".":
                    flag = "float"
                else:
                    append_token()
            else:
                token_sequence.append(char)
        if flag == "float":
            if token_sequence.count(".") > 1:
                raise_parse_error("No such data type with more than 1 dot.", i, 3)
            if char not in string.digits and char != ".":
                append_token()
            else:
                token_sequence.append(char)
        if flag == "addition":
            token_sequence.append(char)
            append_token()
        if flag == "subtraction":
            token_sequence.append(char)
            append_token()
        if flag == "multiplication":
            token_sequence.append(char)
            append_token()
        if flag == "division":
            token_sequence.append(char)
            append_token()
        if flag == "assignment":  # Handles both assignment and comparison
            if char != "=":
                if len(token_sequence) == 2:
                    flag = "comparison"
                elif len(token_sequence) > 2:
                    raise_parse_error(
                        "No such operation for more than 2 equal signs", i, 2
                    )

                append_token()
            else:
                token_sequence.append(char)

        # Append the token if there are no more characters to parse.
        if flag and i == len(line) - 1:
            append_token()

    result["tokens"] = parsed_tokens
    return result


def get_last_five_lines(text: str):
    lines = text.splitlines()
    if len(lines) > 5:
        return "\n".join(lines[-5:])
    else:
        return text


def output_parsing_errors(errors, verbose: int):
    console.print(
        f"[white on red bold]{len(errors)} parsing error{'s' if len(errors) > 1 else ''} raised.",
        highlight=False,
    )
    for error_index, error in enumerate(errors):
        token_index = error["error"]["token_index"]

        console.print(
            f"[[white]{error_index}[red]] {ERROR_CODES[error['error']['code']]['message']} Error Code: {error['error']['code']}",
            style="bold red",
            highlight=False,
        )
        if verbose > 0:
            console.print(
                f'    {error['error']['message']}',
                style="bold red",
                highlight=False,
            )
        if verbose > 1:
            console.print(
                f"    {ERROR_CODES[error['error']['code']]['description']}",
                style="bold red",
                highlight=False,
            )
        console.print(error["code"])
        console.print(
            " " * (token_index + 3 + len(str(error["line"]))) + "^",
            style="bold yellow",
        )


def parse_code(input_code: str, verbose: int = 0):
    processed_code = ""
    found_errors = []

    # Go through each line of the code and parse and put any errors into the found errors list
    for line_number, line_content in enumerate(input_code.splitlines()):
        processed_code += line_content + "\n"
        parsed_line = parse_line(line_content)

        if parsed_line.get("error"):
            syntax = Syntax(
                get_last_five_lines(processed_code[1:-1]),
                "lua",
                theme="monokai",
                line_numbers=True,
                highlight_lines=[line_number],  # NOQA
                start_line=len(processed_code.splitlines()) - 5
                if len(processed_code.splitlines()) > 5
                else 1,
            )
            found_errors.append(
                {"error": parsed_line["error"], "code": syntax, "line": line_number}
            )
        elif parsed_line["tokens"]:
            console.print(parsed_line["tokens"])

    # Output the errors
    if found_errors:
        output_parsing_errors(found_errors, verbose)


ERROR_CODES = {
    -1: {
        "message": "Exception Occured.",
        "description": "An exception, can be casued by different reasons.",
    },
    1: {"message": "Invalid Syntax.", "description": "Caused by inproper syntax."},
    2: {
        "message": "Invalid Syntax.",
        "description": 'Caused if there is more than 2 equal signs in the expression eg "x === y", "1 ======== 53".',
    },
    3: {
        "message": "Invalid Syntax.",
        "description": "Caused if there is more than 1 dot found in a floating number.",
    },
}

example_code = """
1 === 2
print("hello")
print(1.03435.123214)
"""

parse_code(example_code)
