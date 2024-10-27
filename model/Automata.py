# model/Automata.py

class Estado:
    def __init__(self, es_final=False):
        self.transiciones = {}  # Transiciones con formato {'simbolo': [estados_destino]}
        self.es_final = es_final  # Define si es un estado final

    def agregar_transicion(self, simbolo, estado_destino):
        if simbolo not in self.transiciones:
            self.transiciones[simbolo] = []
        self.transiciones[simbolo].append(estado_destino)

class Automata:
    def __init__(self):
        self.estados = []
        self.estado_inicial = None

    def agregar_estado(self, es_final=False):
        estado = Estado(es_final)
        self.estados.append(estado)
        if not self.estado_inicial:
            self.estado_inicial = estado
        return estado

    def validar_cadena(self, cadena):
        estados_actuales = [self.estado_inicial]
        
        for simbolo in cadena:
            nuevos_estados = []
            for estado in estados_actuales:
                if simbolo in estado.transiciones:
                    nuevos_estados.extend(estado.transiciones[simbolo])
            estados_actuales = nuevos_estados
            
        return any(estado.es_final for estado in estados_actuales)
    
    def validar(self, cadena):
        # Lógica para validar la cadena usando el autómata
        print(f"Validando la cadena: {cadena}")  # Debug para ver el proceso de validación
        # Aquí agregarías la lógica de validación real
        return True  # Temporal para pruebas; ajusta según la lógica de tu autómata
