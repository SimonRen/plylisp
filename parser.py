#parser.py
# -*- coding: utf-8 -*-
 
import ply.yacc as yacc
 
from scanner import tokens
 

'''每个文法规则被描述为一个函数，这个函数的文档字符串描述了对应的
文法规则,函数体用来实现规则的语义动作,p[i]即词法分析器中的t.value'''

def if_exp(args):
    if (eval_exp(args[0])):
        return eval_exp(args[1])
    else:
        return eval_exp(args[2])

def def_exp(args):
    global_vars[args[0][1]] = eval_exp(args[1])

##global_vars = {
##        'print' : lambda xs: eval_exp(xs[0]),
##        '+' : lambda xs: reduce(lambda x,y:eval_exp(x)+eval_exp(y), xs),
##        '-' : lambda xs: reduce(lambda x,y:eval_exp(x)-eval_exp(y), xs),
##        '*' : lambda xs: reduce(lambda x,y:eval_exp(x)*eval_exp(y), xs),
##        '/' : lambda xs: reduce(lambda x,y:eval_exp(x)/eval_exp(y), xs),
##        'mul' : lambda xs: reduce(lambda x,y:eval_exp(x)*eval_exp(y), xs),
##        'div' : lambda xs: reduce(lambda x,y:eval_exp(x)/eval_exp(y), xs),
##        'if' : if_exp
##                 
##}

global_vars = {
        'print' : lambda xs: eval_exp(xs[0]),
        '+' : lambda xs: reduce(lambda x,y:eval_exp(x)+eval_exp(y), xs),
        '-' : lambda xs: reduce(lambda x,y:eval_exp(x)-eval_exp(y), xs),
        '*' : lambda xs: reduce(lambda x,y:eval_exp(x)*eval_exp(y), xs),
        '/' : lambda xs: reduce(lambda x,y:eval_exp(x)/eval_exp(y), xs),
        'mul' : lambda xs: reduce(lambda x,y:eval_exp(x)*eval_exp(y), xs),
        'div' : lambda xs: reduce(lambda x,y:eval_exp(x)/eval_exp(y), xs),
        'if' : if_exp,
        'def' : def_exp,
                 
}


def lisp_type(exp):
    return exp[0] 

def type_value(exp):
    return exp[1] 

def eval_exp(p):
    type = lisp_type(p)
    value = type_value(p)
    if type == 'quote':
        print p[1] 
        return p[1]
    elif type == 'integer':
        return p[1]
    elif type == 'float':
        return p[1]
    elif type == 'string':
        return p[1]
    elif type == 'symbol':
        print global_vars[type_value(p)]
        return global_vars[type_value(p)]
    elif type == 'list':
        p_fun = value[0]

        p_fun_type = lisp_type(p_fun)
        p_fun_value = type_value(p_fun)
        
        assert(lisp_type(p_fun) == 'symbol')

        args_value_list = []
        index = 0
        ##这尼玛就是传说中得延迟计算啊, 在这里先不计算参数
        for exp in value:
            if (index != 0):
                args_value_list.append(exp)
            index = index + 1
            
        print args_value_list
        eval_result = eval_exp(p_fun)
        e1 = eval_result(args_value_list)
        print e1
        return e1
    else:
        print 'the first thing is not a function' 
     

#def p_expression_lambda(p):
#    '''expression : LAMBDA explist explist'''
#
#    p[0] = ('lambda', p[2], p[3])

def p_expression_fun(p):
    '''expression : LPAREN explist RPAREN '''

    if p[2] == None:
        p[0] = ('list', [])
    else:
        p[0] = p[2]

def p_expression_list(p):
    '''expression : QUOTE expression '''
    p[0] = ('quote', p[2])

def p_expression_symbol(p):
    '''expression : SYMBOL'''
    p[0] = ('symbol', p[1])

def p_expression_integer(p):
    '''expression : INTEGER'''
    p[0] = ('integer', p[1])

def p_expression_float(p):
    '''expression : FLOAT'''
    p[0] = ('float', p[1])

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = ('string', p[1])
 
def p_error(p):
    print "Syntax error in line %d" %p.lineno
    yacc.errok()

def p_explist(p):
    '''explist : expression 
        | explist expression '''
    if len(p) < 3:
        p[0] = ('list', [p[1]])
    else:
        p[1][1].append(p[2])
        p[0] = p[1]

precedence = (
)
 
yacc.yacc()
 
if __name__ == '__main__':
    while True:
        expr = raw_input('>')
        #print expr
        resl = yacc.parse(expr)
        #print resl
        eval_exp(resl)
        
