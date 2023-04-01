from dataclasses import dataclass

from jianjia.token_type import TokenType


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int
