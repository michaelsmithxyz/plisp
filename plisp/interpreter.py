from plisp import builtins
from plisp import environment
from plisp import parser
from plisp import types


class DefaultEnvironment(environment.Environment): 
    def __init__(self):
        self.table = {
                # Built-in functions
                '+': builtins.AddFunction(self),
                '-': builtins.SubtractFunction(self),
                '*': builtins.MultiplyFunction(self),
                '/': builtins.DivisionFunction(self),
                'eq?': builtins.EqualityFunction(self),
                'type': builtins.TypeFunction(self),
                'print': builtins.PrintFunction(self),
                'import': builtins.ImportFunction(self),
                # Type constants
                'nil': types.List(),
                '#t': types.Boolean(True),
                '#f': types.Boolean(False),
                # Built-in macros
                'define': builtins.DefineMacro(self),
                'lambda': builtins.LambdaMacro(self),
                'fn': builtins.FnMacro(self),
                'quote': builtins.QuoteMacro(self),
                'if': builtins.IfMacro(self),
                '.': builtins.DotMacro(self),
                '!': builtins.BangMacro(self)
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
