from model.Automata import Automata
from model.Validador import Validador

class ControladorVentana:
    def __init__(self, vista):
        self.vista = vista
        self.automata = None
        
    def procesar_expresion(self, regex, cadenas):
        validador = Validador(regex)
        self.automata = Automata(regex)
        resultados = [(cadena.strip(), validador.validar_cadena(cadena.strip())) for cadena in cadenas]
        return resultados
    
    def generar_imagen_automata(self):
        automata = Automata(self.ventana.regex_entry.get())  # Usa la expresión regular ingresada
        return automata.generar_imagen_automata()