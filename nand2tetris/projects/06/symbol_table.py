""" Keeps a correspondence between symbolic labels and numeric addresses """
symbol_table = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN': 16384,
    'KBD': 24576
}

for i in range(0, 16):
    symbol_table[f'R{i}'] = i 

