# Lexer

**Course** : Formal Languages & Finite Automata

**Author** : Mihailiuc Igor

***

## Theory


Lexical analysis is the process of converting a programming language's source code, which is represented as a string of characters, into a collection of useful tokens or lexemes. These tokens are further processed, such as parsing and interpretation, to execute the code. A software called a lexer or tokenizer is responsible for the lexical analysis, which follows pre-established rules or patterns to create tokens for each language component like keywords, identifiers, operators, and literals. These tokens are then used by the parser for further processing.

The development of a lexer is essential when building a compiler, interpreter, or any tool that needs to examine and work with source code. Creating a lexer involves specifying the various tokens and patterns that match them and implementing the system using object-oriented or functional programming techniques.

Python provides several tools and packages that can aid in the development of a lexer, making the process relatively simple.

## Objectives


- Understand what lexical analysis is.
- Get familiar with the inner workings of a lexer/scanner/tokenizer.
- Implement a sample lexer and show how it works.
  
## Implementation description


So the first step was that I created the *Token.py* file to store ther all the tokens that I need. (Also called tokenization)
```
tokens = {
    
    "INT" : r"[0-9]+",
    "PLUS" : r"\+",
    "MINUS" : r"\-",
    "DIVIDE" : r"\/",
    "MULTIPLY" : r"\*",
    "LPAREN" : r"\(",
    "RPAREN" : r"\)",
    "NEWLINE": r"\n | \r | \r \n",
    "WHITESPACE": r"[ ]+",
    "INVALID": r".+"

}
```

The next step is the creation of the *Lexer.py* file. In this file I implemented the Lexer. The main idea of this file is that it transforms the input using the tokens that were stored. 

```
import re
import Tokens


class Lexer:
    file = None
    content = ""
    tokens = "|".join(f"(?P<{name}>{regex})" for name, regex in Tokens.tokens.items())

    def __init__(self, file_name):
        self.file = open(file_name, "r")
        self.content = self.file.read()

    def tokenize(self):
        matches = re.finditer(self.tokens, self.content)

        tokens = []
        for match in matches:
            token_name = match.lastgroup
            token_value = match.group(token_name)

            if token_name in ["WHITESPACE", "NEWLINE"]:
                continue

            if token_name == "INVALID":
                raise Exception(f"Invalid token '{token_value}'")

            tokens.append((token_name, token_value))

        return tokens
```

The final step was the implementation of the *main.py* file, in which I took a random example for the Lexer to show how it works.
```
from Lexer import Lexer

def main():
    program = Lexer("example.txt")
    toks = program.tokenize()
    for t in toks: 
        print(t)

if __name__ == '__main__':
    main()
```

## Results


For the example : ***12 + 23 * 8 / ( 24 / 6 - 3 )*** we have the following output:

```('INT', '12')
('PLUS', '+')
('INT', '23')
('MULTIPLY', '*')
('INT', '8')
('DIVIDE', '/')
('LPAREN', '(')
('INT', '24')
('DIVIDE', '/')
('INT', '6')
('MINUS', '-')
('INT', '3')
('RPAREN', ')')
```

## Conclusion


The process of breaking down the source code into smaller tokens and assigning
them to categories, known as lexical analysis, plays a crucial role in the 
processing of programming languages. This analysis is carried out using a 
program called a lexer or tokenizer, which generates a list of tokens that can 
be used for further processing.

Developers can perform lexical analysis on their code and obtain a list of tokens 
that can be used for parsing, interpretation, and execution of the code by 
creating a lexer in Python. Overall, the creation of a lexer in Python can 
greatly simplify the development of tools and programs that employ programming 
languages.

## References


1. https://docs.python.org/3/reference/lexical_analysis.html
2. https://svn.python.org/projects/external/Pygments-1.1.1/docs/build/lexerdevelopment.html
3. https://svn.python.org/projects/external/Pygments-1.1.1/docs/build/lexerdevelopment.html
   
