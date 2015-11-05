import argparse
import sys

from plisp.interpreter import PLispInterpreter


def setup_args(parser):
    parser.add_argument('file', type=str, nargs='?', default=None, help="the source file to run")

def repl(interpreter):
    while True:
        try:
            line = str(input("> "))
        except (KeyboardInterrupt, EOFError):
            break
        interpreter.load_string(line)
        try:
            res = interpreter.execute()
            print(res)
        except Exception as e:
            print(str(type(e)) + ": " + str(e), file=sys.stderr)

def main():
    parser = argparse.ArgumentParser()
    setup_args(parser)
    args = parser.parse_args()

    interpreter = PLispInterpreter()
    filename = args.file

    if filename is not None:
        try:
            with open(filename, 'r') as source:
                program = source.read()
        except Exception as e:
            print(str(e), filename=sys.stderr)
        interpreter.load_string(program)
        try:
            interpreter.execute()
        except Exception as e:
            print(str(type(e)) + ": " + str(e), file=sys.stderr)
    else:
        repl(interpreter)


if __name__ == '__main__':
    main()
