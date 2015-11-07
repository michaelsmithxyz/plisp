from plisp import types

class Environment:
    def __init__(self, base=None):
        if base is None:
            self.table = {}
            self.macros = {}
            self.forms = {}
        else:
            self.table = base.table.copy()
            self.forms = base.forms.copy()
            self.macros = base.macros.copy()

    def _get_from_table(self, symbol, table):
        if symbol in table:
            return table[symbol]

    def _set_in_table(self, symbol, value, table):
        table[symbol] = value
        return value
    
    def in_forms(self, symbol):
        return symbol in self.forms

    def in_macros(self, symbol):
        return symbol in self.macros

    def in_symbols(self, symbol):
        return symbol in self.table

    def get_form(self, symbol):
        return self._get_from_table(symbol, self.forms)

    def set_form(self, symbol, value):
        return self._set_in_table(symbol, value, self.forms)

    def get_macro(self, symbol):
        return self._get_from_table(symbol, self.macros)

    def set_macro(self, symbol, macro):
        return self._set_in_table(symbol, macro, self.macros)

    def get_symbol(self, symbol):
        return self._get_from_table(symbol, self.table)

    def set_symbol(self, symbol, value):
        return self._set_in_table(symbol, value, self.table)

    def lookup(self, name):
        symbol = types.Symbol(name)
        if self.in_forms(symbol):
            return self.get_form(symbol)
        if self.in_macros(symbol):
            return self.get_macro(symbol)
        if self.in_symbols(symbol):
            return self.get_symbol(symbol)
        return None
