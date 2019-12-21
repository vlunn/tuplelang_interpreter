import tree_print
import syntax_tree_generation

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--treetype', help='type of output tree (unicode/ascii/dot)')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()

    outformat="unicode"
    if ns.treetype:
      outformat = ns.treetype

    if ns.who == True:
        # identify who wrote this
        print( '263461 Vivian Lunnikivi' )
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = syntax_tree_generation.parser.parse(data, lexer=syntax_tree_generation.lexer, debug=False)
        print("\n** SYNTAX TREE **\n")
        tree_print.treeprint(result, outformat)
