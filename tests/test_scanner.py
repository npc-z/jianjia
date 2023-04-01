from jianjia import Scanner, Token, TokenType

from .common import eof_token


def test_empty_source():
    s = ""
    tokens = Scanner(s).scan_tokens()
    assert tokens == [eof_token()]


def test_punctuations():
    s = "()[]{}.,;!=<>>=+-*/"
    tokens = Scanner(s).scan_tokens()
    assert tokens == [
        Token(TokenType.LEFT_PAREN, "(", None, 1),
        Token(TokenType.RIGHT_PAREN, ")", None, 1),
        Token(TokenType.LEFT_BRACE, "{", None, 1),
        Token(TokenType.RIGHT_BRACE, "}", None, 1),
        Token(TokenType.DOT, ".", None, 1),
        Token(TokenType.COMMA, ",", None, 1),
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.BANG_EQUAL, "!=", None, 1),
        Token(TokenType.LESS, "<", None, 1),
        Token(TokenType.GREATER, ">", None, 1),
        Token(TokenType.GREATER_EQUAL, ">=", None, 1),
        Token(TokenType.PLUS, "+", None, 1),
        Token(TokenType.MINUS, "-", None, 1),
        Token(TokenType.STAR, "*", None, 1),
        Token(TokenType.SLASH, "/", None, 1),
        eof_token(),
    ]


def test_numbers():
    s = "1 2 3.14"
    tokens = Scanner(s).scan_tokens()
    assert tokens == [
        Token(TokenType.NUMBER, "1", 1, 1),
        Token(TokenType.NUMBER, "2", 2, 1),
        Token(TokenType.NUMBER, "3.14", 3.14, 1),
        eof_token(),
    ]


def test_strings():
    s = """
        "name" "age"
    """
    tokens = Scanner(s).scan_tokens()
    assert len(tokens) == 3
    assert tokens == [
        Token(TokenType.STRING, '"name"', "name", 2),
        Token(TokenType.STRING, '"age"', "age", 2),
        eof_token(3),
    ]


def test_keywords():
    s = """
        class fun var
        this true false nil
        and or if else print
    """
    tokens = Scanner(s).scan_tokens()
    assert tokens == [
        Token(TokenType.CLASS, "class", None, 2),
        Token(TokenType.FUN, "fun", None, 2),
        Token(TokenType.VAR, "var", None, 2),
        Token(TokenType.THIS, "this", None, 3),
        Token(TokenType.TRUE, "true", None, 3),
        Token(TokenType.FALSE, "false", None, 3),
        Token(TokenType.NIL, "nil", None, 3),
        Token(TokenType.AND, "and", None, 4),
        Token(TokenType.OR, "or", None, 4),
        Token(TokenType.IF, "if", None, 4),
        Token(TokenType.ELSE, "else", None, 4),
        Token(TokenType.PRINT, "print", None, 4),
        eof_token(5),
    ]
