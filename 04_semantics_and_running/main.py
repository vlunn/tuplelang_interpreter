from semantics_common import SymbolData, SemData
import tree_print
import syntax_tree_generation
import semantics_check


def eval_parameters(node, semdata):
    """TN_parameters"""
    if hasattr(node, 'children_params'):
        node.value = []
        for param_node in node.children_params:
            # Evaluate parameter node:
            status = eval_node(param_node, semdata)
            if status is not None:
                return status

            # Append the parameter node value to this node's value
            if isinstance(param_node.value, int):
                node.value.append(param_node.value)
            elif isinstance(param_node.value, list):
                node.value = node.value + param_node.value
            else:
                return "Illegal tuple parameter: {}, expected int or list!".format(node.children_params)
    else:
        return "Missing parameter list definition for node: {}!".format(node)


def eval_tuple_atom(node, semdata):
    """
    Has child_arg_list that is TN_parameters, which has children: params (n atoms)
    :param node:
    :param semdata:
    :return:
    """
    if hasattr(node, 'child_arg_list'):
        status = eval_parameters(node.child_arg_list, semdata)
        if status is not None:
            return status
        node.value = node.child_arg_list.value


def eval_tuple_expr(node, semdata):
    """ Evaluate tuple expression - that is, concatenating tuple atoms.
    :param node: Tuple expression tree node
    """
    if hasattr(node, 'children_args') and len(node.children_args) == 3:
        children = node.children_args

        # Evaluate 1st and 3rd child, aka. operands:
        concatenation_parts = []
        for child in [children[0], children[2]]:
            if child.nodetype == 'TN_tupleIDENT':
                identifier = child.value
                if identifier in semdata.symtbl.keys():
                    concatenation_parts.append(semdata.symtbl[identifier].get_value())
                else:
                    return "Error: cannot access undefined tuple variable: {}!".format(identifier)
            else:
                status = eval_funcs[child.nodetype](child, semdata)
                if status is not None:
                    return status
                concatenation_parts.append(child.value)

        # Concatenate tuples and save the value in this parent node:
        node.value = concatenation_parts[0] + concatenation_parts[1]

    else:
        return "Illegal tuple expression!"


def eval_doubledot(node, semdata):
    """ Operation creates a list containing a range of numbers starting
        from the given lower bound, ending up at the given upper bound."""
    lower = node.children_operands[0].value
    upper = node.children_operands[1].value
    node.value = [x for x in range(lower, upper+1)]


def eval_doublemult(node, semdata):
    """ Operation creates a list containing given element given amount of times."""
    multiplier = node.children_operands[0].value
    element = node.children_operands[1].value
    node.value = [element]*multiplier


def eval_operands(node, semdata):
    """
    Binary operations (PLUS, MINUS, MULT, DIV) have operands. This helper
    function evaluates the operands.
    :param node: binary operation node
    :param semdata:
    :return: status and the first and second evaluated operand.
    """
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
            return "Illegal PLUS-operation: operands must have the same type!"
    else:
        return "Impossible plus statement! {}".format(node.value)


def eval_minus(node, semdata):
    if node.value == '-':
        status, operand1, operand2 = eval_operands(node, semdata)
        if status is not None:
            return status

        # Operands must be of the same type, minus only defined for numbers:
        if isinstance(operand1.value, int) and isinstance(operand2.value, int):
            # Replace TN_MINUS with the result of evaluation:
            difference = operand1.value - operand2.value
            node.value = difference
            semdata.stack[0] = difference  # defined for str and numbers

        else:
            return "Illegal MINUS-operation: operands must have the same type!"
    else:
        return "Impossible minus statement! {}".format(node.value)


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
            return "Illegal MULT-operation: both operands must be numbers!"
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
            return "Illegal div-operation: both operands must be numbers!"
    else:
        return "Impossible division statement!".format(node.value)


