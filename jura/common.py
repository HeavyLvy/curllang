def get_last_five_lines(text: str):
    lines = text.splitlines()
    if len(lines) > 5:
        return '\n'.join(lines[-5:])
    else:
        return text
