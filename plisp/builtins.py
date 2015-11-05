from functools import reduce

from plisp import types
from plisp import environment


class AddFunction(types.Function):
    def __init__(self, env):
        self.env = env

    def apply(self, args):
        env = environment.Environment(base=self.env)
        return reduce(lambda x, y: x + y, [a.evaluate(env) for a in args])


class SubtractFunction(types.Function):
    def __init__(self, env):
        self.env = env

    def apply(self, args):
        env = environment.Environment(base=self.env)
        return reduce(lambda x, y: x - y, [a.evaluate(env) for a in args])
