# Topic: Parser & Building an Abstract Syntax Tree

**Course** : Formal Languages & Finite Automata

**Author** : Mihailiuc Igor

***

## Theory

 In computer science, a parser is a program or a component of a program that analyzes the syntax of a text according to a formal grammar. It takes input in the form of a sequence of tokens (lexical units) and checks whether the sequence
 conforms to the rules defined by the grammar.

Here are some theories related to parsers:


1. Parsing Algorithms: Various parsing algorithms exist to analyze the structure of input strings based on a given grammar. Some popular parsing algorithms include Recursive Descent, LL(k), LR(k), and Earley parsing. Each algorithm has its own characteristics, such as their time complexity and the types of grammars they can handle efficiently.

2. Top-Down Parsing: Top-down parsing is an approach where the parser starts from the root of the parse tree and recursively expands non-terminal symbols based on the production rules of a grammar. Recursive Descent parsing is a common example of a top-down parsing technique. It tries to match the input against the production rules, starting from the top-level non-terminal.

3. Bottom-Up Parsing: Bottom-up parsing is an approach where the parser builds the parse tree from the leaves (tokens) towards the root. The parser identifies portions of the input that match the right-hand side of a production rule and replaces them with the corresponding non-terminal symbol. LR parsing is a well-known bottom-up parsing technique.

4. Abstract Syntax Trees (AST): An abstract syntax tree is a data structure used to represent the structure of a program or a piece of code after it has been parsed. It captures the essential syntax and disregards certain details, such as parentheses and other syntactic sugar. ASTs are often used in compilers and interpreters to perform further analysis and code transformations.

5. Error Handling: Parsers need to handle errors gracefully when encountering input that does not conform to the grammar rules. Error recovery strategies include methods like panic mode recovery, error productions, and error propagation techniques. These techniques aim to provide meaningful error messages and to continue parsing after an error has been detected.

***

## Objectives
- Get familiar with parsing, what it is and how it can be programmed
- Get familiar with the concept of AST

***

## Implementation description

So, the first step to implement the Parser is to create the parser tree, that will define our blocks and how the expression will be split up. Here is the code for the parser tree: 

```
class ParseTree:
    def __init__(self, n_type, value=None, children=None):
        self.type = n_type
        self.value = value
        self.children = children or []

    def __str__(self, level=0):
        if self.value is None:
            ret = "\t" * level + self.type + "\n"
        else:
            ret = "\t" * level + self.type + ": " + str(self.value) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret
```

Next, we create the parser itself. It contains functions, some of them that will iterate the whole program, and some of them that split up the expression given. The first function is used to find the integers that I have: 
```
def parse_factor(self, parent_node):
        parse_node = ParseTree("SECTION")
        parent_node.children.append(parse_node)
        if self.tokens[self.index][0] == "LPAREN":
            parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
            self.index += 1
            self.parse_expression(parse_node)
            if self.tokens[self.index][0] == "RPAREN":
                parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
                self.index += 1
        elif self.tokens[self.index][0] in ["INT"]:
            parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
            self.index += 1
```
The purpose of it is to start the parsing. The next function has the purpose to name all the plus and minus signs in my expression. 
```
def parse_add(self, parent_node):
        parse_node = ParseTree("EXPRESSION")
        parent_node.children.append(parse_node)
        self.parse_multiply(parse_node)
        if self.tokens[self.index][0] in ["PLUS", "MINUS"]:
            parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
            self.index += 1
            self.parse_term(parse_node)
```
And last, but not least, the function that names the multiply and divide signs inside the expression: 
```
def parse_multiply(self, parent_node):
        parse_node = ParseTree("TERM")
        parent_node.children.append(parse_node)
        self.parse_factor(parse_node)
        if self.tokens[self.index][0] in ["MULTIPLY", "DIVIDE"]:
            parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
            self.index += 1
            self.parse_factor(parse_node)
```

Also, I changed the main from laboratory work 3. now it implements the parsing function.
## Results
The expression has been split up into blocks. The parsing tree helped me implement parent nodes and child nodes. Even though the output looks chaotic, it is clealry shown what everything does there:
```
PROGRAM
        EXPRESSION
                TERM
                        SECTION
                                INT: 22
                PLUS: +
                TERM
                        SECTION
                                INT: 12
                        MULTIPLY: *
                        SECTION
                                LPAREN: (
                                EXPRESSION
                                        TERM
                                                SECTION
                                                        INT: 14
                                        MINUS: -
                                        TERM
                                                SECTION
                                                        INT: 1
                                                DIVIDE: /
                                                SECTION
                                                        INT: 6
                                RPAREN: )
```

## Conclusion

In conclusion, parsers play a crucial role in computer science and programming languages. Here are the key reasons why parsers are important:

1. Syntax Analysis: Parsers perform syntax analysis by analyzing the structure of input strings according to a formal grammar. They ensure that the input conforms to the grammar rules and can identify syntactic errors. This process is vital for compilers, interpreters, and other language processing tools to correctly understand and process code.

2. Language Processing: Parsers are fundamental components in language processing tasks such as compiling, interpreting, and transpiling programming languages. They help transform human-readable code into a format that can be executed by machines or further processed.

3. Error Detection and Reporting: Parsers are responsible for identifying and reporting syntax errors in the input. By detecting errors early, parsers help programmers catch and fix mistakes, improving code quality and reducing debugging time. Meaningful error messages generated by parsers facilitate the development process by pinpointing the exact location and nature of errors.

4. Code Transformation and Analysis: Parsers generate structured representations of code, such as abstract syntax trees (ASTs), which capture the essential structure and semantics of programs. ASTs enable further analysis and transformations, such as optimization, refactoring, code generation, and static analysis. These tasks are essential for improving program performance, maintainability, and identifying potential bugs or security vulnerabilities.

5. Language Design and Development: Parsers are vital for designing new programming languages or extending existing ones. They help define the syntax and grammar rules of a language, which form the basis for writing code. Parsers allow language designers to express their language's constructs, constraints, and semantics, enabling programmers to create expressive and powerful applications.

Overall, parsers are fundamental tools in language processing, error detection, code analysis, and code transformation. They enable efficient and accurate interpretation or compilation of programming languages, leading to improved development processes, code quality, and the creation of innovative programming languages and applications.

## References
1. https://www.techtarget.com/searchapparchitecture/definition/parser#:~:text=A%20parser%20is%20a%20program%20that%20is%20part%20of%20the,other%20software%20can%20understand%20it.
2. https://www.javatpoint.com/parser