from lexerutilities import lexer, tokens
import tree_print
import ply.yacc as yacc


class TreeNode:

    def __init__(self, type, terminal=None):

        self.nodetype = type

        if terminal is not None:
            self.value = terminal


def p_program_simplest(p):
    '''program : return_value DOT'''
    p[0] = TreeNode("program")
    p[0].child_return_value = p[1]


def p_program(p):
    '''program : func_or_var_def return_value DOT'''
    p[0] = TreeNode("program")
    p[0].children_stmts = [p[1], p[2]]


def p_func_or_var_def(p):
    '''func_or_var_def : var_def
                       | function_definition'''
    p[0] = p[1]


def p_func_or_var_def_var_func_var(p):
    '''func_or_var_def : var_def func_or_var_def'''
    p[0] = TreeNode("variable_and_func_or_var_definition")
    p[0].children_stmts = [p[1], p[2]]


def p_func_or_var_def_func_func_var(p):
    '''func_or_var_def : function_definition func_or_var_def'''
    p[0] = TreeNode("function_and_func_or_var_definition")
    p[0].children_stmts = [p[1], p[2]]


def p_function_definition_argless_simple_body(p):
    '''function_definition : DEFINE funcIDENT LSQUARE RSQUARE \
                             BEGIN return_value DOT END DOT'''
    print("func_definition( ** {} ** )".format(p[2]))
    p[0] = TreeNode("function_definition_argless_simple", p[2])
    p[0].child_return_value = p[6]              # Return value only


def p_function_definition_argless(p):
    '''function_definition : DEFINE funcIDENT LSQUARE RSQUARE \
                             BEGIN variable_definitions return_value DOT \
                             END DOT'''
    print("func_definition( ** {} ** )".format(p[2]))
    p[0] = TreeNode("function_definition_argless", p[2])
    p[0].children_body_parts = [p[6], p[7]]     # vardefs and return value


