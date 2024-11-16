import re
import tkinter as tk
from vista.ventanaPrincipal import VentanaPrincipal
from modelo.reader import Reader
from modelo.parsing import Parser
from modelo.direct_dfa import DDFA
from modelo.direct_reader import DirectReader
from PIL import Image, ImageTk
# Esta clase es el controlador de la ventana  es la que se encarga de unir la logica con la ventana
class ControladorVentanaPrincipal:
    def __init__(self, root):
        self.ventana = VentanaPrincipal(root, self)# se crea una instancia de la ventana para la comunicacion
        self.regex = None
        self.tree = None
        
    def set_regex(self):
        # Pedimos la expresión al usuario
        self.regex = self.ventana.pedir_expresion_regular()
        
        # Validamos si la expresión está vacía o compuesta solo por espacios
        if not self.regex.strip():
            self.ventana.mostrar_resultado("Por favor, ingrese una expresión regular válida.", resaltar=True)
            return  # Salimos del método sin continuar
        
        try:
            # Intentamos compilar la expresión regular para verificar si es válida
            re.compile(self.regex)  # Esto lanzará un error si la regex es inválida
            
            # Si es válida, procedemos con las siguientes etapas
            reader = Reader(self.regex)  # Llama a la clase Reader para analizar la expresión
            tokens = reader.CreateTokens()  # Crea los tokens
            parser = Parser(tokens)  # Analiza los tokens para generar el árbol sintáctico
            self.tree = parser.Parse()  # Guarda el árbol sintáctico
            
            # Mostramos el mensaje de éxito
            self.ventana.mostrar_resultado(f"Expresión aceptada: {self.regex}", resaltar=True)
        
        except re.error as regex_error:  # Capturamos errores específicos de la regex
            # Mostramos detalles del error
            error_message = f"Error en la expresión regular:\n"
            error_message += f"Posición: {regex_error.pos}\n"
            error_message += f"Parte incorrecta: {self.regex[regex_error.pos-5:regex_error.pos+5]}"  # Contexto del error
            self.ventana.mostrar_resultado(error_message)
        
        except Exception as e:
            # Mostramos cualquier otro error inesperado
            self.ventana.mostrar_resultado(f"Error: {e}")

    def test_string(self):
        if not self.regex:
            #Esto es por si, no se establece una expresion antes de ingresar una cadena
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
                direct_reader = DirectReader(self.regex)#Esta seccion es igual a la anterior solo que esta adactado para el metodo directo
                direct_tokens = direct_reader.CreateTokens()#crea los tokens
                direct_parser = Parser(direct_tokens)
                direct_tree = direct_parser.Parse()#Crea el arbo que es la mejor forma para entender los automatas

                dfa = DDFA(direct_tree, direct_reader.GetSymbols(), input_string)
                dfa_result = dfa.EvalRegex()
                
                dfa.GraphDFA()#Crea el automata
                self.ventana.mostrar_resultado(f"\nResultado con DFA Directo: {dfa_result}")#muestra el resultado
                
                dfa_image = Image.open('./salidas/DirectDFA.png')#ruta de donde lo va abrir 
                dfa_photo = ImageTk.PhotoImage(dfa_image)
                
                label_dfa_image = tk.Label(self.ventana.root, image=dfa_photo)# el nuevo area donde se va mostrar
                label_dfa_image.image = dfa_photo
                label_dfa_image.pack(pady=12)# el tamaño y ajuste de la nueva area donde se va mostrar 
                
            except Exception as e:## capturar error
                self.ventana.mostrar_resultado(f"Error al procesar la cadena: {e}")
