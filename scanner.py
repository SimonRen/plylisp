#scanner.py
# -*- coding: utf-8 -*-

import ply.lex as lex

tokens = (  #tokens元组定义了词法分析器可以产生的所有词法单元的类型
    'QUOTE',
    'LPAREN',
    'RPAREN',
    'INTEGER',
    'FLOAT',
    'STRING',
    'LAMBDA',
    'SYMBOL',
)

t_QUOTE = r'\''
t_LPAREN= r'\('  #词法单元的模式描述，可以采用正则表达式字符串
t_RPAREN= r'\)'
t_LAMBDA= r'lambda'

def t_FLOAT(t):    #若识别出词法单元时需要执行一些动作，可以使用函数
    r'\d+\.\d+'  #这种情况下，要把描述的正则表达式作为函数的doc
    t.value = float(t.value)    #t是LexToken类型，表示识别出的词法单元
    return t

def t_INTEGER(t):    #若识别出词法单元时需要执行一些动作，可以使用函数
    r'\d+'  #这种情况下，要把描述的正则表达式作为函数的doc
    t.value = long(t.value)    #t是LexToken类型，表示识别出的词法单元
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = unicode(t.value[1:-1], 'utf8')
    return t

def t_SYMBOL(t):
    r'[a-zA-Z_+-][a-zA-Z_0-9]*'
    return t

def t_newline(t):   #可以通过t_newline()规则来更新行号信息
    r'\n+'
    t.lineno += len(t.value)

##忽略符号
t_ignore = ' \t'

def t_error(t):     #当检测到非法字符时，t_error()用于处理词法错误
    print "Illegal character '%s'" %t.value[0]
    t.lexer.skip(1)

'''通过调用ply.lex.lex()可以构建词法分析器，这个函数通过python的反射
机制读取调用函数的全局环境以获取所有的规则字符串，然后生成词法分析器'''   
lex.lex()

data = '''
(print "sdfsdf")
'''

lex.input(data)

while True:
    tok = lex.token()
    if not tok: break
    print tok

