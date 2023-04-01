from enum import Enum, auto


class TokenType(Enum):
    # single-character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # one or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()

    EQUAL = auto()
    EQUAL_EQUAL = auto()

    GREATER = auto()
    GREATER_EQUAL = auto()

    LESS = auto()
    LESS_EQUAL = auto()

    # literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # keywords
    CLASS = auto()
    SUPER = auto()
    THIS = auto()

    AND = auto()
    OR = auto()

    IF = auto()
    ELSE = auto()

    TRUE = auto()
    FALSE = auto()
    NIL = auto()

    FOR = auto()
    WHILE = auto()

    FUN = auto()
    VAR = auto()
    PRINT = auto()
    RETURN = auto()

    EOF = auto()
