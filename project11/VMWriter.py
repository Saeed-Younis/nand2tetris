"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.outputVM_File = output_stream
        self.dict_key = {'CONST': 'constant', 'ARG': 'argument',
                         'LOCAL': 'local',
                         'STATIC': 'static',
                         'THIS': 'this', 'THAT': 'that', 'POINTER': 'pointer',
                         'TEMP': 'temp'}
        self.dict_arth = {"ADD": 'add', "SUB": 'sub', "NEG": 'neg',
                          "EQ": 'eq', "GT": 'gt', "LT": 'lt', "AND": 'and', "OR": 'or', "NOT": 'not',
                          "SHIFTLEFT": 'shiftleft', "SHIFTRIGHT": 'shiftright'}

        pass

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """

        if segment in self.dict_key:
            self.outputVM_File.write(f"push {self.dict_key[segment]} {index}\n")

    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.

        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        # Your code goes here!
        if segment in self.dict_key:
            self.outputVM_File.write(f"pop {self.dict_key[segment]} {index}\n")

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG", 
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
        """
        # Your code goes here!
        if command in self.dict_arth:
            self.outputVM_File.write(f"{self.dict_arth[command]}\n")

        pass

    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        # Your code goes here!
        self.outputVM_File.write(f"label {label}\n")

    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        self.outputVM_File.write(f"goto {label}\n")
        pass

    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        self.outputVM_File.write(f"if-goto {label}\n")
        pass

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        # Your code goes here!
        self.outputVM_File.write(f"call {name} {n_args}\n")
        pass

    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        self.outputVM_File.write(f"function {name} {n_locals}\n")
        pass

    def write_return(self) -> None:
        """Writes a VM return command."""
        # Your code goes here!
        self.outputVM_File.write('return' + '\n')
        pass
