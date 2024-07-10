import enum
import pathlib
import sys
from typing import Any, List, Tuple
from dataclasses import dataclass


class TokenType(enum.Enum):
    """
    Enum class for all possible token types.
    """
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    STAR = "STAR"
    DOT = "DOT"
    COMMA = "COMMA"
    PLUS = "PLUS"
    MINUS = "MINUS"
    SEMICOLON = "SEMICOLON"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    SLASH = "SLASH"
    STRING = "STRING"
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    # Reserved words
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FOR = "FOR"
    FUN = "FUN"
    IF = "IF"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"
    EOF = "EOF"


@dataclass
class Token:
    """
    Data class for tokens.
    """
    type: TokenType
    lexeme: str
    literal: Any
    line: int
    end_line: int = None

    def __str__(self) -> str:
        """
        String representation of the Token.
        """
        literal_str = "null" if self.literal is None else str(self.literal)
        return f"{self.type.value} {self.lexeme} {literal_str}"


class Scanner:
    """
    Class responsible for scanning source code and generating tokens.
    """
    RESERVED_KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str) -> None:
        """
        Initializes the Scanner with source code.
        """
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.errors: List[str] = []

    def scan_tokens(self) -> Tuple[List[Token], List[str]]:
        """
        Scans through the source code and returns the list of tokens and errors.
        """
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens, self.errors

    def is_at_end(self) -> bool:
        """
        Checks if the end of the source code is reached.
        """
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        """
        Scans a single token from the source code.
        """
        char = self.advance()
        match char:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case "*":
                self.add_token(TokenType.STAR)
            case ".":
                self.add_token(TokenType.DOT)
            case ",":
                self.add_token(TokenType.COMMA)
            case "+":
                self.add_token(TokenType.PLUS)
            case "-":
                self.add_token(TokenType.MINUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "!":
                self.add_token(TokenType.BANG_EQUAL) if self.match("=") else self.add_token(TokenType.BANG)
            case "=":
                self.add_token(TokenType.EQUAL_EQUAL) if self.match("=") else self.add_token(TokenType.EQUAL)
            case "<":
                self.add_token(TokenType.LESS_EQUAL) if self.match("=") else self.add_token(TokenType.LESS)
            case ">":
                self.add_token(TokenType.GREATER_EQUAL) if self.match("=") else self.add_token(TokenType.GREATER)
            case "/":
                if self.match("/"):
                    # Handle comment until end of line
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                # Ignore whitespace
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(char):
                    self.number()
                elif self.is_alpha(char):
                    self.identifier()
                else:
                    self.errors.append(f"[line {self.line}] Error: Unexpected character: {char}")

    def advance(self) -> str:
        """
        Advances the current position in the source code by one and returns the character at the new position.
        """
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal: Any = None) -> None:
        """
        Adds a token to the tokens list.
        """
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def peek(self) -> str:
        """
        Returns the current character without advancing the position.
        """
        return "\0" if self.is_at_end() else self.source[self.current]

    def peek_next(self) -> str:
        """
        Returns the next character without advancing the position.
        """
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        """
        Checks if the current character matches the expected character.
        Advances the position if it matches.
        """
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def string(self) -> None:
        """
        Handles string literals.
        """
        start_line = self.line
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.errors.append(f"[line {start_line}] Error: Unterminated string.")
            return
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.tokens.append(Token(TokenType.STRING, self.source[self.start:self.current], value, start_line, self.line))

    def is_digit(self, char: str) -> bool:
        """
        Checks if a character is a digit.
        """
        return "0" <= char <= "9"

    def number(self) -> None:
        """
        Handles number literals.
        """
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()
        lexeme = self.source[self.start:self.current]
        if lexeme.count('.') > 1:
            self.errors.append(f"[line {self.line}] Error: Invalid number: {lexeme}")
        else:
            self.add_token(TokenType.NUMBER, float(lexeme))

    def identifier(self) -> None:
        """
        Handles identifiers and reserved words.
        """
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.RESERVED_KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def is_alpha(self, char: str) -> bool:
        """
        Checks if a character is an alphabetic character or an underscore.
        """
        return "a" <= char <= "z" or "A" <= char <= "Z" or char == "_"

    def is_alpha_numeric(self, char: str) -> bool:
        """
        Checks if a character is alphanumeric.
        """
        return self.is_alpha(char) or self.is_digit(char)


def main() -> None:
    """
    Main function to execute the scanner on the provided file.
    """
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)
    command = sys.argv[1]
    filename = sys.argv[2]
    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)
    try:
        file_contents = pathlib.Path(filename).read_text()
    except FileNotFoundError:
        print(f"File not found: {filename}", file=sys.stderr)
        exit(1)
    scanner = Scanner(file_contents)
    tokens, errors = scanner.scan_tokens()
    for error in errors:
        print(error, file=sys.stderr)
    for token in tokens:
        print(token)
    if errors:
        exit(65)


if __name__ == "__main__":
    main()
