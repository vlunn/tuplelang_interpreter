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
    'WHITESPACE',
    'COMMENT',
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
    'LT',
    'LTEQ',
    'GT',
    'GTEQ',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'MOD',
    'NUMBER_LITERAL',
    'STRING_LITERAL',
    'varIDENT',
    'constIDENT',
    'tupleIDENT',
    'funcIDENT'
] + list(reserved.values())

t_ignore = ' \t'        # Recognize whitespace as legal input, but ignore it
t_COMMENT = '{.*}'      # TODO: what about chained, nested or multi-line comments?

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
t_LT = r'<'
t_LTEQ = r'<='
t_GT = r'>'
t_GTEQ = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'\/'
t_MOD = r'%'


# Regular expressions for longer tokens:


def t_NUMBER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING_LITERAL(t):
    r'".+"'      # TODO: Consider this: +The fa-12n021t <"==cat sat1".. ...""" <:o|n:! Eg. 2 string literals on same row
    t.value = t.value[1:-1]
    return t


def t_varIDENT(t):
    r'[a-z]+[a-zA-Z0-9_]+'

    # Pick out reserved words - all of them match varIDENT form:
    if t.value in reserved.keys():
        t.type = reserved[t.value]

    return t


t_constIDENT = r'[A-Z]+'
t_tupleIDENT = r'<[a-z]+>'
t_funcIDENT = r'[A-Z][a-z0-9_]+'    # Note: FFo is not valid - precisely one capital letter in the beginning.


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


def main():
    import argparse, codecs

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')

    ns = parser.parse_args()
    if ns.who:
        # identify who wrote this
        print('263461 Vivian Lunnikivi')
    elif ns.file is None:
        # user didn't provide input filename
        parser.print_help()
    else:
        # using codecs to make sure we process unicode
        with codecs.open(ns.file, 'r', encoding='utf-8') as INFILE:
            # blindly read all to memory (what if that is a 42Gb file?)
            data = INFILE.read()

        lexer = lex.lex()

        try:
            lexer.input(data)

            while True:
                token = lexer.token()
                if token is None:
                    break
                print(token)

        except Exception:
            pass


main()
