**1. What is lexical analysis and how is it related to other parts in compilation?**
    
    Lexical analysis is the first step in the compiling process.
    It parses source code into a series of tokens by removing whitespace and
    comments. Tokens form the basic pieces from which a program constitues - 
    identifiers, literals and structures and they are further analyzed in 
    subsequent compilation phases. Syntactic analysis check if tokens form 
    syntactically correct sequences, semantic analysis checks if syntatically 
    correct pieces constitute a sane program, which can then be parsed into 
    more or less runnable program.  
    
**2. How is the lexical structure of the language expressed in the PLY tool? I.e., what parts are needed in the code and how are they related to lexical rules of the language?**

    The PLY tool requires 1) a list of tokens and 2) rules to define the 
    given tokens. Token list defines all lexems the language contains and the 
    rules define what kind of character sequences the tokens match. Rules are 
    defined as regexes and regex matches can be further handled in optional 
    functions of which names match token names.  
          
    
**3. Explain how the following are recognized and handled in your code:**

    1. Keywords
        - Each keyword is a separate token. Yet to see if this is reasonable.
        - Keywords match varIDENT -regex rule, so each varIDENT match is 
          checked in a parser function just in case it matches a keyword.
        - varIDENT token type is then replaced with the keyword's type if 
          the matched character sequence was indeed a keyword.
          
    2. Comments
        - Greedily match longest character stream within a single row that 
          starts with the character '{' and ends with the character '}' and 
          contains any number of any characters, excluding linebreaks.
           
    3. Whitespace between tokens
        - There is a whitespace token of which rule matches tabs (\t) that in 
          effect matches spaces as well :) 
        
    4. Operators & delimiters (<-, parenthesis, etc.)
        - One letter operators are mathed by regex that contains the given
          character
        - Special characters are escaped (plus, bracets, square brackets, dot, 
          pipe, star, slash).
        - Two-letter tokens are mathed as a simple matching regex string.
        - Double-character regex merely counts the given character. This means
          that eg. +++ will match a doble plus and plus token, in that order.  
         
    5. Integer literals
        - Regex that contains at least one digit (0-9). Token value is cast 
          into an Python3 integer in a supplying function.
        
    6. String literals
        - Regex that matches at least one arbitrary character (except a 
          line break), enclosed in double quotation marks. Supplying function
          removes outermost quotation marks - so the string may contain 
          quotation marks as well. (This is a matter of choice.) 
        
    7. Function names
        - Regex that requires exactly one capital letter followed by at least 
          one lower case letter. Thus, eg. 'FFoo' is not a valid function name. 
        
    8. Tuple names
        - Simple regex that requires angle brackets as enclosing characters.
          In between, there should be at least one lower case letter.   

**4. How can the lexer distinguish between the following lexical elements:**

    NB. None of the rules accept line breaks, so it is enough to consider
    rules from one-row point of view.

    1. Function names & constant names
        - Both start with a capital letter, but no lower case are allowed in 
          constant identifiers, but funtion identifiers require at least one
          lower case letter. 
        
    2. Keywords & variable names
        - Both math the same varIDENT rule, but all varIDENT matches are 
          cross-referenced with a list of reserved words and the token type
          is corrected if the token value mathes a keyword.  
        
    3. Operators - (minus) & -> (right arrow)
        - Regex mathing is greedy and will match the rule that defines 
          longest part of the input. So, '->' will never be parsed as minus 
          and greater than, but will always be right arrow. 
        
    4. String literals & variables names
        - String literals are enclosed in double quotation marks. If there 
          is a single quotation mark, it doesn't match the variable rule since
          it doesn't allow quotation marks. If there are (at least) two 
          quotation marks, the sequence will match string literal rule so that
          anything before (or after) it is discarded (and maybe matched as 
          a variable name) and anything between the outermost quotation marks 
          is contained in the string literal.
        
    5. Comments & other code
        - The parser doesn't recognize comments that expand to more than one 
          line. Inside a line, comment is enclosed in curly braces (more than
          two braces are allowed as long as the first one is opening and the
          last one closing bracket. Anything outside is recognized as normal
          code since it's not a comment. Curly braces aren't used in any other
          tokens, so there's no misidentification risk - all other rules drop
          when there is a curly bracket.
        
    6. Tuple names & two variables compared to each other with <.
        - Parity and extension principles take care of the fact that the lexer
          tries to find longest character sequence until it finds a closing 
          bracket, and if on one row there is not, it must be a comparison
          operator. 

**5. Did you implement any extras? If so explain them (what and how)**

    Nope.

**6. What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?**
    
    I think the assignment was very straight-forward with the given material 
    and I didn't run into anything too difficult that couldn't be completely
    avoided by making assumtions such as not allowing multi-line-tokens. :)
    
    Writing regexes was pretty easy aside from coming up with a way to allow
    multi-line comments that dont't merge separate comments on different rows.
    
    I don't know if I really learned anything new - my version of a lexer is
    an "MVP" of the exercise. Maybe I should've tried to come up with more 
    complex solution - think about how to handle more special cases or 
    automize testing or something like that. Well, now I can write a simple 
    lexer using ply.lexx. 