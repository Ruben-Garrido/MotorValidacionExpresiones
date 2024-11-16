import re
import tkinter as tk
from tkinter import simpledialog

#Esta clase es la ventana principal de la app 
class VentanaPrincipal:
    def __init__(self, root, controlador):#Los init son los contructores de las clases
        self.root = root
        self.controlador = controlador
        self.root.title("EVALUADOR DE EXPRESIONES REGULARES")
        
        self.output_area = tk.Text(self.root, height=15, width=60)## ajuste de la ventana
        self.output_area.pack(pady=10)
        
        # Configuración de tags para colores
        self.output_area.tag_configure("verde", foreground="green")
        self.output_area.tag_configure("azul", foreground="blue")
        self.output_area.tag_configure("rojo", foreground="red")  
        
        self.main_menu()

    def main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="¿Qué te gustaría hacer?", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.root, text="Establecer una expresión regular", command=self.controlador.set_regex).pack(pady=5)
        tk.Button(self.root, text="Probar una cadena con la expresión regular", command=self.controlador.test_string).pack(pady=5)
        tk.Button(self.root, text="Salir", command=self.root.quit, bg="red", fg="white").pack(pady=5)

    def pedir_expresion_regular(self):
        return simpledialog.askstring("Entrada", "Escriba una expresión regular:")

    def pedir_cadena(self):
        return simpledialog.askstring("Entrada", "Ingrese la cadena:")

    def mostrar_resultado(self, mensaje, resaltar=False):
        self.output_area.delete(1.0, tk.END)  # Limpiar el área de texto antes de mostrar. Esto con el fin de evitar otros errores
        if resaltar:
            self.resaltar_sintaxis(mensaje)
        else:
            self.output_area.insert(tk.END, mensaje + "\n")

    def resaltar_sintaxis(self, expresion_regular):
        # Definimos los patrones y colores que queremos resaltar
        patrones = [
            (r"([()])", "azul"),         # Paréntesis () en azul
             (r"([|])", "verde"),         # barra o |  en verde
            (r"(\+|\*)", "rojo"),          # Operadores + y * en rojo
           
        ]
        
        # Insertamos el texto completo primero
        self.output_area.insert(tk.END, expresion_regular)
        
        # Iterar a través de cada patrón y lo aplica
        for patron, color in patrones:
            # Buscamos las coincidencias para cada patrón
            for match in re.finditer(patron, expresion_regular):
                start_idx = self.output_area.index(f"1.0 + {match.start()} chars")  # Índice de inicio
                end_idx = self.output_area.index(f"1.0 + {match.end()} chars")    # Índice de fin
                self.output_area.tag_add(color, start_idx, end_idx)  # Aplicamos el tag de color

    def clear_frame(self):# Metodo para limpiar
        for widget in self.root.winfo_children():
            if widget != self.output_area:
                widget.destroy()
