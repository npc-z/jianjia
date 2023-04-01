from typing import Dict, List

from jianjia.reporter import Reporter
from jianjia.token import Token
from jianjia.token_type import TokenType


class Scanner:
    keywords: Dict[str, TokenType] = {
        "class": TokenType.CLASS,
        "this": TokenType.THIS,
        "super": TokenType.SUPER,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "nil": TokenType.NIL,
        "for": TokenType.FOR,
        "while": TokenType.WHILE,
        "fun": TokenType.FUN,
        "var": TokenType.VAR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
    }

    def __init__(self, source: str) -> None:
        self._source: str = source
        self._source_length: int = len(self._source)
        self._tokens: List[Token] = []
        self._start: int = 0
        self._current: int = 0
        self._line: int = 1

        self._reporter = Reporter()

    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            # At the beginning of the next lexeme.
            self._start = self._current
            self._scan_token()

        self._tokens.append(
            Token(type=TokenType.EOF, lexeme="", literal=None, line=self._line)
        )
        return self._tokens

    def _scan_token(self):
        char = self._advance()

        if char == "(":
            self._add_token(TokenType.LEFT_PAREN)
        elif char == ")":
            self._add_token(TokenType.RIGHT_PAREN)
        elif char == "{":
            self._add_token(TokenType.LEFT_BRACE)
        elif char == "}":
            self._add_token(TokenType.RIGHT_BRACE)
        elif char == ",":
            self._add_token(TokenType.COMMA)
        elif char == ".":
            self._add_token(TokenType.DOT)
        elif char == "-":
            self._add_token(TokenType.MINUS)
        elif char == "+":
            self._add_token(TokenType.PLUS)
        elif char == ";":
            self._add_token(TokenType.SEMICOLON)
        elif char == "*":
            self._add_token(TokenType.STAR)
        elif char == "!":
            self._add_token(
                TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
            )
        elif char == "=":
            self._add_token(
                TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
            )
        elif char == ">":
            self._add_token(
                TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            )
        elif char == "<":
            self._add_token(
                TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
            )
        elif char == "/":
            if self._match("/"):
                # Skip the comment line.
                while self._peek() != "\n" and self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif char == " " or char == "\r" or char == "\t":
            pass
        elif char == "\n":
            self._line += 1
        elif char == '"':
            self._string()
        else:
            if self._is_digit(char=char):
                self._number()
            elif self._is_alpha(char):
                self._identifier()
            else:
                message = f"Unexpected character ({char})."
                self._reporter.error(self._line, message)

    def _identifier(self):
        while self._is_alpha_numeric(self._peek()):
            self._advance()

        text = self._source[self._start : self._current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self._add_token(type=token_type)

    def _number(self):
        while self._is_digit(self._peek()):
            self._advance()

        # Look for a fractional part.
        if self._peek() == "." and self._is_digit(self._peek_next()):
            # Consume the "."
            self._advance()

            while self._is_digit(self._peek()):
                self._advance()

        value = float(self._source[self._start : self._current])
        self.__add_token(type=TokenType.NUMBER, literal=value)

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self._line += 1
            self._advance()

        if self._is_at_end():
            self._reporter.error(self._line, "Unterminated string.")

        # The closing ".
        self._advance()

        # Trim the surrounding quotes.
        value = self._source[self._start + 1 : self._current - 1]
        self.__add_token(type=TokenType.STRING, literal=value)

    def _match(self, expected: str):
        if self._is_at_end():
            return False

        if self._source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _peek(self):
        if self._is_at_end():
            return "\0"

        return self._source[self._current]

    def _peek_next(self):
        if self._current + 1 >= self._source_length:
            return "\0"

        return self._source[self._current + 1]

    @staticmethod
    def _is_alpha(char: str):
        return (
            char == "_"
            or (ord("a") <= ord(char) <= ord("z"))
            or (ord("A") <= ord(char) <= ord("Z"))
        )

    def _is_alpha_numeric(self, char: str):
        return self._is_alpha(char) or self._is_digit(char)

    @staticmethod
    def _is_digit(char: str):
        return ord("0") <= ord(char) <= ord("9")

    def _is_at_end(self):
        return self._current >= self._source_length

    def _advance(self):
        self._current += 1
        return self._source[self._current - 1]

    def _add_token(self, type: TokenType):
        self.__add_token(type=type, literal=None)

    def __add_token(self, type: TokenType, literal: object):
        text = self._source[self._start : self._current]
        token = Token(type=type, lexeme=text, literal=literal, line=self._line)
        self._tokens.append(token)
