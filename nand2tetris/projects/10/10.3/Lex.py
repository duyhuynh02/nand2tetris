""" This Lex class will parse all the files included and 
use regular expression to regconize the pattern """
import re 
import Constant 
from xml.sax.saxutils import escape 

class Lex:
    def __init__(self, file):
        infile = open(file, "r")
        self._lines = infile.read()
        self._tokens = self._tokenize(self._lines)
        self._token_type = Constant.T_ERROR
        self._current_value = 0

    def openout(self, file):
        self._lex_outfile = open(file.replace('.jack', 'T.xml'), 'w')
        self._lex_outfile.write('<tokens>\n')

    def close_out(self):
        self._lex_outfile.write('</tokens>\n')
        self._lex_outfile.close()

    def is_token_available(self):
        return self._tokens != []

    def advance(self):
        if self.is_token_available():
            self._token_type, self._current_value = self._tokens.pop(0)
        else:
            self._token_type, self._current_value = (Constant.T_ERROR, 0)
        self._write_Txml()
        return (self._token_type, self._current_value)

    def peek(self):
        if self.is_token_available():
            return self._tokens[0]
        return (Constant.T_ERROR, 0)

    def _write_Txml(self):
        token, value = self._token_type, self._current_value
        token_type = Constant.tokens[token]
        if token == 5:
            self._lex_outfile.write(f"<ERROR>")
        else:
            self._lex_outfile.write(f"<{token_type}> " + escape(value) + f" </{token_type}>\n")

    def _tokenize(self, lines):
        """Return all the token in each line"""
        result = []
        for word in self._split(self._remove_comments(lines)):
            result.append(self._token(word))
        return result 

    def _remove_comments(self, line):
        """Remove all the comment""" 
        _regex_comment = re.compile(r'//[^\n]*\n|/\*(.*?)\*/', re.MULTILINE|re.DOTALL)
        return _regex_comment.sub('', line)

    #All regular expression. 
    _keyword_re = '|'.join(Constant.keywords)
    _integer_re = r'\d+'
    _string_re = r'"[^"\n"]*"'
    _symbol_re = '[' + re.escape(Constant.symbols) + ']' 
    _identifier_re = r'[\w\_]+' 
    _word_re = re.compile(_keyword_re + '|' + _symbol_re + '|' + _identifier_re + '|'\
                            + _integer_re + '|' + _string_re)
    def _split(self, line):
        return self._word_re.findall(line)

    def _token(self, word):
        if self._is_keyword(word):
            return (Constant.T_KEYWORD, word)
        elif self._is_symbol(word):
            return ((Constant.T_SYM, word))
        elif self._is_num(word):
            return (Constant.T_NUM, word)
        elif self._is_string(word):
            return (Constant.T_STR, word[1:-2])
        elif self._is_identifier(word):
            return (Constant.T_ID, word)
        else:
            return (Constant.T_ERROR, word)

    def _is_match(self, pattern, string):
        return re.match(pattern, string) != None 

    def _is_keyword(self, word):
        return self._is_match(self._keyword_re, word)

    def _is_symbol(self, word):
        return self._is_match(self._symbol_re, word)

    def _is_num(self, word):
        return self._is_match(self._integer_re, word)

    def _is_string(self, word):
        return self._is_match(self._string_re, word)

    def _is_identifier(self, word):
        return self._is_match(self._identifier_re, word)