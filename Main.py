import os
from parsing import Parser
from reader import Reader
from PIL import Image, ImageTk
from nfa import NFA
from dfa import DFA
from direct_dfa import DDFA
from direct_reader import DirectReader
import tkinter as tk
from tkinter import simpledialog


class FiniteAutomataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EVALUADOR DE EXPRESIONES REGULARES")
        self.regex = None
        self.tree = None

        self.output_area = tk.Text(self.root, height=15, width=70)
        self.output_area.pack(pady=10)

        self.main_menu()

    def main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="¿Qué te gustaría hacer?", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.root, text="Establecer una expresión regular", command=self.set_regex).pack(pady=5)
        tk.Button(self.root, text="Probar una cadena con la expresión regular", command=self.test_string).pack(pady=5)
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=5)

    def set_regex(self):
        self.regex = simpledialog.askstring("Entrada", "Escriba una expresión regular:")
        if self.regex:
            try:
                self.reader = Reader(self.regex)
                tokens = self.reader.CreateTokens()
                parser = Parser(tokens)
                self.tree = parser.Parse()
                self.output_area.insert(tk.END, f"Expresión aceptada: {self.regex}\n")
                
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {e}\n")

    def test_string(self):
        if not self.regex:
            self.output_area.insert(tk.END, "Error: Debes establecer una expresión regular primero.\n")
            return

        self.clear_frame()
        tk.Label(self.root, text="Seleccione el método:", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.root, text="Método de Thompson", command=self.metodo_thompson).pack(pady=5)
        tk.Button(self.root, text="Método DFA Directo", command=self.metodo_directo_dfa).pack(pady=5)
        tk.Button(self.root, text="Volver al menú principal", command=self.main_menu).pack(pady=5)

    def metodo_thompson(self):
        input_string = simpledialog.askstring("Entrada", "Ingrese la cadena:")
        if input_string:
            try:
                nfa = NFA(self.tree, self.reader.GetSymbols(), input_string)
                
                nfa_result = nfa.EvalRegex()
                self.output_area.insert(tk.END, f"\nResultado NFA (Thompson): {nfa_result}\n")
                dfa = DFA(nfa.trans_func, nfa.symbols, nfa.curr_state, nfa.accepting_states, input_string)
                dfa.TransformNFAToDFA()
                #dfa_result = dfa.EvalRegex()
                #self.output_area.insert(tk.END, f"\nResultado DFA (Powerset): {dfa_result}\n")
                
                
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {e}\n")

    def metodo_directo_dfa(self):
        input_string = simpledialog.askstring("Entrada", "Ingrese la cadena:")
        if input_string:
            try:
                direct_reader = DirectReader(self.regex)
                direct_tokens = direct_reader.CreateTokens()
                direct_parser = Parser(direct_tokens)
                direct_tree = direct_parser.Parse()

                dfa = DDFA(direct_tree, direct_reader.GetSymbols(), input_string)
                
                dfa_result = dfa.EvalRegex()
                               
                dfa.GraphDFA()
                self.output_area.insert(tk.END, f"\nResultado con DFA Directo: {dfa_result}\n")
                
                # Carga y muestra la imagen del DFA
                dfa_image = Image.open('./output/DirectDFA.png')
                dfa_photo = ImageTk.PhotoImage(dfa_image)
                
                # Muestra la imagen en la interfaz
                label_dfa_image = tk.Label(self.root, image=dfa_photo)
                label_dfa_image.image = dfa_photo  # Referencia para mantener la imagen
                label_dfa_image.pack(pady=10)
               
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {e}\n")
                
        
    def clear_frame(self):
        for widget in self.root.winfo_children():
            if widget != self.output_area:
                widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FiniteAutomataApp(root)
    root.mainloop()

