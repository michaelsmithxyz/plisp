import enum

import plisp.tokenizer as tokenizer


class PLispTokens(enum.Enum):
    START_EXPR = 0
    END_EXPR = 1
    SYMBOL = 2
    ATOM = 3
    QUOTE = 4
    WHITESPACE = 5


class Expression:
    def __repr__(self):
        return str(self)


class Atom(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Symbol(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


class List(Expression):
    def __init__(self, *args):
        self.elements = args

    def __str__(self):
        return str(self.elements)


class Quote(Expression):
    def __init__(self, body):
        self.body = body

    def __str__(self):
        return '#' + str(self.body)


class ParseError(Exception): pass


class PLispParser:
    tokens = [
        (r'[\n\t ]+', PLispTokens.WHITESPACE),
        (r'\(', PLispTokens.START_EXPR),
        (r'\)', PLispTokens.END_EXPR),
        (r'[<>=\+\-\*/]', PLispTokens.SYMBOL),
        (r'[A-z]+[_A-z0-9]*', PLispTokens.SYMBOL),
        (r'[0-9]+', PLispTokens.ATOM),
        (r'#', PLispTokens.QUOTE),
        (r'".*"', PLispTokens.ATOM)
    ]
    
    def __init__(self, string):
        self.string = string
        self.tokenizer = tokenizer.Tokenizer(self.string, self.tokens)

    def get_token(self):
        return self.tokenizer.consume(lambda t: t.type != PLispTokens.WHITESPACE)

    def parse_atom(self, token):
        return Atom(token.value)

    def parse_symbol(self, token):
        return Symbol(token.value)

    def parse_quote(self, token):
        body = self.parse_expression(self.get_token())
        if body is None:
            raise ParseError("Invalid body for quote")
        return Quote(body)

    def parse_list(self, token):
        lst = []
        next_token = self.get_token()
        if next_token is None:
            raise ParseError("Expected end of list before end of input")
        while next_token.type != PLispTokens.END_EXPR:
            lst.append(self.parse_expression(next_token))
            next_token = self.get_token()
            if next_token is None:
                raise ParseError("Expected end of list before end of input")
        return List(*lst)
    
    def parse_expression(self, token):
        if token is None:
            return None
        elif token.type == PLispTokens.ATOM:
            return self.parse_atom(token)
        elif token.type == PLispTokens.START_EXPR:
            return self.parse_list(token)
        elif token.type == PLispTokens.END_EXPR:
            raise ParseError("Unexpected end of list")
        elif token.type == PLispTokens.SYMBOL:
            return self.parse_symbol(token)
        elif token.type == PLispTokens.QUOTE:
            return self.parse_quote(token)
        else:
            raise ParseError("Internal Error: Unhandled token type encountered: %s" % token)

    def parse(self):
        exprs = []
        expr = self.parse_expression(self.get_token())
        while expr is not None:
            exprs.append(expr)
            expr = self.parse_expression(self.get_token())
        return exprs
