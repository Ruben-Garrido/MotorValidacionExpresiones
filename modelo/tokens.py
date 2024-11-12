from enum import Enum

#son las diferentes operaciones que aparecen en la expresion y su precedencia   
class TokenType(Enum):
    LETTER = 0
    APPEND = 1
    OR = 2
    KLEENE = 3
    PLUS = 4
    QUESTION = 5
    LPAR = 6
    RPAR = 7


class Token:
    def __init__(self, type: TokenType, value=None):
        self.type = type                           #type, Almacena el tipo de token
        self.value = value                         #value,Almacena un valor adicional asociado con el token
        self.precedence = type.value               #Almacena la precedencia del token

    def __repr__(self):
        return f'{self.type.name}: {self.value}'   #devuelve una representación en cadena del objeto token osea la clase token.
