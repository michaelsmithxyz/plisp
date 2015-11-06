import re


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return str((str(self.type), str(self.value)))

    def __repr__(self):
        return str(self)


class Tokenizer:
    def __init__(self, string, tokens, start=0):
        self.string = string
        self.tokens = tokens
        self.pos = start

    def peek(self):
        if self.pos > len(self.string):
            return None
        for regex, tok_type in self.tokens:
            match = re.match(regex, self.string[self.pos:])
            if match is not None:
                value = match.group(0)
                return Token(tok_type, value)
        return None

    def consume(self, predicate=lambda t: True):
        token = self.peek()
        if token is not None:
            self.pos += len(token.value)
        if token is None or predicate(token):
            return token
        return self.consume(predicate=predicate)

    def __iter__(self):
        tok = self.consume()
        while tok is not None:
            yld = tok
            tok = self.consume()
            yield yld
