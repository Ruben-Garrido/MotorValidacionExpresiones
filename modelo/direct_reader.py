from modelo.tokens import Token, TokenType

LETTERS = 'abcdefghijklmnopqrstuvwxyz01234567890.' #alfabeto del programa

#Esta clase esta encargada de leer y asignar los tokens de los simbols, que nos ayudara a construir el arbol sintatico
class DirectReader:

    def __init__(self, string: str):
        self.string = iter(string.replace(' ', ''))#borra los espacios de la expresion y se itera caracter por caracter
        self.input = set()#Conjunto que almacenará los caracteres válidos del alfabeto detectados en la expresión.
        self.rparPending = False#Bandera para determinar si es necesario insertar un token 
        self.Next()#Llama a un método que avanza al siguiente carácter en el iterador

    def Next(self):
        try:
            self.curr_char = next(self.string)
        except StopIteration:
            self.curr_char = None
    # Aqui generamos los tokens necesarios para su descomposicion
    def CreateTokens(self):
        while self.curr_char != None:

            if self.curr_char in LETTERS:
                self.input.add(self.curr_char)
                yield Token(TokenType.LETTER, self.curr_char)

                self.Next()

                # Finalmente, verifique si necesitamos agregar un token de adición
                if self.curr_char != None and \
                        (self.curr_char in LETTERS or self.curr_char == '('):
                    yield Token(TokenType.APPEND, '.')

            elif self.curr_char == '|':
                yield Token(TokenType.OR, '|')

                self.Next()

                if self.curr_char != None and self.curr_char not in '()':
                    yield Token(TokenType.LPAR)

                    while self.curr_char != None and self.curr_char not in ')*+?':
                        if self.curr_char in LETTERS:
                            self.input.add(self.curr_char)
                            yield Token(TokenType.LETTER, self.curr_char)

                            self.Next()
                            if self.curr_char != None and \
                                    (self.curr_char in LETTERS or self.curr_char == '('):
                                yield Token(TokenType.APPEND, '.')

                    if self.curr_char != None and self.curr_char in '*+?':
                        self.rparPending = True
                    elif self.curr_char != None and self.curr_char == ')':
                        yield Token(TokenType.RPAR, ')')
                    else:
                        yield Token(TokenType.RPAR, ')')

            elif self.curr_char == '(':
                self.Next()
                yield Token(TokenType.LPAR)

            elif self.curr_char in (')*+?'):

                if self.curr_char == ')':
                    self.Next()
                    yield Token(TokenType.RPAR)

                elif self.curr_char == '*':
                    self.Next()
                    yield Token(TokenType.KLEENE)

                elif self.curr_char == '+':
                    self.Next()
                    yield Token(TokenType.PLUS)

                elif self.curr_char == '?':
                    self.Next()
                    yield Token(TokenType.QUESTION)

                if self.rparPending:
                    yield Token(TokenType.RPAR)
                    self.rparPending = False

                # Finalmente, verifique si necesitamos agregar un token de adición
                if self.curr_char != None and \
                        (self.curr_char in LETTERS or self.curr_char == '('):
                    yield Token(TokenType.APPEND, '.')

            else:
                raise Exception(f'Invalid entry: {self.curr_char}')

        yield Token(TokenType.APPEND, '.')
        yield Token(TokenType.LETTER, '#')

    def GetSymbols(self):#Devolvemos el cojunto de simbolos validos
        return self.input
