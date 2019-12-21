from semantics_common import visit_tree, SymbolData, SemData
import syntax_tree_generation
import tree_print


# Define semantic check functions:

def check_literals(node, semdata):
    nodetype = node.nodetype
    if nodetype == 'NUMBER_LITERAL':
        if node.value > 10:
            return "Literal "+str(node.value)+" too large!"


def semantic_checks(tree, semdata):
    '''run all semantic checks'''
    visit_tree(tree, check_literals, None, semdata)


parser = syntax_tree_generation.parser

if __name__ == "__main__":
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file', help='filename to process')

    ns = arg_parser.parse_args()

    if ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open(ns.file, encoding='utf-8').read()
        ast_tree = parser.parse(data, lexer=syntax_tree_generation.lexer, debug=False)
        tree_print.treeprint(ast_tree)

        semdata = SemData()
        semdata.in_function = None
        semantic_checks(ast_tree, semdata)
        print("Semantics ok.")