def p_function_definition_args_simple_body(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE \
                             BEGIN return_value DOT END DOT'''
    print("func_definition( ** {} ** )".format(p[2]))
    p[0] = TreeNode("function_definition_args_simple", p[2])
    p[0].children_params = [p[4], p[7]]         # parameters and return value


def p_function_definition_args(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE \
                             BEGIN variable_definitions return_value DOT \
                             END DOT'''
    print("func_definition( ** {} ** )".format(p[2]))
    p[0] = TreeNode("function_definition_args", p[2])
    p[0].children_params = [p[4], p[7], p[8]]   # params, vardefs, retval


def p_variable_definition(p):
    '''variable_definitions : var_def'''
    p[0] = p[1]


def p_variable_definitions(p):
    '''variable_definitions : var_def variable_definitions'''
    p[0] = TreeNode("variable_definitions")
    p[0].children_vars = [p[1], p[2]]


def p_formal(p):
    '''formals : varIDENT'''
    p[0] = TreeNode("varIDENT", p[1])


def p_formals(p):   # TODO: testaa, että varIDENT resolvaa nodeksi
    '''formals : varIDENT COMMA formals'''
    p[0] = TreeNode("formals")
    terminal_node = TreeNode("varIDENT", p[1])
    p[0].children_vars = [terminal_node, p[3]]


def p_return_value_eq(p):
    '''return_value : EQ simple_expression'''
    p[0] = TreeNode("return_value_statement_eq")
    terminal_node = TreeNode("EQ", p[1])
    p[0].children_parts = [terminal_node, p[2]]


def p_return_value_not_eq(p):
    '''return_value : NOTEQ pipe_expression'''
    p[0] = TreeNode("return_value_statement_eq")
    terminal_node = TreeNode("NOTEQ", p[1])
    p[0].children_parts = [terminal_node, p[2]]


def p_var_def_variable(p):
    '''var_def : varIDENT LARROW simple_expression DOT'''
    print("variable_definition( ** {} ** )".format(p.slice[1].value))
    p[0] = TreeNode("variable_definition")
    terminal_node = TreeNode("varIDENT", p[1])
    p[0].children_args = [terminal_node, p[3]]


def p_var_def_constant(p):
    '''var_def : constIDENT LARROW constant_expression DOT'''
    print("constant_definition( ** {} ** )".format(p.slice[1].value))
    p[0] = TreeNode("variable_definition")
    terminal_node = TreeNode("constIDENT", p[1])
    p[0].children_args = [terminal_node, p[3]]


def p_var_def_tuple(p):
    '''var_def : tupleIDENT LARROW tuple_expression DOT'''
    print("tuplevariable_definition( ** {} ** )".format(p.slice[1].value))
    p[0] = TreeNode("variable_definition")
    terminal_node = TreeNode("tupleIDENT", p[1])
    p[0].children_args = [terminal_node, p[3]]


def p_var_def_pipe_expr(p):
    '''var_def : pipe_expression RARROW tupleIDENT DOT'''
    print(p.slice[1])
    p[0] = TreeNode("variable_definition")
    terminal_node = TreeNode("tupleIDENT", p[3])
    p[0].children_args = [p[3], terminal_node]   # Swap direction to always assign 2nd parameter to 1st arg


def p_constant_expression_const_id(p):
    '''constant_expression : constIDENT'''
    p[0] = TreeNode("constIDENT", p[1])


def p_constant_expression_num_lit(p):
    '''constant_expression : NUMBER_LITERAL'''
    p[0] = TreeNode("NUMBER_LITERAL", p[1])


def p_pipe_expression_tuple_expr(p):
    '''pipe_expression : tuple_expression'''
    p[0] = p[1]


def p_pipe_expression_tuple_chain(p):
    '''pipe_expression : tuple_expression PIPE pipe_operation'''
    p[0] = TreeNode("pipe_expression")
    p[0].children_args = [p[1], p[3]]


def p_pipe_expression_pipe_chain(p):
    '''pipe_expression : pipe_expression PIPE pipe_operation'''
    p[0] = TreeNode("pipe_expression")
    p[0].children_args = [p[1], p[3]]


def p_pipe_operation_func(p):
    '''pipe_operation : funcIDENT'''
    p[0] = TreeNode("funcIDENT", p[1])


def p_pipe_operation_mult(p):
    '''pipe_operation : MULT'''
    p[0] = TreeNode("MULT", p[1])


def p_pipe_operation_plus(p):
    '''pipe_operation : PLUS'''
    p[0] =  TreeNode("PLUS", p[1])


def p_pipe_operation_each(p):
    '''pipe_operation : each_statement'''
    p[0] = TreeNode("pipe_operation")
    p[0].child_operation = p[1]


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''
    p[0] = TreeNode("each_stmt", p[1])
    p[0].child_arg = p[3]


def p_tuple_expression_atom(p):
    '''tuple_expression : tuple_atom'''
    p[0] = p[1]


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom tuple_operation tuple_expression'''
    p[0] = TreeNode("tuple_expr")
    p[0].children_args = [p[1], p[2], p[3]]


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''
    p[0] = TreeNode("DOUBLEPLUS", p[1])


def p_tuple_atom_tuple_id(p):
    '''tuple_atom : tupleIDENT'''
    p[0] = TreeNode("tupleIDENT", p[1])


def p_tuple_atoms_function_call(p):
    '''tuple_atom : function_call'''
    p[0] = TreeNode("function_call")
    p[0].child_call = p[1]


def p_tuple_atoms_doublemult(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE'''
    p[0] = TreeNode("tuple_doublemult")
    p[0].value = "DOUBLEMULT"
    p[0].children_args = [p[2], p[4]]


def p_tuple_atoms_doubledot(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEDOT constant_expression RSQUARE'''
    p[0] = TreeNode("tuple_doubledot")
    p[0].value = "DOUBLEDOT"
    p[0].children_args = [p[2], p[4]]


def p_tuple_atoms_args(p):
    '''tuple_atom : LSQUARE arguments RSQUARE'''
    p[0] = TreeNode("tuple_atom_args")
    p[0].child_arg_list = p[2]


def p_function_call_paramless(p):
    '''function_call : funcIDENT LSQUARE RSQUARE'''
    print("function_call( ** {} ** )".format(p.slice[1].value))
    p[0] = TreeNode("function_call_parameterless")
    p[0].value = p[1]


def p_function_call_args(p):
    '''function_call : funcIDENT LSQUARE arguments RSQUARE'''
    print("function_call( ** {} ** )".format(p.slice[1].value))
    p[0] = TreeNode("function_call_with_args")
    p[0].value = p[1]
    p[0].child_args = p[3]


def p_argument(p):
    '''arguments : simple_expression'''
    p[0] = TreeNode("argument")
    p[0].child_argument = p[1]


def p_arguments(p):
    '''arguments : simple_expression COMMA arguments'''
    p[0] = TreeNode("argument")
    p[0].children_args = [p[1], p[3]]


def p_atom_literal_num(p):
    '''atom : NUMBER_LITERAL'''
    print("{}( ** {} ** )".format(p.slice[0], p.slice[1].value))
    p[0] = TreeNode("literal_num")
    p[0].value = p[1]


def p_atom_literal_str(p):
    '''atom : STRING_LITERAL'''
    print("{}( ** {} ** )".format(p.slice[0], p.slice[1].value))
    p[0] = TreeNode("literal_str")
    p[0].value = p[1]


def p_atom_literal_var_id(p):
    '''atom : varIDENT'''
    print("{}( ** {} ** )".format(p.slice[0], p.slice[1].value))
    p[0] = TreeNode("literal_varID")
    p[0].value = p[1]


def p_atom_literal_const_id(p):
    '''atom : constIDENT'''
    print("{}( ** {} ** )".format(p.slice[0], p.slice[1].value))
    p[0] = TreeNode("literal_constID")
    p[0].value = p[1]


def p_atom_func_call(p):
    '''atom : function_call'''
    print(p.slice[0])
    p[0] = p[1]


def p_atom_simple_expr(p):
    '''atom : LPAREN simple_expression RPAREN'''
    print(p.slice[0])
    p[0] = p[2]


def p_atom_tuple(p):
    '''atom : SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    print(p.slice[0])
    p[0] = TreeNode("assign_tuple_expr")
    p[0].children_parts = [p[3], p[5]]  # Note: Omits control characters, exist implicitly.


def p_factors_atom(p):
    '''factor : atom'''
    print(p.slice[0])
    p[0] = p[1]


def p_factors_minus_atom(p):
    '''factor : MINUS atom'''
    print(p.slice[0])
    p[0] = TreeNode("factor")
    p[0].children_parts = [p[1], p[2]]


def p_term(p):
    '''term : factor'''
    print(p.slice[0])
    p[0] = p[1]


def p_terms_mult(p):
    '''term : factor MULT term'''
    p[0] = p[2]
    p[0].value = "MULTIPLY"
    p[0].children_terms = [p[1], p[3]]


def p_terms_div(p):
    '''term : factor DIV term'''
    p[0] = p[2]
    p[0].value = "DIVIDE"
    p[0].children_terms = [p[1], p[3]]


def p_simple_expression(p):
    '''simple_expression : term'''
    print(p.slice[0])
    p[0] = p[1]


def p_simple_expression_plus(p):
    '''simple_expression : term PLUS simple_expression'''
    p[0] = p[2]
    p[0].value = "PLUS"
    p[0].children_terms = [p[1], p[3]]


def p_simple_expression_minus(p):
    '''simple_expression : term MINUS simple_expression'''
    p[0] = p[2]
    p[0].value = "MINUS"
    p[0].children_terms = [p[1], p[3]]


# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print("{}:Syntax Error (token:'{}')".format(p.lineno, p.value))
    raise SystemExit


# Build the parser
parser = yacc.yacc()


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
        result = parser.parse(data, lexer=lexer, debug=False)
        print("\n** SYNTAX TREE **\n")
        tree_print.treeprint(result, outformat)
