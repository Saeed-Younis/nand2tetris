"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    parser = Parser(input_file)
    symbol_table = SymbolTable()
    code = Code()

    #first pass
    for symbol in parser.labels.keys():
        if not  symbol_table.contains(symbol):
            symbol_table.add_entry(symbol,parser.labels[symbol])


    # Reset the input file and reinitialize parser for second pass
    input_file.seek(0)
    parser = Parser(input_file)
    next_address = 16  # Start allocating variables from RAM[16]

    # Second pass: Translate instructions into binary
    while parser.has_more_commands():
        if parser.command_type() == "A_COMMAND":
            symbol = parser.symbol()
            if symbol.isdigit():  # Numeric address
                address = int(symbol)
            else:  # Variable or label
                if not symbol_table.contains(symbol):

                    symbol_table.add_entry(symbol, next_address)
                    next_address += 1
                address = symbol_table.get_address(symbol)
            binary_instruction = f"0{address:015b}"  # Format as 16-bit binary
            output_file.write(binary_instruction + "\n")

        elif parser.command_type() == "C_COMMAND":
            dest = code.dest(parser.dest())
            comp = code.comp(parser.comp())
            jump = code.jump(parser.jump())
            binary_instruction = f"111{comp}{dest}{jump}"  # C-instruction format
            output_file.write(binary_instruction + "\n")

        parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
