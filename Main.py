# Model/Main.py
from views.VentanaPrincipal import VentanaPrincipal
from controlador.ControladorVentana import ControladorVentana

class Main:
    def __init__(self):
        # Inicializar la ventana principal y el controlador
        self.ventana = VentanaPrincipal()
        self.controlador = ControladorVentana(self.ventana)
        

    def ejecutar(self):
        # Ejecuta la ventana principal
        self.ventana.mainloop()

if __name__ == "__main__":
    app = Main()
    app.ejecutar()

