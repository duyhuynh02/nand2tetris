import sys 
import os 
from code import comp, dest, jump

#1. Parse the symbolic command into its underlying fields (Parser module)
root = sys.argv[1]

def a_instruction(line):
    a_value = int(line[1:])
    b_value = bin(a_value)[2:].zfill(16)
    return str(b_value)

def c_instruction(line):
    """
        If dest is empty, the "=" is omitted;
        If jump is empty, the ";" is omitted; 
    """
    empty_dest = []
    empty_jump = []
    if "=" not in line:
        for element in line.split(";"):
            empty_jump.append(element.strip())
        dest_val = 'null'
        comp_val = empty_jump[0]
        jump_val = empty_jump[1]
    elif ";" not in line:
        for element in line.split("="):
            empty_dest.append(element.strip())
        dest_val = empty_dest[0]
        comp_val = empty_dest[1]
        jump_val = 'null'
    else:
        c_instruct = line.split("=")
        dest_val = c_instruct[0] 
        dj_instruct = c_instruct[1].split(";")
        comp_val = dj_instruct[0]
        jump_val = dj_instruct[1]
    return comp[comp_val], dest[dest_val], jump[jump_val]


def translate(line):
    """Define it is an A-instruction or C-instruction."""
    if line[0] == '@':
        return a_instruction(line)
    else:
        code = c_instruction(line)
        return '111' + code[0] + code[1] + code[2]


def parse():
    """Open an .asm file and parse it to .tmp file then close it."""
    asm_file = open(root + '.asm')
    tmp_file = open(root + '.tmp', 'w')

    for line in asm_file:
        strip_line = line.strip()
        if strip_line != "":
            if strip_line[0] != '/':
                tmp_file.write(strip_line + '\n')

    asm_file.close()
    tmp_file.close()

def assemble():
    """Open an .tmp file and write it in binary instruction to .hack file then close it"""
    tmp_file = open(root + '.tmp')
    hack_file = open(root + '.hack', 'w')

    for line in tmp_file:
        bi_line = translate(line)
        hack_file.write(bi_line + '\n')

    tmp_file.close()
    hack_file.close()
    os.remove(root + '.tmp')

parse()
assemble()






