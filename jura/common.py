def get_last_five_lines(string: str) -> str:
    """
    :param string: The string to get the last five-lines.
    :type string: String

    :return: A string containing the last five lines of the string argument.
    :rtype: String
    """
    lines = string.splitlines()
    if len(lines) > 5:
        return '\n'.join(lines[-5:])
    else:
        return string
