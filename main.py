
# Two Pack - Ecosistema Unificado de Ciudades Inteligentes
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import hashlib

from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
    COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_RAYO_YELLOW, COLOR_ESCUDO_RED,
    get_db_connection, configurar_animacion_boton
)
from auth import VistaAutenticacion
from dashboard import PanelEstudiante
from comercio_panel import PanelComercio

# --- CLASE PRINCIPAL DE APLICACIÓN ---
class TwoPackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Two Pack - Ecosistema de Ciudades Inteligentes")
        self.geometry("1100x650")
        self.minsize(900, 580)
        self.resizable(True, True)
        self.configure(bg=COLOR_BG)
        
        self.usuario_actual = None
        self.panel_actual = None
        
        # Empezar con la pantalla de autenticación
        self.cambiar_panel(VistaAutenticacion, self.al_ingresar_exitoso)

    def cambiar_panel(self, PanelClase, *args, **kwargs):
        if self.panel_actual:
            self.panel_actual.destroy()
        
        self.panel_actual = PanelClase(self, *args, **kwargs)
        self.panel_actual.pack(fill="both", expand=True)

    def al_ingresar_exitoso(self, usuario):
        self.usuario_actual = usuario
        if usuario["rol"] == "estudiante":
            self.cambiar_panel(PanelEstudiante, usuario, self.cerrar_sesion)
        else:
            self.cambiar_panel(PanelComercio, usuario, self.cerrar_sesion)
    
    def cerrar_sesion(self):
        self.usuario_actual = None
        self.cambiar_panel(VistaAutenticacion, self.al_ingresar_exitoso)

if __name__ == "__main__":
    app = TwoPackApp()
    app.mainloop()
