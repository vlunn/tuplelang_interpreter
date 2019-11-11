**Notes:**
- I wasn't sure how to print out simple_expressions; they consist of other 
  simple_expressions, so should each new match count as a new simple 
  expression? That'll cause some of them to print out "twice"; first, as 
  their own match and again as a part of another simple_expression match. 
  I decided to only print the first match and the same goes for term as well.  
  
- I refactored the lexer utilities into its own module since I found it 
  disturbing to implement two clear modules in the same file. This will in
  no way affect program usage.

**1. What is syntax analysis and how is it related to other parts in compilation?**
    
    The aim of syntax analysis is to check whether a given snippet of 
    arbitrary text follows the syntactical rules - that is, the grammar - 
    of a given programming language.
    
    The first step of compilation - lexical analysis - produces a list of 
    tokens for the syntax analyser to check. Syntax analyser then examines 
    the token sequence and recursively matches its subsequences against
    unambiguous grammar rules that constitute the programming language. 
    Should the program match the rules, the result of this phase is that
    yes, this indeed is a syntactically correct program that can proceed to
    the next phase of compilation - semantic analysis.
    
    However, whether the program is sane in the sense of eg. not containing
    double definitions of variables etc., is in no way guaranteed, even if 
    the program is syntactically correct. Those are semantic errors and
    get checked in semantic analysis.
    
**2. How is the syntactic structure of the language expressed in the PLY tool? I.e., what parts are needed in the code and how are they related to syntactic rules of the language?**
    
    Each grammar rule is defined in a PLY's own version of BNF. For each rule, 
    the programmer defined a normal Python function with an otherwise 
    arbitrary name, as long as it starts with the prefix 'p_'. The yacc-tool 
    recognizes these functions as grammar rule definitions and looks up their 
    docstring.
    
    The actual BNF is defined in the doctrings in a format where the first 
    word is a non-terminal, followed by a type of assignment symbol ':' 
    meaning that the non-terminal on the left can be replaced with the 
    sequence on the right. The sequence can then constitute from further 
    non-terminals or terminal symbols, where terminal symbols correspond to 
    tokens of the language.
    
    What the PLY/yacc tool then does, when it's fed an program candidate as 
    an input, is that it starts from the beginning of the file and tries to 
    match it against the first grammar rule in the grammar definition file. 
    If a match is found, yacc replaces the top of the stack with what's on 
    the right-hand side of the grammar rule and this process is then repeated 
    until the stack either is emptied or the top of the stack doesn't match 
    any rule, which results in syntax error. The stack only gets empty when 
    the whole program has passed syntax checking, meaning that it's syntax 
    is okay.
    
**3. Explain in English what the syntax of the following elements mean (i.e. how would you describe the syntax in textual form):**

    1. Variable definitions
    
        A variable always constitutes from four parts, first of which is 
        either 1) a variable identifier token, 2) constant variable 
        identifier token, 3) tuple variable identifier token or 4) a pipe
        expression. This first token is always followed by left-arrow token,
        that is, '<-', except for the last, pipe expression, which requires
        a right-arrow. The variable definition syntax always ends with a  
        dot token.
        
        Between the left arrow and ending dot, there is another token, 
        which depends on what kind variable is being defined. Normal variable
        identifier requires an non-terminal simple_expression as its pair,
        constant definition required constant expression, tuple definition
        an tuple expression and a pipe expression an tuple identifier.
        
        Furthermore, simple, constant, tuple and pipe expressions are all
        non-terminals, which means that they don't resolve to terminal 
        symbols, but may resolve to different kind of expressions, the 
        syntax of which is separately defined.
        
    2. Function call
        
        A function call always begins with a function identifier - the form of
        which has been defined in the lexer rules. Function identifier is 
        always followed by square braces that enclose a - possibly empty -
        list of arguments between them. These arguments are all simple 
        expressions that constitute from a sequence of terms, each of which is
        separated by either plus or minus terminal token.
        
        So eg. CalculateSum[1 + 2, 4 - 5, 3, -3] could be an function call, 
        having 4 arguments, first two of which constituting from two terms, 
        latter two from one. 
        
        Furthermore, each term constitutes from factors, that can be 
        catenated with MULT or DIV terminals and each of these factors are 
        atoms, that can be eg. function calls, literals such as numbers or 
        strings, or references to other variables. 
        
    3. Tuple expressions
        
        Constitute from either a single tuple atom, or a sequence of them,
        catenated by tuple operation rules. A single tuple atom resolves into
        a 1) tuple identifier, 2) function call, 3) double-multiplication 
        non-terminal rule 4) double-plus non-terminal rule or 5) a list of
        arguments.
        
        Note: Rules 3 and 4 catenate two constant expressions that are either 
        constant identifiers or number literals. So it is likely that these 
        are rules to define how to either sum or multiplicate two constants.
        
