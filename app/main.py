import sys
from enum import Enum, auto

# Define an enum for the different types of tokens
class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    STAR = auto()

# Define a custom exception for unexpected characters
class UnexpectedCharacter(Exception):
    def __init__(self, char, line_number):
        self.char = char
        self.line_number = line_number
        self.message = f"[line {line_number}] Error: Unexpected character: {char}"
        super().__init__(self.message)

# Define a tokenizer class to handle tokenization
class Tokenizer:
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []
        self.errors = []

    # Read the file contents
    def read_file(self):
        with open(self.filename) as file:
            return file.readlines()

    # Tokenize the file contents
    def tokenize(self, file_contents):
        for line_number, line in enumerate(file_contents, start=1):
            for char in line:
                try:
                    token = self.match_char(char, line_number)
                    if token:
                        self.tokens.append((token, char))
                except UnexpectedCharacter as e:
                    self.errors.append(e.message)

    # Match characters to token types
    def match_char(self, char, line_number):
        match char:
            case "(":
                return TokenType.LEFT_PAREN
            case ")":
                return TokenType.RIGHT_PAREN
            case "{":
                return TokenType.LEFT_BRACE
            case "}":
                return TokenType.RIGHT_BRACE
            case ',':
                return TokenType.COMMA
            case '.':
                return TokenType.DOT
            case '-':
                return TokenType.MINUS
            case '+':
                return TokenType.PLUS
            case ';':
                return TokenType.SEMICOLON
            case '*':
                return TokenType.STAR
            case _:
                raise UnexpectedCharacter(char, line_number)

    # Print the tokens
    def print_tokens(self):
        for token, char in self.tokens:
            print(f"{token.name} {char} null")
        print("EOF  null")

    # Print the errors
    def print_errors(self):
        for error in self.errors:
            print(error, file=sys.stderr)

# Main function to handle command-line arguments and initiate tokenization
def main():
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

    # If there are errors, exit with return code 65
    if tokenizer.errors:
        exit(65)

if __name__ == "__main__":
    main()
