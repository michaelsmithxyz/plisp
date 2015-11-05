class Environment:
    def __init__(self, base=None):
        if base is None:
            self.table = {}
        else:
            self.table = base.table.copy()

    def lookup(self, symbol):
        if symbol in self.table:
            return self.table[symbol]
        return None

    def set(self, symbol, value):
        self.table[symbol] = value
        return value
