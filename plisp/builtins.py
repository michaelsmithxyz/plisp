from functools import reduce

from plisp import types
from plisp import environment

class ListReduceBuiltin(types.Function):
    func = lambda x, y: None

    def __init__(self, env):
        self.env = env

    def apply(self, args):
        env = environment.Environment(base=self.env)
        return reduce(self.__class__.func, [a.evaluate(env) for a in args])

class AddFunction(ListReduceBuiltin):
    func = lambda x, y: x + y
    

class SubtractFunction(ListReduceBuiltin):
    func = lambda x, y: x - y


class MultiplyFunction(ListReduceBuiltin):
    func = lambda x, y: x * y


class DivisionFunction(ListReduceBuiltin):
    func = lambda x, y: x / y


class LambdaFunction(types.Function):
    def __init__(self, env):
        self.env = env
