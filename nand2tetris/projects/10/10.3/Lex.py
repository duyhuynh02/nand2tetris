""" This Lex class will parse all the files included and 
use regular expression to regconize the pattern """
import re 
import Constant 

class Lex:
    def __init__(self, file):
        infile = open(file, "r")
        self._lines = infile.read()
        # print(self._lines)
        self._tokens = self._tokenize(self._lines)
        # print(self._tokens)

    def _tokenize(self, lines):
        """Return all the token in each line"""
        result = []
        for word in self._split(self._remove_comments(lines)):
            # print(word)
            result.append(self._token(word))
        return result 

    def _remove_comments(self, line):
        """Remove all the comment""" 
        _regex_comment = re.compile(r'//(.)*|/\*\*(.)*\*/')
        return _regex_comment.sub('', line)


    _keyword_re = '|'.join(Constant.keywords)
    # print(_keyword_re)
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
            # print((Constant.T_KEYWORD, word))
            return (Constant.T_KEYWORD, word)
        elif self._is_symbol(word):
            # print((Constant.T_SYM, word))
            return ((Constant.T_SYM, word))
        elif self._is_num(word):
            # print((Constant.T_NUM, word))
            return (Constant.T_NUM, word)
        elif self._is_string(word):
            # print((Constant.T_STR, word))
            return (Constant.T_STR, word)
        elif self._is_identifier(word):
            print((Constant.T_ID, word))
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







