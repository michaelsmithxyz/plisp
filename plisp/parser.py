import enum

import plisp.tokenizer as tokenizer
from plisp import types


class PLispTokens(enum.Enum):
    START_EXPR = 0
    END_EXPR = 1
    SYMBOL = 2
    NUMBER = 3
    STRING = 4
    QUOTE = 6
    BACKQUOTE = 7
    UNQUOTE = 8
    WHITESPACE = 9
    COMMENT = 10


class PLispParser:
    tokens = [
        (r'[\n\t ]+', PLispTokens.WHITESPACE),
        (r'\(', PLispTokens.START_EXPR),
        (r'\)', PLispTokens.END_EXPR),
        (r'[0-9]+', PLispTokens.NUMBER),
        (r'\'', PLispTokens.QUOTE),
        (r'`', PLispTokens.BACKQUOTE),
        (r',', PLispTokens.UNQUOTE),
        (r'[<>=\+\-\*/]', PLispTokens.SYMBOL),
        (r'[!\.#A-z]+[_A-z0-9\?]*', PLispTokens.SYMBOL),
        (r'"[^"]*"', PLispTokens.STRING),
        (r';.*(?:$|\n)', PLispTokens.COMMENT)
    ]

    class ParseError(Exception): pass
    
    def __init__(self, string):
        self.string = string
        self.tokenizer = tokenizer.Tokenizer(self.string, self.tokens)

    def get_token(self):
        return self.tokenizer.consume(lambda t: t.type not in (PLispTokens.WHITESPACE, PLispTokens.COMMENT))

    def parse_atom(self, token):
        if token.type is PLispTokens.NUMBER:
            return types.Number(token.value)
        elif token.type is PLispTokens.STRING:
            return types.String(token.value[1:-1])
        raise self.ParseError("Unknown atom type")

    def parse_symbol(self, token):
        return types.Symbol(token.value)

    def parse_quote(self, token):
        body = self.parse_expression(self.get_token())
        if body is None:
            raise self.ParseError("Invalid body for quote")
        return types.List(types.Symbol('quote'), body)

    def parse_backquote(self, token):
        body = self.parse_expression(self.get_token())
        if body is None:
            raise self.ParseError("Invalid body for backquote")
        return types.List(types.Symbol('backquote'), body)
    
    def parse_unquote(self, token):
        body = self.parse_expression(self.get_token())
        if body is None:
            raise self.ParseError("Invalid body for unquote")
        return types.List(types.Symbol("unquote"), body)

    def parse_list(self, token):
        lst = []
        next_token = self.get_token()
        if next_token is None:
            raise self.ParseError("Expected end of list before end of input")
        while next_token.type != PLispTokens.END_EXPR:
            lst.append(self.parse_expression(next_token))
            next_token = self.get_token()
            if next_token is None:
                raise self.ParseError("Expected end of list before end of input")
        return types.List(*lst)
    
    def parse_expression(self, token):
        if token is None:
            return None
        elif token.type == PLispTokens.NUMBER or token.type == PLispTokens.STRING:
            return self.parse_atom(token)
        elif token.type == PLispTokens.START_EXPR:
            return self.parse_list(token)
        elif token.type == PLispTokens.END_EXPR:
            raise self.ParseError("Unexpected end of list")
        elif token.type == PLispTokens.SYMBOL:
            return self.parse_symbol(token)
        elif token.type == PLispTokens.QUOTE:
            return self.parse_quote(token)
        elif token.type == PLispTokens.BACKQUOTE:
            return self.parse_backquote(token)
        elif token.type == PLispTokens.UNQUOTE:
            return self.parse_unquote(token)
        else:
            raise self.ParseError("Internal Error: Unhandled token type encountered: %s" % token)

    def parse(self):
        exprs = []
        expr = self.parse_expression(self.get_token())
        while expr is not None:
            exprs.append(expr)
            expr = self.parse_expression(self.get_token())
        return exprs
