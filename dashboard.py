
import tkinter as tk
from tkinter import ttk
import re
import datetime
import random
from chat import SalaChatTemporal
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
    COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_AMARILLO_ORO, COLOR_ESCUDO_RED,
    COLOR_NAV, COLOR_CORAL_FUEGO, COLOR_AZUL_ELECTRICO, cargar_datos, guardar_datos, configurar_animacion_boton,
    base_datos_global
)


class PanelEstudiante(tk.Frame):
    def __init__(self, parent, usuario_actual, al_cerrar_sesion):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion
        self.promo_seleccionada = None
        self.filtro_zona = "Todas"
        self.filtro_categoria = "Todas"
        self.tarjetas = []
        self.hora_fin = None
        self.match_encontrado = None
        self.chat = None
        self.seccion_actual = "inicio"
        self.datos = cargar_datos()
        self.chatbot_expandido = True
        self.filtro_actual = None
        self.tooltip = None
        self.vista_actual = None
        self.toast_list = []

        self.inicializar_ui()

    def inicializar_ui(self):
        self.seccion_actual = "inicio"
        self.promo_seleccionada = None
        self.match_encontrado = None
        self.hora_fin = None
        self.chat = None
        self.tarjetas = []
        self.filtro_zona = "Todas"
        self.filtro_categoria = "Todas"
        self.filtro_actual = None

        self.mostrar_dashboard()
        self.mostrar_bienvenida()
        self.iniciar_toasts()

    def cambiar_vista(self, nueva_vista):
        if self.vista_actual is not None:
            self.vista_actual.destroy()
        self.vista_actual = nueva_vista
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_dashboard(self):
        self.frame_dashboard = tk.Frame(self, bg=COLOR_BG)
        self.frame_contenido = tk.Frame(self.frame_dashboard, bg=COLOR_BG)
        self.frame_contenido.pack(fill="both", expand=True, side="top")

        self._crear_nav_inferior()
        self.cambiar_vista(self.frame_dashboard)
        self.mostrar_inicio()

    def mostrar_bienvenida(self):
        self.bienvenida = tk.Toplevel(self)
        self.bienvenida.title("Two Pack - ¡Nuevo Lanzamiento!")
        self.bienvenida.configure(bg=COLOR_CORAL_FUEGO)
        self.bienvenida.geometry("360x200")
        self.bienvenida.resizable(False, False)

        # Centrar la ventana
        self.bienvenida.update_idletasks()
        ancho_ventana = self.bienvenida.winfo_width()
        alto_ventana = self.bienvenida.winfo_height()
        ancho_pantalla = self.bienvenida.winfo_screenwidth()
        alto_pantalla = self.bienvenida.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.bienvenida.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Contenido
        tk.Frame(self.bienvenida, bg=COLOR_CORAL_FUEGO, height=20).pack()
        tk.Label(self.bienvenida, text="🔥 ¡NUEVO LANZAMIENTO! 🔥", font=("Helvetica", 16, "bold"), bg=COLOR_CORAL_FUEGO, fg=COLOR_TEXT_MAIN).pack()
        tk.Frame(self.bienvenida, bg=COLOR_CORAL_FUEGO, height=10).pack()

        tk.Label(self.bienvenida, text="Prueba la nueva 'Mega Hamburguesa Volcán 2x1'\nen Zona Norte", font=("Helvetica", 12), bg=COLOR_CORAL_FUEGO, fg=COLOR_TEXT_MAIN, justify=tk.CENTER).pack(padx=20)

        tk.Frame(self.bienvenida, bg=COLOR_CORAL_FUEGO, height=15).pack()
        tk.Button(self.bienvenida, text="✕ Cerrar", font=("Helvetica", 10, "bold"), bg=COLOR_RED_ACTIVE, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=self.cerrar_bienvenida, padx=15, pady=6).pack()

    def cerrar_bienvenida(self):
        self.bienvenida.destroy()

    def _crear_nav_inferior(self):
        self.nav_bar = tk.Frame(self.frame_dashboard, bg=COLOR_NAV, height=62)
        self.nav_bar.pack(fill="x", side="bottom")
        self.nav_bar.pack_propagate(False)

        tk.Frame(self.nav_bar, bg="#3D3D3D", height=1).pack(fill="x", side="top")

        frame_btns = tk.Frame(self.nav_bar, bg=COLOR_NAV)
        frame_btns.pack(fill="both", expand=True)

        nav_items = [
            ("🏠", "Inicio", "inicio"),
            ("🗺️", "Mapa", "mapa"),
            ("🤝", "Match", "match"),
            ("💬", "Chat", "chat_tab"),
            ("👤", "Perfil", "perfil"),
        ]

        self.nav_botones = {}
        for icono, texto, seccion in nav_items:
            col = tk.Frame(frame_btns, bg=COLOR_NAV)
            col.pack(side="left", fill="both", expand=True)

            if seccion == "match":
                canvas_fab = tk.Canvas(
                    col, width=52, height=52,
                    bg=COLOR_NAV, bd=0, highlightthickness=0
                )
                canvas_fab.pack(pady=4)
                canvas_fab.create_oval(2, 2, 50, 50, fill=COLOR_ACCENT_RED, outline="")
                canvas_fab.create_text(26, 22, text="🤝", font=("Helvetica", 14))
                canvas_fab.create_text(26, 40, text="Match", font=("Helvetica", 7, "bold"), fill=COLOR_TEXT_MAIN)
                canvas_fab.bind("<Button-1>", lambda e: self.navegar_a("match"))
                self.nav_botones[seccion] = canvas_fab
            else:
                btn = tk.Button(
                    col,
                    text=f"{icono}\n{texto}",
                    font=("Helvetica", 7),
                    bg=COLOR_NAV,
                    fg=COLOR_ACCENT_RED if seccion == "inicio" else COLOR_TEXT_MUTED,
                    bd=0, cursor="hand2",
                    activebackground=COLOR_NAV,
                    activeforeground=COLOR_ACCENT_RED,
                    command=lambda s=seccion: self.navegar_a(s)
                )
                btn.pack(fill="both", expand=True, pady=6)
                self.nav_botones[seccion] = btn

    def navegar_a(self, seccion):
        self.seccion_actual = seccion
        for s, btn in self.nav_botones.items():
            if s == "match":
                continue
            color = COLOR_ACCENT_RED if s == seccion else COLOR_TEXT_MUTED
            btn.config(fg=color)
        for w in self.frame_contenido.winfo_children():
            w.destroy()
        if seccion in ("inicio", "explorar"):
            self.mostrar_inicio()
        elif seccion == "mapa":
            self.mostrar_mapa()
        elif seccion == "match":
            self.mostrar_match_panel()
        elif seccion == "chat_tab":
            self.mostrar_chat_vacio()
        elif seccion == "perfil":
            self.mostrar_perfil()
        elif seccion == "historial":
            self.mostrar_historial()

    def mostrar_inicio(self):
        f = self.frame_contenido

        header = tk.Frame(f, bg=COLOR_ESCUDO_RED, height=130)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Top row with Two Pack, notifications, menu
        f1 = tk.Frame(header, bg=COLOR_ESCUDO_RED)
        f1.pack(fill="x", padx=15, pady=(12, 6))

        tk.Label(f1, text="Two Pack", font=("Georgia", 20, "bold", "italic"), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN).pack(side="left")

        # Notifications, chatbot and menu buttons on right
        f1_right = tk.Frame(f1, bg=COLOR_ESCUDO_RED)
        f1_right.pack(side="right")

        # Menu icon (three bars)
        btn_menu = tk.Label(f1_right, text="☰", font=("Helvetica", 20), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN, cursor="hand2", padx=10)
        btn_menu.pack(side="left")

        # Chatbot button in header
        btn_chatbot_header = tk.Label(f1_right, text="🤖", font=("Helvetica", 18), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN, cursor="hand2", padx=8)
        btn_chatbot_header.pack(side="left")
        btn_chatbot_header.bind("<Button-1>", lambda e: self.toggle_chatbot_panel())

        # Bell icon for notifications
        btn_notificaciones = tk.Label(f1_right, text="🔔", font=("Helvetica", 18), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN, cursor="hand2", padx=10)
        btn_notificaciones.pack(side="left")
        btn_notificaciones.bind("<Button-1>", lambda e: self.mostrar_notificaciones())

        # Second row: location and IA MATCHMAKER
        f2 = tk.Frame(header, bg=COLOR_ESCUDO_RED)
        f2.pack(fill="x", padx=15, pady=(0, 8))

        zona = self.usuario_actual.get("zona_preferida", "Cochabamba Centro")
        tk.Label(f2, text=f"📍 {zona}", font=("Helvetica", 9), bg=COLOR_ESCUDO_RED, fg="#FFCCCC").pack(side="left")

        tk.Label(f2, text=" ⚡ IA MATCHMAKER ACTIVO ", font=("Helvetica", 8, "bold"), bg="#FF6600", fg=COLOR_TEXT_MAIN).pack(side="right")

        # Search bar
        f3 = tk.Frame(header, bg=COLOR_ESCUDO_RED)
        f3.pack(fill="x", padx=15, pady=(0, 10))

        barra = tk.Frame(f3, bg="#FFFFFF")
        barra.pack(fill="x")

        tk.Label(barra, text="🔍", bg="#FFFFFF", fg="#999999", font=("Helvetica", 10)).pack(side="left", padx=(8, 2), pady=5)

        self.ent_busq = tk.Entry(barra, font=("Helvetica", 9), bg="#FFFFFF", fg="#999999", bd=0, insertbackground="#333")
        self.ent_busq.insert(0, "Buscar promociones, lugares o actividades...")
        self.ent_busq.pack(side="left", fill="x", expand=True, ipady=6)

        tk.Label(barra, text="⚙", bg="#FFFFFF", fg=COLOR_ESCUDO_RED, font=("Helvetica", 12)).pack(side="right", padx=8)

        # Urgency header
        self.mostrar_urgencia()

        # Category chips
        frame_chips = tk.Frame(f, bg=COLOR_BG)
        frame_chips.pack(fill="x", padx=10, pady=10)

        chips = [
            ("🏠 Todas", "Todas"),
            ("🍔 Gastronomía", "Gastronomía"),
            ("🎬 Entretenimiento", "Entretenimiento"),
            ("🏨 Alojamientos", "Alojamientos"),
            ("💪 Deportes", "Deportes"),
            ("🛒 Supermercados", "Supermercados"),
            ("🎵 Fiestas", "Fiestas"),
            ("☕ Cafeterías", "Cafeterías"),
        ]
        self.chip_activo = "Todas"
        self.chip_btns = {}

        for txt, val in chips:
            activo = val == self.chip_activo
            b = tk.Button(
                frame_chips, text=txt,
                font=("Helvetica", 7, "bold"),
                bg=COLOR_AZUL_ELECTRICO if activo else "#2A2A2A",
                fg=COLOR_TEXT_MAIN,
                bd=0, cursor="hand2",
                padx=10, pady=5, relief="flat",
                command=lambda v=val: self._chip_click(v)
            )
            b.pack(side="left", padx=3)
            self.chip_btns[val] = b
            configurar_animacion_boton(b, COLOR_AZUL_ELECTRICO if activo else "#2A2A2A", "#0095FF", "#0056B3")

        tk.Label(f, text="Promociones reales. 100% Gratis para todos.", font=("Helvetica", 8), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 8))

        # Chatbot floating button (big and easy to click!)
        self.btn_chatbot_flotante = tk.Button(f, text="🤖", font=("Helvetica", 24), bg=COLOR_AZUL_ELECTRICO, fg=COLOR_TEXT_MAIN, bd=3, cursor="hand2", width=4, height=2, command=self.toggle_chatbot_panel, highlightthickness=0)
        self.btn_chatbot_flotante.place(relx=0.9, rely=0.8, anchor="center")
        self.btn_chatbot_flotante.config(relief="solid", highlightbackground=COLOR_AZUL_ELECTRICO)

        # Promo grid
        frame_scroll = tk.Frame(f, bg=COLOR_BG)
        frame_scroll.pack(fill="both", expand=True)

        self.canvas_cards = tk.Canvas(frame_scroll, bg=COLOR_BG, bd=0, highlightthickness=0)
        sb = ttk.Scrollbar(frame_scroll, orient="vertical", command=self.canvas_cards.yview)
        self.frame_grid = tk.Frame(self.canvas_cards, bg=COLOR_BG)
        self.frame_grid.bind("<Configure>", lambda e: self.canvas_cards.configure(scrollregion=self.canvas_cards.bbox("all")))
        self.canvas_cards.create_window((0, 0), window=self.frame_grid, anchor="nw")
        self.canvas_cards.configure(yscrollcommand=sb.set)
        self.canvas_cards.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._renderizar_grid()

        # Bottom banner
        banner = tk.Frame(f, bg=COLOR_ACCENT_RED, height=32)
        banner.pack(fill="x", side="bottom")
        banner.pack_propagate(False)
        tk.Label(banner, text="Two Pack: Tu ciudad, tus planes, tu mejor match.", font=("Helvetica", 8, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN).pack(expand=True, pady=8)

        # Chatbot panel (initially hidden)
        self.chatbot_panel = tk.Frame(self, bg="#0F1419", width=340, highlightthickness=1, highlightbackground="#333333")
        self.chatbot_panel_visible = False
        # We'll place it when toggled
        self.crear_chatbot_panel()

    def crear_chatbot_panel(self):
        # Header for chatbot panel
        header_chatbot = tk.Frame(self.chatbot_panel, bg=COLOR_AZUL_ELECTRICO, height=50)
        header_chatbot.pack(fill="x")
        header_chatbot.pack_propagate(False)
        tk.Label(header_chatbot, text="🤖 Asistente Two Pack", font=("Helvetica", 12, "bold"), bg=COLOR_AZUL_ELECTRICO, fg=COLOR_TEXT_MAIN).pack(side="left", padx=15, pady=12)
        tk.Button(header_chatbot, text="✕", font=("Helvetica", 12), bg=COLOR_AZUL_ELECTRICO, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=self.toggle_chatbot_panel).pack(side="right", padx=15)

        # Chatbot content
        self.frame_chat_historial = tk.Frame(self.chatbot_panel, bg="#0F1419", height=300)
        self.frame_chat_historial.pack(fill="x", pady=(8, 0), padx=8)
        self.frame_chat_historial.pack_propagate(False)

        self.canvas_chat = tk.Canvas(self.frame_chat_historial, bg="#0F1419", bd=0, highlightthickness=0)
        self.canvas_chat.pack(side="left", fill="both", expand=True)

        self.frame_mensajes = tk.Frame(self.canvas_chat, bg="#0F1419")
        self.frame_mensajes.bind("<Configure>", lambda e: self.canvas_chat.configure(scrollregion=self.canvas_chat.bbox("all")))
        self.canvas_chat.create_window((0, 0), window=self.frame_mensajes, anchor="nw")

        self._agregar_mensaje_bot("¡Hola! Soy tu asistente Two Pack. Cuéntame qué buscas: 🍔 comida, 🎬 entretenimiento, 💪 bienestar...")

        # Quick buttons
        frame_botones_rapidos = tk.Frame(self.chatbot_panel, bg="#1E2732")
        frame_botones_rapidos.pack(fill="x", padx=8, pady=8)
        botones_rapidos = [
            ("🍔 Alitas Hoy", "alitas en la recoleta"),
            ("🎬 Cine", "cine en el centro"),
            ("☕ Cafés", "cafés"),
            ("💪 Gimnasio", "gimnasio"),
        ]
        for txt, comando in botones_rapidos:
            b = tk.Button(frame_botones_rapidos, text=txt, font=("Helvetica", 7, "bold"), bg="#2A2A2A", fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=8, pady=5, relief="flat", command=lambda c=comando: self._enviar_mensaje_rapido(c))
            b.pack(side="left", padx=3, pady=3)
            configurar_animacion_boton(b, "#2A2A2A", COLOR_AZUL_ELECTRICO, "#0056B3")

        # Input
        frame_input = tk.Frame(self.chatbot_panel, bg="#1E2732", height=60)
        frame_input.pack(fill="x", side="bottom")
        frame_input.pack_propagate(False)

        campo = tk.Frame(frame_input, bg="#1E2732")
        campo.pack(fill="x", padx=8, pady=10)
        tk.Label(campo, text="📎", font=("Helvetica", 16), bg="#1E2732", fg=COLOR_TEXT_MUTED, cursor="hand2").pack(side="left", padx=(0, 8))
        self.ent_chatbot = tk.Entry(campo, font=("Helvetica", 9), bg="#273441", fg=COLOR_TEXT_MAIN, bd=0, insertbackground="white", highlightthickness=0)
        self.ent_chatbot.insert(0, "Escribe tu consulta...")
        self.ent_chatbot.pack(side="left", fill="x", expand=True, ipady=8)
        self.ent_chatbot.bind("<Return>", lambda e: self._procesar_mensaje_chatbot())
        btn_enviar_chat = tk.Button(campo, text="➤", font=("Helvetica", 14, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=10, pady=6, command=self._procesar_mensaje_chatbot)
        btn_enviar_chat.pack(side="left", padx=(8, 0))
        configurar_animacion_boton(btn_enviar_chat, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def toggle_chatbot_panel(self):
        if not self.chatbot_panel_visible:
            self.chatbot_panel.place(relx=0.9, rely=0.5, anchor="e")
            self.chatbot_panel.tkraise()
        else:
            self.chatbot_panel.place_forget()
        self.chatbot_panel_visible = not self.chatbot_panel_visible

    def mostrar_notificaciones(self):
        # Show notifications window
        notif_window = tk.Toplevel(self)
        notif_window.title("Notificaciones")
        notif_window.geometry("360x400")
        notif_window.configure(bg=COLOR_BG)
        notif_window.update_idletasks()
        ancho = notif_window.winfo_width()
        alto = notif_window.winfo_height()
        x = (notif_window.winfo_screenwidth() // 2) - (ancho // 2)
        y = (notif_window.winfo_screenheight() // 2) - (alto // 2)
        notif_window.geometry(f"{ancho}x{alto}+{x}+{y}")

        tk.Label(notif_window, text="🔔 Notificaciones", font=("Helvetica", 16, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(pady=20)

        # Use the toast messages as sample notifications
        sample_notifs = [
            "⚡ Match Exitoso en Zona UCATEC! Hace 2 min Carlos y Sofía dividieron un combo 2x1.",
            "📍 Nuevo comercio registrado! 'Cine Center' se ha unido a la red con entradas 2x1.",
            "🍔 ¡10 matches activos en la zona de La Recoleta! ¡Únete a la diversión!",
            "🏃‍♂️ ¡Deportes! 5 personas buscan compañero para gym en Zona Norte ahora mismo.",
            "🎵 ¡Fiesta esta noche! 8 personas buscaron un plan de discotecas en 10 minutos.",
        ]

        for notif in sample_notifs:
            notif_frame = tk.Frame(notif_window, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D", padx=15, pady=10)
            notif_frame.pack(fill="x", padx=15, pady=5)
            tk.Label(notif_frame, text=notif, font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, wraplength=300, justify="left").pack(anchor="w")

    def mostrar_urgencia(self):
        hoy = datetime.datetime.now().strftime("%d/%m/%Y")
        promos_hoy = [p for p in base_datos_global["promociones"] if p.get("vence") == hoy]

        if len(promos_hoy) > 0:
            self.urgencia_frame = tk.Frame(self.frame_contenido, bg=COLOR_AMARILLO_ORO, height=50)
            self.urgencia_frame.pack(fill="x")
            self.urgencia_frame.pack_propagate(False)

            self.urgencia_label = tk.Label(self.urgencia_frame,
                text=f"🚨 ¡ALERTA! Hoy {hoy} se vencen {len(promos_hoy)} promociones!",
                font=("Helvetica", 9, "bold"),
                bg=COLOR_AMARILLO_ORO,
                fg="#1A1A1A")
            self.urgencia_label.pack(pady=12)

            self.urgencia_flash = True
            self.flash_urgencia()

    def flash_urgencia(self):
        if hasattr(self, "urgencia_label") and self.urgencia_label.winfo_exists():
            if self.urgencia_flash:
                self.urgencia_label.config(fg=COLOR_ACCENT_RED)
            else:
                self.urgencia_label.config(fg="#1A1A1A")
            self.urgencia_flash = not self.urgencia_flash
            self.after(500, self.flash_urgencia)

    def iniciar_toasts(self):
        self.toast_messages = [
            "⚡ Match Exitoso en Zona UCATEC! Hace 2 min Carlos y Sofía dividieron un combo 2x1.",
            "📍 Nuevo comercio registrado! 'Cine Center' se ha unido a la red con entradas 2x1.",
            "🍔 ¡10 matches activos en la zona de La Recoleta! ¡Únete a la diversión!",
            "🏃‍♂️ ¡Deportes! 5 personas buscan compañero para gym en Zona Norte ahora mismo.",
            "🎵 ¡Fiesta esta noche! 8 personas buscaron un plan de discotecas en 10 minutos.",
        ]
        self.siguiente_toast()

    def siguiente_toast(self):
        self.after(random.randint(40000, 60000), self.mostrar_toast)

    def mostrar_toast(self):
        msg = random.choice(self.toast_messages)

        # Frame del toast (overlay)
        toast = tk.Toplevel(self)
        toast.wm_overrideredirect(True)
        toast.configure(bg="#2D2D2D")

        # Contenido
        tk.Label(toast, text=msg, font=("Helvetica", 9), bg="#2D2D2D", fg=COLOR_TEXT_MAIN, wraplength=300, padx=15, pady=10).pack()

        # Posicionar en la esquina inferior derecha
        self.update_idletasks()
        ancho_ventana = toast.winfo_reqwidth()
        alto_ventana = toast.winfo_reqheight()
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        x = ancho_pantalla - ancho_ventana - 30
        y = alto_pantalla - alto_ventana - 90
        toast.geometry(f"+{x}+{y}")

        # Desvanecer después de 6 segundos
        self.after(6000, lambda: toast.destroy())
        self.siguiente_toast()

    def _chip_click(self, val):
        self.chip_activo = val
        self.filtro_categoria = val
        for v, b in self.chip_btns.items():
            if v == val:
                b.config(bg=COLOR_AZUL_ELECTRICO)
                configurar_animacion_boton(b, COLOR_AZUL_ELECTRICO, "#0095FF", "#0056B3")
            else:
                b.config(bg="#2A2A2A")
                configurar_animacion_boton(b, "#2A2A2A", COLOR_AZUL_ELECTRICO, "#0056B3")
        self._renderizar_grid()

    def _renderizar_grid(self):
        for w in self.frame_grid.winfo_children():
            w.destroy()
        self.tarjetas = []

        promos = base_datos_global["promociones"]
        if self.filtro_actual:
            promos = self._filtrar_promociones(self.filtro_actual)
        else:
            if self.filtro_categoria != "Todas":
                promos = [p for p in promos if p["cat"] == self.filtro_categoria]

        for i, promo in enumerate(promos):
            fila = i // 2
            col = i % 2
            card = self._crear_card_foto(self.frame_grid, promo)
            card.grid(row=fila, column=col, padx=6, pady=6, sticky="nsew")
            self.frame_grid.grid_columnconfigure(col, weight=1, minsize=180)
            self.tarjetas.append(card)

    def _crear_card_foto(self, parent, promo):
        FOTO_CONFIG = {
            "Gastronomía": ("#5C1010", "#CC3300", "#FF6633", "🍔"),
            "Entretenimiento": ("#0D0D40", "#1A1AFF", "#3333FF", "🎬"),
            "Alojamientos": ("#0D4020", "#1A8040", "#33CC66", "🏨"),
            "Deportes": ("#300D30", "#660066", "#CC33CC", "💪"),
            "Supermercados": ("#40300D", "#80601A", "#CC9933", "🛒"),
            "Fiestas": ("#400D0D", "#801A1A", "#CC3333", "🎵"),
            "Cafeterías": ("#0D300D", "#008030", "#33CC66", "☕"),
            "Tiendas Locales": ("#1A1A1A", "#333333", "#666666", "🛍️"),
            "Otros": ("#1A1A1A", "#333333", "#666666", "🛍️"),
        }
        cat = promo.get("cat", "Otros")
        bg1, bg2, bg3, emoji = FOTO_CONFIG.get(cat, FOTO_CONFIG["Otros"])

        card = tk.Frame(parent, bg=COLOR_CARD, highlightthickness=0)

        canvas_foto = tk.Canvas(card, width=180, height=110, bg=bg1, bd=0, highlightthickness=0)
        canvas_foto.pack(fill="x")

        canvas_foto.create_rectangle(0, 0, 180, 55, fill=bg1, outline="")
        canvas_foto.create_rectangle(0, 55, 180, 110, fill=bg2, outline="")

        canvas_foto.create_text(90, 50, text=emoji, font=("Helvetica", 36))

        canvas_foto.create_rectangle(8, 8, 48, 28, fill=COLOR_ACCENT_RED, outline="")
        canvas_foto.create_text(28, 18, text="2x1", font=("Helvetica", 9, "bold"), fill=COLOR_TEXT_MAIN)

        demanda = promo.get("demanda", "Alta Demanda")
        canvas_foto.create_rectangle(90, 8, 175, 28, fill="#FF6600", outline="")
        canvas_foto.create_text(132, 18, text=f"🔥 {demanda}", font=("Helvetica", 7, "bold"), fill=COLOR_TEXT_MAIN)

        info = tk.Frame(card, bg=COLOR_CARD, padx=8, pady=6)
        info.pack(fill="x")

        comercio_nombre = promo.get("comercio", promo["titulo"].split()[0] + " Local")
        tk.Label(info, text=comercio_nombre, font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, anchor="w").pack(anchor="w")

        tk.Label(info, text=promo["titulo"], font=("Helvetica", 8), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w", wraplength=165).pack(anchor="w")

        dist = promo.get("distancia", "800 m")
        hora = promo.get("hora_hasta", "23:00")
        tk.Label(info, text=f"📍 {dist}   🕐 Hasta {hora}", font=("Helvetica", 7), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(anchor="w", pady=(2, 6))

        btn = tk.Button(
            info,
            text="💙 Encontrar Compañero",
            font=("Helvetica", 8, "bold"),
            bg=COLOR_ACCENT_RED,
            fg=COLOR_TEXT_MAIN,
            bd=0, cursor="hand2",
            pady=6, relief="flat",
            command=lambda p=promo: self.mostrar_detalle_promo(p)
        )
        btn.pack(fill="x")

        return card

    def mostrar_detalle_promo(self, promo):
        self.promo_seleccionada = promo
        for w in self.frame_contenido.winfo_children():
            w.destroy()

        f = self.frame_contenido

        header = tk.Frame(f, bg=COLOR_ESCUDO_RED, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Button(header, text="← Volver", font=("Helvetica", 10, "bold"), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=lambda: self.navegar_a("inicio")).pack(side="left", padx=15, pady=20)
        tk.Label(header, text="Oferta 2x1", font=("Helvetica", 14, "bold"), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN).pack(side="left", padx=10)

        content = tk.Frame(f, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(content, text=promo["comercio"], font=("Helvetica", 18, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        tk.Label(content, text=promo["titulo"], font=("Helvetica", 14), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 10))

        tk.Label(content, text=f"📍 {promo['zona']}", font=("Helvetica", 11), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(5, 0))
        tk.Label(content, text=f"💰 Precio referencia: Bs {promo['precio_ref']}", font=("Helvetica", 11), bg=COLOR_BG, fg=COLOR_AMARILLO_ORO).pack(anchor="w", pady=(5, 0))
        tk.Label(content, text=f"🕐 Hasta: {promo['hora_hasta']}", font=("Helvetica", 11), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(5, 0))
        tk.Label(content, text=f"📅 Vence: {promo['vence']}", font=("Helvetica", 11), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 20))

        tk.Label(content, text="Descripción:", font=("Helvetica", 12, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 5))
        tk.Label(content, text=promo["descripcion"], font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_TEXT_MUTED, wraplength=400, justify="left").pack(anchor="w", pady=(0, 30))

        tk.Button(content, text="🤝 Activar Match", font=("Helvetica", 14, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=30, pady=15, command=lambda: self.activar_match_desde_detalle(promo)).pack()

    def activar_match_desde_detalle(self, promo):
        # Buscar un match real en pool_solicitudes
        match_encontrado = None
        # Primero, buscar en pool_solicitudes por oferta_id
        # O si no hay, usar un usuario existente en base_datos_global['usuarios']
        usuarios_posibles = []
        # Check pool_solicitudes first
        for solicitud in base_datos_global.get('pool_solicitudes', []):
            # Get usuario de la solicitud
            email_usuario_match = base_datos_global['usuarios'].get(solicitud['usuario'], {"nombre": solicitud['usuario']})
            if email_usuario_match.get('nombre') != self.usuario_actual.get('nombre'):
                usuarios_posibles.append(email_usuario_match)
        # If pool_solicitudes has users, use first one
        if usuarios_posibles:
            match_encontrado = usuarios_posibles[0]
        else:
            # Fallback to simulated user
            match_encontrado = {
                "nombre": "María José",
                "genero": "Femenino",
                "confianza": 5.0,
                "matches": 12,
                "estado": "Activo"
            }

        def al_cerrar():
            self.mostrar_dashboard()
            self.mostrar_detalle_promo(promo)

        self.chat = SalaChatTemporal(self, self.usuario_actual, match_encontrado, promo, al_cerrar)
        self.cambiar_vista(self.chat)

    def al_cerrar_chat(self):
        self.chat = None
        self.mostrar_detalle_promo(self.promo_seleccionada)

    def mostrar_match_panel(self):
        f = self.frame_contenido
        header = tk.Frame(f, bg=COLOR_ESCUDO_RED, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🤝 Encontrar Compañero", font=("Helvetica", 14, "bold"), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN).pack(side="left", padx=15, pady=25)

        # Mostrar pool de solicitudes disponibles
        tk.Label(f, text="Personas buscando compañeros ahora", font=("Helvetica", 13, "bold"), bg=COLOR_BG, fg=COLOR_AMARILLO_ORO).pack(anchor="w", padx=15, pady=(20))

        if not base_datos_global.get('pool_solicitudes', []):
            tk.Label(f, text="No hay solicitudes disponibles en este momento", font=("Helvetica", 11), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(pady=40)
            tk.Button(f, text="Ver promociones", font=("Helvetica", 10, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=20, pady=10, command=lambda: self.navegar_a("inicio")).pack()
            return

        frame_lista = tk.Frame(f, bg=COLOR_BG)
        frame_lista.pack(fill="both", expand=True, padx=10)

        for solicitud in base_datos_global.get('pool_solicitudes', []):
            card_solicitud = tk.Frame(frame_lista, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D", padx=12, pady=10)
            card_solicitud.pack(fill="x", pady=5)
            
            usuario_solicitante = base_datos_global['usuarios'].get(solicitud['usuario'], {"nombre": solicitud['usuario'], "genero": "No especificado", "confianza": 5.0, "matches": 0, "estado": "Activo"})
            # Find the promo
            promo_solicitada = None
            for promo in base_datos_global['promociones']:
                if promo['id'] == solicitud['oferta_id']:
                    promo_solicitada = promo
                    break
            if not promo_solicitada:
                promo_solicitada = {'titulo': 'Plan general'}

            canvas_av = tk.Canvas(card_solicitud, width=50, height=50, bg=COLOR_CARD, bd=0, highlightthickness=0)
            canvas_av.pack(side="left", padx=(0, 12))
            canvas_av.create_oval(2, 2, 48, 48, fill=COLOR_ACCENT_RED, outline="")
            ini = usuario_solicitante['nombre'][0].upper()
            canvas_av.create_text(25, 25, text=ini, font=("Helvetica", 22, "bold"), fill=COLOR_TEXT_MAIN)

            info_solicitud = tk.Frame(card_solicitud, bg=COLOR_CARD)
            info_solicitud.pack(side="left", fill="x", expand=True)
            tk.Label(info_solicitud, text=usuario_solicitante['nombre'], font=("Helvetica", 11, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(anchor="w")
            tk.Label(info_solicitud, text=f"Genero: {usuario_solicitante.get('genero', 'No especificado')} | Confianza: {usuario_solicitante.get('confianza', 5.0)}", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            tk.Label(info_solicitud, text=f"Busca: {promo_solicitada['titulo']} ({solicitud['hora_inicio']}:00 - {solicitud['hora_fin']}:00", font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO).pack(anchor="w", pady=(2, 0))
            tk.Button(info_solicitud, text="Unirme", font=("Helvetica", 9, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=15, pady=5, command=lambda p=promo_solicitada: self.activar_match_desde_detalle(p)).pack(anchor="e", pady=(5, 0))

    def mostrar_chat_vacio(self):
        f = self.frame_contenido
        header = tk.Frame(f, bg=COLOR_NAV, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="💬  Mis Chats", font=("Helvetica", 12, "bold"), bg=COLOR_NAV, fg=COLOR_TEXT_MAIN).pack(side="left", padx=15, pady=25)

        historial = base_datos_global.get("historial_matches", [])

        if not historial:
            frame_vacio = tk.Frame(f, bg=COLOR_BG)
            frame_vacio.pack(fill="both", expand=True)
            tk.Label(frame_vacio, text="💬", font=("Helvetica", 40), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(pady=(80, 10))
            tk.Label(frame_vacio, text="No tienes chats activos", font=("Helvetica", 13, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack()
            tk.Label(frame_vacio, text="Activa un match para\nempezar a chatear.", font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_TEXT_MUTED, justify="center").pack(pady=(6, 20))
            btn_explorar = tk.Button(frame_vacio, text="🔍  Explorar Promos", font=("Helvetica", 10, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=lambda: self.navegar_a("inicio"))
            btn_explorar.pack(ipady=10, ipadx=20)
            configurar_animacion_boton(btn_explorar, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)
            return

        tk.Label(f, text="CHATS RECIENTES", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(12, 6))
        canvas_c = tk.Canvas(f, bg=COLOR_BG, bd=0, highlightthickness=0)
        sb_c = ttk.Scrollbar(f, orient="vertical", command=canvas_c.yview)
        frame_lista = tk.Frame(canvas_c, bg=COLOR_BG)
        frame_lista.bind("<Configure>", lambda e: canvas_c.configure(scrollregion=canvas_c.bbox("all")))
        canvas_c.create_window((0, 0), window=frame_lista, anchor="nw")
        canvas_c.configure(yscrollcommand=sb_c.set)
        canvas_c.pack(side="left", fill="both", expand=True)
        sb_c.pack(side="right", fill="y")

        for match in reversed(historial):
            fila_chat = tk.Frame(frame_lista, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D", cursor="hand2")
            fila_chat.pack(fill="x", padx=10, pady=4)
            inner = tk.Frame(fila_chat, bg=COLOR_CARD)
            inner.pack(fill="x", padx=12, pady=10)
            canvas_av = tk.Canvas(inner, width=44, height=44, bg=COLOR_CARD, bd=0, highlightthickness=0)
            canvas_av.pack(side="left", padx=(0, 10))
            canvas_av.create_oval(2, 2, 42, 42, fill=COLOR_ACCENT_RED, outline="")
            ini = match["usuario_match"][0].upper()
            canvas_av.create_text(22, 22, text=ini, font=("Helvetica", 16, "bold"), fill=COLOR_TEXT_MAIN)
            info_c = tk.Frame(inner, bg=COLOR_CARD)
            info_c.pack(side="left", fill="x", expand=True)
            fila_top = tk.Frame(info_c, bg=COLOR_CARD)
            fila_top.pack(fill="x")
            tk.Label(fila_top, text=match["usuario_match"], font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(side="left")
            tk.Label(fila_top, text=match.get("fecha", ""), font=("Helvetica", 8), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(side="right")
            ultimo_msg = match.get("reseña_dada", f"Match en {match.get('zona', '')}")
            tk.Label(info_c, text=ultimo_msg, font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w", wraplength=220).pack(anchor="w", pady=(2, 0))
            tk.Label(info_c, text=f"🎁 {match['promo'][:30]}", font=("Helvetica", 7), bg=COLOR_CARD, fg=COLOR_ACCENT_RED, anchor="w").pack(anchor="w")
            fila_chat.bind("<Button-1>", lambda e: self.mostrar_historial())
            inner.bind("<Button-1>", lambda e: self.mostrar_historial())

    def mostrar_historial(self):
        f = self.frame_contenido
        tk.Label(f, text="📜 Historial de Matches", font=("Helvetica", 18, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(pady=40)
        for item in base_datos_global["historial_matches"]:
            card = tk.Frame(f, bg=COLOR_CARD, padx=15, pady=10)
            card.pack(fill="x", pady=5)
            tk.Label(card, text=f"🤝 {item['usuario_match']}", font=("Helvetica", 11, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(anchor="w")
            tk.Label(card, text=f"{item['promo']} - {item['fecha']}", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w")

    def mostrar_perfil(self):
        f = self.frame_contenido
        u = self.usuario_actual

        header = tk.Frame(f, bg=COLOR_ESCUDO_RED, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="👤  Mi Perfil", font=("Helvetica", 12, "bold"), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN).pack(side="left", padx=15, pady=25)

        canvas_p = tk.Canvas(f, bg=COLOR_BG, bd=0, highlightthickness=0)
        sb_p = ttk.Scrollbar(f, orient="vertical", command=canvas_p.yview)
        frame_scroll = tk.Frame(canvas_p, bg=COLOR_BG)
        frame_scroll.bind("<Configure>", lambda e: canvas_p.configure(scrollregion=canvas_p.bbox("all")))
        canvas_p.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas_p.configure(yscrollcommand=sb_p.set)
        canvas_p.pack(side="left", fill="both", expand=True)
        sb_p.pack(side="right", fill="y")

        card_av = tk.Frame(frame_scroll, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
        card_av.pack(fill="x", padx=12, pady=(16, 10))

        canvas_av = tk.Canvas(card_av, width=80, height=80, bg=COLOR_CARD, bd=0, highlightthickness=0)
        canvas_av.pack(pady=(20, 8))
        canvas_av.create_oval(4, 4, 76, 76, fill=COLOR_ACCENT_RED, outline=COLOR_RED_HOVER, width=2)
        ini = u.get("nombre", "U")[0].upper()
        canvas_av.create_text(40, 40, text=ini, font=("Helvetica", 32, "bold"), fill=COLOR_TEXT_MAIN)

        tk.Label(card_av, text=u.get("nombre", "Usuario"), font=("Helvetica", 13, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack()
        tk.Label(card_av, text=u.get("genero", "No especificado"), font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=(2, 0))

        estado = u.get("estado", "Activo")
        color_e = COLOR_SUCCESS if estado == "Activo" else COLOR_ACCENT_RED
        tk.Label(card_av, text=f"● {estado}", font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=color_e).pack(pady=(4, 12))

        tk.Frame(card_av, bg="#2D2D2D", height=1).pack(fill="x", padx=15, pady=(0, 12))
        frame_stats = tk.Frame(card_av, bg=COLOR_CARD)
        frame_stats.pack(fill="x", padx=15, pady=(0, 16))

        stats = [
            ("⭐", str(u.get("confianza", 5.0)), "Confianza"),
            ("🤝", str(u.get("matches", 0)), "Matches"),
            ("🚫", str(u.get("reportes", 0)), "Reportes"),
        ]
        for icono, valor, etiqueta in stats:
            col = tk.Frame(frame_stats, bg=COLOR_CARD)
            col.pack(side="left", fill="x", expand=True)
            tk.Label(col, text=f"{icono} {valor}", font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO).pack()
            tk.Label(col, text=etiqueta, font=("Helvetica", 8), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack()

        btn_hist = tk.Button(frame_scroll, text="📋  Ver historial de matches", font=("Helvetica", 10, "bold"), bg="#2D2D2D", fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=self.mostrar_historial)
        btn_hist.pack(fill="x", padx=12, ipady=10, pady=(0, 8))
        configurar_animacion_boton(btn_hist, "#2D2D2D", COLOR_ACCENT_RED, COLOR_RED_ACTIVE)

        card_datos = tk.Frame(frame_scroll, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
        card_datos.pack(fill="x", padx=12, pady=(0, 10))
        tk.Label(card_datos, text="INFORMACIÓN DE CUENTA", font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(14, 10))

        self.entradas_perfil = {}
        campos = [
            ("NOMBRE COMPLETO", "nombre"),
            ("UNIVERSIDAD", "universidad"),
            ("GÉNERO", "genero"),
        ]
        for label_txt, clave in campos:
            tk.Label(card_datos, text=label_txt, font=("Helvetica", 7, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(4, 2))
            en = tk.Entry(card_datos, font=("Helvetica", 10), bg="#2D2D2D", fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#3D3D3D")
            en.insert(0, u.get(clave, ""))
            en.pack(fill="x", padx=16, ipady=7, pady=(0, 6))
            self.entradas_perfil[clave] = en

        btn_guardar = tk.Button(card_datos, text="💾  Guardar cambios", font=("Helvetica", 10, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=self.guardar_perfil)
        btn_guardar.pack(fill="x", padx=16, ipady=9, pady=14)
        configurar_animacion_boton(btn_guardar, COLOR_SUCCESS, "#27AE60", "#1E8449")

        card_seg = tk.Frame(frame_scroll, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
        card_seg.pack(fill="x", padx=12, pady=(0, 10))
        tk.Label(card_seg, text="🔒  SEGURIDAD", font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_AMARILLO_ORO).pack(anchor="w", padx=16, pady=(14, 6))
        tk.Label(card_seg, text="Tu correo universitario verifica\n tu identidad en Two Pack.\n Perfil verificado = mayor prioridad\n en el algoritmo de match.", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, justify="left").pack(anchor="w", padx=16, pady=(0, 12))

        btn_logout = tk.Button(frame_scroll, text="🚪  Cerrar Sesión", font=("Helvetica", 10, "bold"), bg="#2A1B1D", fg="#E74C3C", bd=0, cursor="hand2", command=self.al_cerrar_sesion)
        btn_logout.pack(fill="x", padx=12, ipady=10, pady=(0, 16))
        configurar_animacion_boton(btn_logout, "#2A1B1D", COLOR_ACCENT_RED, COLOR_RED_ACTIVE)

    def guardar_perfil(self):
        for clave, entrada in self.entradas_perfil.items():
            valor = entrada.get().strip()
            self.usuario_actual[clave] = valor
            for user in base_datos_global.get('usuarios', []):
                if user.get('email') == self.usuario_actual.get('email'):
                    user[clave] = valor
                    break
        guardar_datos()
        self.mostrar_perfil()

    def mostrar_mapa(self):
        f = self.frame_contenido

        header = tk.Frame(f, bg=COLOR_NAV, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🗺️  Mapa de Promociones", font=("Helvetica", 12, "bold"), bg=COLOR_NAV, fg=COLOR_TEXT_MAIN).pack(side="left", padx=15, pady=25)
        tk.Label(header, text="📍 Cochabamba", font=("Helvetica", 9), bg=COLOR_NAV, fg=COLOR_TEXT_MUTED).pack(side="right", padx=15)

        self.canvas_mapa = tk.Canvas(f, bg="#1C2B1C", bd=0, highlightthickness=0)
        self.canvas_mapa.pack(fill="both", expand=True)

        f.update_idletasks()
        self.W = self.canvas_mapa.winfo_width() or 400
        self.H = self.canvas_mapa.winfo_height() or 420

        self._dibujar_mapa()

        self.frame_card_mapa = tk.Frame(f, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#3D3D3D")
        self.frame_card_mapa.pack(fill="x", padx=10, pady=(6, 8))

        self._actualizar_card_mapa(base_datos_global["promociones"][0])

    def _dibujar_mapa(self):
        self.canvas_mapa.delete("all")

        for i in range(0, self.W + 40, 38):
            self.canvas_mapa.create_line(i, 0, i, self.H, fill="#243024", width=1)
        for j in range(0, self.H + 40, 38):
            self.canvas_mapa.create_line(0, j, self.W, j, fill="#243024", width=1)

        for y in [int(self.H*0.25), int(self.H*0.5), int(self.H*0.75)]:
            self.canvas_mapa.create_line(0, y, self.W, y, fill="#2E3E2E", width=3)
        for x in [int(self.W*0.25), int(self.W*0.5), int(self.W*0.75)]:
            self.canvas_mapa.create_line(x, 0, x, self.H, fill="#2E3E2E", width=3)

        self.canvas_mapa.create_text(self.W // 2, self.H // 2, text="COCHABAMBA", font=("Helvetica", 13, "bold"), fill="#3A5A3A")

        zonas = [
            (int(self.W*0.1), int(self.H*0.1), int(self.W*0.35), int(self.H*0.35), "#1A3A1A", "Zona Norte"),
            (int(self.W*0.55), int(self.H*0.15), int(self.W*0.9), int(self.H*0.4), "#1A2A3A", "La Recoleta"),
            (int(self.W*0.15), int(self.H*0.6), int(self.W*0.45), int(self.H*0.85), "#2A1A1A", "El Prado"),
            (int(self.W*0.55), int(self.H*0.55), int(self.W*0.88), int(self.H*0.82), "#2A2A1A", "Av. América"),
        ]
        for x1, y1, x2, y2, color, nombre in zonas:
            self.canvas_mapa.create_rectangle(x1, y1, x2, y2, fill=color, outline="#3A4A3A", width=1)
            self.canvas_mapa.create_text((x1+x2)//2, (y1+y2)//2, text=nombre, font=("Helvetica", 8), fill="#6A8A6A")

        pins_promos = [
            (int(self.W*0.22), int(self.H*0.20), COLOR_ACCENT_RED, base_datos_global["promociones"][0]),
            (int(self.W*0.70), int(self.H*0.25), "#0066FF", base_datos_global["promociones"][3]),
            (int(self.W*0.28), int(self.H*0.70), "#FF6600", base_datos_global["promociones"][11]),
            (int(self.W*0.65), int(self.H*0.65), COLOR_ACCENT_RED, base_datos_global["promociones"][1]),
            (int(self.W*0.45), int(self.H*0.38), "#0066FF", base_datos_global["promociones"][4]),
            (int(self.W*0.50), int(self.H*0.58), COLOR_ACCENT_RED, base_datos_global["promociones"][7]),
        ]

        for px, py, color, promo in pins_promos:
            oval = self.canvas_mapa.create_oval(px-13, py-13, px+13, py+13, fill=color, outline="white", width=2)
            self.canvas_mapa.create_text(px, py, text="📍", font=("Helvetica", 11))

            tag = f"pin_{promo['id']}"
            click_area = self.canvas_mapa.create_oval(px-15, py-15, px+15, py+15, fill="", outline="", tags=tag)
            self.canvas_mapa.tag_bind(tag, "<Button-1>", lambda e, p=promo: self._click_pin_mapa(p))
            self.canvas_mapa.tag_bind(tag, "<Enter>", lambda e, p=promo: self._mostrar_tooltip(e, p))
            self.canvas_mapa.tag_bind(tag, "<Leave>", lambda e: self._ocultar_tooltip())

    def _mostrar_tooltip(self, event, promo):
        if self.tooltip:
            self._ocultar_tooltip()
        self.tooltip = tk.Toplevel(self)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.geometry(f"+{event.x_root+20}+{event.y_root-30}")
        tk.Label(self.tooltip, text=f"{promo['comercio']}: {promo['titulo']}", bg="#1E1E1E", fg="white", padx=5, pady=3, font=("Helvetica", 9)).pack()

    def _ocultar_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def _click_pin_mapa(self, promo):
        self._actualizar_card_mapa(promo)

    def _actualizar_card_mapa(self, promo):
        for w in self.frame_card_mapa.winfo_children():
            w.destroy()

        COLORES_CAT = {
            "Gastronomía": ("#5C1010", "🍔"),
            "Entretenimiento": ("#0D0D40", "🎬"),
            "Cafeterías": ("#0D300D", "☕"),
            "Alojamientos": ("#0D4020", "🏨"),
            "Deportes": ("#300D30", "💪"),
            "Supermercados": ("#40300D", "🛒"),
            "Fiestas": ("#400D0D", "🎵"),
            "Otros": ("#1A1A1A", "🛍️"),
        }
        cat = promo.get("cat", "Otros")
        bg_mini, emoji = COLORES_CAT.get(cat, ("#1A1A1A", "📍"))

        fila = tk.Frame(self.frame_card_mapa, bg=COLOR_CARD)
        fila.pack(fill="x", padx=10, pady=10)

        mini = tk.Canvas(fila, width=52, height=52, bg=bg_mini, bd=0, highlightthickness=0)
        mini.pack(side="left", padx=(0, 10))
        mini.create_text(26, 26, text=emoji, font=("Helvetica", 20))

        info = tk.Frame(fila, bg=COLOR_CARD)
        info.pack(side="left", fill="x", expand=True)

        comercio = promo.get("comercio", promo["titulo"].split()[0] + " Local")
        tk.Label(info, text=comercio, font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, anchor="w").pack(anchor="w")
        tk.Label(info, text=promo["titulo"], font=("Helvetica", 8), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w", wraplength=200).pack(anchor="w")
        dist = promo.get("distancia", "400 m")
        hora = promo.get("hora_hasta", "19:00")
        tk.Label(info, text=f"📍 {dist}   🕐 Hasta {hora}", font=("Helvetica", 7), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w")

        col_der = tk.Frame(fila, bg=COLOR_CARD)
        col_der.pack(side="right")
        tk.Label(col_der, text=" 2x1 ", font=("Helvetica", 9, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN).pack(pady=(0, 6))
        btn_ir = tk.Button(col_der, text="Ver →", font=("Helvetica", 8, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=8, pady=4, command=lambda p=promo: self.mostrar_detalle_promo(p))
        btn_ir.pack()
        configurar_animacion_boton(btn_ir, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def _crear_seccion_chatbot(self, parent):
        frame_chatbot_container = tk.Frame(parent, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
        frame_chatbot_container.pack(fill="x", padx=10, pady=(0, 8))

        header_chatbot = tk.Frame(frame_chatbot_container, bg=COLOR_CARD)
        header_chatbot.pack(fill="x", padx=12, pady=10)

        tk.Label(header_chatbot, text="🤖 Asistente Two Pack", font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_AZUL_ELECTRICO).pack(side="left")
        self.btn_toggle_chatbot = tk.Button(header_chatbot, text="▼", font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, bd=0, cursor="hand2", command=self._toggle_chatbot)
        self.btn_toggle_chatbot.pack(side="right")
        configurar_animacion_boton(self.btn_toggle_chatbot, COLOR_CARD, "#3A3A3A", COLOR_NAV)

        self.frame_chatbot_cuerpo = tk.Frame(frame_chatbot_container, bg=COLOR_CARD)
        self.frame_chatbot_cuerpo.pack(fill="x", padx=12, pady=(0, 10))

        self.frame_chat_historial = tk.Frame(self.frame_chatbot_cuerpo, bg="#0F1419", height=100)
        self.frame_chat_historial.pack(fill="x", pady=(0, 8))
        self.frame_chat_historial.pack_propagate(False)

        self.canvas_chat = tk.Canvas(self.frame_chat_historial, bg="#0F1419", bd=0, highlightthickness=0)
        self.canvas_chat.pack(side="left", fill="both", expand=True)

        self.frame_mensajes = tk.Frame(self.canvas_chat, bg="#0F1419")
        self.frame_mensajes.bind("<Configure>", lambda e: self.canvas_chat.configure(scrollregion=self.canvas_chat.bbox("all")))
        self.canvas_chat.create_window((0, 0), window=self.frame_mensajes, anchor="nw")

        self._agregar_mensaje_bot("¡Hola! Soy tu asistente Two Pack. Cuéntame qué buscas: 🍔 comida, 🎬 entretenimiento, 💪 bienestar...")

        frame_botones_rapidos = tk.Frame(self.frame_chatbot_cuerpo, bg=COLOR_CARD)
        frame_botones_rapidos.pack(fill="x", pady=(0, 8))

        botones_rapidos = [
            ("🍔 Alitas Hoy", "alitas en la recoleta"),
            ("🎬 Cine en el Centro", "cine en el centro"),
            ("☕ Cafés", "cafés"),
            ("💪 Gimnasio", "gimnasio"),
        ]
        for txt, comando in botones_rapidos:
            b = tk.Button(frame_botones_rapidos, text=txt, font=("Helvetica", 7, "bold"), bg="#2A2A2A", fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=8, pady=5, relief="flat", command=lambda c=comando: self._enviar_mensaje_rapido(c))
            b.pack(side="left", padx=3)
            configurar_animacion_boton(b, "#2A2A2A", COLOR_AZUL_ELECTRICO, "#0056B3")

        frame_input = tk.Frame(self.frame_chatbot_cuerpo, bg=COLOR_CARD)
        frame_input.pack(fill="x")

        self.ent_chatbot = tk.Entry(frame_input, font=("Helvetica", 9), bg="#2D2D2D", fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#3D3D3D")
        self.ent_chatbot.insert(0, "Ej: 'Quiero alitas en la Recoleta' o '¿Qué hay para hoy?'")
        self.ent_chatbot.pack(side="left", fill="x", expand=True, ipady=6)
        self.ent_chatbot.bind("<Return>", lambda e: self._procesar_mensaje_chatbot())

        btn_enviar_chat = tk.Button(frame_input, text="➤", font=("Helvetica", 10, "bold"), bg=COLOR_AZUL_ELECTRICO, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=10, pady=6, command=self._procesar_mensaje_chatbot)
        btn_enviar_chat.pack(side="left", padx=(8, 0))
        configurar_animacion_boton(btn_enviar_chat, COLOR_AZUL_ELECTRICO, "#0095FF", "#0056B3")

    def _toggle_chatbot(self):
        self.chatbot_expandido = not self.chatbot_expandido
        if self.chatbot_expandido:
            self.frame_chatbot_cuerpo.pack(fill="x", padx=12, pady=(0, 10))
            self.btn_toggle_chatbot.config(text="▼")
        else:
            self.frame_chatbot_cuerpo.pack_forget()
            self.btn_toggle_chatbot.config(text="▶")

    def _enviar_mensaje_rapido(self, texto):
        self.ent_chatbot.delete(0, tk.END)
        self.ent_chatbot.insert(0, texto)
        self._procesar_mensaje_chatbot()

    def _agregar_mensaje_usuario(self, texto):
        frame_mensaje = tk.Frame(self.frame_mensajes, bg="#0F1419")
        frame_mensaje.pack(fill="x", padx=8, pady=4)
        tk.Label(frame_mensaje, text=texto, font=("Helvetica", 9), bg="#1E88E5", fg=COLOR_TEXT_MAIN, wraplength=250, justify="left").pack(side="right", padx=4)
        self._scroll_chat_al_final()

    def _agregar_mensaje_bot(self, texto):
        frame_mensaje = tk.Frame(self.frame_mensajes, bg="#0F1419")
        frame_mensaje.pack(fill="x", padx=8, pady=4)
        tk.Label(frame_mensaje, text="🤖", font=("Helvetica", 12), bg="#0F1419", fg=COLOR_AZUL_ELECTRICO).pack(side="left", padx=(0, 4))
        tk.Label(frame_mensaje, text=texto, font=("Helvetica", 9), bg="#263238", fg=COLOR_TEXT_MAIN, wraplength=250, justify="left").pack(side="left")
        self._scroll_chat_al_final()

    def _scroll_chat_al_final(self):
        self.frame_mensajes.update_idletasks()
        self.canvas_chat.yview_moveto(1.0)

    def _procesar_mensaje_chatbot(self):
        texto = self.ent_chatbot.get().strip()
        if not texto or texto in ["Ej: 'Quiero alitas en la Recoleta' o '¿Qué hay para hoy?'", ""]:
            return
        self.ent_chatbot.delete(0, tk.END)
        self._agregar_mensaje_usuario(texto)
        self.filtro_actual = self.procesar_busqueda_chatbot(texto)
        promos_filtradas = self._filtrar_promociones(self.filtro_actual)
        self._generar_respuesta_bot(self.filtro_actual, promos_filtradas)
        self._renderizar_grid()

    def procesar_busqueda_chatbot(self, texto):
        texto = texto.lower()

        palabras_clave_productos = {
            "alitas": ["alita", "alitas", "alitas bbq", "pollo"],
            "hamburguesa": ["hamburguesa", "burger", "hamburguesas"],
            "pizza": ["pizza", "pizzas"],
            "café": ["café", "cafes", "café especial", "latte", "capuchino", "cafetería", "cafeterías"],
            "cine": ["cine", "película", "películas", "entrar", "entrada"],
            "gimnasio": ["gimnasio", "gym", "fitness", "ejercicio", "deporte", "deportes", "crossfit", "yoga"],
            "fiesta": ["fiesta", "fiestas", "discoteca", "discotecas", "club", "clubs", "manilla", "manillas"],
        }

        palabras_clave_categorias = {
            "Gastronomía": ["gastronomía", "comida", "alimentos", "alitas", "hamburguesa", "pizza", "restaurante"],
            "Entretenimiento": ["entretenimiento", "cine", "película", "bowling", "juegos"],
            "Cafeterías": ["café", "cafetería", "cafeterías", "latte", "capuchino"],
            "Alojamientos": ["alojamiento", "alojamientos", "hotel", "hoteles", "hostal", "hostales", "habitación"],
            "Deportes": ["deporte", "bienestar", "yoga", "fitness", "gym", "ejercicio", "gimnasio", "crossfit"],
            "Supermercados": ["supermercado", "supermercados", "tienda", "tiendas", "mercado", "fidalga"],
            "Fiestas": ["fiesta", "fiestas", "discoteca", "club", "party"],
            "Tiendas Locales": ["tienda", "compras", "locales"],
        }

        palabras_clave_zonas = {
            "Zona Norte": ["norte", "zona norte", "ucatec", "campus ucatec"],
            "La Recoleta": ["recoleta", "la recoleta"],
            "El Prado": ["prado", "el prado"],
            "Zona Centro": ["centro", "zona centro"],
            "Av. América": ["américa", "av américa", "avenida américa"],
        }

        producto = None
        categoria = None
        zona = None

        for prod, keywords in palabras_clave_productos.items():
            for kw in keywords:
                if kw in texto:
                    producto = prod
                    break
            if producto:
                break

        for cat, keywords in palabras_clave_categorias.items():
            for kw in keywords:
                if kw in texto:
                    categoria = cat
                    break
            if categoria:
                break

        for zon, keywords in palabras_clave_zonas.items():
            for kw in keywords:
                if kw in texto:
                    zona = zon
                    break
            if zona:
                break

        return {"producto": producto, "categoria": categoria, "zona": zona, "texto_original": texto}

    def _filtrar_promociones(self, resultado):
        promos = base_datos_global["promociones"]
        promos_filtradas = []

        for promo in promos:
            coincide = True
            if resultado["categoria"] and promo["cat"] != resultado["categoria"]:
                coincide = False
            if resultado["zona"]:
                if resultado["zona"] not in promo["zona"]:
                    coincide = False
            if resultado["producto"]:
                if resultado["producto"].lower() not in promo["titulo"].lower():
                    coincide = False
            if coincide:
                promos_filtradas.append(promo)

        if not promos_filtradas and resultado["categoria"]:
            promos_filtradas = [p for p in promos if p["cat"] == resultado["categoria"]]
        if not promos_filtradas:
            promos_filtradas = promos

        return promos_filtradas

    def _generar_respuesta_bot(self, resultado, promos_filtradas):
        if resultado["producto"] and resultado["zona"] and len(promos_filtradas) > 0:
            texto_respuesta = f"¡Entendido! He filtrado la cartelera. Encontré {len(promos_filtradas)} promociones de {resultado['producto']} en {resultado['zona']} ideales para ti. ¡Haz clic en 'Encontrar Compañero' para activar el Matchmaker!"
        elif resultado["producto"] and len(promos_filtradas) > 0:
            texto_respuesta = f"¡Entendido! He filtrado la cartelera. Encontré {len(promos_filtradas)} promociones de {resultado['producto']} ideales para ti. ¡Haz clic en 'Encontrar Compañero' para activar el Matchmaker!"
        elif resultado["categoria"] and len(promos_filtradas) > 0:
            texto_respuesta = f"¡Entendido! He filtrado la cartelera. Encontré {len(promos_filtradas)} promociones de {resultado['categoria']} ideales para ti. ¡Haz clic en 'Encontrar Compañero' para activar el Matchmaker!"
        elif resultado["zona"] and len(promos_filtradas) > 0:
            texto_respuesta = f"¡Entendido! He filtrado la cartelera. Encontré {len(promos_filtradas)} promociones en {resultado['zona']} ideales para ti. ¡Haz clic en 'Encontrar Compañero' para activar el Matchmaker!"
        else:
            if resultado["producto"] and resultado["zona"]:
                texto_respuesta = f"No encontré combos de {resultado['producto']} vigentes en {resultado['zona']}, pero aquí tienes opciones similares en Gastronomía:"
            elif resultado["producto"]:
                texto_respuesta = f"No encontré combos de {resultado['producto']} vigentes, pero aquí tienes opciones similares:"
            else:
                texto_respuesta = "Aquí tienes las mejores promociones del día para ti:"

        self._agregar_mensaje_bot(texto_respuesta)
