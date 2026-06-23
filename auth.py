
import tkinter as tk
from tkinter import ttk
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS,
    COLOR_ACCENT_RED, COLOR_AMARILLO_ORO, COLOR_ESCUDO_RED,
    COLOR_CORAL_FUEGO, COLOR_AZUL_ELECTRICO, COLOR_RAYO_YELLOW,
    cargar_datos, guardar_datos, configurar_animacion_boton,
    configurar_animacion_enlace
)

class VistaAutenticacion(tk.Frame):
    def __init__(self, parent, al_ingresar_exitoso):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.al_ingresar_exitoso = al_ingresar_exitoso
        self.tipo_usuario = "usuario"  # "usuario" or "comercio"
        self.modo = "login"  # "login" or "register"
        self.datos = cargar_datos()
        self.mostrar_principal()
    
    def mostrar_principal(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        # --- SCROLLABLE CONTAINER ---
        self.canvas_main = tk.Canvas(self, bg=COLOR_BG, bd=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas_main.yview)
        self.scrollable_frame = tk.Frame(self.canvas_main, bg=COLOR_BG)
        
        self.scrollable_frame.bind(
            "&lt;Configure&gt;",
            lambda e: self.canvas_main.configure(scrollregion=self.canvas_main.bbox("all"))
        )
        
        self.canvas_main.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_main.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas_main.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # --- HEADER ---
        header = tk.Frame(self.scrollable_frame, bg=COLOR_ESCUDO_RED, height=100)
        header.pack(fill="x")
        tk.Label(header, text="Two Pack", font=("Georgia", 40, "bold", "italic"),
                 bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN).pack(pady=(20, 10))
        
        # --- TABS PRINCIPALES ---
        tabs_frame = tk.Frame(self.scrollable_frame, bg=COLOR_BG)
        tabs_frame.pack(pady=20, fill="x", padx=20)
        
        # Button for USUARIO
        self.btn_usuario = tk.Button(tabs_frame, text="👤 USUARIO",
                                     font=("Helvetica", 14, "bold"),
                                     bg=COLOR_AZUL_ELECTRICO, fg=COLOR_TEXT_MAIN,
                                     bd=0, cursor="hand2", height=2,
                                     command=lambda: self.cambiar_tipo("usuario"))
        self.btn_usuario.pack(side="left", expand=True, fill="x", padx=5)
        configurar_animacion_boton(self.btn_usuario, COLOR_AZUL_ELECTRICO, "#0056b3", "#003d80")
        
        # Button for EMPRESA
        self.btn_empresa = tk.Button(tabs_frame, text="🏪 EMPRESA",
                                     font=("Helvetica", 14, "bold"),
                                     bg="#2a2a2a", fg=COLOR_TEXT_MUTED,
                                     bd=0, cursor="hand2", height=2,
                                     command=lambda: self.cambiar_tipo("comercio"))
        self.btn_empresa.pack(side="left", expand=True, fill="x", padx=5)
        configurar_animacion_boton(self.btn_empresa, "#2a2a2a", "#3a3a3a", "#4a4a4a")
        
        # --- LOGIN/REGISTER TABS ---
        auth_frame = tk.Frame(self.scrollable_frame, bg=COLOR_BG)
        auth_frame.pack(fill="x", padx=20)
        
        # Login button
        self.btn_login = tk.Button(auth_frame, text="INICIAR SESIÓN",
                                   font=("Helvetica", 12, "bold"),
                                   bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO,
                                   bd=0, cursor="hand2", height=2,
                                   command=lambda: self.cambiar_modo("login"))
        self.btn_login.pack(side="left", expand=True, fill="x", padx=2)
        configurar_animacion_enlace(self.btn_login, COLOR_CARD, COLOR_BG)
        
        # Register button
        self.btn_register = tk.Button(auth_frame, text="CREAR CUENTA",
                                     font=("Helvetica", 12, "bold"),
                                     bg=COLOR_BG, fg=COLOR_TEXT_MUTED,
                                     bd=0, cursor="hand2", height=2,
                                     command=lambda: self.cambiar_modo("register"))
        self.btn_register.pack(side="left", expand=True, fill="x", padx=2)
        configurar_animacion_enlace(self.btn_register, COLOR_BG, COLOR_CARD)
        
        # --- FORM ---
        self.form_container = tk.Frame(self.scrollable_frame, bg=COLOR_CARD, padx=30, pady=30)
        self.form_container.pack(fill="x", padx=20, pady=10)
        
        self.renderizar_formulario()
        
        # --- FOOTER ---
        tk.Label(self.scrollable_frame, text="⚡ IA MATCHMAKER ACTIVO - 100% GRATIS",
                font=("Helvetica", 10, "bold"), bg=COLOR_BG, fg=COLOR_SUCCESS).pack(pady=20)
    
    def cambiar_tipo(self, tipo):
        self.tipo_usuario = tipo
        if tipo == "usuario":
            self.btn_usuario.config(bg=COLOR_AZUL_ELECTRICO, fg=COLOR_TEXT_MAIN)
            self.btn_empresa.config(bg="#2a2a2a", fg=COLOR_TEXT_MUTED)
        else:
            self.btn_empresa.config(bg=COLOR_CORAL_FUEGO, fg=COLOR_TEXT_MAIN)
            self.btn_usuario.config(bg="#2a2a2a", fg=COLOR_TEXT_MUTED)
        self.renderizar_formulario()
    
    def cambiar_modo(self, modo):
        self.modo = modo
        if modo == "login":
            self.btn_login.config(bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO)
            self.btn_register.config(bg=COLOR_BG, fg=COLOR_TEXT_MUTED)
        else:
            self.btn_register.config(bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO)
            self.btn_login.config(bg=COLOR_BG, fg=COLOR_TEXT_MUTED)
        self.renderizar_formulario()
    
    def renderizar_formulario(self):
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        titulo = ""
        if self.modo == "login":
            if self.tipo_usuario == "usuario":
                titulo = "Iniciar Sesión - Usuario"
            else:
                titulo = "Iniciar Sesión - Empresa"
        else:
            if self.tipo_usuario == "usuario":
                titulo = "Crear Cuenta - Usuario"
            else:
                titulo = "Crear Cuenta - Empresa"
        
        tk.Label(self.form_container, text=titulo,
                 font=("Helvetica", 20, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(pady=(0, 20))
        
        if self.modo == "login":
            self.renderizar_login()
        else:
            self.renderizar_register()
    
    def renderizar_login(self):
        # Tagline
        tk.Label(
            self.form_container,
            text="Para jóvenes universitarios y profesionales de Cochabamba",
            font=("Helvetica", 9, "italic"),
            bg=COLOR_CARD,
            fg=COLOR_RAYO_YELLOW,
            justify="center"
        ).pack(pady=(0, 12))
        
        # Correo
        tk.Label(self.form_container, text="Correo Electrónico",
                 font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 anchor="w").pack(fill="x", pady=(0, 5))
        self.entry_email = tk.Entry(self.form_container, font=("Helvetica", 12),
                                     bg="#2d2d2d", fg=COLOR_TEXT_MAIN,
                                     insertbackground=COLOR_TEXT_MAIN, bd=0,
                                     highlightthickness=1, highlightbackground="#444")
        self.entry_email.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Contraseña
        tk.Label(self.form_container, text="Contraseña",
                 font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 anchor="w").pack(fill="x", pady=(0, 5))
        self.entry_pass = tk.Entry(self.form_container, font=("Helvetica", 12),
                                     bg="#2d2d2d", fg=COLOR_TEXT_MAIN,
                                     insertbackground=COLOR_TEXT_MAIN, bd=0,
                                     highlightthickness=1, highlightbackground="#444", show="*")
        self.entry_pass.pack(fill="x", ipady=8, pady=(0, 20))
        
        # Botón Login
        btn = tk.Button(self.form_container, text="INICIAR SESIÓN",
                       font=("Helvetica", 13, "bold"), bg=COLOR_ACCENT_RED,
                       fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2",
                       height=2, command=self.procesar_login)
        btn.pack(fill="x")
        configurar_animacion_boton(btn, COLOR_ACCENT_RED, "#ff4d63", "#990a15")
    
    def renderizar_register(self):
        if self.tipo_usuario == "usuario":
            # Nombre
            tk.Label(self.form_container, text="Nombre Completo",
                     font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                     anchor="w").pack(fill="x", pady=(0, 5))
            self.entry_nombre = tk.Entry(self.form_container, font=("Helvetica", 12),
                                         bg="#2d2d2d", fg=COLOR_TEXT_MAIN,
                                         insertbackground=COLOR_TEXT_MAIN, bd=0,
                                         highlightthickness=1, highlightbackground="#444")
            self.entry_nombre.pack(fill="x", ipady=8, pady=(0, 10))
        else:
            # Nombre comercio
            tk.Label(self.form_container, text="Nombre del Comercio",
                     font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                     anchor="w").pack(fill="x", pady=(0, 5))
            self.entry_nombre = tk.Entry(self.form_container, font=("Helvetica", 12),
                                         bg="#2d2d2d", fg=COLOR_TEXT_MAIN,
                                         insertbackground=COLOR_TEXT_MAIN, bd=0,
                                         highlightthickness=1, highlightbackground="#444")
            self.entry_nombre.pack(fill="x", ipady=8, pady=(0, 10))
            
            # Dirección
            tk.Label(self.form_container, text="Dirección",
                     font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                     anchor="w").pack(fill="x", pady=(0, 5))
            self.entry_direccion = tk.Entry(self.form_container, font=("Helvetica", 12),
                                         bg="#2d2d2d", fg=COLOR_TEXT_MAIN,
                                         insertbackground=COLOR_TEXT_MAIN, bd=0,
                                         highlightthickness=1, highlightbackground="#444")
            self.entry_direccion.pack(fill="x", ipady=8, pady=(0, 10))
            
            # Teléfono
            tk.Label(self.form_container, text="Teléfono",
                     font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                     anchor="w").pack(fill="x", pady=(0, 5))
            self.entry_telefono = tk.Entry(self.form_container, font=("Helvetica", 12),
                                         bg="#2d2d2d", fg=COLOR_TEXT_MAIN,
                                         insertbackground=COLOR_TEXT_MAIN, bd=0,
                                         highlightthickness=1, highlightbackground="#444")
            self.entry_telefono.pack(fill="x", ipady=8, pady=(0, 10))
        
        # Correo
        tk.Label(self.form_container, text="Correo Electrónico",
                 font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 anchor="w").pack(fill="x", pady=(0, 5))
        self.entry_email = tk.Entry(self.form_container, font=("Helvetica", 12),
                                     bg="#2d2d2d", fg=COLOR_TEXT_MAIN,
                                     insertbackground=COLOR_TEXT_MAIN, bd=0,
                                     highlightthickness=1, highlightbackground="#444")
        self.entry_email.pack(fill="x", ipady=8, pady=(0, 10))
        
        # Confirmar correo
        tk.Label(self.form_container, text="Confirmar Correo",
                 font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 anchor="w").pack(fill="x", pady=(0, 5))
        self.entry_email2 = tk.Entry(self.form_container, font=("Helvetica", 12),
                                     bg="#2d2d2d", fg=COLOR_TEXT_MAIN,
                                     insertbackground=COLOR_TEXT_MAIN, bd=0,
                                     highlightthickness=1, highlightbackground="#444")
        self.entry_email2.pack(fill="x", ipady=8, pady=(0, 10))
        
        # Contraseña
        tk.Label(self.form_container, text="Contraseña",
                 font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 anchor="w").pack(fill="x", pady=(0, 5))
        self.entry_pass = tk.Entry(self.form_container, font=("Helvetica", 12),
                                     bg="#2d2d2d", fg=COLOR_TEXT_MAIN,
                                     insertbackground=COLOR_TEXT_MAIN, bd=0,
                                     highlightthickness=1, highlightbackground="#444", show="*")
        self.entry_pass.pack(fill="x", ipady=8, pady=(0, 10))
        
        # Confirmar contraseña
        tk.Label(self.form_container, text="Confirmar Contraseña",
                 font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 anchor="w").pack(fill="x", pady=(0, 5))
        self.entry_pass2 = tk.Entry(self.form_container, font=("Helvetica", 12),
                                     bg="#2d2d2d", fg=COLOR_TEXT_MAIN,
                                     insertbackground=COLOR_TEXT_MAIN, bd=0,
                                     highlightthickness=1, highlightbackground="#444", show="*")
        self.entry_pass2.pack(fill="x", ipady=8, pady=(0, 10))
        
        if self.tipo_usuario == "usuario":
            # Género
            tk.Label(self.form_container, text="Género",
                     font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                     anchor="w").pack(fill="x", pady=(0, 5))
            self.combo_genero = ttk.Combobox(self.form_container, values=["Masculino", "Femenino", "Otro"],
                                               font=("Helvetica", 12), state="readonly")
            self.combo_genero.set("Masculino")
            self.combo_genero.pack(fill="x", ipady=8, pady=(0, 15))
        else:
            # Categoría
            tk.Label(self.form_container, text="Categoría",
                     font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                     anchor="w").pack(fill="x", pady=(0, 5))
            self.combo_categoria = ttk.Combobox(self.form_container, values=["Gastronomía", "Entretenimiento", "Deportes", "Supermercados"],
                                               font=("Helvetica", 12), state="readonly")
            self.combo_categoria.set("Gastronomía")
            self.combo_categoria.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Botón Registrar
        btn = tk.Button(self.form_container, text="CREAR CUENTA",
                       font=("Helvetica", 13, "bold"), bg=COLOR_ACCENT_RED,
                       fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2",
                       height=2, command=self.procesar_register)
        btn.pack(fill="x")
        configurar_animacion_boton(btn, COLOR_ACCENT_RED, "#ff4d63", "#990a15")
    
    def _mostrar_dialogo(self, titulo, mensaje, icono="⚠️"):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("400x250")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.transient(self)
        ventana.grab_set()
        ventana.update_idletasks()
        x = (self.winfo_width() // 2) + self.winfo_x()
        y = (self.winfo_height() // 2) + self.winfo_y()
        ventana.geometry(f"+{x - 200}+{y - 125}")
        
        tk.Label(ventana, text=icono, font=("Arial Black", 36), bg=COLOR_CARD).pack(pady=(20, 5))
        tk.Label(ventana, text=titulo, font=("Helvetica", 16, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT_RED).pack(pady=(0, 10))
        tk.Label(ventana, text=mensaje, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=350, justify="center").pack(pady=(0, 20))
        
        btn_aceptar = tk.Button(ventana, text="Aceptar", font=("Helvetica", 11, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=25, pady=10, command=ventana.destroy)
        btn_aceptar.pack(fill="x", padx=50)
        configurar_animacion_boton(btn_aceptar, COLOR_ACCENT_RED, "#ff4d63", "#990a15")
    
    def procesar_login(self):
        email = self.entry_email.get().strip()
        password = self.entry_pass.get().strip()
        
        if not email or not password:
            self._mostrar_dialogo("Campos Incompletos", "Por favor completa todos los campos.")
            return
        
        if email in self.datos["usuarios"]:
            usuario = self.datos["usuarios"][email]
            
            if self.tipo_usuario == "comercio" and usuario["rol"] != "comercio":
                self._mostrar_dialogo("Rol Incorrecto", "Esta cuenta no es de tipo empresa. Por favor, cambia a la pestaña USUARIO.")
                return
            elif self.tipo_usuario == "usuario" and usuario["rol"] != "usuario":
                self._mostrar_dialogo("Rol Incorrecto", "Esta cuenta no es de tipo usuario. Por favor, cambia a la pestaña EMPRESA.")
                return
                
            if usuario["password"] == password:
                self.al_ingresar_exitoso(usuario)
                return
        
        self._mostrar_dialogo("Error de Credenciales", "Correo o contraseña incorrectos. Inténtalo de nuevo.", "❌")
    
    def procesar_register(self):
        email = self.entry_email.get().strip()
        email2 = self.entry_email2.get().strip()
        password = self.entry_pass.get().strip()
        password2 = self.entry_pass2.get().strip()
        
        if self.tipo_usuario == "usuario":
            nombre = self.entry_nombre.get().strip()
            genero = self.combo_genero.get()
            
            if not nombre or not email or not email2 or not password or not password2:
                self._mostrar_dialogo("Campos Incompletos", "Por favor completa todos los campos.")
                return
        else:
            nombre = self.entry_nombre.get().strip()
            direccion = self.entry_direccion.get().strip()
            telefono = self.entry_telefono.get().strip()
            categoria = self.combo_categoria.get()
            
            if not nombre or not direccion or not telefono or not email or not email2 or not password or not password2:
                self._mostrar_dialogo("Campos Incompletos", "Por favor completa todos los campos.")
                return
        
        if email != email2:
            self._mostrar_dialogo("Correos no coincidentes", "Los dos correos electrónicos que ingresaste no son iguales.")
            return
        
        if password != password2:
            self._mostrar_dialogo("Contraseñas no coincidentes", "Las dos contraseñas que ingresaste no son iguales.")
            return
        
        if email in self.datos["usuarios"]:
            self._mostrar_dialogo("Correo ya registrado", "Ya existe una cuenta con este correo electrónico.", "🚫")
            return
        
        if self.tipo_usuario == "usuario":
            self.datos["usuarios"][email] = {
                "nombre": nombre, "password": password, "rol": "usuario",
                "genero": genero, "profesion": "", "confianza": 5.0,
                "matches": 0, "reportes": 0, "estado": "Activo"
            }
            guardar_datos()
            self._mostrar_dialogo("Cuenta creada correctamente!", "¡Bienvenido a Two Pack! Ahora puedes iniciar sesión.", "✅")
            self.cambiar_modo("login")
        else:
            self.datos["usuarios"][email] = {
                "nombre": nombre, "password": password, "rol": "comercio",
                "direccion": direccion, "telefono": telefono, "categoria": categoria,
                "confianza": 5.0, "estado": "Activo"
            }
            guardar_datos()
            self._mostrar_dialogo("Empresa registrada!", "¡Bienvenido a Two Pack! Tu comercio ya forma parte de nuestra plataforma.", "✅")
            self.cambiar_modo("login")

