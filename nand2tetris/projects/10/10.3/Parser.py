""" This class will write all the xml output and compile it for 
each file in jack folder and then close it. """
import os 
import Lex, Constant 

class Parser:
    def __init__(self, file):
        self.lex = Lex.Lex(file)
        self.write_xml_output(file)
        self.compile_class()
        # self.close()

    def write_xml_output(self, path):
        out_dir = os.path.join(os.path.dirname(path), 'output')
        # print(out_dir)
        file = os.path.join(out_dir, os.path.basename(path))
        # print(file)
        try:
            os.mkdir(out_dir)
        except OSError as e:
            pass 
        self._outfile = open(file.replace('.jack', '.xml'), 'w') #Write XML later. 
        # print(self._outfile)
        self.lex.openout(file)

    def compile_class(self):
        self._start_non_terminal(Constant.KW_CLASS)
        


    def _start_non_terminal(self, rule):
        self._outfile.write(f'<{rule}>\n')









