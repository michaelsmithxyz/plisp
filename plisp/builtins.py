from functools import reduce

from plisp import types
from plisp import environment


# Special forms

class LambdaForm(types.Callable):
    def apply(self, args, call_env):
        if len(args) != 2 or type(args[0]) is not types.List:
            raise SyntaxError("lambda must be of form: lambda args expression")
        for arg in args[0]:
            if type(arg) is not types.Symbol:
                raise SyntaxError("lambda argument list must be comprised of symbols")
            return types.Function(args[0], args[1], call_env)


class DefineForm(types.Callable):
    def apply(self, args, call_env):
        if len(args) != 2 or type(args[0]) is not types.Symbol:
            raise SyntaxError("define must be in form: define name expression")
        result = args[1].evaluate(call_env)
        call_env.set_symbol(args[0], result)
        return result


class QuoteForm(types.Callable):
    def apply(self, args, call_env):
        if len(args) == 0:
            return types.List()
        return args[0]


class UnQuoteForm(types.Callable):
    def apply(self, args, call_env):
        if len(args) == 0:
            return types.List()
        return args[0].evaluate(call_env)


class BackquoteForm(types.Callable):
    def backquote_evaluate(self, expr, env):
        if isinstance(expr, types.List):
            if len(expr) > 0:
                if (isinstance(expr.elements[0], types.Symbol) and
                        isinstance(env.get_form(expr.elements[0]), UnQuoteForm)):
                    return expr.evaluate(env)
            ret = []
            for e in expr.elements:
                ret.append(self.backquote_evaluate(e, env))
            return types.List(*ret)
        return expr

    def apply(self, args, call_env):
        if len(args) == 0:
            return types.List()
        return self.backquote_evaluate(args[0], call_env)


class FnForm(types.Callable):
    def apply(self, args, call_env):
        if len(args) != 3 or type(args[0]) is not types.Symbol or type(args[1]) is not types.List:
            raise SyntaxError("fn must be of form: fn name args expression")
        for arg in args[1]:
            if type(arg) is not types.Symbol:
                raise SyntaxError("fn argument list must be comprised only of symbols")
        function = types.Function(args[1], args[2], call_env)
        call_env.set_symbol(args[0], function)
        return function


class IfForm(types.Callable):
    def apply(self, args, call_env):
        if len(args) != 3:
            raise SyntaxError("if must be of form: if test then else")
        test = types.Boolean(args[0].evaluate(call_env))
        if test:
            return args[1].evaluate(call_env)
        else:
            return args[2].evaluate(call_env)


class DoForm(types.Callable):
    def apply(self, args, call_env):
        res = types.List()
        for expr in args:
            res = expr.evaluate(call_env)
        return res


class DotForm(types.Callable):
    def apply(self, args, call_env):
        if len(args) != 2:
            raise SyntaxError(". must be of form: . container field")
        container = args[0].evaluate(call_env)
        return types.to_lisp_type(getattr(container, str(args[1].evaluate(call_env))))


class BangForm(types.Callable):
    def apply(self, args, call_env):
        if len(args) == 0:
            raise SyntaxError("! must be of form: ! callable args")
        fn = args[0].evaluate(call_env)
        return types.to_lisp_type(fn(*[e.evaluate(call_env).pytype() for e in args[1:]]))


class DefMacroForm(types.Callable):
    def apply(self, args, call_env):
        if len(args) != 3 or not isinstance(args[0], types.Symbol) or not isinstance(args[1], types.List):
            raise SyntaxError("defmacro must be of form: defmacro name args expression")
        for arg in args[1]:
            if type(arg) is not types.Symbol:
                raise SyntaxError("defmacro argument list must be comprised of symbols")
        macro = types.Macro(args[1], args[2])
        call_env.set_macro(args[0], macro)
        return macro


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
        return types.Boolean(args[0].evaluate(call_env) == args[1].evaluate(call_env))


class ListFunction(BuiltinFunction):
    def apply(self, args, call_env):
        return types.List(*[e.evaluate(call_env) for e in args])


class FirstFunction(BuiltinFunction):
    def apply(self, args, call_env):
        if len(args) != 1:
            raise Exception("Arity error")
        tgt = args[0].evaluate(call_env)
        if not isinstance(tgt, types.List):
            raise SyntaxError("first only accepts a list")
        if len(tgt) == 0:
            return types.List()
        return tgt.elements[0]


class RestFunction(BuiltinFunction):
    def apply(self, args, call_env):
        if len(args) != 1:
            raise Exception("Arity error")
        tgt = args[0].evaluate(call_env)
        if not isinstance(tgt, types.List):
            raise SyntaxError("rest only accepts a list")
        return types.List(*tgt.elements[1:])


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


class ImportFunction(BuiltinFunction):
    def apply(self, args, call_env):
        if len(args) != 1:
            raise SyntaxError("import must be in form: import name")
        name = args[0].evaluate(call_env)
        if type(name) is not types.String:
            raise SyntaxError("import only accepts a string")
        try:
            mod = __import__(name.value)
        except ImportError as e:
            if name.value in __builtins__:
                return __builtins__[name.value]
            raise
        return mod


# Built-in Macros

class BuiltinMacro(types.Macro):
    def __init__(self, env):
        self.env = env



