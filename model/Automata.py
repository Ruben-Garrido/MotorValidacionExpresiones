import re
import graphviz

class Automata:
    def __init__(self, regex):
        self.regex = regex
        self.automata = None

    def validar_cadena(self, cadena):
        """Valida si la cadena cumple con la expresión regular."""
        patron = re.compile(self.regex)
        return bool(patron.fullmatch(cadena))

    def generar_imagen_automata(self):
        # Crea el autómata y genera su representación en Graphviz
        dot = graphviz.Digraph(format='png')
        # Aquí deberías agregar nodos y aristas según tu autómata
        dot.node('A', 'Estado A')
        dot.node('B', 'Estado B')
        dot.edge('A', 'B', label='a')
        dot.edge('A', 'A', label='b')  # Transiciones adicionales si es necesario


        # Renderiza la imagen en un objeto en memoria
        imagen_en_memoria = dot.pipe()
        return imagen_en_memoria

