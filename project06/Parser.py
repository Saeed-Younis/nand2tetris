"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.file = input_file
        self.input_lines = self.file.read().splitlines()
        self.lines_commands = {}  # Map of address -> command
        self.labels = {}  # Map of label -> address
        self.command_counter = 0  # Tracks only executable commands

        for line in self.input_lines:
            line = line.split('//')[0].strip()
            if not line:
                continue

            if line[0] == '(':
                label = line[1:-1].strip()
                self.labels[label] = self.command_counter
            else:
                self.lines_commands[self.command_counter] = line
                self.command_counter += 1

        self.current_counter = 0
        self.current_command = self.lines_commands.get(self.current_counter, None)

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns;
            bool: True if there are more commands, False otherwise.
        """
        return self.current_counter < self.command_counter

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if a has_more_commands() is true.
        """
        while self.has_more_commands():
            self.current_counter += 1
            self.current_command = self.lines_commands.get(self.current_counter, None)
            if self.current_command and self.current_command[0] != '(':
                break

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if not self.current_command:
            return None
        if self.current_command[0] == '@':
            return "A_COMMAND"
        if self.current_command[0] == '(':
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self.command_type() == "A_COMMAND":
            return self.current_command[1:].strip()
        if self.command_type() == "L_COMMAND":
            return self.current_command[1:-1].strip()

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if '=' in self.current_command:
            return self.current_command.split('=')[0].strip()
        return 'null'

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """

        comp_part = self.current_command
        if '=' in comp_part:
            comp_part = comp_part.split('=')[1]
        if ';' in comp_part:
            comp_part = comp_part.split(';')[0]
        return comp_part.strip()

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if ';' in self.current_command:
            return self.current_command.split(';')[1].strip()
        return 'null'
