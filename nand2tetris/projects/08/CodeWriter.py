"""Translate VM commands into Hack assembly code"""

class CodeWriter:

    def __init__(self, out_file):
        self.root = out_file[:-4]
        self.out_file = open(out_file, "w")
        self.next_label = 0
        self.ret_address = 0 

    def write_bootstrap(self):
        trans = "" 
        trans = "//Boostrap code\n"
        trans += "@256\n"
        trans += "D=A\n"
        trans += "@SP\n"
        trans += "M=D\n"
        trans += "\n"
        self.out_file.write(trans)
        self.write_call('Sys.init', '0')

    def write_arithmetic(self, command):
        """Write the assembly code that is the translation of the given arithmetic command"""
        trans = ""
        trans += "// " + command + "\n"
        if command == "add":
            trans += "@SP\n" #Push first value of stack on D 
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "AM=M-1\n"
            trans += "M=D+M\n"
            trans += "@SP\n"
            trans += "M=M+1\n"
            trans += "\n"
        elif command == "sub":
            trans += "@SP\n"
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "AM=M-1\n"
            trans += "M=M-D\n"
            trans += "@SP\n"
            trans += "M=M+1\n"
            trans += "\n"
        elif command == "neg":
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=-M\n"
            trans += "\n"
        elif command == "eq":
            label = str(self.next_label)
            self.next_label += 1 
            trans += "@SP\n"
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "D=M-D\n"
            trans += "M=-1\n"
            trans += f"@eqTrue{label}\n"
            trans += "D;JEQ\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=0\n"
            trans += f"(eqTrue{label})\n"      
            trans += "\n"   
        elif command == "gt":
            label = str(self.next_label)
            self.next_label += 1 
            trans += "@SP\n"
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "D=M-D\n"
            trans += "M=-1\n"
            trans += f"@gtTrue{label}\n"
            trans += "D;JGT\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=0\n"
            trans += f"(gtTrue{label})\n"
            trans += "\n"
        elif command == "lt":
            label = str(self.next_label)
            self.next_label += 1 
            trans += "@SP\n"
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "D=M-D\n"
            trans += "M=-1\n"
            trans += f"@ltTrue{label}\n"
            trans += "D;JLT\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=0\n"
            trans += f"(ltTrue{label})\n"
            trans += "\n"
        elif command == "and":
            trans += "@SP\n"
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=D&M\n"
            trans += "\n"
        elif command == "or":
            trans += "@SP\n"
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=D|M\n"
            trans += "\n"
        elif command == "not":
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=!M\n"
            trans += "\n"
        else:
            trans = command + " not implemented yet\n"
        self.out_file.write(trans)


    def write_push_pop(self, command, segment, index):
        """Write the assembly code that is the translation of the given command (C_PUSH or C_POP)"""
        trans = ""
        if command == "push":
            trans += "// push " + segment + " " + index + "\n"
            if segment == "constant":
                trans += "@" + index + "\n" 
                trans += "D=A\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
                trans += "\n"
            elif segment == "local":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@LCL\n"
                trans += "A=M+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
                trans += "\n"
            elif segment == "this":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@THIS\n"
                trans += "A=M+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
                trans += "\n"
            elif segment == "that":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@THAT\n"
                trans += "A=M+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
                trans += "\n"
            elif segment == "argument":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@ARG\n"
                trans += "A=M+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
                trans += "\n"
            elif segment == "temp":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@R5\n"
                trans += "A=A+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
                trans += "\n"
            elif segment == "pointer":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@R3\n"
                trans += "A=A+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
                trans += "\n"
            elif segment == "static":
                trans += "@" + self.root + "." + index + "\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
                trans += "\n"
        elif command == "pop":
            trans += "// pop " + segment + " " + index + "\n"
            if segment == "argument":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@ARG\n"
                trans += "D=M+D\n"
                trans += "@R13\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "AM=M-1\n"
                trans += "D=M\n"
                trans += "@R13\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "\n"
            elif segment == "local":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@LCL\n"
                trans += "D=M+D\n"
                trans += "@R13\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "AM=M-1\n"
                trans += "D=M\n"
                trans += "@R13\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "\n"
            elif segment == "this":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@THIS\n"
                trans += "D=M+D\n"
                trans += "@R13\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "AM=M-1\n"
                trans += "D=M\n"
                trans += "@R13\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "\n"
            elif segment == "that":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@THAT\n"
                trans += "D=M+D\n"
                trans += "@R13\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "AM=M-1\n"
                trans += "D=M\n"
                trans += "@R13\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "\n"
            elif segment == "temp":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@5\n"
                trans += "D=D+A\n"
                trans += "@R13\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "AM=M-1\n"
                trans += "D=M\n"
                trans += "@R13\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "\n"
            elif segment == "static":
                trans += "@SP\n"
                trans += "AM=M-1\n"
                trans += "D=M\n"
                trans += "@" + self.root + "." + index + "\n"
                trans += "M=D\n"
                trans += "\n"
            elif segment == "pointer":
                trans += "@SP\n"
                trans += "AM=M-1\n"
                trans += "D=M\n"
                if index == "0":
                    trans += "@THIS\n"
                    trans += "M=D\n"
                elif index == "1":
                    trans += "@THAT\n"
                    trans += "M=D\n"
                trans += "\n"
        self.out_file.write(trans)

    def write_label(self, label):
        """Write assembly code that effects the label command"""
        trans = ""
        trans += "(" + label + ")" + "\n"
        trans += "\n"
        self.out_file.write(trans)


    def write_if(self, label):
        """Assembly code that effects the if-goto command"""
        trans = ""
        trans += "//if-goto label" + "\n"
        trans += "@SP\n"
        trans += "AM=M-1\n"
        trans += "D=M\n"
        trans += "@" + label + "\n"
        trans += "D;JNE\n"
        trans += "\n"
        self.out_file.write(trans)

    def write_goto(self, label):
        """Assembly code that effects the goto command"""
        trans = ""
        trans += "//goto label" + "\n"
        trans += "@SP\n"
        trans += "A=M-1\n"
        trans += "D=M\n"
        trans += "@" + label + "\n"
        trans += "D;JMP\n"
        trans += "\n"
        self.out_file.write(trans)

    def write_return(self):
        """Assembly code that effects the return command"""
        trans = ""
        trans += "//return\n"
        #FRAME = LCL 
        trans += "@LCL\n"
        trans += "D=M\n"
        trans += "@R13\n"
        trans += "M=D\n"
        #Return address = *(FRAME - 5)
        trans += "@5\n"
        trans += "D=A\n"
        trans += "@R13\n"
        trans += "A=M-D\n"
        trans += "D=M\n"
        trans += "@R14\n"
        trans += "M=D\n"
        #*ARG = pop()
        trans += "@SP\n"
        trans += "AM=M-1\n"
        trans += "D=M\n"
        trans += "@ARG\n"
        trans += "A=M\n"
        trans += "M=D\n"
        #SP = ARG + 1
        trans += "@1\n"
        trans += "D=A\n"
        trans += "@ARG\n"
        trans += "D=D+M\n"
        trans += "@SP\n"
        trans += "M=D\n"
        #THAT = *(FRAME - 1)
        trans += "@1\n"
        trans += "D=A\n"
        trans += "@R13\n"
        trans += "A=M-D\n"
        trans += "D=M\n"
        trans += "@4\n"
        trans += "M=D\n"
        #THIS = *(FRAME - 2)
        trans += "@2\n"
        trans += "D=A\n"
        trans += "@R13\n"
        trans += "A=M-D\n"
        trans += "D=M\n"
        trans += "@3\n"
        trans += "M=D\n"
        #ARG = *(FRAME - 3)
        trans += "@3\n"
        trans += "D=A\n"
        trans += "@R13\n"
        trans += "A=M-D\n"
        trans += "D=M\n"
        trans += "@2\n"
        trans += "M=D\n"
        #LCL = *(FRAME - 4)
        trans += "@4\n"
        trans += "D=A\n"
        trans += "@R13\n"
        trans += "A=M-D\n"
        trans += "D=M\n"
        trans += "@1\n"
        trans += "M=D\n"
        #goto RETURN ADDRESS
        trans += "@R14" + "\n"
        trans += "A=M\n"
        trans += "0;JMP\n"
        trans += "\n"
        self.next_label += 1
        self.out_file.write(trans)

    def write_function(self, function_name, num_locals):
        """Assembly code that effects the function command"""
        trans = ""
        trans += "//function " + function_name + " " + num_locals + "\n"
        trans += "(" + function_name + ")\n"
        self.out_file.write(trans)
        # self.out_file.write(trans)
        for i in range(int(num_locals)):
            self.write_push_pop('push', 'constant', '0')
            
            
    def write_call(self, function_name, num_args):
        """Assembly code that effects the call command"""
        trans = ""
        trans += "//call " + function_name + " " + num_args + "\n"
        #Push return-address  @FunctionName$Label
        trans += f"@{function_name}$ret{self.ret_address}\n"
        trans += "D=A\n"
        trans += "@SP\n"
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "M=M+1\n"
        #Push LCL
        trans += "@LCL\n"
        trans += "D=M\n"
        trans += "@SP\n"
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "M=M+1\n"
        #PUSH ARG
        trans += "@ARG\n"
        trans += "D=M\n"
        trans += "@SP\n"
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "M=M+1\n"
        #Push THIS 
        trans += "@THIS\n"
        trans += "D=M\n"
        trans += "@SP\n"
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "M=M+1\n"
        #Push THAT 
        trans += "@THAT\n"
        trans += "D=M\n"
        trans += "@SP\n"
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "M=M+1\n"
        #ARG = SP - n - 5 
        trans += "@SP\n"
        trans += "D=M\n"
        trans += "@5\n"
        trans += "D=D-A\n"
        trans += f"@{num_args}\n"
        trans += "D=D-A\n"
        trans += "@ARG\n"
        trans += "M=D\n"
        #LCL = SP
        trans += "@SP\n"
        trans += "D=M\n"
        trans += "@LCL\n"
        trans += "M=D\n"
        #Go to function name 
        trans += f"@{function_name}\n"
        trans += "0;JMP\n"
        trans += f"({function_name}$ret{self.ret_address})\n"
        trans += "\n"
        self.ret_address += 1 
        self.out_file.write(trans)

    def write_error(self):
        self.out_file.write("//There is no command like this.\n")
        self.out_file.write("\n")