

import tkinter as tk
from tkinter import ttk
import re
import hashlib
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
    COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_AMARILLO_ORO, COLOR_ESCUDO_RED,
    cargar_datos, guardar_datos, configurar_animacion_boton, configurar_animacion_enlace
)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class VistaAutenticacion(tk.Frame):
    def __init__(self, parent, al_ingresar_exitoso):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.al_ingresar_exitoso = al_ingresar_exitoso
        self.modo_registro = False
        self.es_comercio = False
        self.datos = cargar_datos()
        
        self.mostrar_splash()

    def mostrar_splash(self):
        # Pantalla de bienvenida que dura 2.5 segundos
        self.frame_splash = tk.Frame(self, bg=COLOR_ESCUDO_RED)
        self.frame_splash.place(relx=0, rely=0, 
                                 relwidth=1, relheight=1)
 
        # Dibujar el logo grande centrado
        canvas_s = tk.Canvas(self.frame_splash, 
                              width=400, height=300, 
                              bg=COLOR_ESCUDO_RED, bd=0, 
                              highlightthickness=0)
        canvas_s.pack(expand=True, pady=(40, 10))
        
        # Texto Two Pack cursivo
        canvas_s.create_text(202, 130, text="Two Pack", 
                             font=("Georgia", 48, "bold", "italic"), 
                             fill="#B31028")
        canvas_s.create_text(200, 130, text="Two Pack", 
                             font=("Georgia", 48, "bold", "italic"), 
                             fill=COLOR_TEXT_MAIN)
        
        # Subtítulo
        canvas_s.create_text(200, 190, text="Plataforma de Smart Economy para Cochabamba", 
                             font=("Helvetica", 11), 
                             fill="#FFCCCC")
        
        tk.Label(self.frame_splash, 
                 text="Divide el gasto, duplica la experiencia.", 
                 font=("Helvetica", 12, "italic"), 
                 bg=COLOR_ESCUDO_RED, fg=COLOR_AMARILLO_ORO).pack(pady=(0, 10))
 
        tk.Label(self.frame_splash, 
                 text="Cargando plataforma...", 
                 font=("Helvetica", 10), 
                 bg=COLOR_ESCUDO_RED, fg="#FFCCCC").pack()
 
        # Destruir splash y mostrar login después de 2.5s
        self.after(2500, self._terminar_splash)

    def _terminar_splash(self):
        self.frame_splash.destroy()
        self.mostrar_login_registro()

    def dibujar_escudo(self, parent, width=200, height=120):
        canvas = tk.Canvas(parent, width=width, height=height, bg=COLOR_BG, bd=0, highlightthickness=0)
        
        # Texto Two Pack cursivo
        canvas.create_text(width//2 + 1, height//2 - 10 + 1, text="Two Pack", 
                             font=("Georgia", 32, "bold", "italic"), 
                             fill="#C41430")
        canvas.create_text(width//2, height//2 - 10, text="Two Pack", 
                             font=("Georgia", 32, "bold", "italic"), 
                             fill=COLOR_TEXT_MAIN)
        
        # Texto Smart Economy
        canvas.create_text(width//2, height//2 + 25, text="SMART ECONOMY", 
                             font=("Helvetica", 10, "bold"), 
                             fill=COLOR_AMARILLO_ORO)
        
        return canvas

    def mostrar_login_registro(self):
        for widget in self.winfo_children():
            widget.destroy()

        # --- Barra Superior (Header) ---
        frame_header = tk.Frame(self, bg=COLOR_ESCUDO_RED, height=120)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        # Logo pequeño en header
        tk.Label(frame_header, text="Two Pack", 
                 font=("Georgia", 28, "bold", "italic"), 
                 bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN).pack(pady=(25, 5))
        
        tk.Label(frame_header, text="📍 Cochabamba Centro", 
                 font=("Helvetica", 10), 
                 bg=COLOR_ESCUDO_RED, fg="#FFCCCC").pack(pady=(0, 15))
        
        tk.Label(frame_header, text="⚡ IA MATCHMAKER ACTIVO", 
                 font=("Helvetica", 9, "bold"), 
                 bg="#FF4400", fg=COLOR_TEXT_MAIN).pack()

        # --- Contenedor Principal ---
        frame_main = tk.Frame(self, bg=COLOR_BG, padx=25, pady=25)
        frame_main.pack(fill="both", expand=True)

        lbl_slogan = tk.Label(frame_main, 
                             text="Plataforma de Smart Economy para Jóvenes Profesionales y Consumidores Urbanos", 
                             font=("Helvetica", 9), bg=COLOR_BG, fg=COLOR_TEXT_MUTED, justify="center", wraplength=360)
        lbl_slogan.pack(pady=(0, 20))

        self.frame_auth = tk.Frame(frame_main, bg=COLOR_CARD, padx=25, pady=25, highlightthickness=1, highlightbackground="#333333")
        self.frame_auth.pack(fill="x")

        self.lbl_titulo = tk.Label(self.frame_auth, text="Iniciar Sesión",
                                  font=("Helvetica", 18, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN)
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.lbl_email = tk.Label(self.frame_auth, text="Correo Electrónico",
                                 font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w")
        self.lbl_email.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 5))
        self.ent_email = tk.Entry(self.frame_auth, font=("Helvetica", 10),
                                 bg="#2D2D2D", fg=COLOR_TEXT_MAIN,
                                 insertbackground=COLOR_TEXT_MAIN,
                                 bd=0, highlightthickness=1, highlightbackground="#444444")
        self.ent_email.grid(row=2, column=0, columnspan=2, sticky="we", ipady=7, pady=(0, 15))

        self.lbl_pass = tk.Label(self.frame_auth, text="Contraseña",
                                font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w")
        self.lbl_pass.grid(row=3, column=0, columnspan=2, sticky="we", pady=(0, 5))
        self.ent_pass = tk.Entry(self.frame_auth, font=("Helvetica", 10),
                                bg="#2D2D2D", fg=COLOR_TEXT_MAIN,
                                insertbackground=COLOR_TEXT_MAIN,
                                bd=0, highlightthickness=1, highlightbackground="#444444", show="*")
        self.ent_pass.grid(row=4, column=0, columnspan=2, sticky="we", ipady=7, pady=(0, 15))

        self.btn_accion = tk.Button(self.frame_auth, text="Acceder a Two Pack",
                                   bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2",
                                   command=self.procesar_login)
        self.btn_accion.grid(row=5, column=0, columnspan=2, sticky="we", ipady=9, pady=(0, 15))

        configurar_animacion_boton(self.btn_accion, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        lbl_enlace = tk.Label(self.frame_auth, text="¿No tienes una cuenta? Crea una gratuita aquí",
                             font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO,
                             cursor="hand2", anchor="center")
        lbl_enlace.grid(row=6, column=0, columnspan=2, sticky="we", pady=(0, 10))
        lbl_enlace.bind("<Button-1>", lambda e: self.cambiar_modo(True))
        configurar_animacion_enlace(lbl_enlace, COLOR_AMARILLO_ORO, COLOR_ACCENT_RED)
        
        # Enlace discreto para comercios
        self.lbl_comercio = tk.Label(frame_main, text="¿Eres un comercio local? Haz clic aquí",
                                   font=("Helvetica", 8), bg=COLOR_BG, fg=COLOR_TEXT_MUTED,
                                   cursor="hand2", anchor="center")
        self.lbl_comercio.pack(pady=(10, 0))
        self.lbl_comercio.bind("<Button-1>", lambda e: self.cambiar_modo_comercio())
        configurar_animacion_enlace(self.lbl_comercio, COLOR_TEXT_MUTED, COLOR_AMARILLO_ORO)

        # Texto sobre servicio gratuito
        lbl_gratuito = tk.Label(frame_main, text="Servicio 100% Gratis para Usuarios y Comercios Locales",
                                font=("Helvetica", 8, "italic"), bg=COLOR_BG, fg=COLOR_SUCCESS)
        lbl_gratuito.pack(pady=(10, 0))

        # Campo para Registro
        self.lbl_nombre_reg = tk.Label(self.frame_auth, text="Nombre Completo",
                                      font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w")
        self.ent_nombre_reg = tk.Entry(self.frame_auth, font=("Helvetica", 10),
                                      bg="#2D2D2D", fg=COLOR_TEXT_MAIN,
                                      insertbackground=COLOR_TEXT_MAIN,
                                      bd=0, highlightthickness=1, highlightbackground="#444444")

        self.lbl_email2_reg = tk.Label(self.frame_auth, text="Confirmar Correo",
                                      font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w")
        self.ent_email2_reg = tk.Entry(self.frame_auth, font=("Helvetica", 10),
                                      bg="#2D2D2D", fg=COLOR_TEXT_MAIN,
                                      insertbackground=COLOR_TEXT_MAIN,
                                      bd=0, highlightthickness=1, highlightbackground="#444444")

        self.lbl_pass2_reg = tk.Label(self.frame_auth, text="Confirmar Contraseña",
                                     font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w")
        self.ent_pass2_reg = tk.Entry(self.frame_auth, font=("Helvetica", 10),
                                     bg="#2D2D2D", fg=COLOR_TEXT_MAIN,
                                     insertbackground=COLOR_TEXT_MAIN,
                                     bd=0, highlightthickness=1, highlightbackground="#444444", show="*")

        self.lbl_genero_reg = tk.Label(self.frame_auth, text="Género",
                                      font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w")
        self.cb_genero_reg = ttk.Combobox(self.frame_auth, values=["Masculino", "Femenino", "Otro"],
                                         font=("Helvetica", 10), state="readonly")
        self.cb_genero_reg.set("Masculino")

    def cambiar_modo_comercio(self):
        # Cambiar entre modo usuario y modo comercio
        self.es_comercio = not self.es_comercio
        if self.es_comercio:
            self.lbl_titulo.config(text="Iniciar Sesión - Comercio")
            self.lbl_comercio.config(text="Volver a modo usuario")
        else:
            self.lbl_titulo.config(text="Iniciar Sesión")
            self.lbl_comercio.config(text="¿Eres un comercio local? Haz clic aquí")

    def cambiar_modo(self, es_registro):
        self.modo_registro = es_registro

        if es_registro:
            self.lbl_titulo.config(text="Crear Cuenta")
            self.lbl_email.grid(row=3, column=0, columnspan=2, sticky="we", pady=(0, 5))
            self.ent_email.grid(row=4, column=0, columnspan=2, sticky="we", ipady=7, pady=(0, 15))
            self.lbl_nombre_reg.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 5))
            self.ent_nombre_reg.grid(row=2, column=0, columnspan=2, sticky="we", ipady=7, pady=(0, 15))
            self.lbl_email2_reg.grid(row=5, column=0, columnspan=2, sticky="we", pady=(0, 5))
            self.ent_email2_reg.grid(row=6, column=0, columnspan=2, sticky="we", ipady=7, pady=(0, 15))
            self.lbl_pass.grid(row=7, column=0, columnspan=2, sticky="we", pady=(0, 5))
            self.ent_pass.grid(row=8, column=0, columnspan=2, sticky="we", ipady=7, pady=(0, 15))
            self.lbl_pass2_reg.grid(row=9, column=0, columnspan=2, sticky="we", pady=(0, 5))
            self.ent_pass2_reg.grid(row=10, column=0, columnspan=2, sticky="we", ipady=7, pady=(0, 15))
            self.lbl_genero_reg.grid(row=11, column=0, columnspan=2, sticky="we", pady=(0, 5))
            self.cb_genero_reg.grid(row=12, column=0, columnspan=2, sticky="we", ipady=7, pady=(0, 15))
            self.btn_accion.config(text="Crear Cuenta", command=self.procesar_registro)
            self.btn_accion.grid(row=13, column=0, columnspan=2, sticky="we", ipady=9, pady=(0, 15))
        else:
            self.lbl_titulo.config(text="Iniciar Sesión" if not self.es_comercio else "Iniciar Sesión - Comercio")
            self.lbl_nombre_reg.grid_forget()
            self.ent_nombre_reg.grid_forget()
            self.lbl_email2_reg.grid_forget()
            self.ent_email2_reg.grid_forget()
            self.lbl_pass2_reg.grid_forget()
            self.ent_pass2_reg.grid_forget()
            self.lbl_genero_reg.grid_forget()
            self.cb_genero_reg.grid_forget()
            self.lbl_email.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 5))
            self.ent_email.grid(row=2, column=0, columnspan=2, sticky="we", ipady=7, pady=(0, 15))
            self.lbl_pass.grid(row=3, column=0, columnspan=2, sticky="we", pady=(0, 5))
            self.ent_pass.grid(row=4, column=0, columnspan=2, sticky="we", ipady=7, pady=(0, 15))
            self.btn_accion.config(text="Acceder a Two Pack", command=self.procesar_login)
            self.btn_accion.grid(row=5, column=0, columnspan=2, sticky="we", ipady=9, pady=(0, 15))

    def _mostrar_dialogo_alerta(self, titulo, mensaje, icono="⚠️"):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("360x230")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.transient(self)
        ventana.grab_set()
        
        # Center dialog
        ventana.update_idletasks()
        x = (self.winfo_width() // 2) + self.winfo_x()
        y = (self.winfo_height() // 2) + self.winfo_y()
        ventana.geometry(f"+{x - 180}+{y - 115}")
        
        tk.Label(ventana, text=icono, font=("Arial Black", 32), bg=COLOR_CARD).pack(pady=(15, 5))
        
        tk.Label(ventana, text=titulo, font=("Helvetica", 15, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT_RED).pack(pady=(0, 8))
        
        tk.Label(ventana, text=mensaje, font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=320, justify="center").pack(pady=(0, 20))
        
        btn_aceptar = tk.Button(ventana, text="Aceptar", font=("Helvetica", 10, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=20, pady=8, command=ventana.destroy)
        btn_aceptar.pack(fill="x", padx=40)
        configurar_animacion_boton(btn_aceptar, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def _mostrar_dialogo_exito(self, titulo, mensaje):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("360x230")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.transient(self)
        ventana.grab_set()
        
        # Center dialog
        ventana.update_idletasks()
        x = (self.winfo_width() // 2) + self.winfo_x()
        y = (self.winfo_height() // 2) + self.winfo_y()
        ventana.geometry(f"+{x - 180}+{y - 115}")
        
        tk.Label(ventana, text="✅", font=("Arial Black", 32), bg=COLOR_CARD).pack(pady=(15, 5))
        
        tk.Label(ventana, text=titulo, font=("Helvetica", 15, "bold"), bg=COLOR_CARD, fg=COLOR_SUCCESS).pack(pady=(0, 8))
        
        tk.Label(ventana, text=mensaje, font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=320, justify="center").pack(pady=(0, 20))
        
        btn_aceptar = tk.Button(ventana, text="¡Genial!", font=("Helvetica", 10, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=20, pady=8, command=lambda: [ventana.destroy(), self.cambiar_modo(False)])
        btn_aceptar.pack(fill="x", padx=40)
        configurar_animacion_boton(btn_aceptar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")

    def procesar_login(self):
        email = self.ent_email.get().strip()
        password = self.ent_pass.get().strip()

        if not email or not password:
            self._mostrar_dialogo_alerta("Campos Incompletos", "Por favor completa todos los campos.")
            return

        if email in self.datos["usuarios"]:
            usuario = self.datos["usuarios"][email]
            if self.es_comercio and usuario["rol"] != "comercio":
                self._mostrar_dialogo_alerta("Rol Incorrecto", "Esta cuenta no es un comercio.")
                return
            elif not self.es_comercio and usuario["rol"] != "usuario":
                self._mostrar_dialogo_alerta("Rol Incorrecto", "Esta cuenta no es un usuario normal.")
                return
                
            if usuario["password"] == password:
                self.al_ingresar_exitoso(usuario)
                return

        self._mostrar_dialogo_alerta("Error de Credenciales", "Correo o contraseña incorrectos.", "❌")

    def procesar_registro(self):
        nombre = self.ent_nombre_reg.get().strip()
        email = self.ent_email.get().strip()
        email2 = self.ent_email2_reg.get().strip()
        password = self.ent_pass.get().strip()
        password2 = self.ent_pass2_reg.get().strip()
        genero = self.cb_genero_reg.get()

        if not nombre or not email or not email2 or not password or not password2:
            self._mostrar_dialogo_alerta("Campos Incompletos", "Por favor completa todos los campos.")
            return

        if email != email2:
            self._mostrar_dialogo_alerta("Correos no coinciden", "Los correos electrónicos no coinciden.")
            return

        if password != password2:
            self._mostrar_dialogo_alerta("Contraseñas no coinciden", "Las contraseñas no coinciden. Verifica e intenta de nuevo.")
            return

        if email in self.datos["usuarios"]:
            self._mostrar_dialogo_alerta("Correo ya registrado", "Ya existe una cuenta con este correo.", "🚫")
            return

        self.datos["usuarios"][email] = {
            "nombre": nombre,
            "password": password,
            "rol": "usuario",
            "genero": genero,
            "profesion": "",
            "confianza": 5.0,
            "matches": 0,
            "reportes": 0,
            "estado": "Activo"
        }
        guardar_datos()
        self._mostrar_dialogo_exito("Cuenta creada correctamente!", "¡Bienvenido a Two Pack! Ahora puedes iniciar sesión.")
