"""Symbol Table (ST): provide services for creating and using a symbol table
ST implements the abstraction by giving each symbol an index within the scope 
(Index start at 0, increments by 1 each time an identifier is added to the table,
then reset to 0 when starting a new scope"""
from Constant import * 

class SymbolTable:

    def __init__(self):
        """Create a new empty symbol table""" 
        self.class_symbols = {}
        self.subroutine_symbols = {}
        self._symbol_alloc = {SK_STATIC: self.class_symbols, SK_FIELD: self.class_symbols,
                            SK_ARG: self.subroutine_symbols, SK_VAR: self.subroutine_symbols}
        self.index = {SK_STATIC: 0, SK_FIELD: 0, SK_ARG: 0, SK_VAR: 0}

    def __str__(self):
        return self.helper('class', self.class_symbols) +\
                self.helper('subroutine', self.subroutine_symbols)


    def helper(self, name, table_symbol):
        result = 'Symbol table for ' + name + ':\n'
        for name, (_type, kind, index) in table_symbol.items(): 
            result += f'{name} | {_type} | {kind} | {index}\n'
        return result 

    def start_subroutine(self):
        """Start a new subroutine scope (i.e., reset the new subroutine's symbol table)"""
        self.subroutine_symbols.clear()
        self.index[SK_ARG] = self.index[SK_VAR] = 0 

    def define(self, name, _type, kind):
        """"Define a new identifer of a given name, type and kind (static/field/arg/var)
        and assigns it a running index."""
        self._symbol_alloc[kind][name] = (_type, kind, self.index[kind])
        self.index[kind] += 1  

    def var_count(self, kind):
        """Return the number of variables of the given kind already defined in the current scope"""
        count = 0
        for name, (_type, _kind, index) in self._symbol_alloc[kind].items():
            if _kind == kind:
                count += 1 
        return count 

    def type_of(self, name):
        """Return the type of the named identifer in the current scope"""
        (_type, kind, index) = self.current_scope(name)
        return _type 

    def kind_of(self, name):
        """Return the kind of the named identifier in the current scope.""" 
        (_type, kind, index) = self.current_scope(name)
        return kind  

    def index_of(self, name):
        """Return the index assigned to the name identifier"""
        (_type, kind, index) = self.current_scope(name)
        return index 

    def current_scope(self, name):
        if name in self.subroutine_symbols:
            return self.subroutine_symbols[name]
        elif name in self.class_symbols:
            return self.class_symbols[name]
        else:
            return (None, None, None)

        


