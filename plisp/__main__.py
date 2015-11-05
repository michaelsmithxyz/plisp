from plisp.interpreter import PLispInterpreter

if __name__ == '__main__':
    try:
        interpreter = PLispInterpreter()
        while True:
            line = str(input("> "))
            interpreter.load_string(line)
            res = interpreter.execute()
            print(res)
    except KeyboardInterrupt:
        pass
