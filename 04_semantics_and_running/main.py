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
    semdata.old_stacks = []
    semdata.stack = []
    return eval_node(tree, semdata)


def eval_plus(node, semdata):
    if node.value == '+':
        # Evaluate operands:
        for item in [node.children_operands[0], node.children_operands[1]]:
            status = eval_node(item, semdata)
            if status is not None:
                return status

        operand1, operand2 = node.children_operands[0], node.children_operands[1]

        # Operands must be of the same type:
        if isinstance(operand1.value, int) and isinstance(operand2.value, int) or \
                isinstance(operand1.value, str) and isinstance(operand2.value, str):
            # Replace TN_PLUS with the result of evaluation:
            sum = operand1.value + operand2.value
            node.value = sum
            semdata.stack.pop()
            semdata.stack.append(sum)  # defined for str and numbers

        else:
            return "Illegal PLUS-operation: operands must have same type!"
    else:
        return "Impossible plus statement! {}".format(node.value)


def eval_mult(node, semdata):
    if node.value == '*':
        for item in [node.children_operands[0], node.children_operands[1]]:
            status = eval_node(item, semdata)
            if status is not None:
                return status

        operand1, operand2 = node.children_operands[0], node.children_operands[1]

        # Multiplication only defined for numbers:
        if isinstance(operand1.value, int) and isinstance(operand2.value, int):
            result = operand1.value * operand2.value
            node.value = result
            semdata.stack.pop()
            semdata.stack.append(result)
        else:
            return "Illegal MULT-operation: operands must be numbers!"
    else:
        return "Impossible multiplication statement!".format(node.value)


def eval_div(node, semdata):
    if node.value == '/':
        for item in [node.children_operands[0], node.children_operands[1]]:
            status = eval_node(item, semdata)
            if status is not None:
                return status

        operand1, operand2 = node.children_operands[0], node.children_operands[1]

        # Division only defined for numbers:
        if isinstance(operand1.value, int) and isinstance(operand2.value, int):
            if operand2.value != 0:
                result = int(operand1.value / operand2.value)
                node.value = result
                semdata.stack.pop()
                semdata.stack.append(result)
            else:
                return "Illegal division by zero!"
        else:
            return "Illegal div-operation: operands must be numbers!"
    else:
        return "Impossible division statement!".format(node.value)


def eval_return(node, semdata):
    if node.value in ['=', '!=']:
        semdata.stack.append(node.child_expression)
        status = eval_node(node.child_expression, semdata)
        if status is not None:
            return status
        print_stack(semdata, "return")  # Debug
        return None
    else:
        return "Impossible return statement!"


def eval_program(node, semdata):
    # Copy and store current stack
    semdata.old_stacks.append(semdata.stack.copy())
    for i in node.children_stmts:
        status = eval_node(i, semdata)
        if status is not None:
            return status
    # Restore stack
    semdata.stack = semdata.old_stacks.pop()
    return None


def eval_atom(node, semdata):
    if not hasattr(node, "value"):
        eval_node(node.child_atom, semdata)
        node.value = node.child_atom.value
        node.child_atom = None  # Remove child
    elif node.value == '-':
        eval_node(node.child_atom, semdata)
        node.value = node.child_atom.value

        if node.child_atom.nodetype == 'TN_NUMBER_LITERAL':
            node.value = node.value * -1
        elif node.child_atom.nodetype == 'TN_STRING_LITERAL':
            return "Illegal operation: string literal sign assignment!"
        elif node.child_atom.nodetype == 'TN_varIDENT':
            pass  # TODO


# Store function pointers to node evaluation functions:
eval_funcs = {'TN_program': eval_program,
              'TN_return_value_stmt': eval_return,
              'TN_PLUS': eval_plus,
              'TN_MULT': eval_mult,
              'TN_DIV': eval_div,
              'TN_atom': eval_atom}


def eval_node(node, semdata):
    symtbl = semdata.symtbl
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
