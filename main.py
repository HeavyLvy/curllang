import lexer

example_code = """
1 === 2
print("hello")
print(1.03435.123214)
"""

lexer.lex_code(example_code)
