import ply.lex as lex
from ply.yacc import yacc


tokens = ('LBRACKET', 'RBRACKET', '')
t_LBRACKET = r'\['
t_RBRACKET = r'\]'


lexer = lex.lex()




