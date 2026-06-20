# Two Pack - Ecosistema Unificado de Ciudades Inteligentes
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os

# --- PALETA DE COLORES OFICIAL ---
COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_MUTED = "#A0A0A0"
COLOR_SUCCESS = "#2ECC71"
COLOR_SUCCESS_HOVER = "#27AE60"
COLOR_ACCENT_RED = "#FF1E39"
COLOR_RED_HOVER = "#FF4D63"
COLOR_RED_ACTIVE = "#990A15"
COLOR_RAYO_YELLOW = "#FFCC00"
COLOR_ESCUDO_RED = "#B30F1D"

# --- BASE DE DATOS COMPARTIDA EN MEMORIA ---
# Esto permite sincronizar automáticamente las promociones entre paneles
base_datos_global = {
    "promociones": [
        {"id": "001", "titulo": "2x1 en Alitas Universitarias", "cat": "Gastronomía", "zona": "Zona UCATEC", "vence": "25/06/2026", "precio_ref": "35"},
        {"id": "002", "titulo": "Fernet 2x1 Jueves de Frater", "cat": "Pubs / Discotecas", "zona": "La Recoleta", "vence": "28/06/2026", "precio_ref": "50"},
        {"id": "003", "titulo": "2x1 Milkshakes Premium", "cat": "Cafeterías", "zona": "El Prado", "vence": "30/06/2026", "precio_ref": "22"}
    ],
    "historial_matches": [ 
        { 
            "id": "m001", 
            "usuario_match": "Alejandro Gómez", 
            "genero_match": "Masculino", 
            "promo": "2x1 en Alitas Universitarias", 
            "zona": "Zona UCATEC", 
            "fecha": "15/06/2026", 
            "hora": "13:00", 
            "reseña_dada": None, 
            "puntuacion_dada": None 
        }, 
        { 
            "id": "m002", 
            "usuario_match": "Sofía Claros", 
            "genero_match": "Femenino", 
            "promo": "Fernet 2x1 Jueves de Frater", 
            "zona": "La Recoleta", 
            "fecha": "10/06/2026", 
            "hora": "20:00", 
            "reseña_dada": "Muy puntual y simpática", 
            "puntuacion_dada": 5 
        } 
    ],
    "pool_solicitudes": [
        {"usuario": "Alejandro Gómez", "genero": "Masculino", "oferta_id": "001", "hora_inicio": 12, "hora_fin": 14, "filtro_genero": False},
        {"usuario": "Sofía Claros", "genero": "Femenino", "oferta_id": "002", "hora_inicio": 12, "hora_fin": 14, "filtro_genero": False},
        {"usuario": "Diego Torrico", "genero": "Masculino", "oferta_id": "001", "hora_inicio": 18, "hora_fin": 20, "filtro_genero": False},
        {"usuario": "Valeria Rocha", "genero": "Femenino", "oferta_id": "001", "hora_inicio": 12, "hora_fin": 14, "filtro_genero": True}
    ],
    "usuarios": {
        "estudiante@universidad.edu.bo": {"nombre": "Carlos Mendoza", "password": "123", "rol": "estudiante", "genero": "Masculino"},
        "comercio@local.com": {"nombre": "Restaurante Burger Click", "password": "123", "rol": "comercio"}
    }
}

def cargar_datos():
    global base_datos_global
    if os.path.exists("datos.json"):
        with open("datos.json", "r", encoding="utf-8") as f:
            base_datos_global = json.load(f)
    return base_datos_global

def guardar_datos():
    with open("datos.json", "w", encoding="utf-8") as f:
        json.dump(base_datos_global, f, ensure_ascii=False, indent=2)

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
        
        # Cargar datos desde JSON
        cargar_datos()
        
        # Empezar con la pantalla de autenticación
        self.cambiar_panel(PantallaAutenticacion)

    def cambiar_panel(self, PanelClase, *args, **kwargs):
        if self.panel_actual:
            self.panel_actual.destroy()
        
        self.panel_actual = PanelClase(self, *args, **kwargs)
        self.panel_actual.pack(fill="both", expand=True)

    def configurar_animacion_boton(self, boton, color_normal, color_hover, color_active):
        boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
        boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))
        boton.bind("<ButtonPress-1>", lambda e: boton.config(bg=color_active))
        boton.bind("<ButtonRelease-1>", lambda e: boton.config(bg=color_hover))

