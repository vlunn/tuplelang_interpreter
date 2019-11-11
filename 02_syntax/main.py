from lexerutilities import lexer, tokens
import ply.yacc as yacc


def p_minimum_program(p):
    '''program : return_value DOT'''
    pass


def p_program(p):
    '''program : func_or_var_def return_value DOT'''
    pass


def p_func_or_var_def(p):
    '''func_or_var_def : var_def
                       | function_definition'''
    pass


def p_func_or_var_defs(p):
    '''func_or_var_def : var_def func_or_var_def
                       | function_definition func_or_var_def'''
    pass


def p_function_definition(p):
    '''function_definition : DEFINE funcIDENT LSQUARE RSQUARE \
        BEGIN variable_definitions return_value DOT END DOT'''
    print("func_definition( ** {} ** )".format(p[2]))


def p_function_definition_args(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE \
        BEGIN variable_definitions return_value DOT END DOT'''
    print("func_definition( ** {} ** )".format(p[2]))


def p_function_definition_minimum_body(p):
    '''function_definition : DEFINE funcIDENT LSQUARE RSQUARE \
        BEGIN return_value DOT END DOT'''
    print("func_definition( ** {} ** )".format(p[2]))


def p_function_definition_args_minimum_body(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE \
        BEGIN return_value DOT END DOT'''
    print("func_definition( ** {} ** )".format(p[2]))


def p_variable_definition(p):
    '''variable_definitions : var_def'''
    pass


def p_variable_definitions(p):
    '''variable_definitions : var_def variable_definitions'''
    pass


def p_formal(p):
    '''formals : varIDENT'''
    pass


def p_formals(p):
    '''formals : varIDENT COMMA formals'''
    pass


def p_return_value(p):
    '''return_value : EQ simple_expression
                    | NOTEQ pipe_expression'''
    pass


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


def p_constant_expression(p):
    '''constant_expression : constIDENT
                            | NUMBER_LITERAL'''
    pass


def p_pipe_expression(p):   # TODO: Check that recursion works.
    '''pipe_expression : tuple_expression'''
    pass


def p_pipe_expression_op(p):
    '''pipe_expression : tuple_expression PIPE pipe_operation'''
    pass


def p_pipe_expression_ops(p):
    '''pipe_expression : pipe_expression PIPE pipe_operation'''
    pass


def p_pipe_operation(p):
    '''pipe_operation : funcIDENT
                        | MULT
                        | PLUS
                        | each_statement'''
    pass


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''
    pass


def p_tuple_expression(p):  # TODO: tarkista, että toimii, kun ketjussa useampi
    '''tuple_expression : tuple_atom'''
    pass


def p_tuple_expressions(p):
    '''tuple_expression : tuple_atom tuple_operation tuple_expression'''
    pass


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''
    pass


def p_tuple_atom(p):
    '''tuple_atom : tupleIDENT
                | function_call
                | LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
                | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE
                | LSQUARE arguments RSQUARE'''
    pass


def p_function_call_no_args(p):
    '''function_call : funcIDENT LSQUARE RSQUARE'''
    print("function_call( ** {} ** )".format(p.slice[1].value))


def p_function_call(p):
    '''function_call : funcIDENT LSQUARE arguments RSQUARE'''
    print("function_call( ** {} ** )".format(p.slice[1].value))


def p_argument(p):
    '''arguments : simple_expression'''
    pass


def p_arguments(p):     # TODO: Check that works when multiple in chain
    '''arguments : simple_expression COMMA arguments'''
    pass


def p_literal_atom(p):
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


def p_factor(p):
    '''factor : atom'''
    print(p.slice[0])


def p_factor_negative(p):
    '''factor : MINUS atom'''
    print(p.slice[0])


def p_term(p):
    '''term : factor'''
    print(p.slice[0])


def p_terms(p):
    '''term : factor MULT term
            | factor DIV term'''
    pass


def p_simple_expression(p):
    '''simple_expression : term'''
    print(p.slice[0])


def p_simple_expressions(p):
    '''simple_expression : term PLUS simple_expression
                        | term MINUS simple_expression'''
    pass


# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print('syntax error @ line:', p.lineno, 'pos:', p.lexpos, 'value:', p.value)
    raise SystemExit


# Build the parser
parser = yacc.yacc()


if __name__ == '__main__':
    import argparse, codecs

    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')

    ns = arg_parser.parse_args()
    if ns.who:
        # identify who wrote this
        print('263461 Vivian Lunnikivi')

    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()

    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()

        result = parser.parse(data, lexer=lexer, debug=False)
        if result is None:
            print( 'syntax OK' )
