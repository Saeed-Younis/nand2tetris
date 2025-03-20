"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line's end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.input_lines = input_file.read().splitlines()
        self.line_commands = []
        self.commands_counter = 0
        for line in self.input_lines:
            line = line.split('//')[0].strip()
            if not line:
                continue
            self.line_commands.append(line)
            self.commands_counter += 1
        self.current_counter = 0
        self.current_command = self.line_commands[self.current_counter]
        self.arithmetic_cm = ['add', 'sub', 'and', 'or', 'eq', 'gt', 'lt', 'neg', 'not', 'shiftleft', 'shiftright']
        self.other_commands = ['push', 'pop', 'label', 'goto', 'if-goto', 'function', 'call', 'return']

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.current_counter < self.commands_counter

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        if self.has_more_commands():

            self.current_command = self.line_commands[self.current_counter]

            self.current_counter += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        cur = self.current_command.split()
        if cur[0] in self.arithmetic_cm:
            return "C_ARITHMETIC"
        if cur[0] in self.other_commands:
            if cur[0] == 'push':
                return "C_PUSH"
            if cur[0] == 'pop':
                return "C_POP"
            if cur[0] == 'label':
                return "C_LABEL"
            if cur[0] == 'goto':
                return "C_GOTO"
            if cur[0] == 'if-goto':
                return "C_IF"
            if cur[0] == 'function':
                return "C_FUNCTION"
            if cur[0] == 'call':
                return "C_CALL"
            else:
                return "C_RETURN"


    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        if self.current_command in self.arithmetic_cm:
            return self.current_command
        cur = self.current_command.split()
        if cur[0] in self.other_commands:
            return cur[1]


    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        cur = self.current_command.split()
        if cur[0] in self.other_commands:

            if self.command_type() == "C_PUSH":
                return int(cur[2])
            if self.command_type() == "C_POP":
                return int(cur[2])
            if self.command_type() == "C_FUNCTION":
                return int(cur[2])
            if self.command_type() == "C_CALL":
                return int(cur[2])
