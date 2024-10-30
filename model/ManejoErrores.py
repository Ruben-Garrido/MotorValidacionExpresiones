# model/ManejoErrores.py

class ManejoErrores:
    @staticmethod
    def validar_expresion(expresion):
        # En esta implementación básica, solo verificamos que la expresión no esté vacía
        if not expresion:
            print("Error: La expresión está vacía.")
            return False
        return True
