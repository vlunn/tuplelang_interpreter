from lexerutilities import lexer, tokens
import tree_print
import ply.yacc as yacc


class TreeNode:

    def __init__(self, type, parent=None):
        self.nodetype = type


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


def p_function_definition(p):
    '''function_definition : DEFINE funcIDENT LSQUARE RSQUARE BEGIN return_value DOT END DOT
                           | DEFINE funcIDENT LSQUARE RSQUARE BEGIN variable_definitions return_value DOT END DOT
                           | DEFINE funcIDENT LSQUARE formals RSQUARE BEGIN return_value DOT END DOT
                           | DEFINE funcIDENT LSQUARE formals RSQUARE BEGIN variable_definitions return_value DOT END DOT'''
    print("func_definition( ** {} ** )".format(p[2]))


def p_variable_definitions(p):
    '''variable_definitions : var_def
                            | var_def variable_definitions'''
    pass


def p_formal(p):
    '''formals : varIDENT
               | varIDENT COMMA formals'''
    pass


def p_return_value(p):
    '''return_value : EQ simple_expression
                    | NOTEQ pipe_expression'''
    p[0] = TreeNode("return_value_statement")
    p[0].children_parts = [p[1], p[2]]


def p_var_def_variable(p):
    '''var_def : varIDENT LARROW simple_expression DOT'''
    print("variable_definition( ** {} ** )".format(p.slice[1].value))


def p_var_def_constant(p):
    '''var_def : constIDENT LARROW constant_expression DOT'''
    print("constant_definition( ** {} ** )".format(p.slice[1].value))


def p_var_def_tuple(p):
    '''var_def : tupleIDENT LARROW tuple_expression DOT'''
    print("tuplevariable_definition( ** {} ** )".format(p.slice[1].value))


def p_var_def_pipe_expr(p):
    '''var_def : pipe_expression RARROW tupleIDENT DOT'''
    print(p.slice[1])


def p_constant_expressions(p):
    '''constant_expression : constIDENT
                           | NUMBER_LITERAL'''
    pass


def p_pipe_expressions(p):
    '''pipe_expression : tuple_expression
                       | tuple_expression PIPE pipe_operation
                       | pipe_expression PIPE pipe_operation'''
    pass


def p_pipe_operations(p):
    '''pipe_operation : funcIDENT
                      | MULT
                      | PLUS
                      | each_statement'''
    pass


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''
    pass


def p_tuple_expressions(p):
    '''tuple_expression : tuple_atom
                        | tuple_atom tuple_operation tuple_expression'''
    pass


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''
    pass


def p_tuple_atoms(p):
    '''tuple_atom : tupleIDENT
                  | function_call
                  | LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
                  | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE
                  | LSQUARE arguments RSQUARE'''
    pass


def p_function_calls(p):
    '''function_call : funcIDENT LSQUARE RSQUARE
                     | funcIDENT LSQUARE arguments RSQUARE'''
    print("function_call( ** {} ** )".format(p.slice[1].value))


def p_argument(p):
    '''arguments : simple_expression
                 | simple_expression COMMA arguments'''
    pass


def p_atom_literals(p):
    '''atom : NUMBER_LITERAL
            | STRING_LITERAL
            | varIDENT
            | constIDENT'''
    print("{}( ** {} ** )".format(p.slice[0], p.slice[1].value))


def p_atom(p):
    '''atom : function_call
            | LPAREN simple_expression RPAREN
            | SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    print(p.slice[0])


def p_factors(p):
    '''factor : atom
              | MINUS atom'''
    print(p.slice[0])


def p_term(p):
    '''term : factor'''
    print(p.slice[0])
    p[0] = p[1]


def p_terms(p):
    '''term : factor MULT term'''
    p[0] = TreeNode("factor_mult_term")
    p[0].children_parts = [p[1], p[2], p[3]]


def p_terms(p):
    '''term : factor DIV term'''
    p[0] = TreeNode("factor_div_term")
    p[0].children_parts = [p[1], p[2], p[3]]


def p_simple_expression(p):
    '''simple_expression : term'''
    print(p.slice[0])
    p[0] = p[1]


def p_simple_expression_plus(p):
    '''simple_expression : term PLUS simple_expression'''
    p[0] = TreeNode("simple_plus_expr")
    p[0].children_plus_expression = [p[1], p[2], p[3]]


def p_simple_expression_minus(p):
    '''simple_expression : term MINUS simple_expression'''
    p[0] = TreeNode("simple_minus_expr")
    p[0].children_minus_expression = [p[1], p[2], p[3]]


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
