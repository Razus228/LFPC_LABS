from Lexer import Lexer
from ParseTree import ParseTree

class Parser:
    def __init__(self, path):
        program = Lexer(path)
        self.tokens = program.tokenize()
        self.index = 0
        self.ast = None

    def parse(self):
        self.ast = ParseTree("PROGRAM")
        self.parse_expression(self.ast)

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
            
    def parse_expression(self, parent_node):
        parse_node = ParseTree("EXPRESSION")
        parent_node.children.append(parse_node)
        self.parse_term(parse_node)
        if self.tokens[self.index][0] in ["PLUS", "MINUS"]:
            parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
            self.index += 1
            self.parse_term(parse_node)

    def parse_term(self, parent_node):
        parse_node = ParseTree("TERM")
        parent_node.children.append(parse_node)
        self.parse_factor(parse_node)
        if self.tokens[self.index][0] in ["MULTIPLY", "DIVIDE"]:
            parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
            self.index += 1
            self.parse_factor(parse_node)


    def show_ast(self):
        print(self.ast)
