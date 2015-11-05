from functools import reduce

from plisp import types
from plisp import environment


class ListReduceBuiltin(types.Function):
    func = lambda x, y: None

    def __init__(self, env):
        self.env = env

    def apply(self, args, call_env):
        env = environment.Environment(base=self.env)
        return reduce(self.__class__.func, [a.evaluate(call_env) for a in args])


# Built-in functions

class AddFunction(ListReduceBuiltin):
    func = lambda x, y: x + y
    

class SubtractFunction(ListReduceBuiltin):
    func = lambda x, y: x - y


class MultiplyFunction(ListReduceBuiltin):
    func = lambda x, y: x * y


class DivisionFunction(ListReduceBuiltin):
    func = lambda x, y: x / y


class TypeFunction(types.Function):
    def __init__(self, env):
        self.env = env

    def apply(self, args, call_env):
        if len(args) != 1:
            raise SyntaxError("type must be in form: type expression")
        return args[0].evaluate(call_env).__class__


# Built-in Macros

class DefineMacro(types.Macro):
    def __init__(self, env):
        self.env = env

    def apply(self, args, call_env):
        if len(args) != 2 or type(args[0]) is not types.Symbol:
            raise SyntaxError("define must be in form: define name expression")
        result = args[1].evaluate(call_env)
        call_env.set(args[0], result)
        return result


class QuoteMacro(types.Macro):
    def __init__(self, env):
        self.env = env

    def apply(self, args, call_env):
        if len(args) == 0:
            return types.List()
        return args[0]


class LambdaMacro(types.Macro):
    def __init__(self, env):
        self.env = env

    def apply(self, args, call_env):
        if len(args) != 2 or type(args[0]) is not types.List:
            raise SyntaxError("lambda must be of form: lambda args expression")
        for arg in args[0]:
            if type(arg) is not types.Symbol:
                raise SyntaxError("lambda argument list must be comprised of symbols")
            return types.Function(args[0], args[1], call_env)
