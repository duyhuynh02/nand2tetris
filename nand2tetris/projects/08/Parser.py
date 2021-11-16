import sys 
from CodeWriter import CodeWriter


class Parser:
    """Read VM commands, parse them, and provide convenient access to their components"""

    def __init__(self, in_file):
        """Open and clean .vm file"""
        f = open(in_file)
        self.commands = f.readlines()
        f.close() 
        """Clean file"""
        self.commands = [com.split('//')[0] for com in self.commands]
        self.commands = [com.strip() for com in self.commands]
        self.commands = self._trim_lines()

        """Track current line"""
        self.command_index = -1 
        self.current_command = None 

        """C_TYPE"""
        self.c_type = {
            'sub': 'math',
            'add': 'math',
            'neg': 'math',
            'eq': 'math',
            'gt': 'math',
            'lt': 'math',
            'and': 'math',
            'or': 'math',
            'not': 'math',
            'push': 'push',
            'pop': 'pop',
            'label': 'label',
            'if-goto': 'if-goto',
            'goto': 'goto',
            'function': 'function',
            'call': 'call',
            'return': 'return',
        }

    def _trim_lines(self):
        """Clean all the comment and blank lines"""
        temp_commands = []
        for com in self.commands:
            if com != "":
                temp_commands.append(com)
        return temp_commands


    def has_more_commands(self):
        """Are there more commands in the input"""
        return self.command_index < len(self.commands) - 1
        

    def advance(self):
        """Read the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true. Initially there is
        no current command""" 
        if self.has_more_commands:
            self.command_index += 1 
            self.current_command = self.commands[self.command_index].split(' ')


    def command_type(self):
        """Return the type of the current VM command
        C_ARITHMETIC is returned for all the arithmetic commands"""
        return self.c_type.get(self.current_command[0], "invalid cType.")

    def arg1(self):
        """Return the first argument of the current command. 
        In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is returned.
        Should not be called if the current command is C_RETURN 
        """
        return self.current_command[1]

    def arg2(self):
        """"Return the second argument of the current command.
        Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL"""
        return self.current_command[2]

        
def main():
    root = sys.argv[1]
    parser = Parser(root + '.vm')
    writer = CodeWriter(root + '.asm')
    writer.write_bootstrap()

    while parser.has_more_commands():
        parser.advance()
        c_type = parser.command_type()
        if c_type == "push" or c_type == "pop":
            writer.write_push_pop(c_type, parser.arg1(), parser.arg2())
        elif c_type == "math":
            writer.write_arithmetic(parser.current_command[0])
        elif c_type == "label":
            writer.write_label(parser.arg1())
        elif c_type == "if-goto":
            writer.write_if(parser.arg1())
        elif c_type == "goto":
            writer.write_goto(parser.arg1())
        elif c_type == "call":
            writer.write_call(parser.arg1(), parser.arg2())
        elif c_type == "function":
            writer.write_function(parser.arg1(), parser.arg2())
        elif c_type == "return":
            writer.write_return()
        else:
            writer.write_error()


if __name__ == "__main__":
    main()
