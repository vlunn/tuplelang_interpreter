from lexerutilities import lexer, tokens
import ply.yacc as yacc


class TreeNode:

    def __init__(self, type, terminal=None):

        self.nodetype = type

        if terminal is not None:
            self.value = terminal


def p_program_simplest(p):
    '''program : return_value DOT'''
    p[0] = TreeNode("TN_program")
    p[0].children_stmts = [p[1]]


def p_program_1(p):
    '''program : func_or_var_def return_value DOT'''
    p[0] = TreeNode("TN_program")
    p[0].children_stmts = [p[1], p[2]]


def p_program_2(p):
    '''program : program func_or_var_def return_value DOT'''
    p[0] = p[1]
    p[0].children_stmts.append(p[2])


def p_func_or_var_def_v(p):
    '''func_or_var_def : var_def'''
    p[0] = TreeNode("TN_definitions")
    p[0].children_defs = [p[1]]


def p_func_or_var_def_f(p):
    '''func_or_var_def : function_definition'''
    p[0] = TreeNode("TN_definitions")
    p[0].children_defs = [p[1]]


def p_func_or_var_def_and_var_def(p):
    '''func_or_var_def : func_or_var_def var_def'''
    p[0] = p[1]
    p[1].children_defs.append(p[2])


def p_func_or_var_def_func_def(p):
    '''func_or_var_def : func_or_var_def function_definition'''
    p[0] = p[1]
    p[1].children_defs.append(p[2])


def p_function_definition_argless_bodyless(p):
    '''function_definition : DEFINE funcIDENT LSQUARE RSQUARE \
                             BEGIN return_value DOT END DOT'''
    p[0] = TreeNode("TN_fundef_argless_bodyless", p[2])
    p[0].child_return_value = p[6]                 # Return value only


def p_function_definition_argless_with_body(p):
    '''function_definition : DEFINE funcIDENT LSQUARE RSQUARE \
                             BEGIN variable_definitions return_value DOT \
                             END DOT'''
    p[0] = TreeNode("TN_fundef_argless_with_body", p[2])
    p[0].child_return_value = p[7]                 # Return value
    p[0].children_body_statements = [p[6]]         # Variable definitions


