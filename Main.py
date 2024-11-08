
from parsing import Parser
from reader import Reader
from tkinter import simpledialog
from nfa import NFA
import tkinter as tk


class FiniteAutomataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evaluador de expresiones regulares")

        self.regex = None
        self.method = None
        self.tree = None

        self.output_area = tk.Text(self.root, height=10, width=50)
        self.output_area.pack(pady=10)

        self.main_menu()

    def main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="¿Qué te gustaría hacer?", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.root, text="Ingrese la expresión regular", command=self.set_regex).pack(pady=5)
        tk.Button(self.root, text="Prueba una cadena con la expresión regular dada", command=self.test_string).pack(pady=5)
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=5)

    def set_regex(self):
        self.regex = simpledialog.askstring("Entrada", "Escriba una expresión regular:")
        if self.regex:
            self.output_area.insert(tk.END, "Expresión aceptada: {}\n".format(self.regex))
            # Aquí puedes agregar el código para crear tokens y parsear
            self.reader = Reader(self.regex)  # Inicializa el reader aquí
            tokens = self.reader.CreateTokens()
            parser = Parser(tokens)
            self.tree = parser.Parse()  # Inicializa el tree aquí

    def test_string(self):
        if not self.regex:
            self.output_area.insert(tk.END, "Error: Debes establecer una expresión regular primero.\n")
            return

        self.clear_frame()
        tk.Label(self.root, text="Seleccione el método:", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.root, text="Método de Thompson", command=self.thompson_method).pack(pady=5)
        tk.Button(self.root, text="Método DFA directo", command=self.direct_dfa_method).pack(pady=5)
        tk.Button(self.root, text="Volver al menú principal", command=self.main_menu).pack(pady=5)

    def thompson_method(self):
        input_string = simpledialog.askstring("Entrada", "Ingrese la cadena:")
        if input_string:
            try:
                # Configura self.regex con la cadena de entrada para que EvalRegex pueda usarla
                self.regex = input_string  # Asigna la cadena a self.regex antes de llamar a EvalRegex

                nfa = NFA(self.tree, self.reader.GetSymbols(), self.regex)
                nfa_regex = nfa.EvalRegex()  # Llama a EvalRegex sin argumentos
            
                # Prepara el resultado
                result = "Resultado de la evaluación con NFA (método de Thompson): {}\n".format(nfa_regex)
                
                self.output_area.insert(tk.END, result)
                
            except Exception as e:
                self.output_area.insert(tk.END, "Error: {}\n".format(e))




    def direct_dfa_method(self):
        input_string = simpledialog.askstring("Entrada", "Ingrese la cadena:")
        if input_string:
         
            # Aquí va la lógica para Direct DFA
            # Simulación de evaluación, reemplace esto con la lógica real
            result = "Resultado de la evaluación con DFA directo: {} \n".format(input_string)
           
            
            self.output_area.insert(tk.END, result)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            if widget != self.output_area:  # No eliminar el área de texto
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FiniteAutomataApp(root)
    root.mainloop()


