from plisp.interpreter import PLispInterpreter

if __name__ == '__main__':
    interpreter = PLispInterpreter()
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
            print(str(type(e)) + ": " + str(e))