**4. Answer the following based on the syntax definition:**

    a. Is it possible to define a "nested" function, i.e. to define a 
       new function inside another function? Why?
        
        No, it's not possible to define nested functions, since if a function
        definition rule check is entered, its syntax requires it to contain
        only such parts that don't contain other function definitions. 
    
    b. Is it syntactically possible to perform arithmetic with strings 
       ("Hello"+"world")? Why?
        
        It would be, if the lexer wouldn't recognize them as a single string
        literal token. ":)", because there is a simple expression rule that 
        allows two terms to be catenated with a PLUS terminal and each of 
        these terms resolve into factors that further resolve into atoms 
        that can be string literals.
        
        It's hard to tell whether this is a bug or a feature, so I'm not
        going to do anything about it. Please do tell, if I should fix it
        for the next phase.
        
    c. Is it possible to initialize a variable from a constant 
       (N<-1. var<-N.)? Why?
        
        Yes. There is a syntax rule for 'varIDENT LARROW simple_expression DOT'
        that corresponds to this case. Simple expression would resolve into 
        a term, which would then resolve into a factor, which resolves into 
        an atom and an atom can be a constant identifier. If the program then
        knows how to fetch its value, initialization succeeds. Syntactically
        there's nothing wrong with this operation.
        
    d. Is it possible to initialize a constant from a variable 
       (var<-1. N<-var.)? Why?
        
        No. A constant variable definition ('constIDENT LARROW 
        constant_expression DOT') wants an constant expression as its 
        'parameter'. A constant expression can either be constant identifier 
        or number literal, so no, it can't resolve into a variable identifier.  
        
    e. Are the following allowed by the syntax: xx--yy and --xx? Why?
        
        At least the first is a simple expression constituting of the sequence
        term MINUS term, where the first term resolves by the route
        factor -> atom -> varIDENT and the second resolves via route
        factor -> MINUS atom -> varIDENT. So yes, syntactically this is 
        correct at least in an appropriate context where xx--yy resolves into
        a simple expression, eg. along with a variable definition.
        
        With a similar logic, --xx may work in a fitting context, but as a 
        standalone it is a syntax error.  
        
    f. How is it ensured that addition/subtraction are done after 
       multiplication/division?
       
        By precedence. The result of multiplication and division operation
        is fed to the simple expression as already resolved terms, and 
        sum/reduction is performed between these resolved terms.
        
        Of course nothing is calclutaed yet in this phase, but on might think
        that the parsing order is the same in syntax parsing as in actual 
        calculations. 
        
**5. Please mention in the document if you didn't implement functions (i.e. you are ok with passing with the minimum grade).**

    I did implement functions.

**6. What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?**

    I liked the assignment, apart from the problems with my personal timetable,
    but that doesn't have anything to do with the task itself. I think there
    was more confusion here due to my inability to find proper definitions on
    the PLY's BNF syntax, but after I got helpo with those, the task was guite
    straight-forward to finish.