# model/AnalizadorExpresionesRegulares.py

from model.Automata import Automata

class AnalizadorExpresionesRegulares:
    def __init__(self, expresion):
        self.expresion = expresion
        self.automata = Automata()

    def generar_nfa(self):
        # Convertir la expresión regular en un autómata no determinista (NFA)
        # Este método debe implementar la conversión y es una versión simplificada para esta primera versión
        estado_inicial = self.automata.agregar_estado()
        estado_final = self.automata.agregar_estado(es_final=True)
        
        for simbolo in self.expresion:
            estado_inicial.agregar_transicion(simbolo, estado_final)

        return self.automata


    # validacion de cadena  
    def validar_cadena(self, cadena):
        return self.automata.validar_cadena(cadena)

    def generar_automata(self):
        # Aquí se crearía el autómata en función de la expresión regular
        automata = Automata(self.expresion)  # Suponiendo que Automata acepta la expresión en el constructor
        print(f"Autómata generado: {automata}")  # Debug para ver el objeto creado
        return automata