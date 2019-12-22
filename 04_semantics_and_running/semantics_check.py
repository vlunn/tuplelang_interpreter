from semantics_common import visit_tree, SymbolData, SemData
import syntax_tree_generation
import tree_print


def add_symbol(node, symtbl):
    """ Add a new symbol into the symbol table.
    If identifier already exists, returns an error message.
    :param node: Reference to the corresponding AST Tree node.
    :param symtbl: Symbol table to modify.
    :return: None / error_message
    """
    identifier = node.value
    if identifier not in symtbl:
        symtbl[identifier] = SymbolData(node.nodetype[3:], node)
        return None  # Successful add.
    else:
        return "Illegal redefinition of an identifier: {}!".format(identifier)


def create_symbol_table(node, semdata):
    symtbl = semdata.symtbl
    id_ids = {"TN_vardef_": ["varID", "constID", "tupleID", "pipe"],
              "TN_fundef_": ["argless_bodyless", "argless_with_body",
                             "args_bodyless", "args_with_body"]}
    nodetype = node.nodetype

    if nodetype is not None:
        for id_id in id_ids.keys():

            # Check that nodetype is a recognized identifier type (var or func def):
            if nodetype.startswith(id_id):

                # Check what kind of a variable or function definition it is:
                if nodetype[len(id_id):] in id_ids[id_id]:
                    return add_symbol(node, symtbl)     # Try to add symbol to symbol table
                else:
                    return "Undefined type of identifier definition: {}!".format(node.nodetype)


def semantic_checks(tree, semdata):
    '''Run semantic checks

    Note: Some semantic checks are run during interpretation,
    since e.g. variable value expressions need to be evaluated
    before the values can be checked.
    '''

    # "Data collection phase":
    visit_tree(tree, create_symbol_table, None, semdata)


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
