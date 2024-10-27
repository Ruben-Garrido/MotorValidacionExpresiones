# controller/ControladorVentana.py
# Controlador/ControladorVentana.py
class ControladorVentana:
    def __init__(self, ventana):
        self.ventana = ventana
        # Asocia el botón de validar con la función de validación
        self.ventana.validar_button.config(command=self.validar)

    def validar(self):
        # Obtener la expresión y las cadenas ingresadas
        expresion = self.ventana.expresion_entry.get()
        cadenas = self.ventana.cadenas_entry.get().split(',')

        # Aquí puedes agregar el código de validación usando el validador de expresiones
        resultados = [f"{cadena}: Validada" for cadena in cadenas]  # Esto es un ejemplo.
        
        # Mostrar resultados
        self.ventana.resultado_label.config(text="\n".join(resultados))
