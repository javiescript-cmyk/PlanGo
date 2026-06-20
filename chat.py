
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import random
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_ACCENT_RED,
    COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_AMARILLO_ORO, COLOR_SUCCESS, COLOR_NAV,
    base_datos_global, guardar_datos, configurar_animacion_boton
)

class PerfilUsuario(tk.Toplevel):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.title(f"Perfil de {usuario['nombre']}")
        self.geometry("380x500")
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)
        self.grab_set()
        
        # Centrar ventana
        self.update_idletasks()
        x = (parent.winfo_width() // 2) + parent.winfo_x()
        y = (parent.winfo_height() // 2) + parent.winfo_y()
        self.geometry(f"+{x - 190}+{y - 250}")
        
        self.crear_ui()
    
    def crear_ui(self):
        # Header
        header = tk.Frame(self, bg=COLOR_ACCENT_RED, height=120)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Avatar grande
        canvas_av = tk.Canvas(self, width=100, height=100, bg=COLOR_BG, bd=0, highlightthickness=0)
        canvas_av.place(x=140, y=70)
        canvas_av.create_oval(5, 5, 95, 95, fill=COLOR_ACCENT_RED, outline="")
        ini = self.usuario["nombre"][0].upper()
        canvas_av.create_text(50, 50, text=ini, font=("Helvetica", 40, "bold"), fill=COLOR_TEXT_MAIN)
        
        # Info principal
        frame_info = tk.Frame(self, bg=COLOR_BG)
        frame_info.pack(fill="both", expand=True, padx=20, pady=(60, 20))
        
        tk.Label(frame_info, text=self.usuario["nombre"], font=("Helvetica", 20, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(pady=(0, 5))
        tk.Label(frame_info, text=f"Rol: {self.usuario.get('rol', 'Usuario')}", font=("Helvetica", 11), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(pady=(0, 15))
        
        # Tarjeta de estadísticas
        stats_frame = tk.Frame(frame_info, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#3D3D3D", padx=15, pady=15)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(stats_frame, text="📊 Estadísticas", font=("Helvetica", 12, "bold"), bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO).pack(anchor="w", pady=(0, 10))
        
        stats = [
            ("⭐ Confianza", self.usuario.get("confianza", "5.0")),
            ("🤝 Matches", str(self.usuario.get("matches", "0"))),
            ("📅 Miembro desde", "Hoy"),
        ]
        
        for label, valor in stats:
            row = tk.Frame(stats_frame, bg=COLOR_CARD)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(side="left")
            tk.Label(row, text=valor, font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(side="right")
        
        # Género
        if "genero" in self.usuario:
            tk.Label(frame_info, text=f"Género: {self.usuario['genero']}", font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(0, 10))
        
        # Estado
        estado_frame = tk.Frame(frame_info, bg=COLOR_BG)
        estado_frame.pack(fill="x", pady=(10, 0))
        tk.Label(estado_frame, text="🟢", font=("Helvetica", 12), bg=COLOR_BG, fg=COLOR_SUCCESS).pack(side="left")
        tk.Label(estado_frame, text="Disponible", font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(side="left", padx=5)
        
        # Botón cerrar
        btn_cerrar = tk.Button(self, text="Cerrar", font=("Helvetica", 11, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=20, pady=8, command=self.destroy)
        btn_cerrar.pack(pady=(0, 20))
        configurar_animacion_boton(btn_cerrar, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

class SalaChatTemporal(tk.Frame):
    def __init__(self, parent, usuario_actual, match_encontrado, promo, on_close=None):
        super().__init__(parent, bg="#0F1419")
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.match_encontrado = match_encontrado
        self.promo = promo
        self.on_close = on_close
        self.timer_activo = True
        self.primero_mensaje = True
        self.escribiendo = False
        
        self.hora_expiracion = datetime.now() + timedelta(minutes=30) # 30 minutos para chat
        
        self.inicializar_ui()
        self.actualizar_timer()
    
    def inicializar_ui(self):
        # ── HEADER CON FOTO DE PERFIL (CLICKEABLE) ──────────────────────
        header = tk.Frame(self, bg="#1E2732", height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        # Botón volver
        btn_volver = tk.Label(header, text="←", font=("Helvetica", 20), bg="#1E2732", fg=COLOR_TEXT_MAIN, cursor="hand2")
        btn_volver.pack(side="left", padx=12, pady=20)
        btn_volver.bind("<Button-1>", lambda e: self.destruir_chat())
        
        # Avatar del match (clickeable para ver perfil
        self.canvas_av = tk.Canvas(header, width=45, height=45, bg="#1E2732", bd=0, highlightthickness=0, cursor="hand2")
        self.canvas_av.pack(side="left", pady=12)
        self.canvas_av.create_oval(2, 2, 43, 43, fill=COLOR_ACCENT_RED, outline="")
        ini = self.match_encontrado["nombre"][0].upper()
        self.canvas_av.create_text(22, 22, text=ini, font=("Helvetica", 18, "bold"), fill=COLOR_TEXT_MAIN)
        self.canvas_av.bind("<Button-1>", lambda e: self.ver_perfil())
        
        # Info del match
        info_h = tk.Frame(header, bg="#1E2732")
        info_h.pack(side="left", padx=10)
        tk.Label(info_h, text=self.match_encontrado["nombre"], font=("Helvetica", 12, "bold"), bg="#1E2732", fg=COLOR_TEXT_MAIN).pack(anchor="w")
        self.lbl_estado = tk.Label(info_h, text="🟢 En línea", font=("Helvetica", 9), bg="#1E2732", fg=COLOR_SUCCESS)
        self.lbl_estado.pack(anchor="w")
        
        # Timer
        self.lbl_timer = tk.Label(header, text="", font=("Helvetica", 9, "bold"), bg="#1E2732", fg=COLOR_AMARILLO_ORO)
        self.lbl_timer.pack(side="right", padx=12)
        
        # ── CARD PROMO EN EL CHAT (MÁS ELEGANTE) ───────────────────────
        card_promo = tk.Frame(self, bg="#1A232D", highlightthickness=1, highlightbackground=COLOR_ACCENT_RED)
        card_promo.pack(fill="x", padx=10, pady=8)
        
        fila_p = tk.Frame(card_promo, bg="#1A232D")
        fila_p.pack(fill="x", padx=12, pady=10)
        
        tk.Label(fila_p, text=" 2x1 ", font=("Helvetica", 9, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 10))
        tk.Label(fila_p, text=self.promo["titulo"], font=("Helvetica", 11, "bold"), bg="#1A232D", fg=COLOR_TEXT_MAIN).pack(side="left")
        
        zona = self.promo.get("zona", "Zona centro")
        tk.Label(card_promo, text=f"📍 {zona}   🕐 Hasta {self.promo.get('hora_hasta', '23:00')}", font=("Helvetica", 9), bg="#1A232D", fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=12, pady=(0, 8))
        
        # ── ÁREA DE MENSAJES (MEJORADA) ─────────────────────────────
        frame_msgs = tk.Frame(self, bg="#0F1419")
        frame_msgs.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        
        self.canvas_cards = tk.Canvas(frame_msgs, bg="#0F1419", bd=0, highlightthickness=0)
        sb_chat = ttk.Scrollbar(frame_msgs, orient="vertical", command=self.canvas_cards.yview)
        self.frame_burbujas = tk.Frame(self.canvas_cards, bg="#0F1419")
        self.frame_burbujas.bind("<Configure>", lambda e: self.canvas_cards.configure(scrollregion=self.canvas_cards.bbox("all")))
        self.canvas_cards.create_window((0, 0), window=self.frame_burbujas, anchor="nw")
        self.canvas_cards.configure(yscrollcommand=sb_chat.set)
        self.canvas_cards.pack(side="left", fill="both", expand=True)
        sb_chat.pack(side="right", fill="y")
        
        # Mensaje inicial del match
        self.after(1000, lambda: self.agregar_mensaje(f"¡Hola {self.usuario_actual['nombre']}! 😊 Vi que también quieres ir a {self.promo['titulo']}", "otro"))
        
        # Indicador de escribiendo (se creará dinámicamente)
        
        # ── ENTRADA DE MENSAJE (MÁS PROFESIONAL) ───────────────────────
        frame_entrada = tk.Frame(self, bg="#1E2732", height=65)
        frame_entrada.pack(fill="x", side="bottom")
        frame_entrada.pack_propagate(False)
        
        campo = tk.Frame(frame_entrada, bg="#1E2732")
        campo.pack(fill="x", padx=12, pady=12)
        
        # Botón adjuntar (solo visual)
        tk.Label(campo, text="📎", font=("Helvetica", 16), bg="#1E2732", fg=COLOR_TEXT_MUTED, cursor="hand2").pack(side="left", padx=(0, 8))
        
        self.ent_msg = tk.Entry(campo, font=("Helvetica", 11), bg="#273441", fg=COLOR_TEXT_MAIN, bd=0, insertbackground="white", highlightthickness=0)
        self.ent_msg.insert(0, "Escribe un mensaje...")
        self.ent_msg.bind("<FocusIn>", lambda e: self._limpiar_placeholder())
        self.ent_msg.bind("<FocusOut>", lambda e: self._poner_placeholder())
        self.ent_msg.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))
        self.ent_msg.bind("<Return>", lambda e: self.enviar_mensaje())
        
        btn_send = tk.Button(campo, text="➤", font=("Helvetica", 14, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", width=3, command=self.enviar_mensaje)
        btn_send.pack(side="right", ipady=9)
        configurar_animacion_boton(btn_send, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)
    
    def _limpiar_placeholder(self):
        if self.ent_msg.get() == "Escribe un mensaje...":
            self.ent_msg.delete(0, "end")
    
    def _poner_placeholder(self):
        if not self.ent_msg.get().strip():
            self.ent_msg.insert(0, "Escribe un mensaje...")
    
    def ver_perfil(self):
        PerfilUsuario(self, self.match_encontrado)
    
    def actualizar_timer(self):
        if self.timer_activo:
            tiempo_restante = self.hora_expiracion - datetime.now()
            if tiempo_restante.total_seconds() <= 0:
                self.destruir_chat()
                return
            minutos = int(tiempo_restante.total_seconds() // 60)
            segundos = int(tiempo_restante.total_seconds() % 60)
            self.lbl_timer.config(text=f"⏱ {minutos:02d}:{segundos:02d}")
            self.after(1000, self.actualizar_timer)
    
    def enviar_mensaje(self):
        texto = self.ent_msg.get().strip()
        if not texto or texto == "Escribe un mensaje...":
            return
        self.agregar_mensaje(texto, "yo")
        self.ent_msg.delete(0, tk.END)
        # Solo responder automáticamente las primeras veces
        if not hasattr(self, '_respuestas_dadas'):
            self._respuestas_dadas = 0
        if self._respuestas_dadas < 3:
            self._respuestas_dadas += 1
            self.after(800, self.enviar_mensaje_mock)

    def enviar_mensaje_mock(self):
        # 1. Mostrar "está escribiendo..."
        self._mostrar_escribiendo()

        # 2. Después de 1.8 segundos, enviar el mensaje real
        respuestas = [
            f"¡Hola! Nos vemos en {self.promo.get('zona','el local')} en 15 minutos 👍",
            "Perfecto, ya estoy llegando.",
            "¡Excelente! Espero verte pronto 😊",
            "Dale, nos vemos ahí.",
        ]
        msg = random.choice(respuestas)
        self.after(1800, lambda: self._terminar_escribiendo(msg))

    def _mostrar_escribiendo(self):
        # Crear un label de "está escribiendo..."
        # en frame_burbujas
        self.lbl_escribiendo = tk.Frame(
            self.frame_burbujas,
            bg="#0F1419")
        self.lbl_escribiendo.pack(
            fill="x", pady=2, padx=10)

        self.lbl_escribiendo_txt = tk.Label(
            self.lbl_escribiendo,
            text="está escribiendo",
            font=("Helvetica", 9, "italic"),
            bg="#0F1419",
            fg=COLOR_TEXT_MUTED)
        self.lbl_escribiendo_txt.pack(
            side="left")

        # Animación de los 3 puntos
        self._puntos = 0
        self._animar_puntos()

    def _animar_puntos(self):
        # Verificar que el widget siga existiendo
        try:
            self.lbl_escribiendo_txt.winfo_exists()
        except Exception:
            return
        if not hasattr(self, 'lbl_escribiendo'):
            return
        try:
            self._puntos = (self._puntos % 3) + 1
            puntos = "." * self._puntos
            self.lbl_escribiendo_txt.config(
                text=f"está escribiendo{puntos}")
            self._anim_id = self.after(
                400, self._animar_puntos)
        except Exception:
            pass

    def _terminar_escribiendo(self, mensaje):
        # Cancelar animación
        if hasattr(self, '_anim_id'):
            try:
                self.after_cancel(self._anim_id)
            except Exception:
                pass
        # Eliminar el label de escritura
        if hasattr(self, 'lbl_escribiendo'):
            try:
                self.lbl_escribiendo.destroy()
            except Exception:
                pass
        # Mostrar el mensaje real
        self.agregar_mensaje(mensaje, "otro")
    
    def agregar_mensaje(self, texto, remitente):
        es_yo = remitente == "yo"
        
        # Fila del mensaje
        fila = tk.Frame(self.frame_burbujas, bg="#0F1419")
        fila.pack(fill="x", pady=4, padx=10)
        
        # Hora
        hora = datetime.now().strftime("%H:%M")
        
        # Burbuja con mejor diseño
        burbuja_frame = tk.Frame(fila, bg="#0F1419")
        burbuja_frame.pack(side="right" if es_yo else "left")
        
        # Avatar para mensajes del otro
        if not es_yo:
            av_peq = tk.Canvas(burbuja_frame, width=28, height=28, bg="#0F1419", bd=0, highlightthickness=0)
            av_peq.pack(side="left", padx=(0, 8))
            av_peq.create_oval(2, 2, 26, 26, fill=COLOR_ACCENT_RED, outline="")
            av_peq.create_text(14, 14, text=self.match_encontrado["nombre"][0].upper(), font=("Helvetica", 11, "bold"), fill=COLOR_TEXT_MAIN)
        
        # Burbuja
        burbuja = tk.Label(
            burbuja_frame,
            text=texto,
            font=("Helvetica", 11),
            bg=COLOR_ACCENT_RED if es_yo else "#1E88E5",
            fg=COLOR_TEXT_MAIN,
            wraplength=280,
            justify="left",
            padx=14,
            pady=10
        )
        burbuja.pack(side="left")
        
        # Hora y check de visto para mis mensajes
        meta_frame = tk.Frame(burbuja_frame, bg="#0F1419")
        meta_frame.pack(side="right", padx=(8, 0), anchor="s")
        
        if es_yo:
            tk.Label(meta_frame, text="✓✓", font=("Helvetica", 8), bg="#0F1419", fg=COLOR_SUCCESS).pack(side="right")
        
        tk.Label(meta_frame, text=hora, font=("Helvetica", 8), bg="#0F1419", fg=COLOR_TEXT_MUTED).pack(side="right")
        
        self.scroll_al_final()
    
    def scroll_al_final(self):
        self.canvas_cards.update_idletasks()
        self.canvas_cards.yview_moveto(1.0)
    
    def destruir_chat(self):
        self.timer_activo = False
        self._mostrar_pantalla_resena()
    
    def _mostrar_pantalla_resena(self):
        ventana = tk.Toplevel(self)
        ventana.title("¿Cómo fue la experiencia?")
        ventana.geometry("380x480")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.transient(self)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (self.winfo_width() // 2) + self.winfo_x()
        y = (self.winfo_height() // 2) + self.winfo_y()
        ventana.geometry(f"+{x - 190}+{y - 240}")
        
        tk.Label(ventana, text="⭐", font=("Arial Black", 45), bg=COLOR_CARD).pack(pady=(15, 5))
        tk.Label(ventana, text="Califica tu experiencia", font=("Helvetica", 18, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(pady=(0, 5))
        tk.Label(ventana, text=f"¿Cómo fue con {self.match_encontrado['nombre']}?", font=("Helvetica", 12), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, justify="center").pack(pady=(0, 20))
        
        # Selector de estrellas interactivo
        frame_estrellas = tk.Frame(ventana, bg=COLOR_CARD)
        frame_estrellas.pack(pady=(0, 20))
        
        self.estrellas = []
        self.puntuacion = tk.IntVar(value=5)
        
        def actualizar_estrellas(n):
            for i, btn in enumerate(self.estrellas):
                if i < n:
                    btn.config(fg=COLOR_AMARILLO_ORO, font=("Helvetica", 24, "bold"))
                else:
                    btn.config(fg="#555555", font=("Helvetica", 24))
        
        for i in range(5):
            btn_estrella = tk.Label(frame_estrellas, text="★", font=("Helvetica", 24, "bold"), bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO, cursor="hand2")
            btn_estrella.pack(side="left", padx=8)
            btn_estrella.bind("<Button-1>", lambda e, n=i+1: [self.puntuacion.set(n), actualizar_estrellas(n)])
            self.estrellas.append(btn_estrella)
        
        # Campo de comentario
        tk.Label(ventana, text="Comentario (opcional):", font=("Helvetica", 11, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(fill="x", padx=30, pady=(0, 8))
        
        ent_comentario = tk.Text(ventana, font=("Helvetica", 11), bg="#2D2D2D", fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#3D3D3D", height=4, wrap="word")
        ent_comentario.pack(fill="x", padx=30, pady=(0, 25))
        
        # Botones
        btn_enviar = tk.Button(ventana, text="Enviar reseña", font=("Helvetica", 13, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=20, pady=10, command=lambda: self._guardar_resena(ventana, ent_comentario.get("1.0", tk.END).strip()))
        btn_enviar.pack(fill="x", padx=30, pady=(0, 10))
        configurar_animacion_boton(btn_enviar, COLOR_SUCCESS, "#1E8449", "#27AE60")
        
        btn_omitir = tk.Button(ventana, text="Omitir", font=("Helvetica", 11), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, bd=0, cursor="hand2", command=lambda: [ventana.destroy(), self.on_close() if self.on_close else None])
        btn_omitir.pack(pady=5)
    
    def _guardar_resena(self, ventana, comentario):
        nuevo_match = {
            "id": f"m{len(base_datos_global['historial_matches'])+1:03d}",
            "usuario_match": self.match_encontrado["nombre"],
            "genero_match": self.match_encontrado.get("genero", "No especificado"),
            "promo": self.promo["titulo"],
            "zona": self.promo.get("zona", "—"),
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "hora": datetime.now().strftime("%H:%M"),
            "reseña_dada": comentario or "Sin comentario",
            "puntuacion_dada": self.puntuacion.get()
        }
        base_datos_global["historial_matches"].append(nuevo_match)
        guardar_datos()
        ventana.destroy()
        if self.on_close:
            self.on_close()
