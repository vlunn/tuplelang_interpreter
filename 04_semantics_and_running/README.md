**Notes**

    1. Edits to the syntax tree since phase 3 - Removed recursion from:
    
         1. program statement
         2. function call arguments
         3. function and variable definitions
         4. variable definitions in a function body
         5. formal parameters in function definition
         
    2. Fixed phase 2 problems:
    
       - String literal catenation problem.
       - Error from lexer instead of Python interpreter when return 
         statement missing.
       - Quite a few small structural changes and renaming stuff more 
         illustratively.

    3. And last: Why is the author wrong in most of the git commits:
    
       On Friday, my computer broke down (as in, crashed and was 
       unable to restart due to corrupted system files or something). 
       I was unable to do anything about it at the time, so I decided 
       to continue developing on my game PC, that I have in loan from
       my brother. However, **I forgot to update the git config**, so 
       now all my precious commits have the wrong author name ;___;           

**1. Implemented semantic checks**
    
    1. Globally unique variable identifiers aka. each variable can
       only be defined once. Implemented by global symbol table.
       Existing of an identifier is checked before adding, and collision
       causes rejection of the new definition, an error message and abort.
    
    2. Variables can be used once they have been defined and initialized, 
       not before. Trying to access a nonexistent or uninitialized variable 
       leads to an error message printing out and the interpretation aborting.  
    
**2. Implementation level**
    
    1. Support for same nodetype sum, multiplication and division:
    
       operation    |  E.g.      | result
       -----------------------------------
       NUM + NUM    |  2 + 4     | 6
                    |  -2 + 4    | 2
       NUM - NUM    |  2 - 4     | -2
                    |  2 - -4    | 6  (normal sign rules in reducing)
       STR + STR    |  "Hello, " + "world" | "Hello, world"
                    | -"A" + "B" | error msg, signed strings are illegal
       NUM * NUM    |  2 * 4     | 8
       NUM * NUM    | -2 * -4    | 8  (normal sign rules in multiplication)
       NUM / NUM    |  4 / 2     | 2
                    |  4 / 0     | error msg, zero-division is illegal
                    |  3 / 2     | 1 (floor from decimal representation)
       NUM*NUM/NUM  |  4*3/2     | 4 (evaluation from right to left!)
       
       * The interpreter prints out the result.
       * Any combination of number operations (+, -, /, *) is possible 
         with any combination of number literals and integer variables.
       
    2. Integer variables work. Program saves variables into its symbol 
       table (dict), from where the variables are accessible at any time. 
       Values are saved in the corresponding SymbolData objects during
       interpretation once the variable expression is evaluated. 
       
       * Note: Program also accepts string variables, even thought they 
         have little use; they can be catenated ":D".  
         
    3. First part of tuple variables work and normal integer variables 
       can be utilized in tuple variable definitions as long as the program
       syntax allows it. Example operations:
       
          <varname> <- [1,2,3].
          <negseq> <- [1,-2].     // negative elements     
          <var>  <- [one, 2,3].   // variable as element
          <seq>  <- [1..5].       // range definition of sequence
          <seq2> <- [1**5].       // value: [1,1,1,1,1]
          <con1> <- <aa> ++ <bb>  // tuple concatenation
          <con2> <- <aa> ++ [1]   // tuple concatenation with tuple literals
          <con3> <- <aa> ++ [bb]  // tuple concatenation with tuple literals with variables
          
       Illegal operations, doesn't belong to syntax -> syntax error message:

          <seq> <- [-1..4].       // Only positive integers allowed with doubledot
          <seq> <- [-1**4].       // Only positive integers allowed with doubledot
          lower <- 1.
          <seq> <- [lower..4].    // No variables with dot syntax  
          <seq> <- [lower**4].    // No variables with double mult
           
       * It would be rather easy to allow string tuples, or mixing integer and
         str tuples and it wouldn't even cause program crashes, but I don't 
         think that would be a good design choice before diving deeper into 
         possible future developement (eg. functions etc.), so I left them out.
         Now string tuples just raise an error message (or syntax error if it 
         goes against syntax rules). 

**3. Implemented own things**

    1. Line numbers in error messages about redefined identifiers.
    
    2. toString for SymbolData objects and TreeNode objects. 
       Just for convenience.

**6. What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?**

    Overall, I think this part of the assignment was more difficult than 
    the previous ones; This phase required constant thinking and 
    evaluating the consequences of sesign choises.
    
    As an upside; with new eyes, I solved the recursion problem from the 
    previous phase, which was nice. Then again, I got stuck making 
    improvements in the syntax tree and sort of forgot for quite a while
    that I was supposed to actually do the phase 4 ":D".
    
    It was difficult to parse the structure of the program, especially
    figuring out how to evaluate the program and how to save and fetch 
    variable values in/from the symbol table, since there were so many 
    different situations that had to be handled. Even figuring out all 
    the possible scenarios was quite laborious. But in the end, I'm rather
    pleased with myself, having solved the problem despite the 
    difficulties.
    
    As to whether I learned anything; Yes, I think I got a good idea about
    the implementation of semantic checks and interpretation. Didn't find it 
    easy, thought.
    