# --- PANTALLA DE AUTENTICACIÓN EVOLUCIONADA ---
class PantallaAutenticacion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.rol_seleccionado = "estudiante"
        self.modo_registro = False
        
        self.inicializar_ui()

    def inicializar_ui(self):
        # --- CONTENEDOR CENTRAL ---
        self.frame_central = tk.Frame(self, bg=COLOR_BG)
        self.frame_central.pack(expand=True)

        self.mostrar_login_registro()

    def mostrar_login_registro(self):
        for widget in self.frame_central.winfo_children():
            widget.destroy()

        # --- ESCUDO CURVADO ROJO CON ANIMACIONES ---
        self.dibujar_escudo(self.frame_central)

        # --- ESLOGAN OFICIAL ---
        lbl_slogan = tk.Label(self.frame_central, text="Divide el gasto, duplica la experiencia.", 
                              font=("Helvetica Neue", 11, "italic"), bg=COLOR_BG, fg=COLOR_RAYO_YELLOW)
        lbl_slogan.pack(pady=(10, 20))

        # --- SELECTOR DE ROL ---
        frame_selector = tk.Frame(self.frame_central, bg=COLOR_BG)
        frame_selector.pack(pady=(0, 20))

        self.btn_estudiante = tk.Button(frame_selector, text="👤 Iniciar Sesión como Estudiante",
                                        font=("Helvetica", 10, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN,
                                        bd=0, cursor="hand2", padx=15, pady=8,
                                        command=lambda: self.seleccionar_rol("estudiante"))
        self.btn_estudiante.pack(side="left", padx=5)

        self.btn_comercio = tk.Button(frame_selector, text="🏪 Iniciar Sesión como Dueño de Negocio",
                                      font=("Helvetica", 10, "bold"), bg="#333333", fg=COLOR_TEXT_MAIN,
                                      bd=0, cursor="hand2", padx=15, pady=8,
                                      command=lambda: self.seleccionar_rol("comercio"))
        self.btn_comercio.pack(side="left", padx=5)

        self.parent.configurar_animacion_boton(self.btn_estudiante, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)
        self.parent.configurar_animacion_boton(self.btn_comercio, "#333333", "#444444", "#222222")

        if not self.modo_registro:
            # --- FORMULARIO DE LOGIN ---
            frame_form = tk.Frame(self.frame_central, bg=COLOR_BG)
            frame_form.pack(fill="x", padx=40)

            tk.Label(frame_form, text="CORREO ELECTRÓNICO", font=("Helvetica", 8, "bold"), 
                     bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
            self.ent_email = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                      bd=0, insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_email.pack(fill="x", ipady=8, pady=(0, 12))
            self.ent_email.insert(0, "estudiante@universidad.edu.bo")

            tk.Label(frame_form, text="CONTRASEÑA", font=("Helvetica", 8, "bold"), 
                     bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
            self.ent_pass = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                     bd=0, show="*", insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_pass.pack(fill="x", ipady=8, pady=(0, 20))
            self.ent_pass.insert(0, "123")

            # --- BOTÓN DE INGRESO ---
            btn_ingresar = tk.Button(frame_form, text="Ingresar de Forma Segura",
                                     font=("Helvetica", 11, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN,
                                     bd=0, cursor="hand2", command=self.procesar_login)
            btn_ingresar.pack(fill="x", ipady=10)
            self.parent.configurar_animacion_boton(btn_ingresar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")
            
            # --- BOTÓN DE REGISTRO ---
            btn_registrar = tk.Button(frame_form, text="Crear Cuenta Nueva",
                                      font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_ACCENT_RED,
                                      bd=0, cursor="hand2", command=lambda: self.cambiar_modo(True))
            btn_registrar.pack(pady=15)
        else:
            # --- FORMULARIO DE REGISTRO ---
            frame_form = tk.Frame(self.frame_central, bg=COLOR_BG)
            frame_form.pack(fill="x", padx=40)

            tk.Label(frame_form, text="NOMBRE COMPLETO", font=("Helvetica", 8, "bold"), 
                     bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
            self.ent_nombre_reg = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                          bd=0, insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_nombre_reg.pack(fill="x", ipady=8, pady=(0, 12))

            tk.Label(frame_form, text="CORREO ELECTRÓNICO", font=("Helvetica", 8, "bold"), 
                     bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
            self.ent_email_reg = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                          bd=0, insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_email_reg.pack(fill="x", ipady=8, pady=(0, 12))

            # Campo género
            tk.Label(frame_form, text="GÉNERO",
                     font=("Helvetica", 8, "bold"),
                     bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(3, 2))
            self.cb_genero_reg = ttk.Combobox(frame_form,
                                             values=["Masculino", "Femenino", "Prefiero no decir"],
                                             state="readonly",
                                             font=("Helvetica", 12))
            self.cb_genero_reg.pack(fill="x", ipady=4, pady=(0, 12))
            self.cb_genero_reg.set("Masculino")

            tk.Label(frame_form, text="CONTRASEÑA", font=("Helvetica", 8, "bold"), 
                     bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
            self.ent_pass_reg = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                         bd=0, show="*", insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_pass_reg.pack(fill="x", ipady=8, pady=(0, 12))

            # Campo confirmar contraseña
            tk.Label(frame_form, text="CONFIRMAR CONTRASEÑA",
                     font=("Helvetica", 8, "bold"),
                     bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(3, 2))
            self.ent_pass2_reg = tk.Entry(frame_form, font=("Helvetica", 12),
                                          bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                          bd=0, show="*",
                                          highlightthickness=1,
                                          highlightbackground="#2D2D2D")
            self.ent_pass2_reg.pack(fill="x", ipady=8, pady=(0, 20))

            # --- BOTÓN DE REGISTRO ---
            btn_registrar = tk.Button(frame_form, text="Crear Cuenta de Estudiante",
                                      font=("Helvetica", 11, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN,
                                      bd=0, cursor="hand2", command=self.procesar_registro)
            btn_registrar.pack(fill="x", ipady=10)
            self.parent.configurar_animacion_boton(btn_registrar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")
            
            # --- BOTÓN DE VOLVER A LOGIN ---
            btn_volver = tk.Button(frame_form, text="Volver a Iniciar Sesión",
                                   font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_ACCENT_RED,
                                   bd=0, cursor="hand2", command=lambda: self.cambiar_modo(False))
            btn_volver.pack(pady=15)

    def cambiar_modo(self, modo_registro):
        self.modo_registro = modo_registro
        self.mostrar_login_registro()

    def procesar_registro(self):
        nombre = self.ent_nombre_reg.get().strip()
        email = self.ent_email_reg.get().strip()
        password = self.ent_pass_reg.get().strip()
        password2 = self.ent_pass2_reg.get().strip()
        genero = self.cb_genero_reg.get()

        if not nombre or not email or not password or not password2:
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los campos.")
            return

        # Validar que las contraseñas coincidan
        if password != password2:
            messagebox.showerror("Error",
                "Las contraseñas no coinciden. Verifica e intenta de nuevo.")
            return

        # Validar dominio de correo boliviano universitario
        dominios_validos = [".edu.bo", ".umss.edu.bo", ".ucb.edu.bo",
                           ".uatf.edu.bo", ".upsa.edu.bo", ".unifranz.edu.bo",
                           ".ucatec.edu.bo", ".univalle.edu.bo"]
        if not any(email.endswith(d) for d in dominios_validos):
            messagebox.showwarning("Correo inválido",
                "Por favor usa tu correo universitario boliviano.\n"
                "Ejemplo: tu_nombre@umss.edu.bo")
            return

        if email in base_datos_global["usuarios"]:
            messagebox.showerror("Error", "Ya existe una cuenta con este correo.")
            return

        base_datos_global["usuarios"][email] = {
            "nombre": nombre,
            "password": password,
            "rol": "estudiante",
            "genero": genero,
            "confianza": 5.0,
            "matches": 0,
            "reportes": 0,
            "estado": "Activo"
        }
        guardar_datos()
        messagebox.showinfo("Éxito", "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
        self.cambiar_modo(False)

    def dibujar_escudo(self, parent):
        canvas_logo = tk.Canvas(parent, width=280, height=220, bg=COLOR_BG, bd=0, highlightthickness=0)
        canvas_logo.pack(pady=(0, 5))

        # Escudo curvado rojo
        puntos_escudo = [40, 50, 240, 50, 210, 150, 140, 200, 70, 150]
        canvas_logo.create_polygon(puntos_escudo, fill=COLOR_ESCUDO_RED, outline="#800A12", width=2)

        # Rayos cómicos amarillos
        canvas_logo.create_polygon(25, 20, 55, 20, 40, 45, 55, 45, 30, 75, 38, 50, 25, 50, 
                                   fill=COLOR_RAYO_YELLOW, outline="black", width=1)
        canvas_logo.create_polygon(225, 120, 245, 120, 235, 135, 245, 135, 225, 160, 230, 140, 220, 140, 
                                   fill=COLOR_RAYO_YELLOW, outline="black", width=1)

        # Relojes "Tic Tac" abstractos
        canvas_logo.create_oval(75, 175, 105, 205, fill="#E0E0E0", outline="#A0A0A0", width=2)
        canvas_logo.create_line(90, 190, 90, 182, fill="black", width=2)
        canvas_logo.create_line(90, 190, 100, 195, fill="black", width=1.5)
        canvas_logo.create_oval(230, 100, 260, 130, fill="#E0E0E0", outline="#A0A0A0", width=2)
        canvas_logo.create_line(245, 115, 245, 107, fill="black", width=2)
        canvas_logo.create_line(245, 115, 252, 122, fill="black", width=1.5)

        # Detalles morados flotantes
        canvas_logo.create_polygon(50, 160, 60, 150, 65, 165, fill="#5D3FD3")
        canvas_logo.create_oval(190, 25, 202, 35, fill="#E0E0E0", outline="")

        # Texto principal
        canvas_logo.create_text(142, 92, text="2x1", font=("Arial Black", 44, "bold"), fill="#000000")
        canvas_logo.create_text(140, 90, text="2x1", font=("Arial Black", 44, "bold"), fill=COLOR_TEXT_MAIN)
        canvas_logo.create_text(140, 135, text="PROMO", font=("Arial Black", 16, "bold"), fill=COLOR_TEXT_MAIN)

        # Cinta inferior
        canvas_logo.create_polygon(80, 150, 200, 150, 180, 180, 100, 180, fill="#800A12")
        canvas_logo.create_polygon(85, 152, 195, 152, 185, 178, 95, 178, fill=COLOR_TEXT_MAIN, outline="#CCCCCC", width=1)
        canvas_logo.create_text(140, 165, text="Two Pack", font=("Georgia", 15, "bold", "italic"), fill=COLOR_ESCUDO_RED)

    def seleccionar_rol(self, rol):
        self.rol_seleccionado = rol
        if rol == "estudiante":
            self.btn_estudiante.config(bg=COLOR_ACCENT_RED)
            self.btn_comercio.config(bg="#333333")
            self.ent_email.delete(0, tk.END)
            self.ent_email.insert(0, "estudiante@universidad.edu.bo")
        else:
            self.btn_estudiante.config(bg="#333333")
            self.btn_comercio.config(bg=COLOR_ACCENT_RED)
            self.ent_email.delete(0, tk.END)
            self.ent_email.insert(0, "comercio@local.com")

    def procesar_login(self):
        email = self.ent_email.get().strip()
        password = self.ent_pass.get().strip()

        if not email or not password:
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los campos.")
            return

        if email in base_datos_global["usuarios"]:
            usuario = base_datos_global["usuarios"][email]
            if usuario["password"] == password and usuario["rol"] == self.rol_seleccionado:
                self.parent.usuario_actual = usuario
                if usuario["rol"] == "estudiante":
                    self.parent.cambiar_panel(PanelEstudiante)
                else:
                    self.parent.cambiar_panel(PanelComercio)
                return

        messagebox.showerror("Error de Credenciales", "Correo o contraseña incorrectos para este rol.")

# --- SALA DE CHAT TEMPORAL ---
class SalaChatTemporal(tk.Frame):
    def __init__(self, parent, match_encontrado, promo, hora_fin):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.match_encontrado = match_encontrado
        self.promo = promo
        self.timer_activo = True
        self.primero_mensaje = True
        
        # Calcular tiempo de expiración (2 horas después del fin de la ventana temporal)
        self.hora_expiracion = datetime.now() + timedelta(hours=2)
        
        self.inicializar_ui()
        self.actualizar_timer()

    def inicializar_ui(self):
        # --- BARRA SUPERIOR ---
        frame_header = tk.Frame(self, bg="#1A1A1A", height=70)
        frame_header.pack(fill="x", side="top")
        frame_header.pack_propagate(False)

        lbl_header_izq = tk.Frame(frame_header, bg="#1A1A1A")
        lbl_header_izq.pack(side="left", padx=20, pady=10)

        lbl_nombre = tk.Label(lbl_header_izq, text=f"👤 {self.match_encontrado['usuario']}", 
                             font=("Helvetica", 14, "bold"), bg="#1A1A1A", fg=COLOR_TEXT_MAIN)
        lbl_nombre.pack(anchor="w")
        lbl_promo = tk.Label(lbl_header_izq, text=f"🎁 {self.promo['titulo']}", 
                            font=("Helvetica", 10), bg="#1A1A1A", fg=COLOR_TEXT_MUTED)
        lbl_promo.pack(anchor="w")

        lbl_header_der = tk.Frame(frame_header, bg="#1A1A1A")
        lbl_header_der.pack(side="right", padx=20, pady=10)
        
        self.lbl_timer = tk.Label(lbl_header_der, text="", 
                                 font=("Helvetica", 10, "bold"), bg="#1A1A1A", fg=COLOR_RAYO_YELLOW)
        self.lbl_timer.pack(anchor="e", pady=(0, 2))
        
        lbl_seguridad = tk.Label(lbl_header_der, text="🔒 Conexión Encriptada y Temporal", 
                                font=("Helvetica", 9), bg="#1A1A1A", fg=COLOR_SUCCESS)
        lbl_seguridad.pack(anchor="e")

        # --- ÁREA DE MENSAJES ---
        frame_mensajes = tk.Frame(self, bg=COLOR_BG)
        frame_mensajes.pack(fill="both", expand=True, padx=20, pady=10)

        self.text_mensajes = tk.Text(frame_mensajes, bg=COLOR_BG, fg=COLOR_TEXT_MAIN, 
                                     font=("Helvetica", 10), bd=0, padx=15, pady=15, 
                                     wrap="word", state="disabled")
        scrollbar_mensajes = ttk.Scrollbar(frame_mensajes, orient="vertical", command=self.text_mensajes.yview)
        self.text_mensajes.configure(yscrollcommand=scrollbar_mensajes.set)

        self.text_mensajes.pack(side="left", fill="both", expand=True)
        scrollbar_mensajes.pack(side="right", fill="y")

        # Configurar tags para burbujas
        self.text_mensajes.tag_configure("user_right", justify="right", foreground=COLOR_TEXT_MAIN)
        self.text_mensajes.tag_configure("user_right_bubble", background=COLOR_ACCENT_RED)
        self.text_mensajes.tag_configure("user_left", justify="left", foreground=COLOR_TEXT_MAIN)
        self.text_mensajes.tag_configure("user_left_bubble", background=COLOR_CARD)

        # --- ÁREA DE ENTRADA ---
        frame_entrada = tk.Frame(self, bg="#1A1A1A", height=80)
        frame_entrada.pack(fill="x", side="bottom")
        frame_entrada.pack_propagate(False)

        frame_campo = tk.Frame(frame_entrada, bg="#1A1A1A")
        frame_campo.pack(fill="x", padx=20, pady=20)

        self.ent_mensaje = tk.Entry(frame_campo, font=("Helvetica", 10), bg=COLOR_CARD, 
                                    fg=COLOR_TEXT_MAIN, bd=0, insertbackground="white", 
                                    highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_mensaje.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.ent_mensaje.bind("<Return>", lambda e: self.enviar_mensaje())

        btn_enviar = tk.Button(frame_campo, text="🚀 Enviar", 
                              font=("Helvetica", 10, "bold"), bg=COLOR_ACCENT_RED, 
                              fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", 
                              command=self.enviar_mensaje, width=12)
        btn_enviar.pack(side="right", ipady=8)
        self.parent.parent.configurar_animacion_boton(btn_enviar, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def actualizar_timer(self):
        if self.timer_activo:
            tiempo_restante = self.hora_expiracion - datetime.now()
            if tiempo_restante.total_seconds() <= 0:
                self.destruir_chat()
                return
            horas, resto = divmod(tiempo_restante.seconds, 3600)
            minutos, segundos = divmod(resto, 60)
            self.lbl_timer.config(text=f"⏱️ {horas:02d}:{minutos:02d}:{segundos:02d} restantes")
            self.after(1000, self.actualizar_timer)

    def enviar_mensaje(self):
        texto = self.ent_mensaje.get().strip()
        if texto:
            self.agregar_mensaje(texto, "yo")
            self.ent_mensaje.delete(0, tk.END)
            
            if self.primero_mensaje:
                self.primero_mensaje = False
                self.after(2000, self.enviar_mensaje_mock)

    def enviar_mensaje_mock(self):
        respuestas = [
            f"¡Hola! Súper, nos vemos en la sucursal de {self.promo['zona']} en 15 minutos.",
            "Perfecto! ¿Ya estás llegando?",
            "¡Excelente! Allí te espero con la promoción lista.",
            "Genial, nos vemos pronto!"
        ]
        import random
        self.agregar_mensaje(random.choice(respuestas), "otro")

    def agregar_mensaje(self, texto, remitente):
        self.text_mensajes.config(state="normal")
        
        if remitente == "yo":
            self.text_mensajes.insert(tk.END, "\n", "user_right")
            self.text_mensajes.insert(tk.END, f"  {texto}  \n", "user_right_bubble")
        else:
            self.text_mensajes.insert(tk.END, "\n", "user_left")
            self.text_mensajes.insert(tk.END, f"  {texto}  \n", "user_left_bubble")
        
        self.text_mensajes.config(state="disabled")
        self.text_mensajes.yview(tk.END)

    def destruir_chat(self):
        self.timer_activo = False
        messagebox.showinfo("Chat Expirado", "🚫 Este chat ha sido destruido por motivos de seguridad urbana")
        self.parent.cerrar_chat()

# --- PANEL DEL ESTUDIANTE (Catálogo + Matchmaker + Chat) ---
class PanelEstudiante(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.usuario_actual = parent.usuario_actual
        self.promo_seleccionada = None
        self.filtro_zona = "Todas"
        self.filtro_categoria = "Todas"
        self.tarjetas = []
        self.hora_fin = None
        self.match_encontrado = None
        self.chat = None
        self.seccion_actual = "inicio"
        self.sync_after_id = None
        
        self.inicializar_ui()

    def inicializar_ui(self):
        # --- BARRA LATERAL ---
        frame_sidebar = tk.Frame(self, bg="#1A1A1A", width=220)
        frame_sidebar.pack(side="left", fill="y")
        frame_sidebar.pack_propagate(False)

        # Mini logo sidebar
        mini_canvas = tk.Canvas(frame_sidebar, width=160, height=70,
                                bg="#1A1A1A", bd=0, highlightthickness=0)
        mini_canvas.pack(pady=(15, 5))
        
        # Escudo pequeño
        pts = [30, 10, 130, 10, 115, 45, 80, 65, 45, 45]
        mini_canvas.create_polygon(pts, fill="#B30F1D", outline="#800A12", width=1)
        mini_canvas.create_text(80, 30, text="2x1",
                                font=("Arial Black", 16, "bold"), fill="#FFFFFF")
        mini_canvas.create_text(80, 48, text="PROMO",
                                font=("Arial Black", 7, "bold"), fill="#FFFFFF")
        # Cinta inferior
        mini_canvas.create_polygon(
            [48, 45, 112, 45, 105, 62, 55, 62],
            fill="#FFFFFF", outline="#CCCCCC", width=1)
        mini_canvas.create_text(80, 53, text="Two Pack",
                                font=("Georgia", 8, "bold", "italic"),
                                fill="#B30F1D")

        # Separador
        tk.Frame(frame_sidebar, bg="#2D2D2D", height=1).pack(
            fill="x", padx=15, pady=(5, 15))

        # Label sección
        tk.Label(frame_sidebar, text="MENÚ PRINCIPAL",
                 font=("Helvetica", 7, "bold"),
                 bg="#1A1A1A", fg=COLOR_TEXT_MUTED).pack(
            anchor="w", padx=15, pady=(0, 8))

        # Botones de navegación con íconos de texto
        nav_items = [
            ("🏠  Inicio", "inicio"),
            ("🔍  Explorar 2x1", "explorar"),
            ("⚡  Two Pack Match", "match"),
            ("�  Historial", "historial"),
            ("�  Mi Perfil", "perfil"),
        ]

        self.nav_botones = {}
        for texto, seccion in nav_items:
            btn = tk.Button(
                frame_sidebar,
                text=texto,
                font=("Helvetica", 10),
                bg="#1A1A1A",
                fg=COLOR_TEXT_MAIN,
                bd=0,
                anchor="w",
                padx=20,
                pady=6,
                cursor="hand2",
                activebackground=COLOR_ACCENT_RED,
                activeforeground=COLOR_TEXT_MAIN,
                command=lambda s=seccion: self.navegar_a(s)
            )
            btn.pack(fill="x", pady=1)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2D2D2D"))
            btn.bind("<Leave>", lambda e, b=btn, s=seccion: b.config(
                bg=COLOR_ACCENT_RED if self.seccion_actual == s else "#1A1A1D"))
            self.nav_botones[seccion] = btn

        # Set initial nav button color
        if "inicio" in self.nav_botones:
            self.nav_botones["inicio"].config(bg=COLOR_ACCENT_RED)

        lbl_user = tk.Label(frame_sidebar, text=f"👤 {self.usuario_actual['nombre']}", 
                            font=("Helvetica", 10, "bold"), bg="#1A1A1A", fg=COLOR_TEXT_MAIN)
        lbl_user.pack(pady=(20, 10))

        btn_cerrar = tk.Button(frame_sidebar, text="🚪 Cerrar Sesión", 
                               font=("Helvetica", 10, "bold"), bg="#2A1B1D", fg="#E74C3C", 
                               bd=0, cursor="hand2", command=lambda: self.parent.cambiar_panel(PantallaAutenticacion))
        btn_cerrar.pack(side="bottom", fill="x", pady=10)
        self.parent.configurar_animacion_boton(btn_cerrar, "#2A1B1D", COLOR_ACCENT_RED, COLOR_RED_ACTIVE)

        # --- CONTENEDOR PRINCIPAL ---
        self.frame_principal = tk.Frame(self, bg=COLOR_BG)
        self.frame_principal.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.mostrar_catalogo_matchmaker()
        
        # Iniciar sincronización automática del catálogo
        self._iniciar_sincronizacion()
        
    def _iniciar_sincronizacion(self):
        # Only update catalog if we're in a section that shows it and widgets exist
        try:
            if self.seccion_actual in ["inicio", "explorar", "match"]:
                # Check all required widgets
                if (hasattr(self, 'scrollable_frame') and 
                    hasattr(self, 'cb_zona') and 
                    hasattr(self, 'cb_categoria') and 
                    self.scrollable_frame.winfo_exists() and 
                    self.cb_zona.winfo_exists() and 
                    self.cb_categoria.winfo_exists()):
                    self.actualizar_catalogo()
        except Exception:
            pass
            
        # Schedule next sync
        try:
            self.sync_after_id = self.after(5000, self._iniciar_sincronizacion)
        except Exception:
            pass

    def mostrar_catalogo_matchmaker(self):
        # Limpiar contenido principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # --- Sección 1: Catálogo de Descuentos (izquierda) ---
        frame_catalogo = tk.Frame(self.frame_principal, bg=COLOR_BG)
        frame_catalogo.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Título del catálogo
        tk.Label(frame_catalogo, text="🎁 CATÁLOGO DE DESCUENTOS 2x1", font=("Helvetica", 14, "bold"), 
                bg=COLOR_BG, fg=COLOR_RAYO_YELLOW).pack(anchor="w", pady=(0, 10))

        # Filtros rápidos
        frame_filtros = tk.Frame(frame_catalogo, bg=COLOR_BG)
        frame_filtros.pack(fill="x", pady=(0, 15))

        tk.Label(frame_filtros, text="Zona:", font=("Helvetica", 9, "bold"), 
                bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 5))
        self.cb_zona = ttk.Combobox(frame_filtros, values=["Todas", "La Recoleta", "El Prado", "Zona UCATEC", "Zona Central", "América Oeste"], 
                                     state="readonly", width=20)
        self.cb_zona.pack(side="left", padx=(0, 20))
        self.cb_zona.set("Todas")
        self.cb_zona.bind("<<ComboboxSelected>>", lambda e: self.actualizar_catalogo())

        tk.Label(frame_filtros, text="Categoría:", font=("Helvetica", 9, "bold"), 
                bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 5))
        self.cb_categoria = ttk.Combobox(frame_filtros, values=["Todas", "Gastronomía", "Pubs / Discotecas", "Cafeterías", "Eventos / Conciertos", "Otros"], 
                                          state="readonly", width=20)
        self.cb_categoria.pack(side="left")
        self.cb_categoria.set("Todas")
        self.cb_categoria.bind("<<ComboboxSelected>>", lambda e: self.actualizar_catalogo())

        # Canvas y scroll para tarjetas
        frame_scroll = tk.Frame(frame_catalogo, bg=COLOR_BG)
        frame_scroll.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(frame_scroll, bg=COLOR_BG, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLOR_BG)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Renderizar tarjetas iniciales
        self.actualizar_catalogo()

        # --- Sección 2: Motor Matchmaker IA (derecha) ---
        frame_matchmaker = tk.Frame(self.frame_principal, bg=COLOR_CARD, 
                                    highlightthickness=1, highlightbackground="#2D2D2D", width=380)
        frame_matchmaker.pack(side="right", fill="y")
        frame_matchmaker.pack_propagate(False)

        lbl_icon = tk.Label(frame_matchmaker, text="⚡", font=("Helvetica", 28), 
                           bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW)
        lbl_icon.pack(pady=(20, 0))

        lbl_titulo = tk.Label(frame_matchmaker, text="MOTOR MATCHMAKER IA", 
                             font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN)
        lbl_titulo.pack(pady=5)

        lbl_sub = tk.Label(frame_matchmaker, text="Cochabamba Ciudad Inteligente", 
                          font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED)
        lbl_sub.pack(pady=(0, 20))

        # Promo seleccionada
        self.lbl_promo_seleccionada = tk.Label(frame_matchmaker, text="❌ No hay promoción seleccionada", 
                                               font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=340)
        self.lbl_promo_seleccionada.pack(pady=(0, 15))

        # --- FORMULARIO ---
        frame_campos = tk.Frame(frame_matchmaker, bg=COLOR_CARD)
        frame_campos.pack(fill="x", padx=25)

        tk.Label(frame_campos, text="TU VENTANA TEMPORAL DE DISPONIBILIDAD", 
                font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        frame_horas = tk.Frame(frame_campos, bg=COLOR_CARD)
        frame_horas.pack(fill="x", pady=(0, 12))

        tk.Label(frame_horas, text="Desde:", font=("Helvetica", 9), 
                bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.cb_desde = ttk.Combobox(frame_horas, values=[str(i) for i in range(8, 24)], width=5, state="readonly")
        self.cb_desde.pack(side="left", padx=(0, 15))
        self.cb_desde.set("12")

        tk.Label(frame_horas, text="Hasta:", font=("Helvetica", 9), 
                bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.cb_hasta = ttk.Combobox(frame_horas, values=[str(i) for i in range(8, 24)], width=5, state="readonly")
        self.cb_hasta.pack(side="left")
        self.cb_hasta.set("14")

        self.check_genero_var = tk.BooleanVar(value=False)
        chk_genero = tk.Checkbutton(
            frame_campos, 
            text="Activar restricción de seguridad (Match solo con mi mismo género)", 
            variable=self.check_genero_var,
            font=("Helvetica", 9),
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MAIN,
            activebackground=COLOR_CARD,
            activeforeground=COLOR_RAYO_YELLOW,
            selectcolor=COLOR_BG,
            bd=0
        )
        chk_genero.pack(anchor="w", pady=(10, 25))

        self.btn_match = tk.Button(
            frame_matchmaker, 
            text="🤝 Quiero aprovechar este 2x1", 
            font=("Helvetica", 11, "bold"), 
            bg="#333333", 
            fg=COLOR_TEXT_MUTED, 
            bd=0, 
            cursor="hand2",
            state="disabled",
            command=self.ejecutar_matchmaking
        )
        self.btn_match.pack(fill="x", padx=25, ipady=12, pady=(0, 15))

        self.lbl_status = tk.Label(frame_matchmaker, text="Sistema Matchmaker listo. Selecciona una promoción!", 
                                   font=("Helvetica", 9, "italic"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=340)
        self.lbl_status.pack(pady=(0, 15))

    def mostrar_chat(self):
        # Limpiar contenido principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        
        # Crear y mostrar el chat
        self.chat = SalaChatTemporal(self, self.match_encontrado, self.promo_seleccionada, self.hora_fin)
        self.chat.pack(fill="both", expand=True, padx=0, pady=0)

    def cerrar_chat(self):
        self.chat = None
        self.mostrar_catalogo_matchmaker()
        
    def navegar_a(self, seccion):
        self.seccion_actual = seccion
        # Actualizar colores de botones de nav
        for s, btn in self.nav_botones.items():
            btn.config(bg=COLOR_ACCENT_RED if s == seccion else "#1A1A1D")
        # Navegar según sección
        if seccion == "inicio" or seccion == "explorar" or seccion == "match":
            self.mostrar_catalogo_matchmaker()
        elif seccion == "perfil":
            self.mostrar_perfil()
        elif seccion == "historial":
            self.mostrar_historial()

    def mostrar_perfil(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        u = self.usuario_actual

        # Encabezado de sección
        tk.Label(self.frame_principal,
                 text="Mi Perfil Two Pack",
                 font=("Helvetica", 18, "bold"),
                 bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        tk.Label(self.frame_principal,
                 text="Tu identidad en el ecosistema urbano de Cochabamba",
                 font=("Helvetica", 10),
                 bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(0, 20))

        # Layout de dos columnas: izquierda=card avatar, derecha=datos
        frame_body = tk.Frame(self.frame_principal, bg=COLOR_BG)
        frame_body.pack(fill="both", expand=True)

        # --- COLUMNA IZQUIERDA: Avatar y stats ---
        col_izq = tk.Frame(frame_body, bg=COLOR_CARD,
                           highlightthickness=1, highlightbackground="#2D2D2D",
                           width=220)
        col_izq.pack(side="left", fill="y", padx=(0, 15))
        col_izq.pack_propagate(False)

        # Avatar simulado con inicial del nombre
        canvas_av = tk.Canvas(col_izq, width=90, height=90,
                              bg=COLOR_CARD, bd=0, highlightthickness=0)
        canvas_av.pack(pady=(25, 10))
        canvas_av.create_oval(5, 5, 85, 85,
                              fill=COLOR_ACCENT_RED, outline="")
        inicial = u.get("nombre", "U")[0].upper()
        canvas_av.create_text(45, 45, text=inicial,
                              font=("Helvetica", 36, "bold"),
                              fill="#FFFFFF")

        tk.Label(col_izq,
                 text=u.get("nombre", "Usuario"),
                 font=("Helvetica", 13, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                 wraplength=190, justify="center").pack()

        tk.Label(col_izq,
                 text=u.get("genero", "No especificado"),
                 font=("Helvetica", 9),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=(3, 0))

        # Badge de estado
        estado = u.get("estado", "Activo")
        color_estado = COLOR_SUCCESS if estado == "Activo" else COLOR_ACCENT_RED
        tk.Label(col_izq, text=f"● {estado}",
                 font=("Helvetica", 9, "bold"),
                 bg=COLOR_CARD, fg=color_estado).pack(pady=(5, 20))

        # Separador
        tk.Frame(col_izq, bg="#2D2D2D", height=1).pack(
            fill="x", padx=15, pady=(0, 15))

        # Stats de confianza
        stats = [
            ("⭐", str(u.get("confianza", 5.0)), "Puntuación"),
            ("🤝", str(u.get("matches", 0)), "Matches"),
            ("🚫", str(u.get("reportes", 0)), "Reportes"),
        ]
        for icono, valor, etiqueta in stats:
            frame_stat = tk.Frame(col_izq, bg=COLOR_CARD)
            frame_stat.pack(fill="x", padx=15, pady=4)
            tk.Label(frame_stat,
                     text=f"{icono}  {valor}",
                     font=("Helvetica", 13, "bold"),
                     bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW,
                     anchor="w").pack(side="left")
            tk.Label(frame_stat,
                     text=etiqueta,
                     font=("Helvetica", 9),
                     bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                     anchor="e").pack(side="right")

        # --- COLUMNA DERECHA: Datos editables y universidad ---
        col_der = tk.Frame(frame_body, bg=COLOR_BG)
        col_der.pack(side="right", fill="both", expand=True)

        # Card datos editables
        card_datos = tk.Frame(col_der, bg=COLOR_CARD,
                              highlightthickness=1,
                              highlightbackground="#2D2D2D")
        card_datos.pack(fill="x", pady=(0, 15))

        tk.Label(card_datos,
                 text="INFORMACIÓN DE CUENTA",
                 font=("Helvetica", 8, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(
            anchor="w", padx=20, pady=(15, 10))

        self.entradas_perfil = {}

        campos_editables = [
            ("NOMBRE COMPLETO", "nombre"),
            ("UNIVERSIDAD / INSTITUCIÓN", "universidad"),
            ("GÉNERO", "genero"),
        ]
        for label_txt, clave in campos_editables:
            tk.Label(card_datos, text=label_txt,
                     font=("Helvetica", 8, "bold"),
                     bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(
                anchor="w", padx=20, pady=(6, 2))
            en = tk.Entry(card_datos,
                          font=("Helvetica", 11),
                          bg="#2D2D2D", fg=COLOR_TEXT_MAIN,
                          bd=0, highlightthickness=1,
                          highlightbackground="#3D3D3D")
            en.insert(0, u.get(clave, ""))
            en.pack(fill="x", padx=20, ipady=6, pady=(0, 6))
            self.entradas_perfil[clave] = en

        btn_guardar = tk.Button(
            card_datos,
            text="💾  Guardar cambios de perfil",
            font=("Helvetica", 10, "bold"),
            bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN,
            bd=0, cursor="hand2",
            command=self.guardar_perfil
        )
        btn_guardar.pack(fill="x", padx=20, ipady=9, pady=15)
        self.parent.configurar_animacion_boton(
            btn_guardar, COLOR_SUCCESS, "#27AE60", "#1E8449")

        # Card universidad con info de seguridad
        card_seg = tk.Frame(col_der, bg=COLOR_CARD,
                            highlightthickness=1,
                            highlightbackground="#2D2D2D")
        card_seg.pack(fill="x")

        tk.Label(card_seg,
                 text="🔒  SEGURIDAD DE CUENTA",
                 font=("Helvetica", 9, "bold"),
                 bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW).pack(
            anchor="w", padx=20, pady=(15, 8))
        tk.Label(card_seg,
                 text="Tu correo universitario garantiza la autenticidad\n"
                      "de tu perfil dentro del ecosistema Two Pack.\n"
                      "Los perfiles verificados tienen mayor prioridad\n"
                      "en el algoritmo de emparejamiento.",
                 font=("Helvetica", 9),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 justify="left").pack(anchor="w", padx=20, pady=(0, 15))

    def guardar_perfil(self):
        from tkinter import messagebox
        for clave, entrada in self.entradas_perfil.items():
            valor = entrada.get().strip()
            if valor:
                self.usuario_actual[clave] = valor
        messagebox.showinfo(
            "Perfil actualizado ✓",
            f"Los datos de {self.usuario_actual['nombre']} "
            f"han sido guardados correctamente.")

    def mostrar_detalle_promo(self, promo):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # Botón volver
        btn_volver = tk.Button(
            self.frame_principal,
            text="← Volver al catálogo",
            font=("Helvetica", 9),
            bg=COLOR_BG, fg=COLOR_TEXT_MUTED,
            bd=0, cursor="hand2",
            command=self.mostrar_catalogo_matchmaker
        )
        btn_volver.pack(anchor="w", pady=(0, 15))
        btn_volver.bind("<Enter>",
            lambda e: btn_volver.config(fg=COLOR_ACCENT_RED))
        btn_volver.bind("<Leave>",
            lambda e: btn_volver.config(fg=COLOR_TEXT_MUTED))

        # Header de la promo
        frame_header = tk.Frame(self.frame_principal, bg=COLOR_CARD,
                               highlightthickness=1,
                               highlightbackground="#2D2D2D")
        frame_header.pack(fill="x", pady=(0, 15))

        # Badge 2x1
        tk.Label(frame_header, text="  2x1  ",
                 font=("Helvetica", 10, "bold"),
                 bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN).pack(
            anchor="ne", padx=15, pady=(15, 0))

        tk.Label(frame_header,
                 text=promo["titulo"],
                 font=("Helvetica", 16, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                 wraplength=600, justify="left").pack(
            anchor="w", padx=20, pady=(10, 5))

        tk.Label(frame_header,
                 text=f"📂  {promo['cat']}",
                 font=("Helvetica", 10),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(
            anchor="w", padx=20, pady=(0, 15))

        # Cuerpo: dos columnas
        frame_cuerpo = tk.Frame(self.frame_principal, bg=COLOR_BG)
        frame_cuerpo.pack(fill="both", expand=True)

        # Columna izquierda: info
        col_info = tk.Frame(frame_cuerpo, bg=COLOR_BG)
        col_info.pack(side="left", fill="both", expand=True, padx=(0, 15))

        # Card info detallada
        card_info = tk.Frame(col_info, bg=COLOR_CARD,
                            highlightthickness=1,
                            highlightbackground="#2D2D2D")
        card_info.pack(fill="x", pady=(0, 15))

        tk.Label(card_info,
                 text="DETALLES DE LA PROMOCIÓN",
                 font=("Helvetica", 8, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(
            anchor="w", padx=20, pady=(15, 10))

        detalles = [
            ("📍 Zona / Ubicación", promo.get("zona", "—")),
            ("📅 Fecha de vencimiento", promo.get("vence", "—")),
            ("💰 Precio referencial", f"Bs. {promo.get('precio_ref', '—')}"),
            ("💸 Tu ahorro estimado",
             f"Bs. {promo.get('precio_ref', '—')} "
             f"(pagas solo la mitad)"),
        ]
        for etiqueta, valor in detalles:
            fila = tk.Frame(card_info, bg=COLOR_CARD)
            fila.pack(fill="x", padx=20, pady=5)
            tk.Label(fila, text=etiqueta,
                     font=("Helvetica", 9, "bold"),
                     bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                     width=26, anchor="w").pack(side="left")
            tk.Label(fila, text=valor,
                     font=("Helvetica", 10),
                     bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                     anchor="w").pack(side="left")

        tk.Frame(card_info, bg="#2D2D2D", height=1).pack(
            fill="x", padx=20, pady=10)

        tk.Label(card_info,
                 text="DESCRIPCIÓN COMPLETA",
                 font=("Helvetica", 8, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(
            anchor="w", padx=20, pady=(0, 6))

        desc_text = promo.get(
            "descripcion",
            "Disfruta esta promoción exclusiva 2x1 en "
            f"{promo['zona']}, Cochabamba. Válido hasta "
            f"{promo.get('vence', 'fecha indicada')}. "
            "Presenta la app Two Pack al momento de pagar.")
        tk.Label(card_info,
                 text=desc_text,
                 font=("Helvetica", 10),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                 wraplength=380, justify="left").pack(
            anchor="w", padx=20, pady=(0, 20))

        # Card mapa simulado de la zona
        card_mapa = tk.Frame(col_info, bg=COLOR_CARD,
                            highlightthickness=1,
                            highlightbackground="#2D2D2D")
        card_mapa.pack(fill="x")

        tk.Label(card_mapa,
                 text="📍  ZONA DEL ESTABLECIMIENTO",
                 font=("Helvetica", 8, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(
            anchor="w", padx=20, pady=(15, 8))

        # Mapa simulado con canvas
        canvas_mapa = tk.Canvas(card_mapa, width=400, height=120,
                               bg="#1A2A1A", bd=0,
                               highlightthickness=0)
        canvas_mapa.pack(padx=20, pady=(0, 15))

        # Cuadrícula de calles simulada
        for i in range(0, 420, 40):
            canvas_mapa.create_line(i, 0, i, 120,
                                   fill="#2D3D2D", width=1)
        for j in range(0, 130, 30):
            canvas_mapa.create_line(0, j, 400, j,
                                   fill="#2D3D2D", width=1)

        # Pin de ubicación
        canvas_mapa.create_oval(185, 45, 215, 75,
                               fill=COLOR_ACCENT_RED, outline="")
        canvas_mapa.create_text(200, 60,
                               text="📍",
                               font=("Helvetica", 14))
        canvas_mapa.create_text(200, 95,
                               text=promo.get("zona", "Zona"),
                               font=("Helvetica", 9, "bold"),
                               fill=COLOR_RAYO_YELLOW)

        # Columna derecha: panel de acción match
        col_accion = tk.Frame(frame_cuerpo, bg=COLOR_CARD,
                             highlightthickness=1,
                             highlightbackground="#2D2D2D",
                             width=280)
        col_accion.pack(side="right", fill="y")
        col_accion.pack_propagate(False)

        tk.Label(col_accion, text="⚡",
                 font=("Helvetica", 28),
                 bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW).pack(pady=(25, 0))

        tk.Label(col_accion,
                 text="ACTIVAR MATCH",
                 font=("Helvetica", 12, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(pady=5)

        tk.Label(col_accion,
                 text="Selecciona tu disponibilidad\ny encuentra tu compañero",
                 font=("Helvetica", 9),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 justify="center").pack(pady=(0, 20))

        tk.Frame(col_accion, bg="#2D2D2D", height=1).pack(
            fill="x", padx=20, pady=(0, 15))

        # Horario disponible
        tk.Label(col_accion,
                 text="DESDE LAS",
                 font=("Helvetica", 8, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(
            anchor="w", padx=20, pady=(0, 3))
        cb_desde_det = ttk.Combobox(
            col_accion,
            values=[str(i) for i in range(8, 24)],
            state="readonly", width=10)
        cb_desde_det.pack(padx=20, anchor="w", pady=(0, 10))
        cb_desde_det.set("12")

        tk.Label(col_accion,
                 text="HASTA LAS",
                 font=("Helvetica", 8, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(
            anchor="w", padx=20, pady=(0, 3))
        cb_hasta_det = ttk.Combobox(
            col_accion,
            values=[str(i) for i in range(8, 24)],
            state="readonly", width=10)
        cb_hasta_det.pack(padx=20, anchor="w", pady=(0, 20))
        cb_hasta_det.set("14")

        # Botón activar match
        btn_match_det = tk.Button(
            col_accion,
            text="🤝  Quiero este 2x1",
            font=("Helvetica", 11, "bold"),
            bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN,
            bd=0, cursor="hand2",
            command=lambda: self._activar_match_desde_detalle(
                promo, cb_desde_det, cb_hasta_det)
        )
        btn_match_det.pack(fill="x", padx=20, ipady=12, pady=(0, 15))
        self.parent.configurar_animacion_boton(
            btn_match_det, COLOR_ACCENT_RED,
            COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        tk.Label(col_accion,
                 text="🔒 Encuentro seguro en el local",
                 font=("Helvetica", 8),
                 bg=COLOR_CARD, fg=COLOR_SUCCESS).pack()

    def _activar_match_desde_detalle(self, promo, cb_desde, cb_hasta):
        self.promo_seleccionada = promo
        self.mostrar_catalogo_matchmaker()
        # Actualizar los valores en el panel principal
        self.cb_desde.set(cb_desde.get())
        self.cb_hasta.set(cb_hasta.get())
        # Pequeño delay para que cargue el catálogo y luego dispara el match
        self.after(300, self.ejecutar_matchmaking)

    def mostrar_historial(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        tk.Label(self.frame_principal,
                 text="Mis Matches Two Pack",
                 font=("Helvetica", 18, "bold"),
                 bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(
            anchor="w", pady=(0, 4))
        tk.Label(self.frame_principal,
                 text="Historial de experiencias compartidas en Cochabamba",
                 font=("Helvetica", 10),
                 bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(
            anchor="w", pady=(0, 20))

        historial = base_datos_global.get("historial_matches", [])

        if not historial:
            tk.Label(self.frame_principal,
                     text="🤝  Aún no tienes matches.\n"
                          "¡Explora las promos y activa tu primer Two Pack Match!",
                     font=("Helvetica", 12),
                     bg=COLOR_BG, fg=COLOR_TEXT_MUTED,
                     justify="center").pack(expand=True)
            return

        # Scroll
        canvas_h = tk.Canvas(self.frame_principal,
                            bg=COLOR_BG, bd=0, highlightthickness=0)
        scroll_h = ttk.Scrollbar(self.frame_principal,
                               orient="vertical",
                               command=canvas_h.yview)
        frame_lista = tk.Frame(canvas_h, bg=COLOR_BG)
        frame_lista.bind("<Configure>", lambda e: canvas_h.configure(
            scrollregion=canvas_h.bbox("all")))
        canvas_h.create_window((0, 0), window=frame_lista, anchor="nw")
        canvas_h.configure(yscrollcommand=scroll_h.set)
        canvas_h.pack(side="left", fill="both", expand=True)
        scroll_h.pack(side="right", fill="y")

        for match in historial:
            card_m = tk.Frame(frame_lista, bg=COLOR_CARD,
                             highlightthickness=1,
                             highlightbackground="#2D2D2D")
            card_m.pack(fill="x", pady=8)

            # Header del match
            frame_mh = tk.Frame(card_m, bg=COLOR_CARD)
            frame_mh.pack(fill="x", padx=20, pady=(15, 8))

            # Avatar inicial
            canvas_mini = tk.Canvas(frame_mh, width=44, height=44,
                                   bg=COLOR_CARD, bd=0,
                                   highlightthickness=0)
            canvas_mini.pack(side="left", padx=(0, 12))
            canvas_mini.create_oval(2, 2, 42, 42,
                                   fill=COLOR_ACCENT_RED, outline="")
            ini = match["usuario_match"][0].upper()
            canvas_mini.create_text(22, 22, text=ini,
                                   font=("Helvetica", 18, "bold"),
                                   fill="#FFFFFF")

            frame_info_m = tk.Frame(frame_mh, bg=COLOR_CARD)
            frame_info_m.pack(side="left", fill="x", expand=True)

            tk.Label(frame_info_m,
                     text=f"{match['usuario_match']} • {match['genero_match']}",
                     font=("Helvetica", 11, "bold"),
                     bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, anchor="w").pack(fill="x")
            tk.Label(frame_info_m,
                     text=f"{match['promo']} • {match['zona']}",
                     font=("Helvetica", 9),
                     bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(fill="x")

            # Fecha y hora
            tk.Label(frame_mh,
                     text=f"{match['fecha']} • {match['hora']}",
                     font=("Helvetica", 9),
                     bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(side="right")

            # Reseña y puntuación si existen
            if match.get("reseña_dada") or match.get("puntuacion_dada"):
                frame_review = tk.Frame(card_m, bg="#2A1A1A")
                frame_review.pack(fill="x", padx=20, pady=(0, 15))
                
                if match.get("puntuacion_dada"):
                    tk.Label(frame_review,
                             text=f"⭐ {'★' * match['puntuacion_dada']}{'☆' * (5 - match['puntuacion_dada'])}",
                             font=("Helvetica", 12),
                             bg="#2A1A1A", fg=COLOR_RAYO_YELLOW).pack(anchor="w", padx=15, pady=(10, 0))
                
                if match.get("reseña_dada"):
                    tk.Label(frame_review,
                             text=f'"{match["reseña_dada"]}"',
                             font=("Helvetica", 9),
                             bg="#2A1A1A", fg=COLOR_TEXT_MAIN,
                             wraplength=400, justify="left").pack(anchor="w", padx=15, pady=(5, 10))

    def crear_tarjeta_promo(self, parent, promo):
        frame_tarjeta = tk.Frame(parent, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#3D3D3D", padx=15, pady=15)
        
        lbl_badge = tk.Label(frame_tarjeta, text=" 2x1 ", font=("Helvetica", 9, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN)
        lbl_badge.pack(anchor="ne", pady=(0, 5))

        lbl_titulo = tk.Label(frame_tarjeta, text=promo["titulo"], font=("Helvetica", 11, "bold"), 
                             bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, wraplength=320, justify="left")
        lbl_titulo.pack(anchor="w", pady=(0, 5))

        lbl_detalles = tk.Label(frame_tarjeta, text=f"📍 {promo['zona']} • 📂 {promo['cat']}\n📅 Vence: {promo['vence']}", 
                                font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, justify="left")
        lbl_detalles.pack(anchor="w", pady=(0, 10))

        # Badge de ahorro estimado
        precio = promo.get("precio_ref", None)
        if precio:
            frame_precio = tk.Frame(frame_tarjeta, bg=COLOR_CARD)
            frame_precio.pack(anchor="w", pady=(0, 8))
            tk.Label(frame_precio,
                     text=f"💰 Ahorro estimado: Bs. {precio}",
                     font=("Helvetica", 10, "bold"),
                     bg=COLOR_CARD, fg=COLOR_SUCCESS).pack(side="left")

        btn_seleccionar = tk.Button(frame_tarjeta, text="✅ Seleccionar", font=("Helvetica", 9, "bold"), 
                                     bg="#2D2D2D", fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2",
                                     command=lambda p=promo, f=frame_tarjeta: (
                                         self.seleccionar_promo(p, f),
                                         self.mostrar_detalle_promo(p)
                                     ))
        btn_seleccionar.pack(fill="x", ipady=6)
        self.parent.configurar_animacion_boton(btn_seleccionar, "#2D2D2D", COLOR_ACCENT_RED, COLOR_RED_ACTIVE)

        # Almacenar referencia para resaltar
        frame_tarjeta.btn_seleccionar = btn_seleccionar
        frame_tarjeta.promo = promo
        
        return frame_tarjeta

    def seleccionar_promo(self, promo, frame_tarjeta):
        # Desresaltar tarjeta anterior
        for tarjeta in self.tarjetas:
            tarjeta.configure(highlightbackground="#3D3D3D", highlightthickness=1)
            tarjeta.btn_seleccionar.configure(bg="#2D2D2D", text="✅ Seleccionar")
        
        # Resaltar nueva tarjeta
        frame_tarjeta.configure(highlightbackground=COLOR_ACCENT_RED, highlightthickness=2)
        frame_tarjeta.btn_seleccionar.configure(bg=COLOR_ACCENT_RED, text="✓ SELECCIONADA")
        self.promo_seleccionada = promo
        
        # Actualizar panel matchmaker
        self.lbl_promo_seleccionada.config(text=f"📌 {promo['titulo']}", fg=COLOR_RAYO_YELLOW)
        self.btn_match.config(state="normal", bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN)
        self.lbl_status.config(text="Promoción seleccionada! Ingresa tu disponibilidad.")
        self.parent.configurar_animacion_boton(self.btn_match, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def actualizar_catalogo(self):
        try:
            # Check if scrollable_frame still exists
            if not hasattr(self, 'scrollable_frame') or not self.scrollable_frame.winfo_exists():
                return
                
            # Limpiar tarjetas existentes
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self.tarjetas = []
            
            # Obtener filtros
            filtro_zona = self.cb_zona.get()
            filtro_categoria = self.cb_categoria.get()
            
            # Filtrar y renderizar tarjetas
            for promo in base_datos_global["promociones"]:
                if (filtro_zona == "Todas" or promo["zona"] == filtro_zona) and \
                   (filtro_categoria == "Todas" or promo["cat"] == filtro_categoria):
                    tarjeta = self.crear_tarjeta_promo(self.scrollable_frame, promo)
                    tarjeta.pack(fill="x", pady=8)
                    self.tarjetas.append(tarjeta)
            
            # Si había una promo seleccionada y sigue presente, volver a seleccionarla
            if self.promo_seleccionada:
                for tarjeta in self.tarjetas:
                    if tarjeta.promo["id"] == self.promo_seleccionada["id"]:
                        self.seleccionar_promo(tarjeta.promo, tarjeta)
                        break
        except Exception as e:
            # Silently handle any errors if widgets are destroyed
            pass

    def ejecutar_matchmaking(self):
        if not self.promo_seleccionada:
            messagebox.showwarning("Promoción requerida", "Por favor selecciona una promoción primero!")
            return
            
        self.lbl_status.config(text="🤖 Escaneando base de datos urbana en tiempo real...", fg=COLOR_RAYO_YELLOW)
        self.btn_match.config(state="disabled", bg="#444444", text="Procesando algoritmo...")
        
        self.after(1500, self._procesar_match_resultado)
    
    def _procesar_match_resultado(self):
        id_oferta_elegida = self.promo_seleccionada["id"]
        desde = int(self.cb_desde.get())
        hasta = int(self.cb_hasta.get())
        filtro_estricto = self.check_genero_var.get()
        self.hora_fin = hasta

        if desde >= hasta:
            messagebox.showerror("Error de Tiempo", "La hora de inicio debe ser menor a la de conclusión.")
            self.restaurar_boton_match()
            return

        self.match_encontrado = None
        for candidato in base_datos_global["pool_solicitudes"]:
            if candidato["oferta_id"] != id_oferta_elegida:
                continue
            inicio_comun = max(desde, candidato["hora_inicio"])
            fin_comun = min(hasta, candidato["hora_fin"])
            if inicio_comun >= fin_comun:
                continue
            if filtro_estricto and candidato["genero"] != self.usuario_actual["genero"]:
                continue
            if candidato["filtro_genero"] and candidato["genero"] != self.usuario_actual["genero"]:
                continue
            self.match_encontrado = candidato
            break

        self.restaurar_boton_match()

        if self.match_encontrado:
            self.lbl_status.config(text="¡MATCH LOGRADO EXITOSAMENTE! 🎉", fg=COLOR_SUCCESS)
            messagebox.showinfo(
                "⚡ ¡Match Two Pack Detectado!", 
                f"¡Felicidades, {self.usuario_actual['nombre']}!\n\n"
                f"Hemos encontrado un compañero compatible en Cochabamba:\n"
                f"👤 Nombre: {self.match_encontrado['usuario']}\n"
                f"🕒 Ventana de encuentro: Entre las {max(desde, self.match_encontrado['hora_inicio'])}:00 y las {min(hasta, self.match_encontrado['hora_fin'])}:00\n\n"
                f"Se ha habilitado un chat temporal seguro para coordinar el encuentro."
            )
            self.mostrar_chat()
        else:
            self.lbl_status.config(text="Sin coincidencias inmediatas. En cola de espera.", fg=COLOR_TEXT_MUTED)
            messagebox.showwarning(
                "Solicitud en Espera", 
                "No hay solicitudes idénticas en este momento.\n\nTu petición se ha quedado registrada de forma inteligente en la cola de la zona. Te notificaremos de inmediato por WhatsApp en cuanto otro estudiante aplique al mismo beneficio."
            )

    def restaurar_boton_match(self):
        self.btn_match.config(state="normal", bg=COLOR_ACCENT_RED, text="🤝 Quiero aprovechar este 2x1")
        self.parent.configurar_animacion_boton(self.btn_match, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

# --- PANEL DEL COMERCIO LOCAL ---
class PanelComercio(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.usuario_actual = parent.usuario_actual

        self.configurar_estilos_tabla()
        self.inicializar_ui()
        self.actualizar_tabla()

    def configurar_estilos_tabla(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, 
                       fieldbackground=COLOR_CARD, rowheight=28, borderwidth=0)
        style.map("Treeview", background=[("selected", COLOR_ACCENT_RED)], 
                 foreground=[("selected", "white")])
        style.configure("Treeview.Heading", bg="#2D2D2D", fg=COLOR_TEXT_MAIN, 
                       relief="flat", font=("Helvetica", 9, "bold"))
        style.map("Treeview.Heading", background=[("active", "#3D3D3D")])

    def inicializar_ui(self):
        # --- HEADER ---
        frame_header = tk.Frame(self, bg=COLOR_CARD, height=60)
        frame_header.pack(fill="x", side="top")
        frame_header.pack_propagate(False)

        lbl_titulo = tk.Label(frame_header, text=f"🏪 Panel de {self.usuario_actual['nombre']}", 
                              font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN)
        lbl_titulo.pack(side="left", padx=15, pady=15)

        btn_cerrar = tk.Button(frame_header, text="Cerrar Sesión", 
                               font=("Helvetica", 9, "bold"), bg="#333333", fg=COLOR_TEXT_MAIN, 
                               bd=0, cursor="hand2", padx=10, 
                               command=lambda: self.cerrar_sesion())
        btn_cerrar.pack(side="right", padx=15, pady=15)
        self.parent.configurar_animacion_boton(btn_cerrar, "#333333", "#444444", "#222222")

        # --- CUERPO DIVIDIDO ---
        frame_cuerpo = tk.Frame(self, bg=COLOR_BG)
        frame_cuerpo.pack(fill="both", expand=True, padx=15, pady=15)

        # Columna izquierda: Formulario
        frame_izq = tk.Frame(frame_cuerpo, bg=COLOR_BG, width=280)
        frame_izq.pack(side="left", fill="y", padx=(0, 10))
        frame_izq.pack_propagate(False)

        tk.Label(frame_izq, text="PUBLICAR NUEVO 2x1", 
                font=("Helvetica", 10, "bold"), bg=COLOR_BG, fg=COLOR_RAYO_YELLOW).pack(anchor="w", pady=(0, 15))

        tk.Label(frame_izq, text="TÍTULO DE LA OFERTA", 
                font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_titulo = tk.Entry(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                   bd=0, highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_titulo.pack(fill="x", ipady=5, pady=(0, 10))

        tk.Label(frame_izq, text="CATEGORÍA", 
                font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.cb_categoria = ttk.Combobox(frame_izq, values=["Gastronomía", "Pubs / Discotecas", "Cafeterías", "Eventos / Conciertos", "Otros"], state="readonly")
        self.cb_categoria.pack(fill="x", ipady=3, pady=(0, 10))
        self.cb_categoria.set("Gastronomía")

        tk.Label(frame_izq, text="ZONA COMERCIAL", 
                font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.cb_zona = ttk.Combobox(frame_izq, values=["La Recoleta", "El Prado", "Zona UCATEC", "Zona Central", "América Oeste"], state="readonly")
        self.cb_zona.pack(fill="x", ipady=3, pady=(0, 10))
        self.cb_zona.set("Zona UCATEC")

        tk.Label(frame_izq, text="FECHA CADUCIDAD (DD/MM/AAAA)", 
                font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_vence = tk.Entry(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                   bd=0, highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_vence.pack(fill="x", ipady=5, pady=(0, 10))
        self.ent_vence.insert(0, datetime.now().strftime("%d/%m/%Y"))

        tk.Label(frame_izq, text="PRECIO UNITARIO REFERENCIAL (Bs.)", 
                font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_precio = tk.Entry(frame_izq, font=("Helvetica", 10),
                                    bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                    bd=0, highlightthickness=1,
                                    highlightbackground="#2D2D2D")
        self.ent_precio.pack(fill="x", ipady=5, pady=(0, 10))

        tk.Label(frame_izq, text="DESCRIPCIÓN DEL 2x1", 
                font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.txt_desc = tk.Text(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                bd=0, height=4, highlightthickness=1, highlightbackground="#2D2D2D")
        self.txt_desc.pack(fill="x", pady=(0, 15))

        btn_lanzar = tk.Button(frame_izq, text="🚀 Lanzar Promo 2x1", 
                              font=("Helvetica", 11, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN,
                              bd=0, cursor="hand2", command=self.registrar_oferta)
        btn_lanzar.pack(fill="x", ipady=8)
        self.parent.configurar_animacion_boton(btn_lanzar, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        # Columna derecha: Tabla
        frame_der = tk.Frame(frame_cuerpo, bg=COLOR_BG)
        frame_der.pack(side="right", fill="both", expand=True)

        tk.Label(frame_der, text="MIS PROMOCIONES ACTIVAS EN COCHABAMBA", 
                font=("Helvetica", 10, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 15))

        columnas = ("id", "titulo", "categoria", "zona", "vence")
        self.tabla = ttk.Treeview(frame_der, columns=columnas, show="headings")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("titulo", text="Título de la Promo")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("zona", text="Ubicación / Zona")
        self.tabla.heading("vence", text="Vence el")
        self.tabla.column("id", width=40, anchor="center")
        self.tabla.column("titulo", width=180, anchor="w")
        self.tabla.column("categoria", width=100, anchor="center")
        self.tabla.column("zona", width=90, anchor="center")
        self.tabla.column("vence", width=80, anchor="center")
        self.tabla.pack(fill="both", expand=True, pady=(0, 10))

        btn_eliminar = tk.Button(frame_der, text="🗑️ Eliminar Promo Seleccionada", 
                                font=("Helvetica", 9, "bold"), bg="#2D2D2D", fg=COLOR_TEXT_MUTED,
                                bd=0, cursor="hand2", command=self.eliminar_oferta)
        btn_eliminar.pack(anchor="e", ipady=5, ipadx=10)
        self.parent.configurar_animacion_boton(btn_eliminar, "#2D2D2D", COLOR_ACCENT_RED, COLOR_RED_ACTIVE)

    def cerrar_sesion(self):
        self.parent.cambiar_panel(PantallaAutenticacion)

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for promo in base_datos_global["promociones"]:
            self.tabla.insert("", "end", values=(promo["id"], promo["titulo"], promo["cat"], promo["zona"], promo["vence"]))

    def registrar_oferta(self):
        titulo = self.ent_titulo.get().strip()
        categoria = self.cb_categoria.get()
        zona = self.cb_zona.get()
        vence = self.ent_vence.get().strip()
        descripcion = self.txt_desc.get("1.0", tk.END).strip()
        precio_ref = self.ent_precio.get().strip()

        if not titulo or not vence or not descripcion:
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los campos.")
            return

        try:
            datetime.strptime(vence, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error de Formato", "Fecha inválida (usa DD/MM/AAAA).")
            return

        nuevo_id = f"{len(base_datos_global['promociones']) + 1:03d}"
        base_datos_global["promociones"].append({
            "id": nuevo_id, "titulo": titulo, "cat": categoria, "zona": zona, "vence": vence, "precio_ref": precio_ref
        })
        
        guardar_datos()

        self.actualizar_tabla()
        messagebox.showinfo("¡Éxito Total!", f"Tu oferta '{titulo}' está en vivo en Two Pack!")
        
        self.ent_titulo.delete(0, tk.END)
        self.ent_precio.delete(0, tk.END)
        self.txt_desc.delete("1.0", tk.END)

    def eliminar_oferta(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado:
            messagebox.showwarning("Selección Requerida", "Por favor selecciona una promoción.")
            return

        valores = self.tabla.item(item_seleccionado, "values")
        id_promo = valores[0]
        base_datos_global["promociones"] = [p for p in base_datos_global["promociones"] if p["id"] != id_promo]
        
        guardar_datos()
        
        self.actualizar_tabla()
        messagebox.showinfo("Promo Eliminada", "La oferta se ha removido del feed.")

# --- INICIO DE APLICACIÓN ---
if __name__ == "__main__":
    app = TwoPackApp()
    app.mainloop()
