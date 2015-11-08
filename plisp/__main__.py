import argparse
import sys

from plisp.interpreter import PLispInterpreter


def setup_args(parser):
    parser.add_argument('file', type=str, nargs='?', default=None, help="the source file to run")

def repl(interpreter):
    while True:
        try:
            line = str(input("> "))
            res = interpreter.execute_string(line)
            print(res)
        except (KeyboardInterrupt, EOFError):
            break
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
                interpreter.execute_file(source)
        except Exception as e:
            print(str(type(e)) + ": " + str(e), file=sys.stderr)
    else:
        repl(interpreter)


if __name__ == '__main__':
    main()
