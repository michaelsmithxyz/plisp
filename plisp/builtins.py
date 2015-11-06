from functools import reduce

from plisp import types
from plisp import environment


# Built-in functions

class BuiltinFunction(types.Function):
    def __init__(self, env):
        self.env = env

class ListReduceBuiltin(BuiltinFunction):
    func = lambda x, y: None

    def apply(self, args, call_env):
        return reduce(self.__class__.func, [a.evaluate(call_env) for a in args])


class AddFunction(ListReduceBuiltin):
    func = lambda x, y: x + y
    

class SubtractFunction(ListReduceBuiltin):
    func = lambda x, y: x - y


class MultiplyFunction(ListReduceBuiltin):
    func = lambda x, y: x * y


class DivisionFunction(ListReduceBuiltin):
    func = lambda x, y: x / y


class EqualityFunction(BuiltinFunction):
    def apply(self, args, call_env):
        if len(args) != 2:
            raise Exception("Arity error")
        return types.Boolean(args[0] == args[1])



class TypeFunction(BuiltinFunction):
    def apply(self, args, call_env):
        if len(args) != 1:
            raise SyntaxError("type must be in form: type expression")
        return args[0].evaluate(call_env).__class__


class PrintFunction(BuiltinFunction):
    def apply(self, args, call_env):
        string = ' '.join([str(a.evaluate(call_env)) for a in args])
        print(string)
        return types.List()


# Built-in Macros

class BuiltinMacro(types.Macro):
    def __init__(self, env):
        self.env = env


class DefineMacro(BuiltinMacro):
    def apply(self, args, call_env):
        if len(args) != 2 or type(args[0]) is not types.Symbol:
            raise SyntaxError("define must be in form: define name expression")
        result = args[1].evaluate(call_env)
        call_env.set(args[0], result)
        return result


class QuoteMacro(BuiltinMacro):
    def apply(self, args, call_env):
        if len(args) == 0:
            return types.List()
        return args[0]


class LambdaMacro(BuiltinMacro):
    def apply(self, args, call_env):
        if len(args) != 2 or type(args[0]) is not types.List:
            raise SyntaxError("lambda must be of form: lambda args expression")
        for arg in args[0]:
            if type(arg) is not types.Symbol:
                raise SyntaxError("lambda argument list must be comprised of symbols")
            return types.Function(args[0], args[1], call_env)


class FnMacro(BuiltinMacro):
    def apply(self, args, call_env):
        if len(args) != 3 or type(args[0]) is not types.Symbol or type(args[1]) is not types.List:
            raise SyntaxError("fn must be of form: fn name args expression")
        for arg in args[1]:
            if type(arg) is not types.Symbol:
                raise SyntaxError("fn argument list must be comprised only of symbols")
        function = types.Function(args[1], args[2], call_env)
        call_env.set(args[0], function)
        return function


class IfMacro(BuiltinMacro):
    def apply(self, args, call_env):
        if len(args) != 3:
            raise SyntaxError("if must be of form: if test then else")
        test = types.Boolean(args[0].evaluate(call_env))
        if test:
            return args[1].evaluate(call_env)
        else:
            return args[2].evaluate(call_env)
