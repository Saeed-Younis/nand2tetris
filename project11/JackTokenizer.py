"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.

    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters,
    and comments, which are ignored. There are three possible comment formats:
    /* comment until closing / , /* API comment until closing */ , and
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' |
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' |
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' |
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate
    file. A compilation unit is a single class. A class is a sequence of tokens
    structured according to the following context free syntax:

    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type)
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement |
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{'
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions

    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName |
            varName '['expression']' | subroutineCall | '(' expression ')' |
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className |
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'

    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Initializes the tokenizer with the input stream."""
        self.input_file = input_stream.read() + '\n'
        self.index = 0
        self.curr_token = ""
        self.previous_token = ""
        self.prev_index=0

    def has_more_tokens(self) -> bool:
        """Checks if there are more tokens to process in the input."""
        while self.index < len(self.input_file):
            char = self.input_file[self.index]

            # Handle single-line comments
            if char == '/' and self.input_file[self.index:self.index + 2] == '//':
                self.skip_comment()
            # Handle multi-line comments
            elif char == '/' and self.input_file[self.index:self.index + 2] == '/*':
                self.skip_multi_comments()
            # Skip whitespace characters
            elif char in {' ', '\n', '\t'}:
                self.index += 1
            else:
                return True
        return False

    def unadvance(self):
        """Moves the tokenizer back to the previous token."""
        self.index = self.prev_index  # Revert to the previous index
        self.curr_token = self.previous_token[0]  # Restore the previous token

    def advance(self) -> None:
        """Advances to the next token."""
        if self.has_more_tokens():
            char = self.input_file[self.index]

            # Handle string constants
            if char == '"':
                self.curr_token = self.read_string()
            # Handle symbols
            elif char in {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
                          '-', '*', '/', '&', '|', '<', '>', '=', '~', '^', '#'}:
                self.curr_token = char
                self.replace_token()
                self.index += 1
            # Handle keywords, identifiers, or numbers
            else:
                self.curr_token = self.read_letters()

    def skip_comment(self):
        """Skips a single-line comment."""
        while self.index < len(self.input_file) and self.input_file[self.index] != '\n':
            self.index += 1
        self.index += 1  # Skip the newline

    def skip_multi_comments(self):
        """Skips a multi-line comment."""
        while self.index < len(self.input_file) - 1 and self.input_file[self.index:self.index + 2] != '*/':
            self.index += 1
        self.index += 2  # Skip the '*/'

    def read_string(self) -> str:
        """Reads a string constant enclosed in double quotes."""
        start = self.index
        self.index += 1  # Skip the opening quote
        while self.index < len(self.input_file) and self.input_file[self.index] != '"':
            self.index += 1
        self.index += 1  # Skip the closing quote
        return self.input_file[start:self.index]

    def read_letters(self) -> str:
        """Reads an alphanumeric sequence (identifier, keyword, or number)."""
        start = self.index
        while self.index < len(self.input_file) and self.input_file[self.index] not in \
                {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=',
                 '~', '^', '#'} and self.input_file[self.index] not in {' ', '\n', '\t'}:
            self.index += 1
        return self.input_file[start:self.index]

    def next_token(self):
        self.previous_token = (self.curr_token, self.token_type())
        self.prev_index = self.index
        if self.has_more_tokens():
            self.advance()

    def replace_token(self):
        if self.curr_token == '<':
            self.curr_token = '&lt;'
        if self.curr_token == '>':
            self.curr_token = '&gt;'
        if self.curr_token == '&':
            self.curr_token = '&amp;'

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if self.curr_token in ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
                               '-', '*', '/', '&', '|', '<', '>', '=', '~', '^', '#']:
            return "SYMBOL"
        elif self.curr_token in ['class', 'constructor', 'function', 'method', 'field',
                                 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
                                 'let', 'do', 'if', 'else', 'while', 'return']:
            return "KEYWORD"

        elif self.curr_token.isnumeric():
            if 0 <= int(self.curr_token) <= 32767:
                return "INT_CONST"

        elif self.curr_token.startswith('"') and self.curr_token.endswith('"'):
            return "STRING_CONST"

        # elif not self.curr_token[0].isnumeric():
        else:
            return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO",
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        ret = self.curr_token
        return ret.upper()

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' |
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        return self.curr_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        return self.curr_token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        return int(self.curr_token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including
                      double quote or newline '"'
        """
        return self.curr_token[1:-1]
