
import tkinter as tk
from tkinter import ttk
import re
import hashlib
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
<<<<<<< Updated upstream
    COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_RAYO_YELLOW, COLOR_ESCUDO_RED,
    get_db_connection, configurar_animacion_boton, configurar_animacion_enlace
=======
    COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_AMARILLO_ORO, COLOR_ESCUDO_RED,
    cargar_datos, guardar_datos, configurar_animacion_boton, configurar_animacion_enlace
>>>>>>> Stashed changes
)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class VistaAutenticacion(tk.Frame):
    def __init__(self, parent, al_ingresar_exitoso):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.al_ingresar_exitoso = al_ingresar_exitoso
        self.modo_registro = False
        
        self.mostrar_splash()

    def mostrar_splash(self):
<<<<<<< Updated upstream
        self.frame_splash = tk.Frame(self, bg=COLOR_BG)
        self.frame_splash.place(relx=0, rely=0, relwidth=1, relheight=1)

        canvas_s = tk.Canvas(self.frame_splash, width=300, height=240, bg=COLOR_BG, bd=0, highlightthickness=0)
        canvas_s.pack(expand=True, pady=(60, 10))

        pts = [40, 30, 260, 30, 210, 140, 140, 200, 70, 140]
        canvas_s.create_polygon(pts, fill=COLOR_ESCUDO_RED, outline="#800A12", width=2)

        canvas_s.create_polygon([25, 20, 50, 20, 38, 43, 52, 43, 30, 73, 36, 48, 25, 48], fill=COLOR_RAYO_YELLOW, outline="black", width=1)
        canvas_s.create_polygon([230, 115, 248, 115, 240, 130, 250, 130, 227, 155, 235, 138, 220, 138], fill=COLOR_RAYO_YELLOW, outline="black", width=1)

        canvas_s.create_text(152, 92, text="2x1", font=("Arial Black", 46, "bold"), fill="#000000")
        canvas_s.create_text(150, 90, text="2x1", font=("Arial Black", 46, "bold"), fill=COLOR_TEXT_MAIN)
        canvas_s.create_text(150, 135, text="PROMO", font=("Arial Black", 16, "bold"), fill=COLOR_TEXT_MAIN)

        canvas_s.create_polygon([85, 148, 215, 148, 197, 178, 103, 178], fill=COLOR_TEXT_MAIN, outline="#CCCCCC", width=1)
        canvas_s.create_text(150, 163, text="Two Pack", font=("Georgia", 16, "bold", "italic"), fill=COLOR_ESCUDO_RED)

        tk.Label(self.frame_splash, text="Divide el gasto, duplica la experiencia.", font=("Helvetica", 11, "italic"), bg=COLOR_BG, fg=COLOR_RAYO_YELLOW).pack(pady=(0, 10))
        tk.Label(self.frame_splash, text="Cargando ecosistema urbano...", font=("Helvetica", 9), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack()

=======
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
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
        lbl_slogan = tk.Label(self, text="Divide el gasto, duplica la experiencia.", font=("Helvetica Neue", 11, "italic"), bg=COLOR_BG, fg=COLOR_RAYO_YELLOW)
        lbl_slogan.pack(pady=(10, 20))
=======
        # --- Contenedor Principal ---
        frame_main = tk.Frame(self, bg=COLOR_BG, padx=25, pady=25)
        frame_main.pack(fill="both", expand=True)
>>>>>>> Stashed changes

        lbl_slogan = tk.Label(frame_main, 
                             text="Plataforma de Smart Economy para Jóvenes Profesionales y Consumidores Urbanos", 
                             font=("Helvetica", 9), bg=COLOR_BG, fg=COLOR_TEXT_MUTED, justify="center", wraplength=360)
        lbl_slogan.pack(pady=(0, 20))

        frame_selector = tk.Frame(frame_main, bg=COLOR_BG)
        frame_selector.pack(pady=(0, 20))

<<<<<<< Updated upstream
        self.btn_estudiante = tk.Button(frame_selector, text="👤 Iniciar Sesión como Estudiante", font=("Helvetica", 10, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=15, pady=8)
        self.btn_estudiante.pack(side="left", padx=5)

        self.btn_comercio = tk.Button(frame_selector, text="🏪 Iniciar Sesión como Dueño de Negocio", font=("Helvetica", 10, "bold"), bg="#333333", fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=15, pady=8)
        self.btn_comercio.pack(side="left", padx=5)
=======
        self.btn_usuario = tk.Button(frame_selector, text="👤 Usuario",
                                        font=("Helvetica", 9, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN,
                                        bd=0, cursor="hand2", padx=15, pady=7, 
                                        command=lambda: self.cambiar_modo(False))
        self.btn_usuario.pack(side="left", padx=3)

        self.btn_comercio = tk.Button(frame_selector, text="🏪 Comercio",
                                    font=("Helvetica", 9, "bold"), bg="#2A2A2A", fg=COLOR_TEXT_MAIN,
                                    bd=0, cursor="hand2", padx=15, pady=7, 
                                    command=lambda: self.cambiar_modo(False, es_comercio=True))
        self.btn_comercio.pack(side="left", padx=3)
>>>>>>> Stashed changes

        configurar_animacion_boton(self.btn_usuario, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)
        configurar_animacion_boton(self.btn_comercio, "#2A2A2A", "#333333", "#1A1A1A")

        self.frame_auth = tk.Frame(frame_main, bg=COLOR_CARD, padx=25, pady=25, highlightthickness=1, highlightbackground="#333333")
        self.frame_auth.pack(fill="x")

<<<<<<< Updated upstream
            tk.Label(frame_form, text="CORREO ELECTRÓNICO", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
            self.ent_email = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_email.pack(fill="x", ipady=8, pady=(0, 12))
            self.ent_email.insert(0, "estudiante@universidad.edu.bo")

            tk.Label(frame_form, text="CONTRASEÑA", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
            self.ent_pass = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, show="*", insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_pass.pack(fill="x", ipady=8, pady=(0, 20))
            self.ent_pass.insert(0, "123")

            btn_ingresar = tk.Button(frame_form, text="Ingresar de Forma Segura", font=("Helvetica", 11, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=self.procesar_login)
            btn_ingresar.pack(fill="x", ipady=10)
            configurar_animacion_boton(btn_ingresar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")
            
            btn_registrar = tk.Button(frame_form, text="Crear Cuenta Nueva", font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_ACCENT_RED, bd=0, cursor="hand2", command=lambda: self.cambiar_modo(True))
            btn_registrar.pack(pady=15)
=======
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
                                   font=("Helvetica", 11, "bold"),
                                   bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2",
                                   command=self.procesar_login)
        self.btn_accion.grid(row=5, column=0, columnspan=2, sticky="we", ipady=9, pady=(0, 15))

        configurar_animacion_boton(self.btn_accion, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        lbl_enlace = tk.Label(self.frame_auth, text="¿No tienes una cuenta? Crea una gratuita aquí",
                             font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO,
                             cursor="hand2", anchor="center")
        lbl_enlace.grid(row=6, column=0, columnspan=2, sticky="we")
        lbl_enlace.bind("<Button-1>", lambda e: self.cambiar_modo(True))
        configurar_animacion_enlace(lbl_enlace, COLOR_AMARILLO_ORO, COLOR_ACCENT_RED)
        
        # Texto sobre servicio gratuito
        lbl_gratuito = tk.Label(frame_main, text="Servicio 100% gratuito para Usuarios y Comercios Locales",
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

    def cambiar_modo(self, es_registro, es_comercio=False):
        self.modo_registro = es_registro

        if es_registro:
            self.btn_usuario.config(bg="#2A2A2A")
            self.btn_comercio.config(bg="#2A2A2A")
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
>>>>>>> Stashed changes
        else:
            if es_comercio:
                self.btn_usuario.config(bg="#2A2A2A")
                self.btn_comercio.config(bg=COLOR_ACCENT_RED)
            else:
                self.btn_usuario.config(bg=COLOR_ACCENT_RED)
                self.btn_comercio.config(bg="#2A2A2A")
                
            self.lbl_titulo.config(text="Iniciar Sesión")
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
            self.btn_accion.config(text="Acceder a Two Pack", command=lambda: self.procesar_login(es_comercio=es_comercio))
            self.btn_accion.grid(row=5, column=0, columnspan=2, sticky="we", ipady=9, pady=(0, 15))

<<<<<<< Updated upstream
            tk.Label(frame_form, text="NOMBRE COMPLETO", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
            self.ent_nombre_reg = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_nombre_reg.pack(fill="x", ipady=8, pady=(0, 12))

            tk.Label(frame_form, text="CORREO ELECTRÓNICO", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
            self.ent_email_reg = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_email_reg.pack(fill="x", ipady=8, pady=(0, 12))

            tk.Label(frame_form, text="GÉNERO", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(3, 2))
            self.cb_genero_reg = ttk.Combobox(frame_form, values=["Masculino", "Femenino", "Prefiero no decir"], state="readonly", font=("Helvetica", 12))
            self.cb_genero_reg.pack(fill="x", ipady=4, pady=(0, 12))
            self.cb_genero_reg.set("Masculino")

            tk.Label(frame_form, text="UNIVERSIDAD", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(3, 2))
            self.ent_universidad_reg = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_universidad_reg.pack(fill="x", ipady=8, pady=(0, 12))

            tk.Label(frame_form, text="CONTRASEÑA", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
            self.ent_pass_reg = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, show="*", insertbackground="white", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_pass_reg.pack(fill="x", ipady=8, pady=(0, 12))

            tk.Label(frame_form, text="CONFIRMAR CONTRASEÑA", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(3, 2))
            self.ent_pass2_reg = tk.Entry(frame_form, font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, show="*", highlightthickness=1, highlightbackground="#2D2D2D")
            self.ent_pass2_reg.pack(fill="x", ipady=8, pady=(0, 20))

            btn_registrar = tk.Button(frame_form, text="Crear Cuenta de Estudiante", font=("Helvetica", 11, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=self.procesar_registro)
            btn_registrar.pack(fill="x", ipady=10)
            configurar_animacion_boton(btn_registrar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")
            
            btn_volver = tk.Button(frame_form, text="Volver a Iniciar Sesión", font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_ACCENT_RED, bd=0, cursor="hand2", command=lambda: self.cambiar_modo(False))
            btn_volver.pack(pady=15)

    def cambiar_modo(self, modo_registro):
        self.modo_registro = modo_registro
        self.mostrar_login_registro()

    def dibujar_escudo(self):
        canvas_logo = tk.Canvas(self, width=280, height=220, bg=COLOR_BG, bd=0, highlightthickness=0)
        canvas_logo.pack(pady=(0, 5))

        puntos_escudo = [40, 50, 240, 50, 210, 150, 140, 200, 70, 150]
        canvas_logo.create_polygon(puntos_escudo, fill=COLOR_ESCUDO_RED, outline="#800A12", width=2)

        canvas_logo.create_polygon([25, 20, 55, 20, 40, 45, 55, 45, 30, 75, 36, 48, 25, 48], fill=COLOR_RAYO_YELLOW, outline="black", width=1)
        canvas_logo.create_polygon([225, 120, 245, 120, 235, 135, 245, 135, 225, 160, 235, 140, 220, 140], fill=COLOR_RAYO_YELLOW, outline="black", width=1)

        canvas_logo.create_oval(75, 175, 105, 205, fill="#E0E0E0", outline="#A0A0A0", width=2)
        canvas_logo.create_line(90, 190, 90, 182, fill="black", width=2)
        canvas_logo.create_line(90, 190, 100, 195, fill="black", width=1.5)
        canvas_logo.create_oval(230, 100, 260, 130, fill="#E0E0E0", outline="#A0A0A0", width=2)
        canvas_logo.create_line(245, 115, 245, 107, fill="black", width=2)
        canvas_logo.create_line(245, 115, 252, 122, fill="black", width=1.5)

        canvas_logo.create_polygon([50, 160, 60, 150, 65, 165], fill="#5D3FD3")
        canvas_logo.create_oval(190, 25, 202, 35, fill="#E0E0E0", outline="")

        canvas_logo.create_text(152, 92, text="2x1", font=("Arial Black", 44, "bold"), fill="#000000")
        canvas_logo.create_text(150, 90, text="2x1", font=("Arial Black", 44, "bold"), fill=COLOR_TEXT_MAIN)
        canvas_logo.create_text(150, 135, text="PROMO", font=("Arial Black", 16, "bold"), fill=COLOR_TEXT_MAIN)

        canvas_logo.create_polygon([80, 150, 200, 150, 180, 180, 100, 180], fill="#800A12")
        canvas_logo.create_polygon([85, 152, 195, 152, 185, 178, 95, 178], fill=COLOR_TEXT_MAIN, outline="#CCCCCC", width=1)
        canvas_logo.create_text(150, 163, text="Two Pack", font=("Georgia", 15, "bold", "italic"), fill=COLOR_ESCUDO_RED)

    def seleccionar_rol(self, rol):
        self.rol_actual = rol
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
=======
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
        
        tk.Label(ventana, text=titulo, font=("Helvetica", 15, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT_RED).pack(pady=(0, 10))
        
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
        
        tk.Label(ventana, text=titulo, font=("Helvetica", 15, "bold"), bg=COLOR_CARD, fg=COLOR_SUCCESS).pack(pady=(0, 10))
        
        tk.Label(ventana, text=mensaje, font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=320, justify="center").pack(pady=(0, 20))
        
        btn_aceptar = tk.Button(ventana, text="¡Genial!", font=("Helvetica", 10, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=20, pady=8, command=lambda: [ventana.destroy(), self.cambiar_modo(False)])
        btn_aceptar.pack(fill="x", padx=40)
        configurar_animacion_boton(btn_aceptar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")

    def procesar_login(self, es_comercio=False):
>>>>>>> Stashed changes
        email = self.ent_email.get().strip()
        password = self.ent_pass.get().strip()

        if not email or not password:
            self._mostrar_dialogo_alerta("Campos Incompletos", "Por favor completa todos los campos.")
            return

<<<<<<< Updated upstream
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (email,))
            estudiante = cursor.fetchone()
            
            if estudiante and estudiante['password_hash'] == hash_password(password):
                usuario = {
                    'id': estudiante['id'],
                    'nombre': estudiante['nombre'],
                    'apellido': estudiante['apellido'],
                    'correo': estudiante['correo'],
                    'rol': 'estudiante',
                    'universidad': estudiante['universidad'],
                    'genero': estudiante.get('genero', ''),
                    'confianza': float(estudiante['reputacion'])
                }
                self.al_ingresar_exitoso(usuario)
                conn.close()
                return
            
            cursor.execute("SELECT * FROM negocios WHERE correo = %s", (email,))
            negocio = cursor.fetchone()
            
            if negocio and negocio['password_hash'] == hash_password(password):
                usuario = {
                    'id': negocio['id'],
                    'nombre': negocio['nombre'],
                    'correo': negocio['correo'],
                    'rol': 'comercio'
                }
                self.al_ingresar_exitoso(usuario)
                conn.close()
                return
            
            messagebox.showerror("Error de Credenciales", "Correo o contraseña incorrectos.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            conn.close()

    def procesar_registro(self):
        nombre_completo = self.ent_nombre_reg.get().strip()
        email = self.ent_email_reg.get().strip()
        password = self.ent_pass_reg.get().strip()
=======
        if email in self.datos["usuarios"]:
            usuario = self.datos["usuarios"][email]
            if es_comercio and usuario["rol"] != "comercio":
                self._mostrar_dialogo_alerta("Rol Incorrecto", "Esta cuenta no es un comercio.")
                return
            elif not es_comercio and usuario["rol"] != "usuario":
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
>>>>>>> Stashed changes
        password2 = self.ent_pass2_reg.get().strip()
        genero = self.cb_genero_reg.get()
        universidad = self.ent_universidad_reg.get().strip()

<<<<<<< Updated upstream
        if not nombre_completo or not email or not password or not password2 or not universidad:
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los campos.")
            return

        if password != password2:
            messagebox.showerror("Error", "Las contraseñas no coinciden. Verifica e intenta de nuevo.")
            return

        partes = nombre_completo.split(' ', 1)
        nombre = partes[0]
        apellido = partes[1] if len(partes) > 1 else ''

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Ya existe una cuenta con este correo.")
                conn.close()
                return
            
            cursor.execute(
                "INSERT INTO usuarios (nombre, apellido, correo, password_hash, universidad, reputacion, estado) VALUES (%s, %s, %s, %s, %s, 5.0, 'activo') RETURNING id",
                (nombre, apellido, email, hash_password(password), universidad)
            )
            conn.commit()
            nuevo_id = cursor.fetchone()[0]
            
            messagebox.showinfo("Éxito", "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
            self.cambiar_modo(False)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
            conn.rollback()
        finally:
            conn.close()

=======
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
>>>>>>> Stashed changes
