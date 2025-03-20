"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.out_stream = output_stream
        self.arg_translate = {'@SP': '@0', '@LCL': '@1', '@ARG': '@2', '@THIS': '@3', '@THAT': '@4'}
        self.arg_shortcuts = {'LOCAL': 'LCL', 'ARGUMENT': 'ARG'}
        # self.root = output_stream[:-4].split('/')[-1]
        self.label_counter = 0
        self.file_name = ''
        self.continue_counter = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.file_name = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        if command == 'add':
            for i in self.add_translate():
                self.out_stream.write(i)
                self.out_stream.write('\n')
        if command == 'sub':
            for j in self.sub_translate():
                self.out_stream.write(j)
                self.out_stream.write('\n')
        if command == 'neg':
            for m in self.neg_translate():
                self.out_stream.write(m)
                self.out_stream.write('\n')
        if command == 'eq':
            for s in self.eq_translate():
                self.out_stream.write(s)
                if s[0] == '(' and s[1] == 'c':
                    self.continue_counter += 1
                if s[0] == '(' and s[1] != 'c':
                    self.label_counter += 1
                self.out_stream.write('\n')
        if command == 'gt':
            for r in self.gt_translate():
                self.out_stream.write(r)
                if r[0] == '(' and r[1] == 'c':
                    self.continue_counter += 1
                if r[0] == '(' and r[1] != 'c':
                    self.label_counter += 1
                self.out_stream.write('\n')
        if command == 'lt':
            for k in self.lt_translate():
                self.out_stream.write(k)
                if k[0] == '(' and k[1] == 'c':
                    self.continue_counter += 1
                if k[0] == '(' and k[1] != 'c':
                    self.label_counter += 1
                self.out_stream.write('\n')
        if command == 'and':
            for h in self.and_translate():
                self.out_stream.write(h)
                self.out_stream.write('\n')

        if command == 'not':
            for n in self.not_translate():
                self.out_stream.write(n)
                self.out_stream.write('\n')
        if command == 'or':
            for b in self.or_translate():
                self.out_stream.write(b)
                self.out_stream.write('\n')

    def gt_translate(self):
        return ['@SP', 'AM=M-1', 'D=M', '@neg2' + str(self.label_counter), 'D;JLT', '@SP', 'A=M-1', 'D=M',
                '@pos2neg1' + str(self.label_counter), 'D;JLT', '@neg2neg1' + str(self.label_counter),
                '0;JMP',
                '(pos2neg1' + str(self.label_counter) + ')', '@SP', 'A=M-1', 'M=0',
                '@continue' + str(self.continue_counter), '0;JMP', '(neg2' + str(self.label_counter) + ')',
                '@SP', 'A=M-1', 'D=M',
                '@neg2neg1' + str(self.label_counter), 'D;JLT', '@SP', 'A=M-1', 'M=-1',
                '@continue' + str(self.continue_counter)
            , '(neg2neg1' + str(self.label_counter) + ')', '@SP',
                'A=M', 'D=M', 'A=A-1', 'M=M-D', 'D=M',
                '@true' + str(self.label_counter), 'D;JGT',
                '@SP', 'A=M-1', 'M=0',
                '@continue' + str(self.continue_counter), '0;JMP', '(true' + str(self.label_counter) + ')', '@SP',
                'A=M-1', 'M=-1', '(continue' + str(self.continue_counter) + ')']

    def lt_translate(self):
        return ['@SP', 'AM=M-1', 'D=M', '@neg2' + str(self.label_counter), 'D;JLT', '@SP', 'A=M-1', 'D=M',
                '@pos2neg1' + str(self.label_counter), 'D;JLT', '@neg2neg1' + str(self.label_counter),
                '0;JMP',
                '(pos2neg1' + str(self.label_counter) + ')', '@SP', 'A=M-1', 'M=-1',
                '@continue' + str(self.continue_counter), '0;JMP', '(neg2' + str(self.label_counter) + ')',
                '@SP', 'A=M-1', 'D=M',
                '@neg2neg1' + str(self.label_counter), 'D;JLT', '@SP', 'A=M-1', 'M=0',
                '@continue' + str(self.continue_counter)
            , '(neg2neg1' + str(self.label_counter) + ')', '@SP',
                'A=M', 'D=M', 'A=A-1', 'M=M-D', 'D=M',
                '@true' + str(self.label_counter), 'D;JLT',
                '@SP', 'A=M-1', 'M=0',
                '@continue' + str(self.continue_counter), '0;JMP', '(true' + str(self.label_counter) + ')', '@SP',
                'A=M-1', 'M=-1', '(continue' + str(self.continue_counter) + ')']

    def and_translate(self):
        return ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=D&M']

    def or_translate(self):
        return ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=M|D']

    def not_translate(self):
        return ['@SP', 'A=M-1', 'M=!M']

    def eq_translate(self):
        return ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=M-D',
                'D=M', '@true' + str(self.label_counter), 'D;JEQ', '@SP', 'A=M-1',
                'M=0', '@continue' + str(self.continue_counter), '0;JMP', '(true' + str(self.label_counter) + ')',
                '@SP', 'A=M-1', 'M=-1',
                '(continue' + str(self.continue_counter) + ')']

    def neg_translate(self):
        return ['@SP', 'A=M-1', 'M=-M']

    def add_translate(self):
        return ['@SP', 'AM=M-1', 'D=M', '@SP', 'A=M-1', 'M=M+D']

    def sub_translate(self):
        return ['@SP', 'AM=M-1', 'D=M', '@SP', 'A=M-1', 'M=M-D']

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        index = str(index)
        if command == "push":
            if segment == 'constant':
                constant_push = ['@' + index, 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
                for i in constant_push:
                    self.out_stream.write(i)
                    self.out_stream.write('\n')
            if segment == 'static':
                static_push = ['@' + self.file_name + '.' + index, 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
                for s in static_push:
                    self.out_stream.write(s)
                    self.out_stream.write('\n')
            if segment == 'this':
                this_push = ['@' + index, 'D=A', '@THIS', 'A=M+D', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
                for this in this_push:
                    self.out_stream.write(this)
                    self.out_stream.write('\n')
            if segment == 'that':
                that_push = ['@' + index, 'D=A', '@THAT', 'A=M+D', 'D=M', '@SP', 'A=M',
                             'M=D', '@SP', 'M=M+1']
                for that in that_push:
                    self.out_stream.write(that)
                    self.out_stream.write('\n')
            if segment == 'argument':
                argument_push = ['@' + index, 'D=A', '@ARG', 'A=M+D', 'D=M', '@SP', 'A=M', 'M=D',
                                 '@SP', 'M=M+1']
                for arg in argument_push:
                    self.out_stream.write(arg)
                    self.out_stream.write('\n')
            if segment == 'local':
                local_push = ['@' + index, 'D=A', '@LCL', 'A=M+D', 'D=M', '@SP'
                    , 'A=M', 'M=D', '@SP', 'M=M+1']
                for lcl in local_push:
                    self.out_stream.write(lcl)
                    self.out_stream.write('\n')
            if segment == 'temp':
                temp_push = ['@' + index, 'D=A', '@5', 'A=A+D', 'D=M', '@SP', 'A=M', 'M=D',
                             '@SP', 'M=M+1']
                for tem in temp_push:
                    self.out_stream.write(tem)
                    self.out_stream.write('\n')
            if segment == 'pointer':
                pointer_push = ['@' + index, 'D=A', '@3', 'A=A+D', 'D=M', '@SP'
                    , 'A=M', 'M=D', '@SP', 'M=M+1']
                for pr in pointer_push:
                    self.out_stream.write(pr)
                    self.out_stream.write('\n')


        elif command == "pop":
            if segment == 'static':
                static_pop = ['@SP', 'AM=M-1', 'D=M', '@' + self.file_name + '.' + index, 'M=D']
                for st in static_pop:
                    self.out_stream.write(st)
                    self.out_stream.write('\n')
            if segment == 'this':
                this_pop = ['@' + index, 'D=A', '@THIS', 'D=M+D', '@R13', 'M=D',
                            '@SP', 'AM=M-1', 'D=M'
                    , '@R13', 'A=M', 'M=D']
                for th in this_pop:
                    self.out_stream.write(th)
                    self.out_stream.write('\n')
            if segment == 'that':
                that_pop = ['@' + index, 'D=A', '@THAT', 'D=M+D', '@R13', 'M=D',
                            '@SP', 'AM=M-1', 'D=M'
                    , '@R13', 'A=M', 'M=D']
                for that in that_pop:
                    self.out_stream.write(that)
                    self.out_stream.write('\n')
            if segment == 'argument':
                argument_pop = ['@' + index, 'D=A', '@ARG', 'D=M+D', '@R13', 'M=D'
                    , '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
                for arg in argument_pop:
                    self.out_stream.write(arg)
                    self.out_stream.write('\n')
            if segment == 'local':
                local_pop = ['@' + index, 'D=A', '@LCL', 'D=M+D', '@R13',
                             'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
                for lcl in local_pop:
                    self.out_stream.write(lcl)
                    self.out_stream.write('\n')
            if segment == 'pointer':
                pointer_pop = ['@' + index, 'D=A', '@3', 'D=A+D', '@R14', 'M=D',
                               '@SP', 'AM=M-1', 'D=M', '@R14', 'A=M', 'M=D']
                for pr in pointer_pop:
                    self.out_stream.write(pr)
                    self.out_stream.write('\n')
            if segment == 'temp':
                temp_pop = ['@' + index, 'D=A', '@5', 'D=A+D', '@R14', 'M=D', '@SP'
                    , 'AM=M-1', 'D=M', '@R14', 'A=M', 'M=D']
                for tem in temp_pop:
                    self.out_stream.write(tem)
                    self.out_stream.write('\n')

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