def p_function_definition_args_bodyless(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE \
                             BEGIN return_value DOT END DOT'''
    p[0] = TreeNode("TN_fundef_args_bodyless", p[2])
    p[0].child_return_value = p[7]                 # Return value
    p[0].children_formals = [p[4]]                 # Formal parameters


def p_function_definition_args_with_body(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE \
                             BEGIN variable_definitions return_value DOT \
                             END DOT'''
    p[0] = TreeNode("TN_fundef_args_with_body", p[2])
    p[0].child_return_value = p[8]                 # Return value
    p[0].children_formals_and_body = [p[4], p[7]]  # Formals, vardefs


def p_variable_definition(p):
    '''variable_definitions : var_def'''
    p[0] = TreeNode("TN_function_body")
    p[0].children_var_defs = [p[1]]


def p_variable_definitions(p):
    '''variable_definitions : variable_definitions var_def'''
    p[0] = p[1]
    p[0].children_var_defs.append(p[2])


def p_formal(p):
    '''formals : varIDENT'''
    p[0] = TreeNode("TN_formal_parameters")
    p[0].children_formals = [TreeNode("TN_varIDENT", p[1])]


def p_formals(p):
    '''formals : formals COMMA varIDENT'''
    p[0] = p[1]
    p[0].children_formals.append(TreeNode("TN_varIDENT", p[3]))


def p_return_value_eq(p):
    '''return_value : EQ simple_expression'''
    p[0] = TreeNode("TN_return_value_stmt")
    terminal_node = TreeNode("TN_EQ", p[1])
    p[0].children_parts = [terminal_node, p[2]]


def p_return_value_not_eq(p):
    '''return_value : NOTEQ pipe_expression'''
    p[0] = TreeNode("TN_return_value_stmt")
    terminal_node = TreeNode("TN_NOTEQ", p[1])
    p[0].children_parts = [terminal_node, p[2]]


def p_var_def_variable(p):
    '''var_def : varIDENT LARROW simple_expression DOT'''
    p[0] = TreeNode("TN_variable_definition")
    terminal_node = TreeNode("TN_varIDENT", p[1])
    p[0].children_id_and_expression = [terminal_node, p[3]]


def p_var_def_constant(p):
    '''var_def : constIDENT LARROW constant_expression DOT'''
    p[0] = TreeNode("TN_variable_definition")
    terminal_node = TreeNode("TN_constIDENT", p[1])
    p[0].children_id_and_expression = [terminal_node, p[3]]


def p_var_def_tuple(p):
    '''var_def : tupleIDENT LARROW tuple_expression DOT'''
    p[0] = TreeNode("TN_variable_definition")
    terminal_node = TreeNode("TN_tupleIDENT", p[1])
    p[0].children_id_and_expression = [terminal_node, p[3]]


def p_var_def_pipe_expr(p):
    '''var_def : pipe_expression RARROW tupleIDENT DOT'''
    p[0] = TreeNode("TN_variable_definition")
    terminal_node = TreeNode("TN_tupleIDENT", p[3])
    p[0].children_id_and_expression = [terminal_node, p[1]]


def p_constant_expression_const_id(p):
    '''constant_expression : constIDENT'''
    p[0] = TreeNode("TN_constIDENT", p[1])


def p_constant_expression_num_lit(p):
    '''constant_expression : NUMBER_LITERAL'''
    p[0] = TreeNode("TN_NUMBER_LITERAL", p[1])


def p_pipe_expression_tuple_expr(p):
    '''pipe_expression : tuple_expression'''
    p[0] = p[1]


def p_pipe_expression_tuple_chain(p):
    '''pipe_expression : tuple_expression PIPE pipe_operation'''
    p[0] = TreeNode("TN_pipe_expression", p[2])
    p[0].children_expression_and_operation = [p[1], p[3]]


def p_pipe_expression_pipe_chain(p):
    '''pipe_expression : pipe_expression PIPE pipe_operation'''
    p[0] = TreeNode("TN_pipe_expression", p[2])
    p[0].children_expression_and_operation = [p[1], p[3]]


def p_pipe_operation_func(p):
    '''pipe_operation : funcIDENT'''
    p[0] = TreeNode("TN_pipeop_funcIDENT", p[1])


def p_pipe_operation_mult(p):
    '''pipe_operation : MULT'''
    p[0] = TreeNode("TN_pipeop_MULT", p[1])


def p_pipe_operation_plus(p):
    '''pipe_operation : PLUS'''
    p[0] =  TreeNode("TN_pipeop_PLUS", p[1])


def p_pipe_operation_each(p):
    '''pipe_operation : each_statement'''
    p[0] = TreeNode("TN_pipeop_each")
    p[0].child_operation = p[1]


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''
    p[0] = TreeNode("TN_each_stmt", p[1])
    p[0].child_arg = TreeNode("TN_funcIDENT", p[3])


def p_tuple_expression_atom(p):
    '''tuple_expression : tuple_atom'''
    p[0] = p[1]


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom tuple_operation tuple_expression'''
    p[0] = TreeNode("TN_tuple_expr")
    p[0].children_args = [p[1], p[2], p[3]]


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''
    p[0] = TreeNode("TN_DOUBLEPLUS", p[1])


def p_tuple_atom_tuple_id(p):
    '''tuple_atom : tupleIDENT'''
    p[0] = TreeNode("TN_tupleIDENT", p[1])


def p_tuple_atoms_function_call(p):
    '''tuple_atom : function_call'''
    p[0] = p[1]


def p_tuple_atoms_doublemult(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE'''
    p[0] = TreeNode("TN_DOUBLEMULT", p[3])
    p[0].children_operands = [p[2], p[4]]


def p_tuple_atoms_doubledot(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEDOT constant_expression RSQUARE'''
    p[0] = TreeNode("TN_DOUBLEDOT", p[3])
    p[0].children_operands = [p[2], p[4]]


def p_tuple_atoms_args(p):
    '''tuple_atom : LSQUARE arguments RSQUARE'''
    p[0] = TreeNode("TN_tuple_atom_args")
    p[0].child_arg_list = p[2]


def p_function_call_paramless(p):
    '''function_call : funcIDENT LSQUARE RSQUARE'''
    p[0] = TreeNode("TN_function_call_paramless", p[1])


def p_function_call_args(p):
    '''function_call : funcIDENT LSQUARE arguments RSQUARE'''
    p[0] = TreeNode("TN_function_call_with_params", p[1])
    p[0].child_p_list = p[3]


def p_argument(p):
    '''arguments : simple_expression'''
    p[0] = TreeNode("TN_parameters")
    p[0].children_params = [p[1]]


def p_arguments(p):
    '''arguments : arguments COMMA simple_expression'''
    p[0] = p[1]
    p[1].children_params.append(p[3])


def p_atom_literal_num(p):
    '''atom : NUMBER_LITERAL'''
    p[0] = TreeNode("TN_NUMBER_LITERAL", p[1])


def p_atom_literal_str(p):
    '''atom : STRING_LITERAL'''
    p[0] = TreeNode("TN_STRING_LITERAL", p[1])


def p_atom_literal_var_id(p):
    '''atom : varIDENT'''
    p[0] = TreeNode("TN_varIDENT", p[1])


def p_atom_literal_const_id(p):
    '''atom : constIDENT'''
    p[0] = TreeNode("TN_constIDENT", p[1])


def p_atom_func_call(p):
    '''atom : function_call'''
    p[0] = p[1]


def p_atom_simple_expr(p):
    '''atom : LPAREN simple_expression RPAREN'''
    p[0] = p[2]


def p_atom_tuple(p):
    '''atom : SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    p[0] = TreeNode("TN_select_from_tuple", p[1])
    p[0].children_parts = [p[3], p[5]]  # Note: Omits control characters, exist implicitly.


def p_factors_atom(p):
    '''factor : atom'''
    p[0] = TreeNode("TN_atom")
    p[0].child_atom = p[1]


def p_factors_minus_atom(p):
    '''factor : MINUS atom'''
    p[0] = TreeNode("TN_atom", p[1])
    p[0].child_atom = p[2]


def p_term(p):
    '''term : factor'''
    p[0] = p[1]


def p_terms_mult(p):
    '''term : factor MULT term'''
    p[0] = TreeNode("TN_MULT", p[2])
    p[0].children_operands = [p[1], p[3]]


def p_terms_div(p):
    '''term : factor DIV term'''
    p[0] = TreeNode("TN_DIV", p[2])
    p[0].children_operands = [p[1], p[3]]


def p_simple_expression(p):
    '''simple_expression : term'''
    p[0] = p[1]


def p_simple_expression_plus(p):
    '''simple_expression : term PLUS simple_expression'''
    p[0] = TreeNode("TN_PLUS", p[2])
    p[0].children_operands = [p[1], p[3]]


def p_simple_expression_minus(p):
    '''simple_expression : term MINUS simple_expression'''
    p[0] = TreeNode("TN_MINUS", p[2])
    p[0].children_operands = [p[1], p[3]]


# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    if p is not None:
        print("{}:Syntax Error (token:'{}')".format(p.lineno, p.value))
    else:
        print("Missing return statement from the end of the input file!")
    raise SystemExit


# Build the parser
parser = yacc.yacc()
