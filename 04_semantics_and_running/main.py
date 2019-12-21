from semantics_common import SymbolData, SemData
import tree_print
import syntax_tree_generation
import semantics_check


def run_program(tree, semdata):
    semdata.old_stacks = []
    semdata.stack = []
    eval_node(tree, semdata)


def eval_node(node, semdata):
    symtbl = semdata.symtbl
    nodetype = node.nodetype
    if nodetype == 'program':
        # Copy and store current stack
        semdata.old_stacks.append(semdata.stack.copy())
        for i in node.children_stmts:
            eval_node(i, semdata)
        # Restore stack
        semdata.stack = semdata.old_stacks.pop()
        return None


parser = syntax_tree_generation.parser

if __name__ == "__main__":
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')

    ns = arg_parser.parse_args()

    if ns.who:
        # identify who wrote this
        print( '263461 Vivian Lunnikivi' )
    elif ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        ast_tree = parser.parse(data, lexer=syntax_tree_generation.lexer, debug=False)

        semdata = SemData()
        semdata.in_function = None
        semantics_check.semantic_checks(ast_tree, semdata)
        tree_print.treeprint(ast_tree)
        print("Semantics ok.")
        run_program(ast_tree, semdata)
        print("Program finished.")
