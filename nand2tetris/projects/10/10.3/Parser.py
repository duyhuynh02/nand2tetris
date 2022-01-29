""" This class will write all the xml output and compile it for 
each file in jack folder and then close it. """
import os 
import Lex, Constant 
from xml.sax.saxutils import escape

class ParserError(Exception):
    def __init__(self, message):
        self.message = message 

class Parser:
    def __init__(self, file):
        self.lex = Lex.Lex(file)
        self.write_xml_output(file)
        self.compile_class()
        self.close_out()

    def write_xml_output(self, path):
        out_dir = os.path.join(os.path.dirname(path), 'output')
        file = os.path.join(out_dir, os.path.basename(path))
        try:
            os.mkdir(out_dir)
        except OSError as e:
            pass 
        self.lex.openout(file) #Write T_XML file 
        self._outfile = open(file.replace('.jack', '.xml'), 'w') #Write XML later. 

    def compile_class(self):
        #Main class method 
        self._start_non_terminal(Constant.KW_CLASS)
        self._require(Constant.T_KEYWORD, 'class') 
        self._require(Constant.T_ID)
        self._require(Constant.T_SYM, '{')

        while self._is_class_var_dec():
            self.compile_class_var_dec()

        while self._is_subroutine():
            self.compile_subroutine_dec()

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
        self._advance()
        self._compile_variable_declare()
        self._end_non_terminal('classVarDec')

    def _compile_variable_declare(self):
        self._compile_type()
        self._compile_variable_name()
        while self._is_token(Constant.T_SYM, ','):
            self._advance()
            self._compile_variable_name()

        self._require(Constant.T_SYM, ';')

    def _is_type(self):
        token, value = self.lex.peek()
        return ((token == Constant.T_KEYWORD)\
            and (value in [Constant.KW_INT, Constant.KW_BOOLEAN, Constant.KW_CHAR]))\
                or (token == Constant.T_ID)
        
    def _compile_type(self):
        return self._advance() if self._is_type() else "There is no such type variable"

    def _compile_variable_name(self):
        self._require(Constant.T_ID)

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
        self._require(Constant.T_ID)

    def _is_var_dec(self):
        return self._is_token(Constant.T_KEYWORD, Constant.KW_VAR)

    def _is_sameline_var(self):
        return self._is_token(Constant.T_SYM, ',')

    def _compile_subroutine_body(self):
        self._start_non_terminal('subroutineBody')
        self._advance()

        while self._is_var_dec():
            self._start_non_terminal('varDec')
            self._require(Constant.T_KEYWORD, 'var')
            self._compile_type()
            self._compile_variable_name()
            while self._is_sameline_var():
                self._require(Constant.T_SYM, ',')
                self._compile_variable_name()
            self._require(Constant.T_SYM, ';')
            self._end_non_terminal('varDec')

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
        self._start_non_terminal('ifStatement')
        self._require(Constant.T_KEYWORD, Constant.KW_IF)
        self._compile_condition_statement()
        self._end_non_terminal('ifStatement')

    def _compile_condition_statement(self):
        self._require(Constant.T_SYM, '(')
        self._compile_expression()
        self._require(Constant.T_SYM, ')')
        self._require(Constant.T_SYM, '{')
        self._compile_possible_statements()
        self._require(Constant.T_SYM, '}')
        if self._is_token(Constant.T_KEYWORD, Constant.KW_ELSE):
            self._advance()
            self._require(Constant.T_SYM, '{')
            self._compile_possible_statements()
            self._require(Constant.T_SYM, '}')

    def _compile_return_statement(self):
        self._start_non_terminal('returnStatement')
        self._require(Constant.T_KEYWORD, Constant.KW_RETURN)
        if self._is_token(Constant.T_ID) or self._is_kw_constant():
            self._compile_expression()
        self._require(Constant.T_SYM, ';')
        self._end_non_terminal('returnStatement')


    def _compile_do_statement(self):
        self._start_non_terminal('doStatement')
        self._require(Constant.T_KEYWORD, Constant.KW_DO)
        if self.is_variable_name():
            self._compile_variable_name()
            if self._is_token(Constant.T_SYM, '['):
                self._advance()
                self._compile_expression()
                self._require(Constant.T_SYM, ']')
            elif self._is_token(Constant.T_SYM, '.') or self._is_token(Constant.T_SYM, '('):
                self._compile_subroutine_call()
        self._require(Constant.T_SYM, ';')
        self._end_non_terminal('doStatement')


    def _compile_while_statement(self):
        self._start_non_terminal('whileStatement')
        self._require(Constant.T_KEYWORD, Constant.KW_WHILE)
        self._require(Constant.T_SYM, '(')
        self._compile_expression()
        self._require(Constant.T_SYM, ')')
        self._require(Constant.T_SYM, '{')
        self._compile_possible_statements()
        self._require(Constant.T_SYM, '}')
        self._end_non_terminal('whileStatement')

    def _compile_let_statement(self):
        self._start_non_terminal('letStatement')
        self._require(Constant.T_KEYWORD, Constant.KW_LET)
        self._compile_variable_name()
        if self._is_token(Constant.T_SYM, '['):            
            self._advance()
            self._compile_expression()
            self._require(Constant.T_SYM, ']')
        self._require(Constant.T_SYM, '=')
        self._compile_expression()
        self._require(Constant.T_SYM, ';')
        self._end_non_terminal('letStatement')

    def _compile_expression(self):
        if not self._is_term():
            return 
        self._start_non_terminal('expression')
        self._compile_term()
        while self._op_term():
            self._advance()
            self._compile_term()
        self._end_non_terminal('expression')


    def _compile_term(self):
        self._start_non_terminal('term')
        if self._is_integer() or self._is_string() or self._is_kw_constant():
            self._advance()
        elif self._is_token(Constant.T_SYM, '('):
            self._advance()
            self._compile_expression()
            self._require(Constant.T_SYM, ')')
        elif self._is_unary_op():
            self._advance()
            self._compile_term()
        elif self.is_variable_name():
            self._compile_variable_name()
            if self._is_token(Constant.T_SYM, '['):
                self._advance()
                self._compile_expression()
                self._require(Constant.T_SYM, ']')
            elif self._is_token(Constant.T_SYM, '.') or self._is_token(Constant.T_SYM, '('):
                self._compile_subroutine_call()

        self._end_non_terminal('term')

    def _op_term(self):
        token, value = self.lex.peek()
        return token == Constant.T_SYM and value in '+-*/&|<>='


    def _compile_method_call_name(self):
        self._require(Constant.T_ID)

    def _compile_subroutine_call(self):
        if self._is_token(Constant.T_SYM, '.'):
            self._advance()
            self._compile_method_call_name()
        self._require(Constant.T_SYM, '(')
        self._compile_expression_list()
        self._require(Constant.T_SYM, ')')

    def _compile_expression_list(self):
        self._start_non_terminal('expressionList')
        self._compile_expression()
        while self._is_token(Constant.T_SYM, ','):
            self._advance()
            self._compile_expression()
        self._end_non_terminal('expressionList')

    def _is_term(self):
        return self._is_string() or self._is_integer() or self.is_variable_name() or\
            self._is_kw_constant() or self._is_unary_op() or self._is_token(Constant.T_SYM, '(') 

    def _is_string(self):
        return self._is_token(Constant.T_STR)

    def _is_integer(self):
        return self._is_token(Constant.T_NUM)

    def is_variable_name(self):
        return self._is_token(Constant.T_ID)

    def _is_kw_constant(self):
        token, value = self.lex.peek()
        return (token == Constant.T_KEYWORD) and\
                    value in [Constant.KW_TRUE, Constant.KW_FALSE, Constant.KW_NULL, Constant.KW_THIS]

    def _is_unary_op(self):
        token, value = self.lex.peek()
        return (token == Constant.T_SYM) and value in '-~'

    def _compile_parameter_list(self):
        self._start_non_terminal('parameterList')
        # print(self.lex._tokens)
        if self._is_type():
            self._advance()
            self._compile_variable_name()
            while self._is_token(Constant.T_SYM, ','):
                self._require(Constant.T_SYM, ',')
                self._advance()
                self._compile_variable_name()
        self._end_non_terminal('parameterList')

    def compile_subroutine_dec(self):
        self._start_non_terminal('subroutineDec')
        self._advance()
        self._compile_void_or_type()
        self._compile_subroutine_name()
        self._require(Constant.T_SYM, '(')
        self._compile_parameter_list()
        self._require(Constant.T_SYM, ')')
        self._compile_subroutine_body()
        self._end_non_terminal('subroutineDec')
