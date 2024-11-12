import tkinter as tk
from controlador.controladorVentanaPrincipal import ControladorVentanaPrincipal

if __name__ == "__main__":
    root = tk.Tk()
    controlador = ControladorVentanaPrincipal(root)
    root.mainloop()