import io
import tkinter as tk
from tkinter import messagebox
from controlador.ControladorVentana import ControladorVentana
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado

class VentanaPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Validador de Expresiones Regulares")

        tk.Label(self.root, text="Expresión Regular:").pack()
        self.regex_entry = tk.Entry(self.root, width=40)
        self.regex_entry.pack()

        tk.Label(self.root, text="Cadenas (separadas por coma):").pack()
        self.cadenas_entry = tk.Entry(self.root, width=40)
        self.cadenas_entry.pack()

        self.validar_button = tk.Button(self.root, text="Validar", command=self.validar)
        self.validar_button.pack()

        self.resultados_text = tk.Text(self.root, height=10, width=50)
        self.resultados_text.pack()

        self.automata_label = tk.Label(self.root)
        self.automata_label.pack()

        self.controlador = ControladorVentana(self)

    def validar(self):
        regex = self.regex_entry.get()
        cadenas = self.cadenas_entry.get().split(',')

        resultados = self.controlador.procesar_expresion(regex, cadenas)

        mensaje = "\n".join([f"'{cadena.strip()}': {'Válida' if es_valida else 'No válida'}" for cadena, es_valida in resultados])
        self.resultados_text.delete(1.0, tk.END)  # Limpiar el área de texto antes de mostrar nuevos resultados
        self.resultados_text.insert(tk.END, mensaje)

        # Mostrar el autómata
        self.mostrar_automata()

    def mostrar_automata(self):
        # Genera la imagen del autómata usando la instancia creada
        imagen_en_memoria = self.controlador.automata.generar_imagen_automata()

        # Cargar la imagen en Pillow
        imagen = Image.open(io.BytesIO(imagen_en_memoria))
        imagen.thumbnail((400, 300))  # Ajustar tamaño según necesites
        self.imagen_tk = ImageTk.PhotoImage(imagen)
        self.automata_label.config(image=self.imagen_tk)
        self.automata_label.image = self.imagen_tk  # Mantener una referencia


    def iniciar(self):
        self.root.mainloop()


