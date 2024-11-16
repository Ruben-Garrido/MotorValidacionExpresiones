from modelo.tokens import Token, TokenType

LETTERS = 'abcdefghijklmnopqrstuvwxyz01234567890.' #abecedario del programa

"""analizar y tokenizar una expresión regular proporcionada como entrada. Convierte la expresión
en una secuencia de tokens, que son representaciones abstractas de los elementos individuales 
(símbolos, operadores, paréntesis, etc.)"""
class Reader:#basicamente este es nuestro analizador quien convierte la cadena en algo que el programa 
    #pueda modelar y funcion de igual forma que el direct reader
    def __init__(self, string: str):
        self.string = iter(string.replace(' ', ''))
        self.input = set()
        self.Next()

    def Next(self):
        try:
            self.curr_char = next(self.string)
        except StopIteration:
            self.curr_char = None

    def CreateTokens(self):
        while self.curr_char != None:

            if self.curr_char in LETTERS:
                self.input.add(self.curr_char)
                yield Token(TokenType.LPAR, '(')
                yield Token(TokenType.LETTER, self.curr_char)

                self.Next()
                added_parenthesis = False

                while self.curr_char != None and \
                        (self.curr_char in LETTERS or self.curr_char in '*+?'):

                    if self.curr_char == '*':
                        yield Token(TokenType.KLEENE, '*')
                        yield Token(TokenType.RPAR, ')')
                        added_parenthesis = True

                    elif self.curr_char == '+':
                        yield Token(TokenType.PLUS, '+')
                        yield Token(TokenType.RPAR, ')')
                        added_parenthesis = True

                    elif self.curr_char == '?':
                        yield Token(TokenType.QUESTION, '?')
                        yield Token(TokenType.RPAR, ')')
                        added_parenthesis = True

                    elif self.curr_char in LETTERS:
                        self.input.add(self.curr_char)
                        yield Token(TokenType.APPEND)
                        yield Token(TokenType.LETTER, self.curr_char)

                    self.Next()

                    if self.curr_char != None and self.curr_char == '(' and added_parenthesis:
                        yield Token(TokenType.APPEND)

                if self.curr_char != None and self.curr_char == '(' and not added_parenthesis:
                    yield Token(TokenType.RPAR, ')')
                    yield Token(TokenType.APPEND)

                elif not added_parenthesis:
                    yield Token(TokenType.RPAR, ')')

            elif self.curr_char == '|':
                self.Next()
                yield Token(TokenType.OR, '|')

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

                # Finalmente, verifique si necesitamos agregar un token de adición
                if self.curr_char != None and \
                        (self.curr_char in LETTERS or self.curr_char == '('):
                    yield Token(TokenType.APPEND, '.')

            else:
                raise Exception(f'Invalid entry: {self.curr_char}')

    def GetSymbols(self):
        return self.input
