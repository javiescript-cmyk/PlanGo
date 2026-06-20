
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import random
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_ACCENT_RED,
    COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_RAYO_YELLOW,
    COLOR_SUCCESS, base_datos_global, guardar_datos, configurar_animacion_boton
)

class SalaChatTemporal(tk.Frame):
    def __init__(self, parent, match_encontrado, promo, hora_fin, on_close=None):
        super().__init__(parent, bg=COLOR_BG)
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

        # Frame scrollable para burbujas
        frame_mensajes_outer = tk.Frame(self, bg=COLOR_BG)
        frame_mensajes_outer.pack(fill="both", expand=True, padx=15, pady=(10, 0))
 
        self.canvas_chat = tk.Canvas(frame_mensajes_outer, 
                                      bg=COLOR_BG, bd=0, 
                                      highlightthickness=0)
        scroll_chat = ttk.Scrollbar(frame_mensajes_outer, 
                                     orient="vertical", 
                                     command=self.canvas_chat.yview)
        self.frame_burbujas = tk.Frame(self.canvas_chat, bg=COLOR_BG)
        self.frame_burbujas.bind(
            "<Configure>", 
            lambda e: self.canvas_chat.configure(
                scrollregion=self.canvas_chat.bbox("all")))
        self.canvas_chat.create_window(
            (0, 0), window=self.frame_burbujas, anchor="nw")
        self.canvas_chat.configure(yscrollcommand=scroll_chat.set)
        self.canvas_chat.pack(side="left", fill="both", expand=True)
        scroll_chat.pack(side="right", fill="y")

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
        
        configurar_animacion_boton(btn_enviar, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def actualizar_timer(self):
        if self.timer_activo:
            tiempo_restante = self.hora_expiracion - datetime.now()
            if tiempo_restante.total_seconds() <= 0:
                self.destruir_chat()
                return
            horas, resto = divmod(int(tiempo_restante.total_seconds()), 3600)
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
        self.agregar_mensaje(random.choice(respuestas), "otro")

    def agregar_mensaje(self, texto, remitente):
        es_yo = remitente == "yo"
 
        # Contenedor de la fila
        fila = tk.Frame(self.frame_burbujas, bg=COLOR_BG)
        fila.pack(fill="x", pady=4, padx=10)
 
        # Burbuja
        color_burbuja = COLOR_ACCENT_RED if es_yo else "#2D2D2D"
        color_texto = COLOR_TEXT_MAIN
 
        burbuja = tk.Label(
            fila,
            text=texto,
            font=("Helvetica", 10),
            bg=color_burbuja,
            fg=color_texto,
            wraplength=320,
            justify="left" if not es_yo else "right",
            padx=14,
            pady=10
        )
        if es_yo:
            burbuja.pack(side="right")
        else:
            burbuja.pack(side="left")
 
        # Scroll automático al último mensaje
        self.canvas_chat.update_idletasks()
        self.canvas_chat.yview_moveto(1.0)

    def destruir_chat(self):
        self.timer_activo = False
        self._mostrar_pantalla_resena()

    def _mostrar_pantalla_resena(self):
        ventana = tk.Toplevel(self)
        ventana.title("¿Cómo fue la experiencia?")
        ventana.geometry("420x380")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.grab_set()  # Modal
 
        tk.Label(ventana,
                 text="⭐  Califica tu experiencia",
                 font=("Helvetica", 14, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(pady=(25, 5))
 
        tk.Label(ventana,
                 text=f"¿Cómo fue el encuentro con\n"
                      f"{self.match_encontrado['usuario']}?",
                 font=("Helvetica", 10),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 justify="center").pack(pady=(0, 20))
 
        # Selector estrellas
        puntuacion_var = tk.IntVar(value=5)
        frame_stars = tk.Frame(ventana, bg=COLOR_CARD)
        frame_stars.pack(pady=(0, 15))
        for n in range(1, 6):
            tk.Radiobutton(
                frame_stars,
                text=f"{n} ⭐",
                variable=puntuacion_var,
                value=n,
                font=("Helvetica", 10),
                bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                activebackground=COLOR_CARD,
                activeforeground=COLOR_RAYO_YELLOW,
                selectcolor=COLOR_BG, bd=0
            ).pack(side="left", padx=5)
 
        # Campo de comentario
        tk.Label(ventana,
                 text="Comentario (opcional):",
                 font=("Helvetica", 9, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(
                 anchor="w", padx=30, pady=(0, 4))
 
        ent_comentario = tk.Entry(
            ventana,
            font=("Helvetica", 10),
            bg="#2D2D2D", fg=COLOR_TEXT_MAIN,
            bd=0, highlightthickness=1,
            highlightbackground="#3D3D3D"
        )
        ent_comentario.pack(fill="x", padx=30, ipady=7, pady=(0, 20))
 
        def enviar_resena():
            nuevo_match = {
                "id": f"m{len(base_datos_global['historial_matches'])+1:03d}",
                "usuario_match": self.match_encontrado["usuario"],
                "genero_match": self.match_encontrado["genero"],
                "promo": self.promo["titulo"],
                "zona": self.promo.get("zona", "—"),
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "hora": datetime.now().strftime("%H:%M"),
                "reseña_dada": ent_comentario.get().strip() or "Sin comentario",
                "puntuacion_dada": puntuacion_var.get()
            }
            base_datos_global["historial_matches"].append(nuevo_match)
            guardar_datos()
            ventana.destroy()
            if self.on_close:
                self.on_close()
 
        btn_enviar = tk.Button(
            ventana,
            text="Enviar reseña y cerrar chat",
            font=("Helvetica", 10, "bold"),
            bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN,
            bd=0, cursor="hand2",
            command=enviar_resena
        )
        btn_enviar.pack(fill="x", padx=30, ipady=10)
 
        btn_omitir = tk.Button(
            ventana,
            text="Omitir por ahora",
            font=("Helvetica", 9),
            bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
            bd=0, cursor="hand2",
            command=lambda: [ventana.destroy(), self.on_close() if self.on_close else None]
        )
        btn_omitir.pack(pady=10)
