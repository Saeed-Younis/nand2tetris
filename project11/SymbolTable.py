"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import*

class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        # Your code goes here!
        self.class_dec = []
        self.subroutine_dec = []
        self.field_index = 0
        self.static_index = 0
        self.var_index = 0
        self.arg_index = 0

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        # Your code goes here!
        self.subroutine_dec = []
        self.var_index = 0
        self.arg_index = 0
        return

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        # Your code goes here!

        if kind == 'STATIC':
            self.class_dec.append([name, type, kind, self.static_index])
            self.static_index += 1
            return
        if kind == 'FIELD':
            self.class_dec.append([name, type, kind, self.field_index])
            self.field_index += 1
            return
        if kind == 'ARG':
            self.subroutine_dec.append([name, type, kind, self.arg_index])
            self.arg_index += 1
            return
        if kind == 'VAR':
            self.subroutine_dec.append([name, type, kind, self.var_index])
            self.var_index += 1
            return

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        if kind == 'STATIC':
            return self.static_index
        elif kind == 'FIELD':
            return self.field_index
        elif kind == 'ARG':
            return self.arg_index
        elif kind == 'VAR':
            return self.var_index

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        # Your code goes here!
        for n in range(len(self.subroutine_dec)):
            if self.subroutine_dec[n][0] == name:
                return self.subroutine_dec[n][2]
        for i in range(len(self.class_dec)):
            if self.class_dec[i][0] == name:
                return self.class_dec[i][2]
        return ''

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        # Your code goes here!
        for n in range(len(self.subroutine_dec)):
            if self.subroutine_dec[n][0] == name:
                return self.subroutine_dec[n][1]
        for i in range(len(self.class_dec)):
            if self.class_dec[i][0] == name:
                return self.class_dec[i][1]
        return ''

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        # Your code goes here!
        for n in range(len(self.subroutine_dec)):
            if self.subroutine_dec[n][0] == name:
                return self.subroutine_dec[n][3]
        for i in range(len(self.class_dec)):
            if self.class_dec[i][0] == name:
                return self.class_dec[i][3]
        return -1