def eval_atom(node, semdata):
    """ Evaluates an atom node.

    Atom node can contain a:
      - number literal,
      - string literal,
      - variable or
      - binary operation node
    as it's child. The child is evaluated according to the
    semantic rules and it's value is saved in the atom node's
    value attribute. There are multiple semantic checks here.

    Note: constants, function calls, simple_expressions or
    tuple select are also possible atom child nodes according
    to the syntax rules, but they have not been implemented yet.

    :param node: Atom type tree node.
    :param semdata: Semantic data containing a symbol table.
    :return: None if all goes well, error message otherwise.
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

        elif child_node_type in ['TN_varIDENT', 'TN_constIDENT']:
            identifier = node.child_atom.value
            if identifier not in semdata.symtbl.keys():
                return "Error: Cannot access undefined variable: {}!".format(identifier)
            # Fetch child value, which can only contain a number or None:
            node.value = semdata.symtbl[identifier].get_value()
            if node.value is not None:
                if signed and child_node_type == 'TN_varIDENT':
                    node.value = node.value * -1
                elif signed and child_node_type == 'TN_constIDENT':
                    return "Illegal operation: Cannot reassign constant!"

        elif child_node_type in ['TN_PLUS', 'TN_MINUS', 'TN_DIV', 'TN_MULT']:
            status = eval_node(node.child_atom, semdata)
            if status is not None:
                return status
            node.value = node.child_atom.value
            if signed:
                node.value = node.value * -1


def eval_vardef_varID(node, semdata):
    """ Evaluate variable definition node.
    Child simple_expression can be: an atom tree node
    or PLUS, MINUS, DIV or MULT operation.
    :param node:
    :param semdata:
    :return:
    """
    symtbl = semdata.symtbl

    if hasattr(node.child_expression, "nodetype"):
        child_node_type = node.child_expression.nodetype

        if child_node_type in ['TN_atom', 'TN_PLUS', 'TN_MINUS', 'TN_MULT', 'TN_DIV']:
            status = eval_funcs[child_node_type](node.child_expression, semdata)
            if status is not None:
                return status
            symtbl[node.value].set_value(node.child_expression.value)


def eval_vardef_tupleID(node, semdata):
    """ Evaluate tuple variable definition node.
    Child expression can be: TN_tuple_expr, TN_tuple_atom_args,
    TN_DOUBLEDOT or TN_DOUBLEMULT.
    :param node: TN_vardef_tupleID tree node
    :param semdata:
    :return:
    """
    symtbl = semdata.symtbl

    if hasattr(node.child_expression, "nodetype"):
        child_node_type = node.child_expression.nodetype

        if child_node_type in ['TN_tuple_expr', 'TN_tuple_atom_args',
                               'TN_DOUBLEDOT', 'TN_DOUBLEMULT']:
            status = eval_funcs[child_node_type](node.child_expression, semdata)
            if status is not None:
                return status
            symtbl[node.value].set_value(node.child_expression.value)


def eval_return(node, semdata):
    """Evaluate return tree node"""

    if node.value in ['=', '!=']:
        # Evaluate return value statement:
        status = eval_node(node.child_expression, semdata)
        if status is not None:
            return status

        # Print out the program return value:
        child = node.child_expression
        if child.nodetype in ['TN_atom', 'TN_PLUS', 'TN_MINUS',
                              'TN_MULT', 'TN_DIV', 'TN_tuple_expr']:
            retval = child.value
        else:
            retval = semdata.symtbl[child.value].get_value()
        print("Program result: ", retval, sep="")

    else:
        return "Impossible return statement!"


def eval_children(node, semdata):
    """Evaluate node's children statements"""

    for i in node.children_stmts:
        status = eval_node(i, semdata)
        if status is not None:
            return status


# Store function pointers to node evaluation functions:
eval_funcs = {'TN_program': eval_children,
              'TN_definitions': eval_children,
              'TN_vardef_varID': eval_vardef_varID,
              'TN_vardef_tupleID': eval_vardef_tupleID,
              'TN_return_value_stmt': eval_return,
              'TN_PLUS': eval_plus,
              'TN_MINUS': eval_minus,
              'TN_MULT': eval_mult,
              'TN_DIV': eval_div,
              'TN_atom': eval_atom,
              'TN_tuple_atom_args': eval_tuple_atom,
              'TN_tuple_expr': eval_tuple_expr,
              'TN_DOUBLEDOT' : eval_doubledot,
              'TN_DOUBLEMULT': eval_doublemult}


def eval_node(node, semdata):
    node_type = node.nodetype

    # Evaluate current node:
    if node_type in eval_funcs.keys():
        status = eval_funcs[node_type](node, semdata)
        if status is not None:
            return status


def run_program(tree, semdata):
    """ Starting point to evaluating the syntax tree.
    Effectively, runs the program.
    :param tree: Syntax tree
    :param semdata: Semantic data, containing a symbol table.
    :return: None if all goes well, error message otherwise.
    """
    semdata.stack = [None]
    return eval_node(tree, semdata)


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
        print("Checking sematics...")
        semantics_check.semantic_checks(ast_tree, semdata)
        tree_print.treeprint(ast_tree)
        print("Semantics ok. Running the program...")

        status = run_program(ast_tree, semdata)
        if status is not None:
            print(status)
        else:
            print("Program finished.")
