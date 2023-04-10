from Lexer import Lexer

def main():
    program = Lexer("example.txt")
    toks = program.tokenize()
    for t in toks: 
        print(t)

if __name__ == '__main__':
    main()