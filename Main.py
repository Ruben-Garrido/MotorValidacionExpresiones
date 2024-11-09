from parsing import Parser
from reader import Reader
from PIL import Image, ImageTk
from nfa import NFA
from dfa import DFA
from direct_dfa import DDFA
from direct_reader import DirectReader
import tkinter as tk
from tkinter import Image, simpledialog
from time import process_time


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
        tk.Button(self.root, text="Método de Thompson", command=self.thompson_method).pack(pady=5)
        tk.Button(self.root, text="Método DFA Directo", command=self.direct_dfa_method).pack(pady=5)
        tk.Button(self.root, text="Volver al menú principal", command=self.main_menu).pack(pady=5)

    def thompson_method(self):
        input_string = simpledialog.askstring("Entrada", "Ingrese la cadena:")
        if input_string:
            try:
                nfa = NFA(self.tree, self.reader.GetSymbols(), input_string)
                
                nfa_result = nfa.EvalRegex()
                end_time = process_time()
                self.output_area.insert(tk.END, f"\nResultado NFA (Thompson): {nfa_result}\n")
               
                dfa = DFA(nfa.trans_func, nfa.symbols, nfa.curr_state, nfa.accepting_states, input_string)
                dfa.TransformNFAToDFA()
                
                dfa_result = dfa.EvalRegex()
                end_time = process_time()
                self.output_area.insert(tk.END, f"\nResultado DFA (Powerset): {dfa_result}\n")
                
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {e}\n")

    def direct_dfa_method(self):
        input_string = simpledialog.askstring("Entrada", "Ingrese la cadena:")
        if input_string:
            try:
                direct_reader = DirectReader(self.regex)
                direct_tokens = direct_reader.CreateTokens()
                direct_parser = Parser(direct_tokens)
                direct_tree = direct_parser.Parse()

                dfa = DDFA(direct_tree, direct_reader.GetSymbols(), input_string)
                
                dfa_result = dfa.EvalRegex()
                
                self.output_area.insert(tk.END, f"\nResultado con DFA Directo: {dfa_result}\n")
               
            except Exception as e:
                self.output_area.insert(tk.END, f"Error: {e}\n")
                
                ## metodos para ver el automata
                
    def display_diagrams(self, nfa, dfa):
        nfa.WriteNFADiagram("nfa_diagram.png")
        dfa.GraphDFA("dfa_diagram.png")
        self.display_image("nfa_diagram.png", "DFA (Thompson y Powerset)")

    def display_diagram_ddfa(self, ddfa):
        ddfa.GraphDFA("direct_dfa_diagram.png")
        self.display_image("direct_dfa_diagram.png", "DFA Directo")

    def display_image(self, image_path, title):
        img = Image.open(image_path)
        img = img.resize((400, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.diagram_label.config(image=img, text=title, compound="top")
        self.diagram_label.image = img  # Necesario para evitar que la imagen sea recolectada por el recolector de basura


    def clear_frame(self):
        for widget in self.root.winfo_children():
            if widget != self.output_area:
                widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FiniteAutomataApp(root)
    root.mainloop()

