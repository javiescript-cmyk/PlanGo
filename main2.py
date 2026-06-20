# main2.py
import tkinter as tk
from config import COLOR_BG, COLOR_ESCUDO_RED
from auth import VistaAutenticacion
from dashboard import PanelEstudiante
from comercio_panel import PanelComercio

class AplicacionPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Two Pack — Ecosistema Urbano de Cochabamba")
 
        # Intentar cargar ícono si existe, si no ignora el error
        try:
            self.iconbitmap("icon.ico")
        except Exception:
            pass
 
        # Centrar ventana en la pantalla al abrir
        self.update_idletasks()
        ancho_ventana = 1100
        alto_ventana = 650
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.minsize(900, 580)
        self.configure(bg=COLOR_BG)
        
        self.vista_actual = None
        self.usuario_logueado = None
        
        # Arrancar mostrando el inicio de sesión
        self.cargar_autenticacion()

    def cambiar_vista(self, nueva_vista_clase, *args, **kwargs):
        # Si ya hay una pantalla dibujada, borrarla por completo
        if self.vista_actual is not None:
            self.vista_actual.destroy()
            
        # Instanciar la nueva pantalla dentro de la ventana principal
        self.vista_actual = nueva_vista_clase(self, *args, **kwargs)
        self.vista_actual.pack(fill="both", expand=True)

    def cargar_autenticacion(self):
        self.title("Two Pack - Iniciar Sesión")
        # Le pasamos la función que debe ejecutar cuando el login sea exitoso
        self.cambiar_vista(VistaAutenticacion, al_ingresar_exitoso=self.al_autenticar_usuario)

    def al_autenticar_usuario(self, datos_usuario):
        self.usuario_logueado = datos_usuario
        
        # Dependiendo del rol, cargar la pantalla correspondiente
        if datos_usuario.get("rol") == "Dueño de Negocio":
            self.title("Two Pack - Panel de Comercio Local")
            self.cambiar_vista(PanelComercio, al_cerrar_sesion=self.cargar_autenticacion)
        else:
            self.title("Two Pack - Dashboard Estudiante")
            # Cambiamos al Dashboard pasándole los datos capturados del estudiante
            self.cambiar_vista(PanelEstudiante, usuario_actual=self.usuario_logueado, al_cerrar_sesion=self.cargar_autenticacion)

if __name__ == "__main__":
    app = AplicacionPrincipal()
    app.mainloop()