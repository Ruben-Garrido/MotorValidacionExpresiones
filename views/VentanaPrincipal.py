import tkinter as tk

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Validador de Expresiones Regulares")

        # Dimensiones de la ventana
        ancho_ventana = 600
        alto_ventana = 400

        # Calcula las coordenadas para centrar la ventana
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        posicion_x = (ancho_pantalla - ancho_ventana) // 2
        posicion_y = (alto_pantalla - alto_ventana) // 2

        # Configura el tamaño y posición de la ventana en la pantalla
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        # Etiqueta y entrada para la expresión regular
        tk.Label(self, text="Expresión Regular:").pack(pady=10)
        self.expresion_entry = tk.Entry(self)
        self.expresion_entry.pack()

        # Etiqueta y entrada para la cadena a validar
        tk.Label(self, text="Cadena(s) a validar (separadas por coma):").pack(pady=10)
        self.cadenas_entry = tk.Entry(self)
        self.cadenas_entry.pack()

        # Botón para iniciar la validación
        self.validar_button = tk.Button(self, text="Validar")
        self.validar_button.pack(pady=20)
     
        self.resultado_label = tk.Label(self, text="")
        self.resultado_label.pack()

