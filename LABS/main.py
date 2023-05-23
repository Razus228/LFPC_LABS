from Parser import Parser

def main():
    program = Parser("example/example.txt")
    program.parse()
    program.show_ast()

if __name__ == '__main__':
    main()