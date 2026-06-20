
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import random
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_ACCENT_RED,
    COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_RAYO_YELLOW, COLOR_AMARILLO_ORO,
    COLOR_SUCCESS, base_datos_global, guardar_datos, configurar_animacion_boton,
    COLOR_NAV
)

class SalaChatTemporal(tk.Frame):
    def __init__(self, parent, match_encontrado, promo, hora_fin, on_close=None):
        super().__init__(parent, bg="#121B22")
        self.parent = parent
        self.match_encontrado = match_encontrado
        self.promo = promo
        self.hora_fin = hora_fin
        self.on_close = on_close
        self.timer_activo = True
        self.primero_mensaje = True
        
        self.hora_expiracion = datetime.now() + timedelta(minutes=10)
        
        self.inicializar_ui()
        self.actualizar_timer()

    def inicializar_ui(self):
        # ── HEADER CON FOTO DE PERFIL ──────────────
        header = tk.Frame(self, bg=COLOR_NAV, height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Botón volver
        tk.Label(header, text="←", font=("Helvetica", 16), bg=COLOR_NAV, fg=COLOR_TEXT_MAIN, cursor="hand2").pack(side="left", padx=10, pady=14)

        # Avatar del match
        canvas_av = tk.Canvas(header, width=38, height=38, bg=COLOR_NAV, bd=0, highlightthickness=0)
        canvas_av.pack(side="left", pady=10)
        canvas_av.create_oval(2, 2, 36, 36, fill=COLOR_ACCENT_RED, outline="")
        ini = self.match_encontrado["usuario"][0].upper()
        canvas_av.create_text(19, 19, text=ini, font=("Helvetica", 14, "bold"), fill=COLOR_TEXT_MAIN)

        # Info del match
        info_h = tk.Frame(header, bg=COLOR_NAV)
        info_h.pack(side="left", padx=8)
        tk.Label(info_h, text=self.match_encontrado["usuario"], font=("Helvetica", 11, "bold"), bg=COLOR_NAV, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        tk.Label(info_h, text="🟢 En línea", font=("Helvetica", 8), bg=COLOR_NAV, fg=COLOR_SUCCESS).pack(anchor="w")

        # Timer
        self.lbl_timer = tk.Label(header, text="", font=("Helvetica", 8, "bold"), bg=COLOR_NAV, fg=COLOR_RAYO_YELLOW)
        self.lbl_timer.pack(side="right", padx=10)

        # ── CARD PROMO EN EL CHAT ─────────────────
        card_promo = tk.Frame(self, bg="#1A0A0A", highlightthickness=1, highlightbackground=COLOR_ACCENT_RED)
        card_promo.pack(fill="x", padx=8, pady=6)

        fila_p = tk.Frame(card_promo, bg="#1A0A0A")
        fila_p.pack(fill="x", padx=10, pady=8)
        tk.Label(fila_p, text=" 2x1 ", font=("Helvetica", 8, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 8))
        tk.Label(fila_p, text=self.promo["titulo"], font=("Helvetica", 9, "bold"), bg="#1A0A0A", fg=COLOR_TEXT_MAIN).pack(side="left")

        zona = self.promo.get("zona", "")
        tk.Label(card_promo, text=f"📍 {zona} 🕐 Hasta 21:00", font=("Helvetica", 7), bg="#1A0A0A", fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=10, pady=(0, 6))

        # ── ÁREA DE MENSAJES ──────────────────────
        frame_msgs = tk.Frame(self, bg="#121B22")
        frame_msgs.pack(fill="both", expand=True, padx=8, pady=(0, 6))

        self.canvas_chat = tk.Canvas(frame_msgs, bg="#121B22", bd=0, highlightthickness=0)
        sb_chat = ttk.Scrollbar(frame_msgs, orient="vertical", command=self.canvas_chat.yview)
        self.frame_burbujas = tk.Frame(self.canvas_chat, bg="#121B22")
        self.frame_burbujas.bind(
            "<Configure>",
            lambda e: self.canvas_chat.configure(
                scrollregion=self.canvas_chat.bbox("all")))
        self.canvas_chat.create_window(
            (0, 0), window=self.frame_burbujas, anchor="nw")
        self.canvas_chat.configure(yscrollcommand=sb_chat.set)
        self.canvas_chat.pack(side="left", fill="both", expand=True)
        sb_chat.pack(side="right", fill="y")

        # Mensaje inicial del match
        self.after(800, lambda: self.agregar_mensaje(
            f"¡Hola! Vi que quieres ir a {self.promo['titulo']} 🎉", "otro"))

        # ── ENTRADA DE MENSAJE ────────────────────
        frame_entrada = tk.Frame(self, bg=COLOR_NAV, height=56)
        frame_entrada.pack(fill="x", side="bottom")
        frame_entrada.pack_propagate(False)

        campo = tk.Frame(frame_entrada, bg=COLOR_NAV)
        campo.pack(fill="x", padx=10, pady=10)

        self.ent_msg = tk.Entry(campo, font=("Helvetica", 10), bg="#2D2D2D", fg=COLOR_TEXT_MAIN, bd=0, insertbackground="white", highlightthickness=1, highlightbackground="#3D3D3D")
        self.ent_msg.insert(0, "Escribe un mensaje...")
        self.ent_msg.bind("<FocusIn>", lambda e: self.ent_msg.delete(0, "end") if "Escribe" in self.ent_msg.get() else None)
        self.ent_msg.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 8))
        self.ent_msg.bind("<Return>", lambda e: self.enviar_mensaje())

        btn_send = tk.Button(campo, text="➤", font=("Helvetica", 13, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", width=3, command=self.enviar_mensaje)
        btn_send.pack(side="right", ipady=7)
        configurar_animacion_boton(btn_send, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def _regresar(self):
        self.destruir_chat()

    def actualizar_timer(self):
        if self.timer_activo:
            tiempo_restante = self.hora_expiracion - datetime.now()
            if tiempo_restante.total_seconds() <= 0:
                self.destruir_chat()
                return
            self.after(1000, self.actualizar_timer)

    def enviar_mensaje(self):
        texto = self.ent_msg.get().strip()
        if texto:
            self.agregar_mensaje(texto, "yo")
            self.ent_msg.delete(0, tk.END)
            
            if self.primero_mensaje:
                self.primero_mensaje = False
                self.after(2000, self.enviar_mensaje_mock)

    def enviar_mensaje_mock(self):
        respuestas = [
            f"¡Perfecto! Nos vemos en la sucursal de {self.promo['zona']}",
            "¿Ya estás por ahí?",
            "¡Excelente! Espero verte pronto",
            "Perfecto, nos vemos en 10 minutos!"
        ]
        self.agregar_mensaje(random.choice(respuestas), "otro")

    def agregar_mensaje(self, texto, remitente):
        es_yo = remitente == "yo"

        # Fila del mensaje
        fila = tk.Frame(self.frame_burbujas, bg="#121B22")
        fila.pack(fill="x", pady=3, padx=10)

        # Hora
        hora = datetime.now().strftime("%H:%M")

        # Burbuja
        burbuja = tk.Label(fila, text=texto, font=("Helvetica", 10), bg=COLOR_ACCENT_RED if es_yo else "#2D2D2D", fg=COLOR_TEXT_MAIN, wraplength=260, justify="left", padx=12, pady=8)
        if es_yo:
            burbuja.pack(side="right")
        else:
            burbuja.pack(side="left")

        tk.Label(fila, text=hora, font=("Helvetica", 6), bg="#121B22", fg=COLOR_TEXT_MUTED).pack(side="right" if es_yo else "left", padx=4, anchor="s")

        # Scroll automático
        self.canvas_chat.update_idletasks()
        self.canvas_chat.yview_moveto(1.0)

    def destruir_chat(self):
        self.timer_activo = False
        self._mostrar_pantalla_resena()

    def _mostrar_pantalla_resena(self):
        ventana = tk.Toplevel(self)
        ventana.title("¿Cómo fue la experiencia?")
        ventana.geometry("420x450")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.transient(self)
        ventana.grab_set()

        # Centrar ventana
        ventana.update_idletasks()
        x = (self.winfo_width() // 2) + self.winfo_x()
        y = (self.winfo_height() // 2) + self.winfo_y()
        ventana.geometry(f"+{x - 210}+{y - 225}")

        tk.Label(ventana, text="⭐", font=("Arial Black", 40), bg=COLOR_CARD).pack(pady=(15, 5))
        tk.Label(ventana, text="Califica tu experiencia", font=("Helvetica", 16, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(pady=(0, 5))
        tk.Label(ventana, text=f"¿Cómo fue con {self.match_encontrado['usuario']}?", font=("Helvetica", 11), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, justify="center").pack(pady=(0, 15))

        # Selector de estrellas
        frame_estrellas = tk.Frame(ventana, bg=COLOR_CARD)
        frame_estrellas.pack(pady=(0, 15))

        self.puntuacion = tk.IntVar(value=5)

        for i in range(5, 0, -1):
            btn_estrella = tk.Radiobutton(
                frame_estrellas,
                text=f"{i} ⭐",
                variable=self.puntuacion,
                value=i,
                font=("Helvetica", 14),
                bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO,
                activebackground=COLOR_CARD, activeforeground=COLOR_AMARILLO_ORO,
                selectcolor=COLOR_CARD, bd=0, cursor="hand2"
            )
            btn_estrella.pack(side="right", padx=5)

        # Campo de comentario
        tk.Label(ventana, text="Comentario (opcional):", font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(fill="x", padx=30, pady=(0, 5))

        ent_comentario = tk.Text(ventana, font=("Helvetica", 11), bg="#2D2D2D", fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#3D3D3D", height=4, wrap="word")
        ent_comentario.pack(fill="x", padx=30, pady=(0, 20))

        # Botones
        btn_enviar = tk.Button(
            ventana, text="Enviar reseña", font=("Helvetica", 12, "bold"),
            bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2",
            command=lambda: self._guardar_resena(ventana, ent_comentario.get("1.0", tk.END))
        )
        btn_enviar.pack(fill="x", padx=30, pady=(0, 10))
        configurar_animacion_boton(btn_enviar, COLOR_SUCCESS, "#1E8449", "#27AE60")

        btn_omitir = tk.Button(
            ventana, text="Omitir", font=("Helvetica", 10),
            bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, bd=0, cursor="hand2",
            command=lambda: [ventana.destroy(), self.on_close if self.on_close else None]
        )
        btn_omitir.pack(pady=5)

    def _guardar_resena(self, ventana, comentario):
        comentario = comentario.strip()
        nuevo_match = {
            "id": f"m{len(base_datos_global['historial_matches']) + 1:03d}",
            "usuario_match": self.match_encontrado["usuario"],
            "genero_match": self.match_encontrado["genero"],
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
