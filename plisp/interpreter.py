from plisp import builtins
from plisp import environment
from plisp import parser
from plisp import types


class DefaultEnvironment(environment.Environment): 
    def __init__(self):
        self.forms = {
                'lambda': builtins.LambdaForm(),
                'define': builtins.DefineForm(),
                'quote': builtins.QuoteForm(),
                'backquote': builtins.BackquoteForm(),
                'unquote': builtins.UnQuoteForm(),
                'defmacro': builtins.DefMacroForm(),
                'fn': builtins.FnForm(),
                'if': builtins.IfForm(),
                'do': builtins.DoForm(),
                '.': builtins.DotForm(),
                '!': builtins.BangForm()
                }

        self.macros = {}

        self.table = {
                # Built-in functions
                '+': builtins.AddFunction(self),
                '-': builtins.SubtractFunction(self),
                '*': builtins.MultiplyFunction(self),
                '/': builtins.DivisionFunction(self),
                'eq?': builtins.EqualityFunction(self),
                'list': builtins.ListFunction(self),
                'cons': builtins.ConsFunction(self),
                'first': builtins.FirstFunction(self),
                'rest': builtins.RestFunction(self),
                'type': builtins.TypeFunction(self),
                'print': builtins.PrintFunction(self),
                'import': builtins.ImportFunction(self),
                # Type constants
                'nil': types.List(),
                '#t': types.Boolean(True),
                '#f': types.Boolean(False),
            }


class PLispInterpreter:
    instance = None

    def __init__(self):
        self.environment = DefaultEnvironment()
        PLispInterpreter.instance = self

    def _execute(self, program):
        plist_parser = parser.PLispParser(program) 
        ast = plist_parser.parse()
        results = [ex.evaluate(self.environment) for ex in ast]
        return results[-1]

    def execute_file(self, f):
        program = f.read()
        return self._execute(program)

    def execute_string(self, string):
        return self._execute(string)
