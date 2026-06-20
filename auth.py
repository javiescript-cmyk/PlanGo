
import tkinter as tk
from tkinter import ttk, messagebox
import re
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
    COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_RAYO_YELLOW, COLOR_ESCUDO_RED,
    cargar_datos, guardar_datos, configurar_animacion_boton, configurar_animacion_enlace
)

class VistaAutenticacion(tk.Frame):
    def __init__(self, parent, al_ingresar_exitoso):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.al_ingresar_exitoso = al_ingresar_exitoso
        self.modo_registro = False
        
        self.datos = cargar_datos()
        
        self.mostrar_splash()

    def mostrar_splash(self):
        # Pantalla de bienvenida que dura 2.5 segundos
        self.frame_splash = tk.Frame(self, bg=COLOR_BG)
        self.frame_splash.place(relx=0, rely=0, 
                                 relwidth=1, relheight=1)
 
        # Dibujar el logo grande centrado
        canvas_s = tk.Canvas(self.frame_splash, 
                              width=300, height=240, 
                              bg=COLOR_BG, bd=0, 
                              highlightthickness=0)
        canvas_s.pack(expand=True, pady=(60, 10))
 
        # Escudo
        pts = [40, 30, 260, 30, 210, 140, 
               140, 200, 70, 140]
        canvas_s.create_polygon(
            pts, fill=COLOR_ESCUDO_RED, 
            outline="#800A12", width=2)
 
        # Rayos
        canvas_s.create_polygon(
            [25, 20, 50, 20, 38, 43, 52, 43, 
             30, 73, 36, 48, 23, 48], 
            fill=COLOR_RAYO_YELLOW, 
            outline="black", width=1)
        canvas_s.create_polygon(
            [230, 115, 248, 115, 240, 130, 
             250, 130, 227, 155, 235, 138, 
             222, 138], 
            fill=COLOR_RAYO_YELLOW, 
            outline="black", width=1)
 
        # Texto del escudo
        canvas_s.create_text(
            152, 92, text="2x1", 
            font=("Arial Black", 46, "bold"), 
            fill="#000000")
        canvas_s.create_text(
            150, 90, text="2x1", 
            font=("Arial Black", 46, "bold"), 
            fill=COLOR_TEXT_MAIN)
        canvas_s.create_text(
            150, 135, text="PROMO", 
            font=("Arial Black", 16, "bold"), 
            fill=COLOR_TEXT_MAIN)
 
        # Cinta inferior
        canvas_s.create_polygon(
            [85, 148, 215, 148, 197, 178, 103, 178], 
            fill=COLOR_TEXT_MAIN, 
            outline="#CCCCCC", width=1)
        canvas_s.create_text(
            150, 163, text="Two Pack", 
            font=("Georgia", 16, "bold", "italic"), 
            fill=COLOR_ESCUDO_RED)
 
        tk.Label(self.frame_splash, 
                 text="Divide el gasto, duplica la experiencia.", 
                 font=("Helvetica", 11, "italic"), 
                 bg=COLOR_BG, fg=COLOR_RAYO_YELLOW).pack(pady=(0, 10))
 
        tk.Label(self.frame_splash, 
                 text="Cargando ecosistema urbano...", 
                 font=("Helvetica", 9), 
                 bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack()
 
        # Destruir splash y mostrar login después de 2.5s
        self.after(2500, self._terminar_splash)

    def _terminar_splash(self):
        self.frame_splash.destroy()
        self.mostrar_login_registro()

    def mostrar_login_registro(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.dibujar_escudo()

        lbl_slogan = tk.Label(self, text="Divide el gasto, duplica la experiencia.", 
                            font=("Helvetica Neue", 11, "italic"), bg=COLOR_BG, fg=COLOR_RAYO_YELLOW)
        lbl_slogan.pack(pady=(10, 20))

        frame_selector = tk.Frame(self, bg=COLOR_BG)
        frame_selector.pack(pady=(0, 20))

        self.btn_estudiante = tk.Button(frame_selector, text="👤 Iniciar Sesión como Estudiante",
                                        font=("Helvetica", 10, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN,
                                        bd=0, cursor="hand2", padx=15, pady=8)
        self.btn_estudiante.pack(side="left", padx=5)

        self.btn_comercio = tk.Button(frame_selector, text="🏪 Iniciar Sesión como Dueño de Negocio",
                                    font=("Helvetica", 10, "bold"), bg="#333333", fg=COLOR_TEXT_MAIN,
                                    bd=0, cursor="hand2", padx=15, pady=8)
        self.btn_comercio.pack(side="left", padx=5)

        configurar_animacion_boton(self.btn_estudiante, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)
        configurar_animacion_boton(self.btn_comercio, "#333333", "#444444", "#222222")
        self.btn_estudiante.config(command=lambda: self.seleccionar_rol("estudiante"))
        self.btn_comercio.config(command=lambda: self.seleccionar_rol("comercio"))

        if not self.modo_registro:
            frame_form = tk.Frame(self, bg=COLOR_BG)
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

            btn_ingresar = tk.Button(frame_form, text="Ingresar de Forma Segura",
                                    font=("Helvetica", 11, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN,
                                    bd=0, cursor="hand2", command=self.procesar_login)
            btn_ingresar.pack(fill="x", ipady=10)
            configurar_animacion_boton(btn_ingresar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")
            
            btn_registrar = tk.Button(frame_form, text="Crear Cuenta Nueva",
                                    font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_ACCENT_RED,
                                    bd=0, cursor="hand2", command=lambda: self.cambiar_modo(True))
            btn_registrar.pack(pady=15)
        else:
            frame_form = tk.Frame(self, bg=COLOR_BG)
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

            tk.Label(frame_form, text="CONFIRMAR CONTRASEÑA",
                    font=("Helvetica", 8, "bold"),
                    bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(3, 2))
            self.ent_pass2_reg = tk.Entry(frame_form, font=("Helvetica", 12),
                                        bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                                        bd=0, show="*",
                                        highlightthickness=1,
                                        highlightbackground="#2D2D2D")
            self.ent_pass2_reg.pack(fill="x", ipady=8, pady=(0, 20))

            btn_registrar = tk.Button(frame_form, text="Crear Cuenta de Estudiante",
                                    font=("Helvetica", 11, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN,
                                    bd=0, cursor="hand2", command=self.procesar_registro)
            btn_registrar.pack(fill="x", ipady=10)
            configurar_animacion_boton(btn_registrar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")
            
            btn_volver = tk.Button(frame_form, text="Volver a Iniciar Sesión",
                                font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_ACCENT_RED,
                                bd=0, cursor="hand2", command=lambda: self.cambiar_modo(False))
            btn_volver.pack(pady=15)

    def cambiar_modo(self, modo_registro):
        self.modo_registro = modo_registro
        self.mostrar_login_registro()

    def dibujar_escudo(self):
        canvas_logo = tk.Canvas(self, width=280, height=220, bg=COLOR_BG, bd=0, highlightthickness=0)
        canvas_logo.pack(pady=(0, 5))

        puntos_escudo = [40, 50, 240, 50, 210, 150, 140, 200, 70, 150]
        canvas_logo.create_polygon(puntos_escudo, fill=COLOR_ESCUDO_RED, outline="#800A12", width=2)

        canvas_logo.create_polygon(25, 20, 55, 20, 40, 45, 55, 45, 30, 75, 38, 50, 25, 50, 
                                fill=COLOR_RAYO_YELLOW, outline="black", width=1)
        canvas_logo.create_polygon(225, 120, 245, 120, 235, 135, 245, 135, 225, 160, 230, 140, 220, 140, 
                                fill=COLOR_RAYO_YELLOW, outline="black", width=1)

        canvas_logo.create_oval(75, 175, 105, 205, fill="#E0E0E0", outline="#A0A0A0", width=2)
        canvas_logo.create_line(90, 190, 90, 182, fill="black", width=2)
        canvas_logo.create_line(90, 190, 100, 195, fill="black", width=1.5)
        canvas_logo.create_oval(230, 100, 260, 130, fill="#E0E0E0", outline="#A0A0A0", width=2)
        canvas_logo.create_line(245, 115, 245, 107, fill="black", width=2)
        canvas_logo.create_line(245, 115, 252, 122, fill="black", width=1.5)

        canvas_logo.create_polygon(50, 160, 60, 150, 65, 165, fill="#5D3FD3")
        canvas_logo.create_oval(190, 25, 202, 35, fill="#E0E0E0", outline="")

        canvas_logo.create_text(142, 92, text="2x1", font=("Arial Black", 44, "bold"), fill="#000000")
        canvas_logo.create_text(140, 90, text="2x1", font=("Arial Black", 44, "bold"), fill=COLOR_TEXT_MAIN)
        canvas_logo.create_text(140, 135, text="PROMO", font=("Arial Black", 16, "bold"), fill=COLOR_TEXT_MAIN)

        canvas_logo.create_polygon(80, 150, 200, 150, 180, 180, 100, 180, fill="#800A12")
        canvas_logo.create_polygon(85, 152, 195, 152, 185, 178, 95, 178, fill=COLOR_TEXT_MAIN, outline="#CCCCCC", width=1)
        canvas_logo.create_text(140, 165, text="Two Pack", font=("Georgia", 15, "bold", "italic"), fill=COLOR_ESCUDO_RED)

    def seleccionar_rol(self, rol):
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

        if email in self.datos["usuarios"]:
            usuario = self.datos["usuarios"][email]
            if usuario["password"] == password:
                self.al_ingresar_exitoso(usuario)
                return

        messagebox.showerror("Error de Credenciales", "Correo o contraseña incorrectos.")

    def procesar_registro(self):
        nombre = self.ent_nombre_reg.get().strip()
        email = self.ent_email_reg.get().strip()
        password = self.ent_pass_reg.get().strip()
        password2 = self.ent_pass2_reg.get().strip()
        genero = self.cb_genero_reg.get()

        if not nombre or not email or not password or not password2:
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los campos.")
            return

        if password != password2:
            messagebox.showerror("Error", "Las contraseñas no coinciden. Verifica e intenta de nuevo.")
            return

        dominios_validos = [".edu.bo", ".umss.edu.bo", ".ucb.edu.bo",
                        ".uatf.edu.bo", ".upsa.edu.bo", ".unifranz.edu.bo",
                        ".ucatec.edu.bo", ".univalle.edu.bo"]
        if not any(email.endswith(d) for d in dominios_validos):
            messagebox.showwarning("Correo inválido",
                                "Por favor usa tu correo universitario boliviano.\n"
                                "Ejemplo: tu_nombre@umss.edu.bo")
            return

        if email in self.datos["usuarios"]:
            messagebox.showerror("Error", "Ya existe una cuenta con este correo.")
            return

        self.datos["usuarios"][email] = {
            "nombre": nombre,
            "password": password,
            "rol": "estudiante",
            "genero": genero,
            "universidad": "",
            "confianza": 5.0,
            "matches": 0,
            "reportes": 0,
            "estado": "Activo"
        }
        guardar_datos()
        messagebox.showinfo("Éxito", "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
        self.cambiar_modo(False)
