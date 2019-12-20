import ply.lex as lex

# Reserved words:
reserved = {
    'define': 'DEFINE',
    'begin': 'BEGIN',
    'end': 'END',
    'each': 'EACH',
    'select': 'SELECT'
}

# List of token names:
tokens = [
    'LARROW',
    'RARROW',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'COMMA',
    'DOT',
    'PIPE',
    'DOUBLEPLUS',
    'DOUBLEMULT',
    'DOUBLEDOT',
    'COLON',
    'EQ',
    'NOTEQ',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'NUMBER_LITERAL',
    'STRING_LITERAL',
    'varIDENT',
    'constIDENT',
    'tupleIDENT',
    'funcIDENT'
] + list(reserved.values())

t_ignore = ' \t'        # Recognize whitespace as legal input, but ignore it

# Regular expressions for simple, one and two letter tokens:
t_LARROW = r'<-'
t_RARROW = r'->'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COMMA = r','
t_DOT = r'\.'
t_PIPE = r'\|'
t_DOUBLEPLUS = r'\+{2}'
t_DOUBLEMULT = r'\*{2}'
t_DOUBLEDOT = r'\.{2}'
t_COLON = r':'

t_EQ = r'='
t_NOTEQ = r'!='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'\/'


# Regular expressions for longer tokens:


def t_NUMBER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING_LITERAL(t):
    r'\"([^\"]*)\"'
    t.value = t.value[1:-1]
    return t


def t_varIDENT(t):
    r'[a-z]+[a-zA-Z0-9_]+'

    # Pick out reserved words - all of them match varIDENT form:
    if t.value in reserved.keys():
        t.type = reserved[t.value]

    return t


def t_COMMENT(t):
    r'{.*}'
    pass    # ignore comments


t_constIDENT = r'[A-Z]+'
t_tupleIDENT = r'<[a-z]+>'
t_funcIDENT = r'[A-Z][a-z0-9_]+'


# Keep track of line numbers:
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling:
def t_error(t):
    msg = "Illegal character '{}' at line {}".format(
        t.value[0], t.lexer.lineno)
    print(msg)
    raise Exception(msg)


lexer = lex.lex()
