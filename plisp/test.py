import tokenizer
import parser

if __name__ == '__main__':
    program = "#(1 2 3)"
    test_parser = parser.LispParser(program)
    print(test_parser.parse())
