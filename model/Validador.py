import re

class Validador:
    def __init__(self, expresion_regular):
        self.expresion = expresion_regular
        self.patron = re.compile(expresion_regular)

    def validar_cadena(self, cadena):
        return bool(self.patron.fullmatch(cadena))
