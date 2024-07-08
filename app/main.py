import sys
from dataclasses import dataclass


@dataclass
class Token:
    type: str
    lexeme: str
    line: int


# Define the token types as class constants
class TokenType:
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    SEMICOLON = 'SEMICOLON'
    STAR = 'STAR'
    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    BANG = 'BANG'
    BANG_EQUAL = 'BANG_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'
    SLASH = 'SLASH'
    COMMENT = 'COMMENT'
    SPACE = '|SPACE|'
    TAB = '|TAB|'


# Define a custom exception for unexpected characters
class UnexpectedCharacter(Exception):
    def __init__(self, char, line_number):
        """
        Initialize the exception with the unexpected character and the line number where it was found.

        Args:
            char (str): The unexpected character.
            line_number (int): The line number where the unexpected character was found.
        """
        self.char = char
        self.line_number = line_number
        self.message = f"[line {line_number}] Error: Unexpected character: {char}"
        super().__init__(self.message)


# Define a tokenizer class to handle tokenization
class Tokenizer:
    def __init__(self, filename):
        """
        Initialize the tokenizer with the given filename.

        Args:
            filename (str): The name of the file to tokenize.
        """
        self.filename = filename
        self.tokens = []
        self.errors = []

    def read_file(self):
        """
        Read the contents of the file.

        Returns:
            list[str]: The lines of the file.
        """
        with open(self.filename) as file:
            return file.readlines()

    def tokenize(self, file_contents):
        """
        Tokenize the contents of the file.

        Args:
            file_contents (list[str]): The lines of the file.
        """
        for line_number, line in enumerate(file_contents, start=1):
            i = 0
            while i < len(line):
                char = line[i]
                try:
                    if i < len(line) - 1:
                        token_type, skip = self.match_char(char, line[i + 1], line_number)
                    else:
                        token_type, skip = self.match_char(char, None, line_number)
                    if token_type:
                        lexeme = char if not skip else line[i:i + 2]
                        token = Token(token_type, lexeme, line_number)
                        self.tokens.append(token)
                        if token.type == TokenType.COMMENT:
                            break

                    i += 1 if not skip else 2
                except UnexpectedCharacter as e:
                    self.errors.append(e.message)
                    i += 1

    @staticmethod
    def match_char(char, next_char, line_number):
        """
        Match characters to token types, including handling lookahead for multi-character tokens.

        Args:
            char (str): The current character.
            next_char (str or None): The next character for lookahead.
            line_number (int): The line number where the character is found.

        Returns:
            tuple: A tuple containing the token type and a boolean indicating whether to skip the next character.

        Raises:
            UnexpectedCharacter: If the character does not match any known token.
        """
        match char:
            case "(":
                return TokenType.LEFT_PAREN, False
            case ")":
                return TokenType.RIGHT_PAREN, False
            case "{":
                return TokenType.LEFT_BRACE, False
            case "}":
                return TokenType.RIGHT_BRACE, False
            case ',':
                return TokenType.COMMA, False
            case '.':
                return TokenType.DOT, False
            case '-':
                return TokenType.MINUS, False
            case '+':
                return TokenType.PLUS, False
            case ';':
                return TokenType.SEMICOLON, False
            case '*':
                return TokenType.STAR, False
            case ' ':
                return TokenType.SPACE, False
            case '\t':
                return TokenType.TAB, False
            case '=':
                if next_char == '=':
                    return TokenType.EQUAL_EQUAL, True
                else:
                    return TokenType.EQUAL, False
            case '!':
                if next_char == '=':
                    return TokenType.BANG_EQUAL, True
                else:
                    return TokenType.BANG, False
            case '<':
                if next_char == '=':
                    return TokenType.LESS_EQUAL, True
                else:
                    return TokenType.LESS, False
            case '>':
                if next_char == '=':
                    return TokenType.GREATER_EQUAL, True
                else:
                    return TokenType.GREATER, False
            case '/':
                if next_char == '/':
                    return TokenType.COMMENT, True
                else:
                    return TokenType.SLASH, False
            case _:
                raise UnexpectedCharacter(char, line_number)

    def print_tokens(self):
        """
        Print the tokens in the specified format.
        """
        for token in self.tokens:
            if token.type not in (TokenType.COMMENT,TokenType.SPACE,TokenType.TAB):
                print(f"{token.type} {token.lexeme} null")
        print("EOF  null")

    def print_errors(self):
        """
        Print the errors to stderr.
        """
        for error in self.errors:
            print(error, file=sys.stderr)


def main():
    """
    Main function to handle command-line arguments and initiate tokenization.
    """
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    tokenizer = Tokenizer(filename)
    file_contents = tokenizer.read_file()
    tokenizer.tokenize(file_contents)
    tokenizer.print_errors()
    tokenizer.print_tokens()

    if tokenizer.errors:
        exit(65)


if __name__ == "__main__":
    main()
