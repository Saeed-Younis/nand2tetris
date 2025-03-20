"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import *
from VMWriter import *
from SymbolTable import *


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
        self.symbol_table = SymbolTable()
        self.tokenizer = input_stream
        self.vm_write = VMWriter(output_stream)

        self.indent = ""
        self.subroutine_dec = ['constructor', 'function', 'method']
        self.class_var_dec = ['static', 'field']
        self.types = ['int', 'char', 'boolean']
        self.op = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
        self.unaryOp = ['-', '~']
        self.keyword_constant = {'true': 0, 'false': 0, 'null': 0, 'this': 1}
        self.class_name = ''
        self.while_label_c = 0
        self.if_label_c = 0

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # starts of class
        # self.outputFile.write('<class>' + '\n')
        if self.tokenizer.curr_token == 'class':
            # self.write_tag('keyword', self.tokenizer.curr_token)
            self.tokenizer.next_token()
            if self.tokenizer.token_type() == 'IDENTIFIER':
                self.class_name = self.tokenizer.curr_token

                self.tokenizer.next_token()
                if self.tokenizer.curr_token == '{':
                    # self.write_tag('symbol', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
                    if self.tokenizer.curr_token in self.class_var_dec:
                        self.compile_class_var_dec()

                    self.compile_subroutine()
                    self.tokenizer.next_token()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # self.outputFile.write('<classVarDec>' + '\n')
        while self.tokenizer.curr_token in self.class_var_dec:
            # self.outputFile.write('<classVarDec>' + '\n')
            kind = self.tokenizer.keyword()
            self.tokenizer.next_token()
            self.compile_type(kind)

    def compile_type(self, kind):
        if self.tokenizer.curr_token in self.types or self.tokenizer.token_type() == 'IDENTIFIER':
            if self.tokenizer.token_type() == 'IDENTIFIER':
                type = self.tokenizer.curr_token
                self.tokenizer.next_token()
            else:
                type = self.tokenizer.curr_token
                self.tokenizer.next_token()

            while self.tokenizer.token_type() == 'IDENTIFIER':
                name = self.tokenizer.curr_token
                self.symbol_table.define(name, type, kind)

                self.tokenizer.next_token()
                # ('symbol', self.tokenizer.curr_token)
                self.tokenizer.next_token()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11
        .
        """

        while self.tokenizer.curr_token in self.subroutine_dec:

            kind = self.tokenizer.curr_token
            self.symbol_table.start_subroutine()  # new subroutine table
            self.while_label_c = 0
            self.if_label_c = 0
            self.tokenizer.next_token()
            if ((self.tokenizer.curr_token == 'void') or (self.tokenizer.curr_token in self.types) or
                    (self.tokenizer.token_type() == 'IDENTIFIER')):
                if self.tokenizer.curr_token == 'void':
                    # self.write_tag('keyword', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
                elif self.tokenizer.curr_token in self.types:
                    # self.write_tag('keyword', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
                elif self.tokenizer.token_type() == 'IDENTIFIER':
                    # self.write_tag('identifier', self.tokenizer.curr_token)
                    self.tokenizer.next_token()
                if self.tokenizer.token_type() == 'IDENTIFIER':
                    func_name = self.tokenizer.curr_token
                    self.tokenizer.next_token()
                    if self.tokenizer.curr_token == '(':
                        # self.write_tag('symbol', self.tokenizer.curr_token)
                        self.tokenizer.next_token()

                        self.compile_parameter_list(kind)
                        # self.vm_write.write_function(self.class_name + '.' + func_name,
                        #                              self.symbol_table.var_count('VAR'))
                        if self.tokenizer.curr_token == ')':
                            # self.write_tag('symbol', self.tokenizer.curr_token)
                            self.tokenizer.next_token()
                            self.compile_subroutine_body(func_name, kind)
                            self.tokenizer.next_token()

    def compile_subroutine_body(self, func_name, kind):
        if self.tokenizer.curr_token == '{':

            self.tokenizer.next_token()
            while self.tokenizer.curr_token == 'var':
                self.compile_var_dec()

            self.vm_write.write_function(self.class_name + '.' + func_name,
                                         self.symbol_table.var_count('VAR'))
            if kind == 'constructor':
                self.vm_write.write_push('CONST', self.symbol_table.var_count('FIELD'))
                self.vm_write.write_call('Memory.alloc', 1)
                self.vm_write.write_pop('POINTER', 0)
            if kind == 'method':
                self.vm_write.write_push('ARG', 0)
                self.vm_write.write_pop('POINTER', 0)
            self.compile_statements(func_name)

    def compile_parameter_list(self, kind) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """

        if kind == 'method':
            self.symbol_table.define('this', self.class_name, 'ARG')
        while self.tokenizer.curr_token in self.types or self.tokenizer.token_type() == 'IDENTIFIER':

            if self.tokenizer.token_type() == 'IDENTIFIER' and self.tokenizer.curr_token == self.class_name:
                type = self.tokenizer.curr_token
                self.tokenizer.next_token()

            else:
                type = self.tokenizer.curr_token
                self.tokenizer.next_token()
            if self.tokenizer.token_type() == 'IDENTIFIER':
                name = self.tokenizer.curr_token
                self.tokenizer.next_token()
                self.symbol_table.define(name, type, 'ARG')
            if self.tokenizer.curr_token == ',':
                # self.write_tag('symbol',self.tokenizer.curr_token)
                self.tokenizer.next_token()
        # self.outputFile.write('</parameterList>' + '\n')
        # return

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # ready
        # the type of it or (int , bool,char)
        # self.outputFile.write('<varDec>'+'\n')
        if self.tokenizer.curr_token == 'var':
            kind = self.tokenizer.curr_token
            self.tokenizer.next_token()
            self.compile_type(kind.upper())
            # return
        # self.outputFile.write('</varDec>'+'\n')

    def compile_statements(self, func_name) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """

        # self.outputFile.write('<statements>' + '\n')

        state = self.tokenizer.curr_token

        # while state in ["LET", "IF", "WHILE", "RETURN", "DO"]:
        while state in ["if", "while", "do", "let", "return"]:
            if state == "if":
                self.compile_if(func_name)
            elif state == "while":
                self.compile_while(func_name)
            elif state == "do":
                self.compile_do()
            elif state == "let":
                self.compile_let()
            elif state == "return":
                self.compile_return()
            self.tokenizer.next_token()
            state = self.tokenizer.curr_token

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.tokenizer.next_token()
        self.tokenizer.next_token()
        flag = 0
        if self.tokenizer.previous_token[0] == 'IDENTIFIER' and self.tokenizer.curr_token == '.':
            flag = 1
        self.tokenizer.unadvance()
        self.subroutine_call()
        if not flag:
            self.vm_write.write_pop('TEMP', 0)
        self.tokenizer.next_token()

    def compile_let(self) -> None:
        """Compiles a let statement."""

        self.tokenizer.next_token()
        if self.tokenizer.token_type() == 'IDENTIFIER':
            var_name = self.tokenizer.curr_token
            self.tokenizer.next_token()
            array = 0
            if self.tokenizer.curr_token == '[':
                self.tokenizer.next_token()
                self.compile_expression()
                self.compileArray(var_name)
                array = 1
                if self.tokenizer.curr_token == ']':
                    self.tokenizer.next_token()
            if self.tokenizer.curr_token == '=':
                self.tokenizer.next_token()
                self.compile_expression()

                if not array:
                    kind = self.symbol_table.kind_of(var_name)
                    index = self.symbol_table.index_of(var_name)
                    if kind and index != -1:
                        if kind == 'VAR':
                            kind = 'LOCAL'
                            self.vm_write.write_pop(kind, index)
                        elif kind == 'FIELD':
                            self.vm_write.write_pop('THIS', index)
                        else:
                            self.vm_write.write_pop(kind, index)

                else:
                    self.vm_write.write_pop('TEMP', 0)
                    self.vm_write.write_pop('POINTER', 1)
                    self.vm_write.write_push('TEMP', 0)
                    self.vm_write.write_pop('THAT', 0)

    def compileArray(self, name):
        if self.symbol_table.kind_of(name):
            if self.symbol_table.kind_of(name) == 'VAR':
                self.vm_write.write_push('LOCAL', self.symbol_table.index_of(name))
            elif self.symbol_table.kind_of(name) == 'ARG':
                self.vm_write.write_push('ARG', self.symbol_table.index_of(name))

            elif self.symbol_table.kind_of(name) == 'STATIC':
                self.vm_write.write_push('STATIC', self.symbol_table.index_of(name))
            else:
                self.vm_write.write_push('THIS', self.symbol_table.index_of(name))
        self.vm_write.write_arithmetic('ADD')

    def compile_while(self, func_name) -> None:
        """Compiles a while statement."""
        label1 = f"WHILE_EXP{self.while_label_c}"
        label2 = f"WHILE_END{self.while_label_c}"
        self.while_label_c += 1
        self.vm_write.write_label(label1)

        self.tokenizer.next_token()
        if self.tokenizer.curr_token == '(':
            self.tokenizer.next_token()
            self.compile_expression()
            self.vm_write.write_arithmetic('NOT')
            self.vm_write.write_if(label2)
            if self.tokenizer.curr_token == ')':
                self.tokenizer.next_token()
                if self.tokenizer.curr_token == '{':
                    self.tokenizer.next_token()
                    self.compile_statements(func_name)

                    self.vm_write.write_goto(label1)
                    if self.tokenizer.curr_token == '}':
                        self.vm_write.write_label(label2)

    def compile_return(self) -> None:
        """Compiles a return statement."""

        self.tokenizer.next_token()
        if self.tokenizer.curr_token != ';':
            self.compile_expression()
            self.vm_write.write_return()
        else:
            self.vm_write.write_push('CONST', 0)
            self.vm_write.write_return()

    def compile_if(self, func_name) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        label1 = f"IF_TRUE{self.if_label_c}"
        label2 = f"IF_FALSE{self.if_label_c}"
        label3 = f"IF_END{self.if_label_c}"
        self.if_label_c += 1
        self.tokenizer.next_token()
        if self.tokenizer.curr_token == '(':
            self.tokenizer.next_token()
            self.compile_expression()
            self.vm_write.write_if(label1)  # true
            self.vm_write.write_goto(label2)  # false
            if self.tokenizer.curr_token == ')':
                self.tokenizer.next_token()
                if self.tokenizer.curr_token == '{':
                    self.vm_write.write_label(label1)  # TRUE
                    self.tokenizer.next_token()
                    self.compile_statements(func_name)
                    self.tokenizer.next_token()

                    if self.tokenizer.previous_token[0] == '}' and self.tokenizer.curr_token == 'else':
                        self.tokenizer.next_token()
                        self.vm_write.write_goto(label3)  # end
                        if self.tokenizer.curr_token == '{':
                            self.vm_write.write_label(label2)  # false
                            self.tokenizer.next_token()
                            self.compile_statements(func_name)

                            if self.tokenizer.curr_token == '}':
                                self.vm_write.write_label(label3)  # end

                    else:
                        self.tokenizer.unadvance()
                        # false
                        self.vm_write.write_label(label2)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!

        self.compile_term()

        while self.tokenizer.curr_token in self.op:
            arth = self.tokenizer.curr_token
            self.tokenizer.next_token()
            self.compile_term()
            if arth == '+':
                self.vm_write.write_arithmetic('ADD')
            elif arth == '-':
                self.vm_write.write_arithmetic('SUB')
            elif arth == '*':
                self.vm_write.write_call('Math.multiply', 2)
            elif arth == '&lt;':
                self.vm_write.write_arithmetic('LT')
            elif arth == '&gt;':
                self.vm_write.write_arithmetic('GT')
            elif arth == '=':
                self.vm_write.write_arithmetic('EQ')
            elif arth == '&amp;':
                self.vm_write.write_arithmetic('AND')
            elif arth == '/':
                self.vm_write.write_call('Math.divide', 2)
            elif arth == '|':
                self.vm_write.write_arithmetic('OR')

    def subroutine_call(self):
        if not (self.tokenizer.previous_token[1] == 'IDENTIFIER' and self.tokenizer.curr_token == '.'):
            self.tokenizer.next_token()
        if self.tokenizer.previous_token[1] == 'IDENTIFIER' and self.tokenizer.curr_token == '.':
            self.subroutine_call_2pos()

        else:
            self.subroutine_call_1pos(self.tokenizer.previous_token[1])

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

        self.tokenizer.next_token()
        if self.tokenizer.previous_token[1] == 'INT_CONST':
            self.vm_write.write_push('CONST', self.tokenizer.previous_token[0])

        elif self.tokenizer.previous_token[1] == 'STRING_CONST':
            string_const = self.tokenizer.previous_token[0]
            self.vm_write.write_push('CONST', len(string_const))
            self.vm_write.write_call('String.new', 1)
            for char in string_const:
                self.vm_write.write_push('CONST', ord(char))
                self.vm_write.write_call('String.appendChar', 2)

        elif self.tokenizer.previous_token[0] in self.keyword_constant:
            if self.tokenizer.previous_token[0] == 'this':
                self.vm_write.write_push('POINTER', 0)
            else:
                kind = 'CONST'
                index = self.keyword_constant[self.tokenizer.previous_token[0]]
                self.vm_write.write_push(kind, index)
                if self.tokenizer.previous_token[0] == 'true':
                    self.vm_write.write_arithmetic('NOT')


        elif self.tokenizer.previous_token[1] == 'IDENTIFIER' and self.tokenizer.curr_token == '[':

            var_name = self.tokenizer.previous_token[0]
            self.tokenizer.next_token()
            self.compile_expression()
            self.compileArray(var_name)
            self.vm_write.write_pop('POINTER', 1)
            self.vm_write.write_push('THAT', 0)

            if self.tokenizer.curr_token == ']':
                self.tokenizer.next_token()

        elif self.tokenizer.previous_token[1] == 'IDENTIFIER' and self.tokenizer.curr_token != '.':
            name = self.tokenizer.previous_token[0]
            kind = self.symbol_table.kind_of(name)
            index = self.symbol_table.index_of(name)
            if kind and index != -1:
                if kind == 'FIELD':
                    self.vm_write.write_push('THIS', index)
                if kind == 'VAR':
                    kind = 'LOCAL'
                    self.vm_write.write_push(kind, index)
                else:
                    self.vm_write.write_push(kind, index)
            # return
        elif self.tokenizer.previous_token[0] == '(':

            self.compile_expression()

            if self.tokenizer.curr_token == ')':
                self.tokenizer.next_token()

        elif self.tokenizer.previous_token[0] in self.unaryOp:

            if self.tokenizer.previous_token[0] == '~':
                op = '~'
            else:
                op = '-'
            self.compile_term()
            if op == '~':
                self.vm_write.write_arithmetic('NOT')
            else:
                self.vm_write.write_arithmetic('NEG')
            # self.outputFile.write('</term>' + '\n')
            # return
        else:
            self.subroutine_call()
            # self.outputFile.write('</term>' + '\n')
            self.tokenizer.next_token()
            # return

    def subroutine_call_1pos(self, class1):
        # subroutineName and (expression list)
        func_name1 = self.tokenizer.previous_token[0]
        n_arg = 0

        self.tokenizer.next_token()

        if self.symbol_table.kind_of(class1):
            kind = self.symbol_table.kind_of(class1)
            if kind == 'VAR':
                kind = 'LOCAL'
                self.vm_write.write_push(kind, self.symbol_table.index_of(class1))
            elif kind == 'FIELD':
                self.vm_write.write_push('THIS', self.symbol_table.index_of(class1))
            else:
                self.vm_write.write_push(kind, self.symbol_table.index_of(class1))
        if class1 == 'IDENTIFIER':
            self.vm_write.write_push('POINTER', 0)

            n_arg += 1
            name = self.class_name + '.' + func_name1
        elif self.symbol_table.type_of(class1):
            n_arg += 1
            name = self.symbol_table.type_of(class1) + '.' + func_name1
        else:

            name = class1 + '.' + func_name1
        n_arg += self.compile_expression_list()
        self.vm_write.write_call(name, n_arg)

    def subroutine_call_2pos(self):
        class1 = self.tokenizer.previous_token[0]
        self.tokenizer.next_token()
        self.tokenizer.next_token()
        self.subroutine_call_1pos(class1)

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # (expression)

        if self.tokenizer.curr_token == ')':

            return 0
        else:

            self.compile_expression()

            # (,expression*)
            expression_count = 1
            while self.tokenizer.curr_token == ',':
                self.tokenizer.next_token()

                self.compile_expression()

                expression_count += 1
            return expression_count


