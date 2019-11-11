**TODO:**
- Improve error messages in the lexer, try http://www.dabeaz.com/ply/ply.html#ply_nn10

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
    
    TODO
    
**3. Explain in English what the syntax of the following elements mean (i.e. how would you describe the syntax in textual form):**

    1. Variable definitions
        - TODO 
        
    2. Function call
        - TODO 
        
    3. Tuple expressions
        - TODO 
        
**4. Answer the following based on the syntax definition:**

    a. Is it possible to define a "nested" function, i.e. to define a new function inside another function? Why?
        - TODO
        
    b. Is it syntactically possible to perform arithmetic with strings ("Hello"+"world")? Why?
        - TODO
        
    c. Is it possible to initialize a variable from a constant (N<-1. var<-N.)? Why?
        - TODO
        
    d. Is it possible to initialize a constant from a variable (var<-1. N<-var.)? Why?
        - TODO
        
    e. Are the following allowed by the syntax: xx--yy and --xx? Why?
        - TODO
        
    f. How is it ensured that addition/subtraction are done after multiplication/division?
        - TODO
        
**5. Please mention in the document if you didn't implement functions (i.e. you are ok with passing with the minimum grade).**


**6. What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?**