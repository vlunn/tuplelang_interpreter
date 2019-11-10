from lexerutilities import parse_into_tokens
import ply.yacc as yacc


def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


def analyze_syntax(tokens):

    # Build the parser
    parser = yacc.yacc()

    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)


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

        tokens = parse_into_tokens(data)
        analyze_syntax(tokens)


main()
