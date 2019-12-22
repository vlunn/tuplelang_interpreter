from semantics_common import SymbolData, SemData
import tree_print
import syntax_tree_generation
import semantics_check


def print_stack(semdata, opt=""):  # For debugging purposes
    print("Stack {}: ".format(opt))
    for item in semdata.stack:
        print(item)
    print()


def run_program(tree, semdata):
    semdata.stack = [None]
    return eval_node(tree, semdata)


def eval_operands(node, semdata):

    status = eval_node(node.children_operands[0], semdata)
    if status is not None:
        return status, None, None

    status = eval_node(node.children_operands[1], semdata)
    if status is not None:
        return status, None, None

    return status, node.children_operands[0], node.children_operands[1]


def eval_plus(node, semdata):
    if node.value == '+':
        status, operand1, operand2 = eval_operands(node, semdata)
        if status is not None:
            return status

        # Operands must be of the same type:
        if isinstance(operand1.value, int) and isinstance(operand2.value, int) or \
                isinstance(operand1.value, str) and isinstance(operand2.value, str):
            # Replace TN_PLUS with the result of evaluation:
            sum = operand1.value + operand2.value
            node.value = sum
            semdata.stack[0] = sum  # defined for str and numbers

        else:
            return "Illegal PLUS-operation: operands must have same type!"
    else:
        return "Impossible plus statement! {}".format(node.value)


def eval_mult(node, semdata):
    if node.value == '*':
        status, operand1, operand2 = eval_operands(node, semdata)
        if status is not None:
            return status

        # Multiplication only defined for numbers:
        if isinstance(operand1.value, int) and isinstance(operand2.value, int):
            result = operand1.value * operand2.value
            node.value = result
            semdata.stack [0] = result
        else:
            return "Illegal MULT-operation: operands must be numbers!"
    else:
        return "Impossible multiplication statement!".format(node.value)


def eval_div(node, semdata):
    if node.value == '/':
        status, operand1, operand2 = eval_operands(node, semdata)
        if status is not None:
            return status

        # Division only defined for numbers:
        if isinstance(operand1.value, int) and isinstance(operand2.value, int):
            if operand2.value != 0:
                result = int(operand1.value / operand2.value)
                node.value = result
                semdata.stack[0] = result
            else:
                return "Illegal division by zero!"
        else:
            return "Illegal div-operation: operands must be numbers!"
    else:
        return "Impossible division statement!".format(node.value)


def eval_return(node, semdata):
    if node.value in ['=', '!=']:
        semdata.stack[0] = node.child_expression
        status = eval_node(node.child_expression, semdata)
        if status is not None:
            return status
        print_stack(semdata, "return")  # Debug
    else:
        return "Impossible return statement!"


def eval_program(node, semdata):
    for i in node.children_stmts:
        status = eval_node(i, semdata)
        if status is not None:
            return status

    for key in semdata.symtbl.keys():  # Print symbol table, debugging-purpose
        print(key, ": ", semdata.symtbl[key])


def eval_atom(node, semdata):
    """
    TN_atom can contain: numlit, stringlit, varIDENT, constIDENT, fun_call, simple_expr or select.
    :param node:
    :param semdata:
    :return:
    """

    if hasattr(node, "child_atom") and hasattr(node.child_atom, "nodetype"):
        child_node_type = node.child_atom.nodetype
        signed = hasattr(node, "value")

        if child_node_type == 'TN_NUMBER_LITERAL':
            node.value = node.child_atom.value
            if signed:
                node.value = node.value * -1

        elif child_node_type == 'TN_STRING_LITERAL':
            node.value = node.child_atom.value
            if signed:
                return "Illegal operation: string literal sign assignment!"

        elif child_node_type in ['TN_varIDENT', 'TN_constIDENT']:  # Can contain only numeric data
            identifier = node.child_atom.value
            if identifier not in semdata.symtbl.keys():
                return "Error: Cannot access undefined variable!"

            node.value = semdata.symtbl[identifier].get_value()
            if node.value is not None:
                if signed and child_node_type == 'TN_varIDENT':
                    node.value = node.value * -1
                elif signed and child_node_type == 'TN_constIDENT':
                    return "Illegal operation: Cannot reassign constant!"
            else:
                print("DEBUG: {}:n {} value oli virheellisesti None; ".format(child_node_type, identifier))

        elif child_node_type in ['TN_PLUS', 'TN_MINUS', 'TN_DIV', 'TN_MULT']:
            status = eval_node(node.child_atom, semdata)
            if status is not None:
                return status
            node.value = node.child_atom.value
            if signed:
                node.value = node.value * -1


def eval_program_body(node, semdata):
    for i in node.children_defs:
        status = eval_node(i, semdata)
        if status is not None:
            return status


def eval_vardef_varID(node, semdata):
    """
    Child simple_expression can be:
    Child simple_expression can be: atom, PLUS, MINUS, DIV, MULT
    :param node:
    :param semdata:
    :return:
    """
    symtbl = semdata.symtbl

    if hasattr(node.child_expression, "nodetype"):
        child_node_type = node.child_expression.nodetype

        if child_node_type in ['TN_atom', 'TN_PLUS', 'TN_MINUS', 'TN_MULT', 'TN_DIV']:
            status = eval_funcs[child_node_type](node.child_expression, semdata)  # Evaluate variable expression
            if status is not None:
                return status
            symtbl[node.value].set_value(node.child_expression.value)


def eval_vardef_constID(node, semdata):
    pass


def eval_vardef_tupleID(node, semdata):
    pass


def eval_vardef_pipe(node, semdata):
    pass


# Store function pointers to node evaluation functions:
eval_funcs = {'TN_program': eval_program,
              'TN_definitions': eval_program_body,
              'TN_vardef_varID': eval_vardef_varID,
              'TN_vardef_constID': eval_vardef_constID,
              'TN_vardef_tupleID': eval_vardef_tupleID,
              'TN_vardef_pipe': eval_vardef_pipe,
              'TN_return_value_stmt': eval_return,
              'TN_PLUS': eval_plus,
              'TN_MULT': eval_mult,
              'TN_DIV': eval_div,
              'TN_atom': eval_atom}


def eval_node(node, semdata):
    nodetype = node.nodetype

    # Evaluate current node:
    if nodetype in eval_funcs.keys():
        status = eval_funcs[nodetype](node, semdata)
        if status is not None:
            return status


parser = syntax_tree_generation.parser

if __name__ == "__main__":
    import argparse, codecs

    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')

    ns = arg_parser.parse_args()

    if ns.who:
        # identify who wrote this
        print('263461 Vivian Lunnikivi')
    elif ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open(ns.file, encoding='utf-8').read()
        ast_tree = parser.parse(data, lexer=syntax_tree_generation.lexer, debug=False)

        semdata = SemData()
        semdata.in_function = None
        semantics_check.semantic_checks(ast_tree, semdata)
        tree_print.treeprint(ast_tree)
        print("Semantics ok. Running the program...\n")

        status = run_program(ast_tree, semdata)
        if status is not None:
            print(status)
        else:
            print("Program finished.")
