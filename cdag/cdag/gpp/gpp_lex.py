import gpp.lex as lex
from gpp.lex import TOKEN
import re


# TODO:
#  - change number type to int & float
#  - include complex numbers
#  - check how to represent numbers

actions = ('names',
           'renames',
           'loads', #
           'inputs', #
           'outputs', #
           'reads', #
           'applies', #
           'starts',
           'divides', #
           'powers', #
           'maps', #
           'adds', #
           'multiplies', #
           'keeps', #
           'publishes', #
           'invokes', #
           'dequeues', #
           'queues', #
           'parallels', #
           'processes',
           'threads',
           'produces', #
           'consumes', #
           'uses', #
           'roots',
           'sets', #
           'brings',
           'calls',
           'waits', #
           'moves', #
           'resets', #
           'repeats',
           'executes', #
           'checks', #
           'evaluates',
           'computes',
           'defines',
           'compares',
           'loops',
           'returns', #
           'translates',
           'amplifies')

# @ for quantum actions
complements = ('with', 'where', 'as', 'if', 'else')
complements2 = ('at', 'qubit')

reserved = actions + complements + complements2

# .
element = ('period',)

# $
variables = ('dollar',)  # related to wildcard references ("variables")

# & |
addition = ('and', 'or')

# = (!=, ~=, <>, =!=) > (=>, >=) < (<=, =<)
comp_symbols = ('equal', 'notequal',
                'gt', 'gte', 'lt', 'lte', 'mod')

# _ ...
loop = ('underscore', 'dots')

ids = ('id',)

str = ('str',)

numeric = ('realnum',)

boolean = ('bool',)

num_repr = ('bin', 'hex')

numeric_expr = numeric + boolean + num_repr

parens = ('lparen', 'rparen')

brackets = ('lbracket', 'rbracket')

void = ('null', 'none', 'void')

attr_types = ('string', 'real', 'boolean', 'binary', 'hexadecimal', 'qubin') + void

# quantum to be used with @
# special = ('quantum',)

tokens = reserved + element + variables + addition\
         + loop + ids + str + comp_symbols + parens +\
         numeric_expr + brackets + attr_types

t_ignore = ' \t\n;,'
t_ignore_comment = r'(\#\#.*\#\#|\/\*.*\*\/|\/\/.*\/\/|--.*--)'

# : for subjects
literals = [':']

t_period = r'\.'
t_dollar = r'\$'
t_and = r'\&'
t_or = r'\|'
t_dots = r'\.\.\.'
t_underscore = r'\_'
t_at = r'\@'
t_str = r'(?V1)(\".*?\"|«.*?»|„.*?“|\'.*?\')'

t_notequal = r'(!=|~=|<>|=!=)'
t_equal = r'(=|==)'
t_gt = r'>'
t_lt = r'<'
t_gte = r'(>=|=>)'
t_lte = r'(<=|=<)'
t_mod = r'%'


def t_lbracket(t):
    r'\[|「|『'
    return t


def t_rbracket(t):
    r'\]|」|』'
    return t


t_lparen = r'\(|（'
t_rparen = r'\)|）'


def t_colon(t):
    r'\:'
    t.type = ':'
    return t


id_regex = r'(?V1)(?![\"\'\[\]\s\&\d\:@!<>=~\|_\.\-\+«»„“「」『』（）])[[\w*]--[@\s\:\&\'\"\|!<>=~\.\+«»„“「」『』\[\]\(\)_]]+'


@TOKEN(id_regex)
def t_id(t):
    if t.value in reserved:
        t.type = t.value
    else:
        t.type = 'id'
    return t


bool2 = r'^(true|false)$'
bool_vals = ('true', 'false')

@TOKEN(bool2)
def t_bool(t):
    return bool(t)


@TOKEN(bool2)
def t_bin(t):
    r'^0b[0-1]+'
    return t


def t_hex(t):
    r'^0x[a-fA-F0-9]+'
    return t


new_real = r'(?V1)((?!(0[xb]))[+-]?(\d+([.]{1}\d+)?([eE][+-]+(\d+([.]{1}\d*)?))?|[.]{1}\d+([eE][+-]+(\d+([.]{1}\d+)?))))'


@TOKEN(new_real)
def t_realnum(t):
    try:
        t.value = int(t.value)
    except:
        t.value = float(t.value)
    finally:
        return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex(reflags=re.UNICODE | re.VERBOSE)
