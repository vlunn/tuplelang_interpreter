**Notes:**
- No notes for the time being.

**1. What is an (abstract) syntax tree and how is it related to other parts in compilation?**
    
    AST is a tree-like data structure that is produced during syntax analysis 
    phase of compilation/interpretation. It represents the syntactic 
    structure of the program (that still might not be semantically correct).
    
    Syntax analyser takes the token stream produced by lexical analysis and 
    compares the stream against the program's syntax, defined by BNF. Rule
    matches are constructed into a data structure, which depicts the 
    derivation from the syntax rules.
    
    Syntax tree can then be further analysed and optimized in the next 
    phases of the compilation or interpretation. It is used for construct 
    a symbol table, it can be optimized and together with the symbol table,
    it can be used to determine if there are conflicts such as double 
    definition for identifiers. 
    
**2. How is the syntax tree generated using the PLY tool? I.e., what things are needed in the code and how are they related to syntactic rules of the language and the tree?**
    
    The BNF describing program syntax was defined in the block comments. The 
    PLY tool then uses the BNF rules to match token streams into syntactic 
    rules and produces YaccProduction-objects that represent those said 
    elements.
    
    These YaccProduction objects can be edited and utilized in constructing 
    a Python data structure containing the whole syntax tree. This is done
    in the body of the production functions that the PLY tool uses for 
    matching the program syntax.
    
**3. Explain in English what kind of tree is formed in your code from the following syntactic elements**

    1. Variable definitions
    
        One variable definition constructs a node (variable_definition) that
        has two children; first of which is the variable type, represented as
        a leaf node and the second child being a node containing the 
        expression that constitutes the value of the variable.
        
        Should there be more than one consecutive variable definitions, they
        construct a recursive stucture of consecutive nodes, first of which
        is a join-construction variable_and_func_or_var_definition that has
        two children; first of which is the first variable definition and the 
        second node is a reference to the next recursion node. Both children 
        of the last recursion node are variable definitions.
        
        Note: all variable definitions work by identical principle, whether a
        definition is for varIDENT, constIDENT or tupleIDENT with pipe or 
        tuple expression.    
        
    2. Pipe expressions
        
        The first node of the expression is a pipe_expression node, which has
        PIPE as its value. The node has two parameters, first of which is
        either a tuple expression or another pipe expression. The second child
        of the pipe exression is a pipe operation that can resolve to either a
        leaf node ( funcIDENT, MULT, PLUS ) or each statement.
        
    3. Function call
        
        The first node in a parsed function call is of the type of the 
        function call (four types; with or without parameters and simple 
        body with only return value or variable definitions as well). The 
        value of the function call node is its name and it can have a child 
        to define a recursive list of parameters.
        
        Should there be a parameter list child, the first node is param_list
        node containing the first parameter and the rest can be found by
        following the next_param child chain.
        
**4. Answer the following based on the syntax definition and your implementation:**

    a. In which cases is it possible in your implementation to end up with a 
       tree with empty child attributes (somewhere in the tree there is a 
       place for a child node (or nodes), but there is none)? I.e., in which 
       situations you end up with tree nodes with child_... attribute being 
       None, or children_... attribute being an empty list?
       
        At least all of the terminal nodes are such that they don't have any
        children - but they neither have empty child attributes. The attribute
        just doesn't exist for such nodes. I don't think I define child(ren)
        attributes for any node that doesn't have them.
    
    b. Are there places in your implementation where you were able to 
       "simplify" the tree by omitting trivial/non-useful nodes or by 
       collecting a recursive repeating structure into a list of child 
       nodes?
        
        I omitted quite a few such nodes that didn't seem useful at the time
        being:
        
            1. func_or_var_def resolution to either variable of function 
               definition
            2. variable_definitions resolving to var_def
            3. pipe_expression -> tuple_expression
            4. tuple_expression -> tuple_atom
            5. tuple_atom -> function_call
            6. arguments -> simple_expression
            7. atom -> function_call
            8. factor -> atom
            9. term -> factor
            10. simple_expression -> term
            
        For example, 8 and 9 can be omitted since there's no other difference 
        between a factor and a term than calculation order, and the BNF 
        matching takes care of it.
        
        What I didn't do - at least yet - was get rid of the recursion.
        I think the easiest way to do that might be during the next iteration
        of the tree, so there's no need to create backlinks to be able to
        append nodes to their parents' child lists directly.
        
**5. Please mention in the document if you didn't implement functions (i.e. you are ok with passing with the minimum grade).**

    I did implement functions.

**6. What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?**

    I think the recursion problem was the most difficult one, otherwise I 
    think the assignment was ok: not too big or small or too difficult or 
    too easy. I think I got some hang of the syntax tree construction, 
    although Iäm still left wondering whether the recursion is any way 
    reasonably possibly to get rid of during the tree creation; how does one
    get access to parent nodes?