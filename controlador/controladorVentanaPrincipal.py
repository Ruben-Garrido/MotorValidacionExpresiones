import re
from vista.ventanaPrincipal import VentanaPrincipal
import tkinter as tk
from modelo.reader import Reader
from modelo.parsing import Parser
from modelo.direct_dfa import DDFA
from modelo.direct_reader import DirectReader
from PIL import Image, ImageTk

class ControladorVentanaPrincipal:
    def __init__(self, root):
        self.ventana = VentanaPrincipal(root, self)
        self.regex = None
        self.tree = None
        
    def set_regex(self):
        self.regex = self.ventana.pedir_expresion_regular()
        if self.regex:
            
            try:
                # Intentamos compilar la expresión regular para verificar si es válida
                re.compile(self.regex)  # Esto lanzará un error si la regex es inválida
                reader = Reader(self.regex)
                tokens = reader.CreateTokens()
                parser = Parser(tokens)
                self.tree = parser.Parse()
                self.ventana.mostrar_resultado(f"Expresión aceptada: {self.regex}", resaltar=True)
                
            except re.error as regex_error:  # Capturamos errores específicos de regex
                # Mostramos detalles del error
                error_message = f"Error en la expresión regular:\n"
                error_message += f"Posición: {regex_error.pos}\n"
                error_message += f"Parte incorrecta: {self.regex[regex_error.pos-5:regex_error.pos+5]}"  # Mostramos la parte de la regex alrededor del error
                self.ventana.mostrar_resultado(error_message)
            except Exception as e:
                self.ventana.mostrar_resultado(f"Error: {e}")
                
    def test_string(self):
        if not self.regex:
            self.ventana.mostrar_resultado("Error: Debes establecer una expresión regular primero.")
            return

        self.ventana.clear_frame()
        tk.Label(self.ventana.root, text="Seleccione el método:", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.ventana.root, text="DFA Directo", command=self.metodo_directo_dfa).pack(pady=5)
        tk.Button(self.ventana.root, text="Volver al menú principal", command=self.ventana.main_menu).pack(pady=5)

    def metodo_directo_dfa(self):
        input_string = self.ventana.pedir_cadena()
        if input_string:
            try:
                direct_reader = DirectReader(self.regex)
                direct_tokens = direct_reader.CreateTokens()
                direct_parser = Parser(direct_tokens)
                direct_tree = direct_parser.Parse()

                dfa = DDFA(direct_tree, direct_reader.GetSymbols(), input_string)
                dfa_result = dfa.EvalRegex()
                
                dfa.GraphDFA()
                self.ventana.mostrar_resultado(f"\nResultado con DFA Directo: {dfa_result}")
                
                dfa_image = Image.open('./salidas/DirectDFA.png')
                dfa_photo = ImageTk.PhotoImage(dfa_image)
                
                label_dfa_image = tk.Label(self.ventana.root, image=dfa_photo)
                label_dfa_image.image = dfa_photo
                label_dfa_image.pack(pady=10)
                
            except Exception as e:
                self.ventana.mostrar_resultado(f"Error al procesar la cadena: {e}")
