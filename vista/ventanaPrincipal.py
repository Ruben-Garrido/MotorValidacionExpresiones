import tkinter as tk
from tkinter import simpledialog

class VentanaPrincipal:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("EVALUADOR DE EXPRESIONES REGULARES")
        
        self.output_area = tk.Text(self.root, height=15, width=70)
        self.output_area.pack(pady=10)

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

    def mostrar_resultado(self, mensaje):
        self.output_area.insert(tk.END, mensaje + "\n")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            if widget != self.output_area:
                widget.destroy()
