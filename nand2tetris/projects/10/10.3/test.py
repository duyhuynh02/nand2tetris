import re, os 
import os
import Constant

"""OS module"""
# path = 'File.txt'

# basename = os.path.basename(path)
# print(basename)

"""pop() method"""
# a = [1, 3, 11, 131]

# b = a.pop()
# print(b) #131 

# c = a.pop(0)
# print(c) #1 

"""Regular Expression"""
# paragraph = "//Things get to move\nThen we assign this to somebody else.\n\
# This will get you free.\nFor the fucking stupid work.\nThis thing even\
#  not from your side.\n/**Fuck it or leave it, it depends on you.*/"

# _comment_re = re.compile(r'//[^\n]*\n|/\*(.*?)\*/')

# print(paragraph)
# print()
# print(_comment_re.sub('', paragraph))


# os.chdir('/Users/Huynh Minh Duy/Desktop/ex10/')

# for dirpath, dirnames, filenames in os.walk('/Users/Huynh Minh Duy/Desktop/ex10/10.3'):
#     print('Current path is: ', dirpath)
#     print('Folder is: ', dirnames)
#     print('File names are: ', filenames)

# str1 = 'Never believe someone\'s word when you are young. believe is a hardest thing\
#  if you want to become'

# str2 = str1.replace('believe', 'trust', 1)

# print(str1)
# print(str2)



# """Class declaration test"""
# class Human:

#     def __init__(self, name, age, job):
#         self.name = name 
#         self.age = age 
#         self.job = job

#     def work(self, salary=0):
#         self.salary = salary  

#     ot_time = 2000 
#     def overtime(self, money):
#         self.salary += money 
#         self.ot_time = self.ot_time + money 

# first_human = Human('Duy', 25, 'Software Engineer')
# first_human.work(10000)
# first_human.overtime(2000)
# print(first_human.ot_time)
# # first_human.salary
# print(Human.ot_time)

# a = 15 

# def change():
#     global a 
#     a = a + 5
#     print("Value of a inside a function: ", a)

# change()
# print("Outside a function: ", a)

symbols = '{}()[].,;+-*/&|<>=~'

_keyword_re = r'|'.join(Constant.keywords)
# print(_keyword_re)
_integer_re = r'\d+'
_string_re = r'"\w*"'
# _symbol_re = r'[{}()[].,;+-*/&|<>=~]' #Not sure about this - will come back later )
_symbol_re = '[' + re.escape(symbols) + ']' # [Add escape character for not alpha-numeric]
_identifier_re = r'[\w\_]+'
_word_re = re.compile(_keyword_re + '|' + _symbol_re + '|' + _identifier_re + '|'\
                        + _integer_re + '|' + _string_re)

# print(_word_re)

f = open("Main.jack", "r")

for line in f:
    a = _word_re.findall(line)
    print(a)