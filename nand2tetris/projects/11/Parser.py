""" This class will write all the xml output and compile it for 
each file in jack folder and then close it. """
import os 
import Lex, Constant 
from SymbolTable import * 
from xml.sax.saxutils import escape
from Writer import * 

class ParserError(Exception):
    def __init__(self, message):
        self.message = message 

class Parser:
    def __init__(self, file):
        self.count = 0 
        self.lex = Lex.Lex(file)
        self.vm = VMWriter(file)
        self.write_xml_output(file)
        self.symbols = SymbolTable()
        self.compile_class()
        self.close_out()

    def write_xml_output(self, path):
        out_dir = os.path.join(os.path.dirname(path), 'output')
        file = os.path.join(out_dir, os.path.basename(path))
        try:
            os.mkdir(out_dir)
        except OSError as e:
            pass 
        self.vm.openout(file)
        self.lex.openout(file) #Write T_XML file 
        self._outfile = open(file.replace('.jack', '.xml'), 'w') #Write XML later. 

    def compile_class(self):
        #Main class method 
        self._start_non_terminal(Constant.KW_CLASS)     
        self._require(Constant.T_KEYWORD, 'class')      #Class 
        self.class_name = self._compile_variable_name() #Name 
        self._require(Constant.T_SYM, '{')              # { 

        while self._is_class_var_dec():     
            self.compile_class_var_dec()

        while self._is_subroutine():
            self.compile_subroutine_dec(self.class_name)
            # print(self.symbols)                 #For testing purpose
            
        self._require(Constant.T_SYM, '}')
        self._end_non_terminal(Constant.KW_CLASS)

    def close_out(self):
        self.lex.close_out()
        self._outfile.close()

    def _is_class_var_dec(self):
        token, value = self.lex.peek()
        return (token == Constant.T_KEYWORD) and\
                        ((value == Constant.KW_STATIC) or (value == Constant.KW_FIELD))

    def compile_class_var_dec(self):
        """ Compile class variable declaration """
        self._start_non_terminal('classVarDec')
        self._compile_variable_declare()
        self._end_non_terminal('classVarDec')

    def _compile_variable_declare(self):
        kind = None 
        if self._is_class_var_dec():
            token, value = self._advance()
            if value == Constant.KW_STATIC:
                kind = Constant.SK_STATIC
            elif value == Constant.KW_FIELD:
                kind = Constant.SK_FIELD

        if self._is_type():
            token, _type = self._compile_type() 

        token, name = self._advance()
        #Define for symbol table 
        self.symbols.define(name, _type, kind)
        while self._is_token(Constant.T_SYM, ','):
            self._advance()
            token, name = self._advance()
            self.symbols.define(name, _type, kind)

        # print(self.symbols)
        self._require(Constant.T_SYM, ';')

    def _is_type(self):
        token, value = self.lex.peek()
        return ((token == Constant.T_KEYWORD)\
            and (value in [Constant.KW_INT, Constant.KW_BOOLEAN, Constant.KW_CHAR]))\
                or (token == Constant.T_ID)
        
    def _compile_type(self):
        return self._advance() if self._is_type() else "There is no such type variable"

    def _compile_variable_name(self):
        return self._require(Constant.T_ID)

    def _start_non_terminal(self, rule):
        self._outfile.write(f'<{rule}>\n')

    def _end_non_terminal(self, rule):
        self._outfile.write(f'</{rule}>\n')

    def _is_token(self, token, value=None):
        lex_token, lex_value = self.lex.peek()
        if value == None:
            return lex_token == token
        return (lex_token, lex_value) == (token, value)

    def _require(self, token, value=None):
        lex_token, lex_value = self._advance()
        if (token != lex_token) or\
                (token in [Constant.T_SYM, Constant.T_KEYWORD] and value != lex_value):
            raise ParserError(self._require_failed_msg(token, value))
        return lex_value 

    def _require_failed_msg(self, token, value):
        if value == None: 
            value = token 
        return 'Expected ' + str(value)

    def _advance(self):
        token, value = self.lex.advance()
        self._write_terminal(token, value)
        return token, value 

    def _write_terminal(self, token, value):
        self._outfile.write('<' + Constant.tokens[token] + '> ' + escape(value)\
                                + ' </' + Constant.tokens[token] + '>\n')

    def _is_subroutine(self):
        token, value = self.lex.peek()
        return (token == Constant.T_KEYWORD) and ((value == Constant.KW_METHOD) or\
                                        (value == Constant.KW_FUNCTION) or\
                                        (value == Constant.KW_CONSTRUCTOR))

    def _compile_void_or_type(self):
        token, value = self.lex.peek()
        if (token == Constant.T_KEYWORD and (value in [Constant.KW_VOID, Constant.KW_INT,\
                                    Constant.KW_BOOLEAN, Constant.KW_CHAR]))\
            or (token == Constant.T_ID):
            self._advance()
        else:
            print("Syntax error when compilling for type in subroutine")

    def _compile_subroutine_name(self):
        return self._require(Constant.T_ID)

    def _is_var_dec(self):
        return self._is_token(Constant.T_KEYWORD, Constant.KW_VAR)

    def _is_sameline_var(self):
        return self._is_token(Constant.T_SYM, ',')

    def _compile_subroutine_body(self, subroutine_name, procedure_type):
        kind = Constant.SK_VAR
        self._start_non_terminal('subroutineBody')
        self._advance()

        while self._is_var_dec():
            self._start_non_terminal('varDec')
            self._require(Constant.T_KEYWORD, 'var')
            token, _type = self._compile_type()
            var_name = self._compile_variable_name()
            self.symbols.define(var_name, _type, kind)
            while self._is_sameline_var():
                self._require(Constant.T_SYM, ',')
                var_name = self._compile_variable_name()
                self.symbols.define(var_name, _type, kind)
            self._require(Constant.T_SYM, ';')
            self._end_non_terminal('varDec')

        self.vm.write_function(self.class_name + '.' + subroutine_name,\
                                self.symbols.var_count(SK_VAR)) #1: function | not method 

        if procedure_type == 'constructor':
            self.vm.write_push('constant', self.symbols.var_count(SK_FIELD))
            self.vm.write_call('Memory.alloc', '1')
            self.vm.write_pop('pointer', '0')
        elif procedure_type == 'method':
            self.vm.write_push('argument', '0')
            self.vm.write_pop('pointer', '0')

        self._compile_possible_statements() 
        self._require(Constant.T_SYM, '}')
        self._end_non_terminal('subroutineBody')


    def _is_statement(self):
        return self._is_do() or self._is_while() or\
                    self._is_let() or self._is_if() or self._is_return()

    def _is_do(self):
        return self._is_token(Constant.T_KEYWORD, Constant.KW_DO)

    def _is_while(self):
        return self._is_token(Constant.T_KEYWORD, Constant.KW_WHILE)

    def _is_let(self):
        return self._is_token(Constant.T_KEYWORD, Constant.KW_LET)

    def _is_if(self):
        return self._is_token(Constant.T_KEYWORD, Constant.KW_IF)

    def _is_return(self):
        return self._is_token(Constant.T_KEYWORD, Constant.KW_RETURN)

    def _compile_possible_statements(self):
        self._start_non_terminal('statements')
        while self._is_statement():
            self._compile_statement()
        self._end_non_terminal('statements')


    def _compile_statement(self):
        token, value = self.lex.peek()
        if value == Constant.KW_LET:
            self._compile_let_statement()
        elif value == Constant.KW_WHILE:
            self._compile_while_statement()
        elif value == Constant.KW_DO:
            self._compile_do_statement()
        elif value == Constant.KW_RETURN:
            self._compile_return_statement()
        elif value == Constant.KW_IF:
            self._compile_if_statement()

    def _compile_if_statement(self):
        """
        'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """ 
        self._start_non_terminal('ifStatement')
        self._require(Constant.T_KEYWORD, Constant.KW_IF)
        end_label = self._create_new_label_helper()
        self._compile_condition_statement(end_label)
        if self._is_token(Constant.T_KEYWORD, Constant.KW_ELSE): 
            self._advance()                 
            self._require(Constant.T_SYM, '{')
            self._compile_possible_statements()    # Compile Statements 2 
            self._require(Constant.T_SYM, '}')
        self._end_non_terminal('ifStatement')
        self.vm.write_label(end_label)              # Label L2

    def _compile_while_statement(self):
        """  'while' '(' expression ')' '{' statements '} """
        self._start_non_terminal('whileStatement')
        start_label = self._create_new_label_helper()           #Label L1 
        self.vm.write_label(start_label)
        self._require(Constant.T_KEYWORD, Constant.KW_WHILE)    
        self._compile_condition_statement(start_label) #'(' expression ')' '{' statements '}'   
        self._end_non_terminal('whileStatement')


    def _create_new_label_helper(self):
        self.count += 1 
        return str(self.count)

    def _compile_condition_statement(self, new_label):   
        #'(' expression ')' '{' statements '}'                 
        self._require(Constant.T_SYM, '(')
        self._compile_expression()                      #Expression       | Expression 
        self._require(Constant.T_SYM, ')')
        self.vm.write_arithmetic('not')                 #Not                | Not 
        notif_label = self._create_new_label_helper()        
        self.vm.write_if(notif_label)                    #If-goto L2        | If-goto L1 
        self._require(Constant.T_SYM, '{')                              
        self._compile_possible_statements()             #Compile statement   | Compile_statements 1 
        self._require(Constant.T_SYM, '}')      
        self.vm.write_goto(new_label)                 #Goto-L1              |Goto L2 
        self.vm.write_label(notif_label)                #Label L2              | Label L1 


    
    def _compile_return_statement(self):
        """ 'return' expression? ';' 
        """
        void_type = True 
        self._start_non_terminal('returnStatement')
        self._require(Constant.T_KEYWORD, Constant.KW_RETURN)
        if self._is_integer() or self._is_token(Constant.T_ID) or self._is_kw_constant():
            self._compile_expression()
            void_type = False 
        # token, value = self.lex.peek()
        self._require(Constant.T_SYM, ';')
        self._end_non_terminal('returnStatement')
        if void_type:
            self.vm.write_push('constant', 0)
        self.vm.write_return()


    def _compile_do_statement(self):
        #doStatement: 'do' subroutineCall ';'
        self._start_non_terminal('doStatement')
        self._require(Constant.T_KEYWORD, Constant.KW_DO)
        identifier_name = self._require(Constant.T_ID)
        if self._is_token(Constant.T_SYM, '.') or self._is_token(Constant.T_SYM, '('):
            if self._is_token(Constant.T_SYM, '.'): 
                self._compile_subroutine_call(identifier_name)
            else: 
                self.vm.write_push('pointer', 0)
                method_call_name, nExpressions = self._method_and_args_helper(identifier_name)
                self.vm.write_call(self.class_name + '.'\
                                            + method_call_name, nExpressions + 1)  #On current object

        self._require(Constant.T_SYM, ';')
        self._end_non_terminal('doStatement')   #Class name | function name | nArgs 
        self.vm.write_pop('temp', '0')

    def _compile_term(self):
        """
        Constant
        Arg/Local/Static/This
        That/Pointer/Temp

        intergerConstant | stringConstant | keywordConstant | 
        varName | varName '[' expression ']' | subroutineCall |
        '(' expression ')' | unaryOp term 
        """
        self._start_non_terminal('term')
        if self._is_integer() or self._is_string() or self._is_kw_constant():
            # intergerConstant | stringConstant | keywordConstant |
            self._compile_constant()
        elif self._is_token(Constant.T_SYM, '('): 
            #'(' expression ')'   
            self._advance()
            self._compile_expression()
            self._require(Constant.T_SYM, ')')
        elif self._is_unary_op():          
            # "-" or "~" | unaryOp term  
            token, unary_op_value = self._advance()
            self._compile_term()
            self.vm.write_arithmetic(Constant.unary_symbols[unary_op_value])
        elif self._is_identifier_name():      
            #varName | varName '[' expression ']' | subroutineCall |
            identifier_name = self._compile_variable_name()
            if self._is_token(Constant.T_SYM, '['):
                #varName '[' expression ']'
                self.vm.write_push(Constant.segments[self.symbols.kind_of(identifier_name)],\
                                    self.symbols.index_of(identifier_name)) 
                self._advance()
                self._compile_expression()
                self._require(Constant.T_SYM, ']')
                self.vm.write_arithmetic('add')
                self.vm.write_pop('pointer', '1')
                self.vm.write_push('that', '0')
            elif self._is_token(Constant.T_SYM, '.') or self._is_token(Constant.T_SYM, '('):
                # subroutineCall
                self._compile_subroutine_call(identifier_name)
            else:
                #for any varName 
                self.vm.write_push(Constant.segments[self.symbols.kind_of(identifier_name)],\
                                    self.symbols.index_of(identifier_name))

        self._end_non_terminal('term')

    def _compile_subroutine_call(self, id_name):
        if self._is_token(Constant.T_SYM, '.'):
            if id_name in self.symbols.subroutine_symbols or\
                                id_name in self.symbols.class_symbols: 
                self.vm.write_push(Constant.segments[self.symbols.kind_of(id_name)],\
                                                self.symbols.index_of(id_name))
                method_call_name, nExpressions = self._method_and_args_helper(id_name)
                self.vm.write_call(self.symbols.type_of(id_name) + '.'\
                                    + method_call_name, nExpressions + 1) 
            else:
                method_call_name, nExpressions = self._method_and_args_helper(id_name)
                self.vm.write_call(id_name + '.' + method_call_name, nExpressions)  


    def _method_and_args_helper(self, identifier_name):
        """"subroutineName '(' expressionList ') | 
        (className | varName) '.' subroutineName '(' expressionList ')' """
        if self._is_token(Constant.T_SYM, '.'):
            self._advance()
            method_call_name = self._compile_method_call_name()
        else:
            method_call_name = identifier_name
        self._require(Constant.T_SYM, '(')
        nExpressions = self._compile_expression_list()
        self._require(Constant.T_SYM, ')')
        return method_call_name, nExpressions 

    def _compile_let_statement(self):
        """ 'let' varName ('[' expression ']'?) '=' expression ';'
        """
        isArray = False 
        self._start_non_terminal('letStatement')
        self._require(Constant.T_KEYWORD, Constant.KW_LET) #Let 
        var_name = self._compile_variable_name()    #keyword name: e.g., 'loop' 
        if self._is_token(Constant.T_SYM, '['): 
            isArray = True 
            self.vm.write_push(Constant.segments[self.symbols.kind_of(var_name)],\
                                            self.symbols.index_of(var_name)) 
            self._advance()                         #'['
            self._compile_expression()              #expression 2 
            self._require(Constant.T_SYM, ']')      #']'
            self.vm.write_arithmetic('add')
        self._require(Constant.T_SYM, '=')          # '='
        self._compile_expression()                  #Expression: in this case: true
        self._require(Constant.T_SYM, ';')
        self._end_non_terminal('letStatement')
        if not isArray: 
            self.vm.write_pop(Constant.segments[self.symbols.kind_of(var_name)],\
                                                self.symbols.index_of(var_name))
        else: 
            self._compile_sub_array()

    def _compile_sub_array(self):
        self.vm.write_pop('temp', '0')
        self.vm.write_pop('pointer', '1')
        self.vm.write_push('temp', '0')
        self.vm.write_pop('that', '0')


    def _compile_expression(self):
        """ term (op term)* """
        if not self._is_term():
            return              #no expression in this 
        self._start_non_terminal('expression')  
        self._compile_term()
        while self._op_term():
            token, operator = self._advance()
            self._compile_term()
            if operator == '*':
                self.vm.write_call('Math.multiply', '2')
            elif operator == '/':
                self.vm.write_call('Math.divide', '2')
            else: 
                self.vm.write_arithmetic(Constant.arithmetic_symbols[operator])
        self._end_non_terminal('expression')
        return True                    #at least one expression 

    def _compile_constant(self): 
        if self._is_integer():      #intergerConstant 
            token, int_value = self._advance()
            self.vm.write_push('constant', int_value) 
        elif self._is_string():         #stringConstant 
            token, str_value = self._advance()
            self.vm.write_push('constant', len(str_value))
            self.vm.write_call('String.new', '1')
            for c in str_value:
                self.vm.write_push('constant', ord(c)) 
                self.vm.write_call('String.appendChar', '2')
        elif self._is_kw_constant():   #true = -1 | false = 0 | null = 0 | this  #keywordConstant
            token, const_value = self._advance()
            if const_value == Constant.KW_TRUE:
                self.vm.write_push('constant', '1')
                self.vm.write_arithmetic('neg')
            elif const_value == Constant.KW_FALSE or const_value == Constant.KW_NULL:
                self.vm.write_push('constant', '0')
            elif const_value == Constant.KW_THIS:
                self.vm.write_push('pointer', '0')

    def _op_term(self):
        token, value = self.lex.peek()
        return token == Constant.T_SYM and value in '+-*/&|<>='

    def _compile_method_call_name(self):
        return self._require(Constant.T_ID)

    def _compile_expression_list(self):
        """(expression(',' expression)*)? """
        self._start_non_terminal('expressionList')
        if not self._compile_expression():
            count = 0
        else: 
            count = 1 

        while self._is_token(Constant.T_SYM, ','):
            count += 1 
            self._advance()
            self._compile_expression()
        self._end_non_terminal('expressionList')
        return count 

    def _is_term(self):
        return self._is_string() or self._is_integer() or self._is_identifier_name() or\
            self._is_kw_constant() or self._is_unary_op() or self._is_token(Constant.T_SYM, '(') 

    def _is_string(self):
        return self._is_token(Constant.T_STR)

    def _is_integer(self):
        return self._is_token(Constant.T_NUM)

    def _is_identifier_name(self):
        return self._is_token(Constant.T_ID)

    def _is_kw_constant(self):
        token, value = self.lex.peek()
        return (token == Constant.T_KEYWORD) and\
                    value in [Constant.KW_TRUE, Constant.KW_FALSE, Constant.KW_NULL, Constant.KW_THIS]

    def _is_unary_op(self):
        token, value = self.lex.peek()
        return (token == Constant.T_SYM) and value in '-~'

    def _compile_parameter_list(self, class_name_type, procedure_type):
        count = 0
        kind = Constant.SK_ARG      #SK_ARG = 2
        if procedure_type == 'method':
            self.symbols.define(Constant.KW_THIS, class_name_type, kind)
        self._start_non_terminal('parameterList')
        if self._is_type():
            token, _type = self._advance()      #TYPE = int 
            token, name = self._advance()       #Name = ax 
            self.symbols.define(name, _type, kind)  #(Ax, int, 2)
            while self._is_token(Constant.T_SYM, ','):
                self._require(Constant.T_SYM, ',')
                self._advance()
                token, name = self._advance()
                self.symbols.define(name, _type, kind)
        self._end_non_terminal('parameterList')
        return count 

    def compile_subroutine_dec(self, class_name):
        self.symbols.start_subroutine()
        self._start_non_terminal('subroutineDec')
        token, procedure_type = self._advance()
        self._compile_void_or_type()
        subroutine_name = self._compile_subroutine_name()
        self._require(Constant.T_SYM, '(')
        self._compile_parameter_list(class_name, procedure_type)
        self._require(Constant.T_SYM, ')')
        self._compile_subroutine_body(subroutine_name, procedure_type)
        self._end_non_terminal('subroutineDec')
