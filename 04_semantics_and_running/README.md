**Notes:**
- Edits to the syntax tree since phase 3:
  
  - Removed recursion from:
  
    1. program statement
    2. function call arguments
    3. function and variable definitions
    4. variable definitions in a function body
    5. formal parameters in function definition
    
- Fixed phase 2 problems:

  - String literal catenation problem
  - Error from lexer instead of Python interpreter when return statement missing.    

**1. Implemented semantic checks**
    
    1. Globally unique variable and function identifiers
    
**2. Implementation level**
    
    1. Support for same nodetype sum, multiplication and division:
    
       operation    |  E.g.      | result
       -----------------------------------
       NUM + NUM    |  2 + 4     | 6
                    |  -2 + 4    | 2
       STR + STR    |  "Hello, " + "world" | "Hello, world"
                    | -"A" + "B" | error msg, signed strings are illegal
       NUM * NUM    |  2 * 4     | 8
       NUM * NUM    | -2 * -4    | 8  (normal sign rules)
       NUM / NUM    |  4 / 2     | 2
                    |  4 / 0     | error msg, zero-division is illegal
                    |  3 / 2     | 1 (floor from decimal representation)
       NUM*NUM/NUM  |  4*3/2     | 4 (evaluation from right to left!)
       
**3. Implemented own things**

    1. Line numbers in error messages about redefined identifiers.
    2. toString for SymbolData objects

**6. What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?**

    TODO