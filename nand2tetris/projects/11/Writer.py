"""Output module for generating VM code
Release VM commands into a file, using the VM command syntax"""

class VMWriter:

    def __init__(self, file):
        """Creates a new file and prepares it for writing"""
        pass 

    def openout(self, file):
        self._vm_outfile = open(file.replace('.jack', '.vm'), 'w')

    def close_out(self):
        """"Close the output file"""
        self._vm_outfile.close()

    def write_push(self, segment, index):
        """"Write a VM push command
        Segment (Constant/Arg/Local/Static/This/That/Pointer/Temp"""
        self._vm_outfile.write('push ' + segment + ' ' + str(index) + '\n')

    def write_pop(self, segment, index):
        """"Write a VM pop command
        Segment (Constant/Arg/Local/Static/This/That/Pointer/Temp """
        self._vm_outfile.write('pop ' + segment + ' ' + str(index) + '\n')

    def write_arithmetic(self, command):
        """"Write a VM arithmetic command (Add/Sub/Neg/Eq/Gt/Lt/And/Or/Not)"""
        self._vm_outfile.write(command + '\n')

    def write_label(self, label):
        """"Write a VM label (String) command"""
        self._vm_outfile.write('label ' + 'label@' + str(label) + '\n')

    def write_goto(self, label):
        """"Write a VM goto command"""
        self._vm_outfile.write('goto ' + 'label@' + str(label) + '\n')

    def write_if(self, label):
        """"Write a VM if-goto command"""
        self._vm_outfile.write('if-goto ' + 'label@' + str(label) + '\n') 

    def write_call(self, name, nArgs):
        """"Write a VM call command"""
        self._vm_outfile.write('call ' + name + ' ' + str(nArgs) + '\n')      

    def write_function(self, name, nlocals):
        """"Write a VM function command"""
        self._vm_outfile.write('function ' + name + ' ' + str(nlocals) + '\n')
          
    def write_return(self):
        """"Write a VM return command"""
        self._vm_outfile.write('return\n')