# matchmaker.py
import tkinter as tk
from tkinter import messagebox, ttk
import time

# --- PALETA DE COLORES (Identidad Two Pack - Dark Mode) ---
COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_MUTED = "#A0A0A0"
COLOR_SUCCESS = "#2ECC71"
COLOR_ACCENT_RED = "#FF1E39"
COLOR_RED_HOVER = "#FF4D63"
COLOR_RED_ACTIVE = "#990A15"
COLOR_RAYO_YELLOW = "#FFCC00"

class MotorMatchmaker(tk.Frame):
    def __init__(self, parent, usuario_actual=None):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        
        # Datos del estudiante usando el sistema (MVP)
        self.usuario_actual = usuario_actual or {
            "nombre": "Carlos Mendoza",
            "genero": "Masculino",
            "universidad": "UCATEC"
        }
        
        # Base de datos simulada de solicitudes en espera (Pool de la Ciudad)
        # Aquí demostramos la lógica de emparejamiento inteligente
        self.pool_solicitudes = [
            # Caso 1: Match Perfecto para Alitas (Mismo ID, hora cruzada, mismo género)
            {"usuario": "Alejandro Gómez", "genero": "Masculino", "oferta_id": "001", "hora_inicio": 12, "hora_fin": 14, "filtro_genero": False},
            # Caso 2: Quiere otra cosa (Falla por ID de Oferta)
            {"usuario": "Sofía Claros", "genero": "Femenino", "oferta_id": "002", "hora_inicio": 12, "hora_fin": 14, "filtro_genero": False},
            # Caso 3: Falla por ventana de tiempo (Muy tarde)
            {"usuario": "Diego Torrico", "genero": "Masculino", "oferta_id": "001", "hora_inicio": 18, "hora_fin": 20, "filtro_genero": False},
            # Caso 4: Filtro de género estricto activo (Si Carlos fuera mujer, haría match, pero Sofía solo quiere mujeres)
            {"usuario": "Valeria Rocha", "genero": "Femenino", "oferta_id": "001", "hora_inicio": 12, "hora_fin": 14, "filtro_genero": True}
        ]
        
        self.inicializar_ui()

    def configurar_animacion_boton(self, boton, color_normal, color_hover, color_active):
        boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
        boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))
        boton.bind("<ButtonPress-1>", lambda e: boton.config(bg=color_active))
        boton.bind("<ButtonRelease-1>", lambda e: boton.config(bg=color_hover))

    def inicializar_ui(self):
        # --- CONTENEDOR TÁCTICO CENTRAL ---
        frame_central = tk.Frame(self, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
        frame_central.pack(pady=30, padx=40, fill="both", expand=True)
        
        # Cabecera de Inteligencia Urbana
        lbl_icon = tk.Label(frame_central, text="⚡", font=("Helvetica", 28), bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW)
        lbl_icon.pack(pady=(15, 0))
        
        lbl_titulo = tk.Label(frame_central, text="MOTOR MATCHMAKER IA", font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN)
        lbl_titulo.pack(pady=5)
        
        lbl_sub = tk.Label(frame_central, text="Cochabamba Ciudad Inteligente • Algoritmo de Coincidencia", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED)
        lbl_sub.pack(pady=(0, 20))
        
        # --- FORMULARIO DE REQUISITOS TEMPORALES Y SEGURIDAD ---
        frame_campos = tk.Frame(frame_central, bg=COLOR_CARD)
        frame_campos.pack(fill="x", padx=30)
        
        # Selección de Oferta Simulada para la Prueba
        tk.Label(frame_campos, text="SELECCIONAR PROMO ACTIVA", font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.cb_oferta = ttk.Combobox(frame_campos, values=["001 - 2x1 en Alitas Universitarias", "002 - Fernet 2x1 Jueves de Frater", "003 - 2x1 Milkshakes Premium"], state="readonly")
        self.cb_oferta.pack(fill="x", ipady=3, pady=(0, 12))
        self.cb_oferta.set("001 - 2x1 en Alitas Universitarias")
        
        # Ventana Temporal (Rango de horas)
        tk.Label(frame_campos, text="TU VENTANA TEMPORAL DE DISPONIBILIDAD", font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        frame_horas = tk.Frame(frame_campos, bg=COLOR_CARD)
        frame_horas.pack(fill="x", pady=(0, 12))
        
        tk.Label(frame_horas, text="Desde las:", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.cb_desde = ttk.Combobox(frame_horas, values=[str(i) for i in range(8, 24)], width=5, state="readonly")
        self.cb_desde.pack(side="left", padx=(0, 15))
        self.cb_desde.set("12")
        
        tk.Label(frame_horas, text="Hasta las:", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.cb_hasta = ttk.Combobox(frame_horas, values=[str(i) for i in range(8, 24)], width=5, state="readonly")
        self.cb_hasta.pack(side="left")
        self.cb_hasta.set("14")
        
        # Control de Filtro de Género (UX de Privacidad y Seguridad)
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
        
        # --- BOTÓN DE ACCIÓN PROMAX CON ANIMACIÓN ---
        self.btn_match = tk.Button(
            frame_central, 
            text="🤝 Quiero aprovechar este 2x1", 
            font=("Helvetica", 11, "bold"), 
            bg=COLOR_ACCENT_RED, 
            fg=COLOR_TEXT_MAIN, 
            bd=0, 
            cursor="hand2",
            command=self.ejecutar_matchmaking
        )
        self.btn_match.pack(fill="x", padx=30, ipady=12, pady=(0, 15))
        self.configurar_animacion_boton(self.btn_match, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)
        
        # Consola de estado del escáner de la IA
        self.lbl_status = tk.Label(frame_central, text="Sistema Matchmaker listo. Esperando solicitud...", font=("Helvetica", 9, "italic"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED)
        self.lbl_status.pack(pady=(0, 15))

    def ejecutar_matchmaking(self):
        # Cambiar UI a estado de procesamiento dinámico
        self.lbl_status.config(text="🤖 Escaneando base de datos urbana en tiempo real...", fg=COLOR_RAYO_YELLOW)
        self.btn_match.config(state="disabled", bg="#444444", text="Procesando algoritmo...")
        self.update()
        
        # Simulación de latencia de red/procesamiento de la IA para una UX satisfactoria
        time.sleep(1.5)
        
        # Extracción de parámetros ingresados
        id_oferta_elegida = self.cb_oferta.get().split(" ")[0]
        desde = int(self.cb_desde.get())
        hasta = int(self.cb_hasta.get())
        filtro_estricto = self.check_genero_var.get()
        
        if desde >= hasta:
            messagebox.showerror("Error de Tiempo", "La hora de inicio de tu disponibilidad debe ser menor a la hora de conclusión.")
            self.restaurar_boton_match()
            return

        # --- ARQUITECTURA DEL ALGORITMO MATCHMAKER (Criterios de Prioridad) ---
        match_encontrado = None
        
        for candidato in self.pool_solicitudes:
            # Criterio 1: Coincidencia estricta de ID de Oferta
            if candidato["oferta_id"] != id_oferta_elegida:
                continue
                
            # Criterio 2: Ventana Temporal Común (Cruce de rangos matemáticos)
            # Existe intersección si el inicio máximo es menor o igual al fin mínimo
            inicio_comun = max(desde, candidato["hora_inicio"])
            fin_comun = min(hasta, candidato["hora_fin"])
            if inicio_comun >= fin_comun:
                continue # No coinciden en el tiempo libre
                
            # Criterio 3: Restricción de Género Recíproca por Seguridad Urbana
            # Si el usuario actual pide restricción, los géneros deben ser iguales
            if filtro_estricto and candidato["genero"] != self.usuario_actual["genero"]:
                continue
            # Si el candidato tenía activado su propio filtro de género, verificamos si cumplimos su condición
            if candidato["filtro_genero"] and candidato["genero"] != self.usuario_actual["genero"]:
                continue
                
            # Si superó todos los filtros, es nuestro match perfecto de la ciudad
            match_encontrado = candidato
            break

        # --- RESPUESTA DE LA INTERFAZ ---
        self.restaurar_boton_match()
        
        if match_encontrado:
            self.lbl_status.config(text="¡MATCH LOGRADO EXITOSAMENTE! 🎉", fg=COLOR_SUCCESS)
            messagebox.showinfo(
                "⚡ ¡Match Two Pack Detectado!", 
                f"¡Felicidades, {self.usuario_actual['nombre']}!\n\n"
                f"Hemos encontrado un compañero compatible en Cochabamba:\n"
                f"👤 Nombre: {match_encontrado['usuario']}\n"
                f"🕒 Ventana de encuentro: Entre las {max(desde, match_encontrado['hora_inicio'])}:00 y las {min(hasta, match_encontrado['hora_fin'])}:00\n\n"
                f"Se ha habilitado un chat temporal seguro para coordinar el encuentro."
            )
        else:
            self.lbl_status.config(text="Sin coincidencias inmediatas. En cola de espera.", fg=COLOR_TEXT_MUTED)
            messagebox.showwarning(
                "Solicitud en Espera", 
                "No hay solicitudes idénticas en este momento.\n\nTu petición se ha quedado registrada de forma inteligente en la cola de la zona. Te notificaremos de inmediato por WhatsApp en cuanto otro estudiante aplique al mismo beneficio."
            )

    def restaurar_boton_match(self):
        self.btn_match.config(state="normal", bg=COLOR_ACCENT_RED, text="🤝 Quiero aprovechar este 2x1")
        self.configurar_animacion_boton(self.btn_match, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

# --- EJECUCIÓN DIRECTA PARA PRUEBAS ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Two Pack - Motor Algorítmico IA")
    root.geometry("550x480")
    root.configure(bg=COLOR_BG)
    
    app = MotorMatchmaker(root)
    app.pack(fill="both", expand=True)
    
    root.mainloop()