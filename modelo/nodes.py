"""representan los nodos que componen el árbol sintáctico de una expresión regular.
Cada clase modela un operador o símbolo específico en la expresión regular y forma parte del 
proceso de construir y manipular el árbol sintáctico para generar un autómata finito"""

class Letter:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'


class Append():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'({self.a}.{self.b})'


class Or():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'({self.a}|{self.b})'


class Kleene():
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f'{self.a}*'


class Plus():
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f'{self.a}+'


class Expression():
    def __init__(self, a, b=None):
        self.a = a
        self.b = b

    def __repr__(self):
        if self.b != None:
            return f'{self.a}{self.b}'
        return f'{self.a}'
