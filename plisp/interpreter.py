from plisp import builtins
from plisp import environment
from plisp import parser


class DefaultEnvironment(environment.Environment): 
    def __init__(self):
        self.table = {
                '+': builtins.AddFunction(self)
            }


class PLispInterpreter:
    def __init__(self):
        self.program = None
        self.environment = DefaultEnvironment()

    def load_file(self, f):
        self.program = self.f.read()

    def load_string(self, string):
        self.program = string

    def execute(self):
        plist_parser = parser.PLispParser(self.program) 
        ast = plist_parser.parse()
        results = [ex.evaluate(self.environment) for ex in ast]
        return results[-1]
