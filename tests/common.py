from jianjia import Token, TokenType


def eof_token(line: int = 1):
    return Token(type=TokenType.EOF, lexeme="", literal=None, line=line)
