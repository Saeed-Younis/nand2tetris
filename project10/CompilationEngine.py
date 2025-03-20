"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import *


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """

        # Your code goes here!
        # Note that you can write to output_stream like so:
        self.tokenizer = input_stream
        self.outputFile = output_stream
        self.indent = ""
        self.subroutine_dec = ['constructor', 'function', 'method']
        self.class_var_dec = ['static', 'field']
        self.types = ['int', 'char', 'boolean']
        self.op = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
        self.unaryOp = ['-', '~']
        self.keyword_constant = ['true', 'false', 'null', 'this']

    def write_tag(self, tag: str, content: str) -> None:
        """Helper to write a single XML tag."""
        self.outputFile.write(f"<{tag}> {content} </{tag}>\n")

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # starts of class
        self.outputFile.write('<class>' + '\n')

        self.write_tag('keyword', self.tokenizer.curr_token)  # class
        self.tokenizer.next_token()

        self.write_tag('identifier', self.tokenizer.curr_token)  # class name
        self.tokenizer.next_token()

        self.write_tag('symbol', self.tokenizer.curr_token)  # {
        self.tokenizer.next_token()
        if self.tokenizer.curr_token in self.class_var_dec:
            self.compile_class_var_dec()

        self.compile_subroutine()
        self.tokenizer.next_token()

        self.write_tag('symbol', self.tokenizer.curr_token)  # }
        self.outputFile.write('</class>' + '\n')

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # self.outputFile.write('<classVarDec>' + '\n')
        while self.tokenizer.curr_token in self.class_var_dec:
            self.outputFile.write('<classVarDec>' + '\n')
            self.write_tag('keyword', self.tokenizer.curr_token)
            self.tokenizer.next_token()
            self.compile_type()
            self.outputFile.write('</classVarDec>' + '\n')
        # return

    def compile_type(self):
        if self.tokenizer.curr_token in self.types or self.tokenizer.token_type() == 'IDENTIFIER':
            if self.tokenizer.token_type() == 'IDENTIFIER':
                self.write_tag('identifier', self.tokenizer.curr_token)
                self.tokenizer.next_token()
            else:
                self.write_tag('keyword', self.tokenizer.curr_token)
                self.tokenizer.next_token()

            while self.tokenizer.token_type() == 'IDENTIFIER':
                self.write_tag('identifier', self.tokenizer.curr_token)

                self.tokenizer.next_token()
                self.write_tag('symbol', self.tokenizer.curr_token)
                self.tokenizer.next_token()
            if self.tokenizer.curr_token == ';':
                self.write_tag('symbol', self.tokenizer.curr_token)
                # return

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11
        .
        """
        # self.outputFile.write('<subroutineDec>' + '\n')
        while self.tokenizer.curr_token in self.subroutine_dec:
            self.outputFile.write('<subroutineDec>' + '\n')
            self.write_tag('keyword', self.tokenizer.curr_token)
            self.tokenizer.next_token()
            if ((self.tokenizer.curr_token == 'void') or (self.tokenizer.curr_token in self.types) or
                    (self.tokenizer.token_type() == 'IDENTIFIER')):
                if self.tokenizer.curr_token == 'void':
                    self.write_tag('keyword', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
                elif self.tokenizer.curr_token in self.types:
                    self.write_tag('keyword', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
                elif self.tokenizer.token_type() == 'IDENTIFIER':
                    self.write_tag('identifier', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
                if self.tokenizer.token_type() == 'IDENTIFIER':
                    self.write_tag('identifier', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
                    if self.tokenizer.curr_token == '(':
                        self.write_tag('symbol', self.tokenizer.curr_token)
                        self.tokenizer.next_token()

                        self.compile_parameter_list()
                        if self.tokenizer.curr_token == ')':
                            self.write_tag('symbol', self.tokenizer.curr_token)
                            self.tokenizer.next_token()
                            self.compile_subroutine_body()
                            self.tokenizer.next_token()
            self.outputFile.write('</subroutineDec>' + '\n')

        # self.outputFile.write('</subroutineDec>' + '\n')

    def compile_subroutine_body(self):

        self.outputFile.write('<subroutineBody>' + '\n')
        self.write_tag('symbol', self.tokenizer.curr_token)  # {
        self.tokenizer.next_token()
        while self.tokenizer.curr_token == 'var':
            self.compile_var_dec()
            # self.tokenizer.next_token()
        self.compile_statements()
        # self.tokenizer.next_token()

        self.write_tag('symbol', self.tokenizer.curr_token)  # }
        self.outputFile.write('</subroutineBody>' + '\n')
        # return

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """

        if self.tokenizer.curr_token == ")":
            self.outputFile.write('<parameterList>' + '\n' + '</parameterList>' + '\n')
        else:
            self.outputFile.write('<parameterList>' + '\n')
            while self.tokenizer.curr_token in self.types or self.tokenizer.token_type() == 'IDENTIFIER':

                if self.tokenizer.token_type() == 'IDENTIFIER':
                    self.write_tag('identifier', self.tokenizer.curr_token)
                    self.tokenizer.next_token()

                else:
                    self.write_tag('keyword', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
                if self.tokenizer.curr_token == ',':
                    self.write_tag('symbol', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
            self.outputFile.write('</parameterList>' + '\n')
            # return

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""

        # the type of it or (int , bool,char)
        self.outputFile.write('<varDec>' + '\n')
        if self.tokenizer.curr_token == 'var':
            self.write_tag('keyword', self.tokenizer.curr_token)
            self.tokenizer.next_token()
            self.compile_type()
            # return
        self.outputFile.write('</varDec>' + '\n')

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """

        self.outputFile.write('<statements>' + '\n')

        state = self.tokenizer.curr_token

        # while state in ["LET", "IF", "WHILE", "RETURN", "DO"]:
        while state in ["if", "while", "do", "let", "return"]:
            if state == "if":
                self.compile_if()
            elif state == "while":
                self.compile_while()
            elif state == "do":
                self.compile_do()
            elif state == "let":
                self.compile_let()
            elif state == "return":
                self.compile_return()
            self.tokenizer.next_token()
            state = self.tokenizer.curr_token
        self.outputFile.write('</statements>' + '\n')
        # return

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.outputFile.write('<doStatement>' + '\n')
        self.write_tag('keyword', self.tokenizer.curr_token)
        self.tokenizer.next_token()
        self.subroutine_call()
        self.tokenizer.next_token()
        if self.tokenizer.curr_token == ';':
            self.write_tag('symbol', self.tokenizer.curr_token)
            self.outputFile.write('</doStatement>' + '\n')
            # return

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.outputFile.write('<letStatement>' + '\n')
        self.write_tag('keyword', self.tokenizer.curr_token)
        self.tokenizer.next_token()
        if self.tokenizer.token_type() == 'IDENTIFIER':
            self.write_tag('identifier', self.tokenizer.curr_token)
            self.tokenizer.next_token()
            if self.tokenizer.curr_token == '[':
                self.write_tag('symbol', self.tokenizer.curr_token)
                self.tokenizer.next_token()
                self.compile_expression()
                if self.tokenizer.curr_token == ']':
                    self.write_tag('symbol', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
            if self.tokenizer.curr_token == '=':
                self.write_tag('symbol', self.tokenizer.curr_token)
                self.tokenizer.next_token()
                self.compile_expression()
                if self.tokenizer.curr_token == ';':
                    self.write_tag('symbol', self.tokenizer.curr_token)
                    self.outputFile.write('</letStatement>' + '\n')
                    # return

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.outputFile.write('<whileStatement>' + '\n')
        self.write_tag('keyword', self.tokenizer.curr_token)
        self.tokenizer.next_token()
        if self.tokenizer.curr_token == '(':
            self.write_tag('symbol', self.tokenizer.curr_token)
            self.tokenizer.next_token()
            self.compile_expression()

            if self.tokenizer.curr_token == ')':
                self.write_tag('symbol', self.tokenizer.curr_token)
                self.tokenizer.next_token()
                if self.tokenizer.curr_token == '{':
                    self.write_tag('symbol', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
                    self.compile_statements()
                    # self.tokenizer.next_token()
                    if self.tokenizer.curr_token == '}':
                        self.write_tag('symbol', self.tokenizer.curr_token)
                        self.outputFile.write('</whileStatement>' + '\n')
                        # return

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.outputFile.write('<returnStatement>' + '\n')
        self.write_tag('keyword', self.tokenizer.curr_token)
        self.tokenizer.next_token()
        if self.tokenizer.curr_token != ';':
            self.compile_expression()

        if self.tokenizer.curr_token == ';':
            self.write_tag('symbol', self.tokenizer.curr_token)
            self.outputFile.write('</returnStatement>' + '\n')
            # return

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.outputFile.write('<ifStatement>' + '\n')
        self.write_tag('keyword', self.tokenizer.curr_token) # if
        self.tokenizer.next_token()

        self.write_tag('symbol', self.tokenizer.curr_token) # (
        self.tokenizer.next_token()
        self.compile_expression()

        self.write_tag('symbol', self.tokenizer.curr_token) #)
        self.tokenizer.next_token()

        self.write_tag('symbol', self.tokenizer.curr_token) #{
        self.tokenizer.next_token()
        self.compile_statements()
        self.tokenizer.next_token()

        if self.tokenizer.previous_token[0] == '}' and self.tokenizer.curr_token == 'else':
            self.write_tag('symbol', self.tokenizer.previous_token[0])
            self.write_tag('keyword', self.tokenizer.curr_token)
            self.tokenizer.next_token()

            self.write_tag('symbol', self.tokenizer.curr_token) #{
            self.tokenizer.next_token()
            self.compile_statements()


            self.write_tag('symbol', self.tokenizer.curr_token) #}
            self.outputFile.write('</ifStatement>' + '\n')

        else:
            self.tokenizer.unadvance()
            self.write_tag('symbol', self.tokenizer.curr_token)
            self.outputFile.write('</ifStatement>' + '\n')

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.outputFile.write('<expression>' + '\n')
        self.compile_term()
        # self.tokenizer.next_token()
        while self.tokenizer.curr_token in self.op:
            self.write_tag('symbol', self.tokenizer.curr_token)
            self.tokenizer.next_token()
            self.compile_term()

        self.outputFile.write('</expression>' + '\n')
        # return

    def subroutine_call(self):
        # self.outputFile.write('<subroutineCall>' + '\n')
        if not (self.tokenizer.previous_token[1] == 'IDENTIFIER' and self.tokenizer.curr_token == '.'):
            self.tokenizer.next_token()
        if self.tokenizer.previous_token[1] == 'IDENTIFIER' and self.tokenizer.curr_token == '.':
            self.subroutine_call_2pos()
            # return
        else:
            self.subroutine_call_1pos()
            # return

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self.outputFile.write('<term>' + '\n')

        self.tokenizer.next_token()
        if self.tokenizer.previous_token[1] == 'INT_CONST':
            self.write_tag('integerConstant', self.tokenizer.previous_token[0])
            self.outputFile.write('</term>' + '\n')
            # return
        elif self.tokenizer.previous_token[1] == 'STRING_CONST':
            self.write_tag('stringConstant', self.tokenizer.previous_token[0].replace('"', ''))
            self.outputFile.write('</term>' + '\n')
            # return
        elif self.tokenizer.previous_token[0] in self.keyword_constant:
            self.write_tag('keyword', self.tokenizer.previous_token[0])
            self.outputFile.write('</term>' + '\n')
            # return
        elif self.tokenizer.previous_token[1] == 'IDENTIFIER' and self.tokenizer.curr_token == '[':
            self.write_tag('identifier', self.tokenizer.previous_token[0])
            self.write_tag('symbol', self.tokenizer.curr_token)
            self.tokenizer.next_token()
            self.compile_expression()
            # self.tokenizer.next_token()
            if self.tokenizer.curr_token == ']':
                self.write_tag('symbol', self.tokenizer.curr_token)
                self.outputFile.write('</term>' + '\n')
                self.tokenizer.next_token()
                # return
        elif self.tokenizer.previous_token[1] == 'IDENTIFIER' and self.tokenizer.curr_token != '.':
            self.write_tag('identifier', self.tokenizer.previous_token[0])
            self.outputFile.write('</term>' + '\n')
            # return
        elif self.tokenizer.previous_token[0] == '(':
            self.write_tag('symbol', self.tokenizer.previous_token[0])
            self.compile_expression()
            # self.tokenizer.next_token()
            if self.tokenizer.curr_token == ')':
                self.write_tag('symbol', self.tokenizer.curr_token)
                self.tokenizer.next_token()
                self.outputFile.write('</term>' + '\n')
                # return
        elif self.tokenizer.previous_token[0] in self.unaryOp:
            self.write_tag('symbol', self.tokenizer.previous_token[0])
            self.compile_term()
            self.outputFile.write('</term>' + '\n')
            # return
        else:
            self.subroutine_call()
            self.outputFile.write('</term>' + '\n')
            self.tokenizer.next_token()
            # return

    def subroutine_call_1pos(self):
        # subroutineName and (expression list)
        self.write_tag('identifier', self.tokenizer.previous_token[0])
        self.write_tag('symbol', self.tokenizer.curr_token)
        self.tokenizer.next_token()

        self.compile_expression_list()
        # self.tokenizer.next_token()
        if self.tokenizer.curr_token == ')':
            self.write_tag('symbol', self.tokenizer.curr_token)
            # return

    def subroutine_call_2pos(self):
        self.write_tag('identifier', self.tokenizer.previous_token[0])
        self.write_tag('symbol', self.tokenizer.curr_token)
        self.tokenizer.next_token()
        self.tokenizer.next_token()
        self.subroutine_call_1pos()
        # return

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ')':
        #     # return
        # (expression)
        # self.outputFile.write('<expressionList>' + '\n')
        if self.tokenizer.curr_token == ')':
            self.outputFile.write('<expressionList>' + '\n' + '</expressionList>' + '\n')
        else:
            self.outputFile.write('<expressionList>' + '\n')
            self.compile_expression()
            # self.tokenizer.next_token()
            # (,expression*)
            while self.tokenizer.curr_token == ',':
                self.write_tag('symbol', self.tokenizer.curr_token)
                self.tokenizer.next_token()

                self.compile_expression()
                # self.tokenizer.next_token()

            self.outputFile.write('</expressionList>' + '\n')
        # return

    ## not sure if we will use them
    def expect_symbol(self, symbol: str):
        if self.tokenizer.token_type() != 'SYMBOL' or self.tokenizer.symbol() != symbol:
            raise ValueError(f"Expected symbol '{symbol}' but found '{self.tokenizer.symbol()}'")

    def expect_keyword(self, keyword: str):
        if self.tokenizer.token_type() != 'KEYWORD' or self.tokenizer.curr_token != keyword:
            raise ValueError(f"Expected keyword '{keyword}' but found '{self.tokenizer.curr_token}'")

    def close(self):
        self.outputFile.close()
