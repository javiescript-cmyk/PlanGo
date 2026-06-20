
import tkinter as tk
from tkinter import ttk
from chat import SalaChatTemporal
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
    COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_RAYO_YELLOW, COLOR_ESCUDO_RED,
<<<<<<< Updated upstream
    get_db_connection, configurar_animacion_boton
=======
    COLOR_NAV, COLOR_CORAL_FUEGO, cargar_datos, guardar_datos, configurar_animacion_boton,
    base_datos_global
>>>>>>> Stashed changes
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
        self.sync_after_id = None
        
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

<<<<<<< Updated upstream
        mini_canvas = tk.Canvas(frame_sidebar, width=160, height=70, bg="#1A1A1A", bd=0, highlightthickness=0)
        mini_canvas.pack(pady=(15, 5))
        
        pts = [30, 10, 130, 10, 115, 45, 80, 65, 45, 45]
        mini_canvas.create_polygon(pts, fill=COLOR_ESCUDO_RED, outline="#800A12", width=1)
        mini_canvas.create_text(80, 30, text="2x1", font=("Arial Black", 16, "bold"), fill=COLOR_TEXT_MAIN)
        mini_canvas.create_text(80, 48, text="PROMO", font=("Arial Black", 7, "bold"), fill=COLOR_TEXT_MAIN)
        mini_canvas.create_polygon([48, 45, 112, 45, 105, 62, 55, 62], fill=COLOR_TEXT_MAIN, outline="#CCCCCC", width=1)
        mini_canvas.create_text(80, 53, text="Two Pack", font=("Georgia", 8, "bold", "italic"), fill=COLOR_ESCUDO_RED)

        tk.Frame(frame_sidebar, bg="#2D2D2D", height=1).pack(fill="x", padx=15, pady=(5, 15))

        tk.Label(frame_sidebar, text="MENÚ PRINCIPAL", font=("Helvetica", 7, "bold"), bg="#1A1A1A", fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 8))
=======
        # Marco principal que ocupa todo menos la nav bar
        self.frame_contenido = tk.Frame(self, bg=COLOR_BG)
        self.frame_contenido.pack(fill="both", expand=True, side="top")

        # Barra de navegación inferior fija
        self._crear_nav_inferior()

        # Mostrar pantalla inicial
        self.mostrar_inicio()

    def _crear_nav_inferior(self):
        self.nav_bar = tk.Frame(self, bg=COLOR_NAV, height=62)
        self.nav_bar.pack(fill="x", side="bottom")
        self.nav_bar.pack_propagate(False)

        # Separador superior de la nav bar
        tk.Frame(self.nav_bar, bg="#2D2D2D", height=1).pack(fill="x", side="top")

        frame_btns = tk.Frame(self.nav_bar, bg=COLOR_NAV)
        frame_btns.pack(fill="both", expand=True)
>>>>>>> Stashed changes

        nav_items = [
            ("🏠", "Inicio",  "inicio"),
            ("🗺️",  "Mapa",    "mapa"),
            ("🤝",  "Match",   "match"),
            ("💬",  "Chat",    "chat_tab"),
            ("👤",  "Perfil",  "perfil"),
        ]

        self.nav_botones = {}
<<<<<<< Updated upstream
        for texto, seccion in nav_items:
            btn = tk.Button(frame_sidebar, text=texto, font=("Helvetica", 10), bg="#1A1A1A", fg=COLOR_TEXT_MAIN, bd=0, anchor="w", padx=20, pady=6, cursor="hand2", activebackground=COLOR_ACCENT_RED, activeforeground=COLOR_TEXT_MAIN, command=lambda s=seccion: self.navegar_a(s))
            btn.pack(fill="x", pady=1)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2D2D2D"))
            btn.bind("<Leave>", lambda e, b=btn, s=seccion: b.config(bg=COLOR_ACCENT_RED if self.seccion_actual == s else "#1A1A1A"))
            self.nav_botones[seccion] = btn

        if "inicio" in self.nav_botones:
            self.nav_botones["inicio"].config(bg=COLOR_ACCENT_RED)

        lbl_user = tk.Label(frame_sidebar, text=f"👤 {self.usuario_actual['nombre']}", font=("Helvetica", 10, "bold"), bg="#1A1A1A", fg=COLOR_TEXT_MAIN)
        lbl_user.pack(pady=(20, 10))

        btn_cerrar = tk.Button(frame_sidebar, text="🚪 Cerrar Sesión", font=("Helvetica", 10, "bold"), bg="#2A1B1D", fg="#E74C3C", bd=0, cursor="hand2", command=self.al_cerrar_sesion)
        btn_cerrar.pack(side="bottom", fill="x", pady=10)
        configurar_animacion_boton(btn_cerrar, "#2A1B1D", COLOR_ACCENT_RED, COLOR_RED_ACTIVE)

        self.frame_principal = tk.Frame(self, bg=COLOR_BG)
        self.frame_principal.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.mostrar_catalogo_matchmaker()

    def _iniciar_sincronizacion(self):
        try:
            if self.seccion_actual in ["inicio", "explorar", "match"]:
                if (hasattr(self, 'scrollable_frame') and hasattr(self, 'cb_categoria') and self.scrollable_frame.winfo_exists() and self.cb_categoria.winfo_exists()):
                    self.actualizar_catalogo()
        except Exception:
            pass
        
        try:
            self.sync_after_id = self.after(5000, self._iniciar_sincronizacion)
        except Exception:
            pass
=======
        for icono, texto, seccion in nav_items:
            col = tk.Frame(frame_btns, bg=COLOR_NAV)
            col.pack(side="left", fill="both", expand=True)

            # Botón central Match más grande y rojo
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
>>>>>>> Stashed changes

    def navegar_a(self, seccion):
        self.seccion_actual = seccion
        # Actualizar colores nav
        for s, btn in self.nav_botones.items():
            if s == "match":
                continue
            color = COLOR_ACCENT_RED if s == seccion else COLOR_TEXT_MUTED
            btn.config(fg=color)
        # Limpiar contenido
        for w in self.frame_contenido.winfo_children():
            w.destroy()
        # Enrutar
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

        # ── HEADER ROJO ──────────────────────────────
        header = tk.Frame(f, bg=COLOR_ESCUDO_RED, height=115)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Fila logo + íconos
        f1 = tk.Frame(header, bg=COLOR_ESCUDO_RED)
        f1.pack(fill="x", padx=14, pady=(10, 2))

        tk.Label(f1, text="Two Pack",
                 font=("Georgia", 20, "bold", "italic"),
                 bg=COLOR_ESCUDO_RED,
                 fg=COLOR_TEXT_MAIN).pack(side="left")

        tk.Label(f1, text="🔔  ☰",
                 font=("Helvetica", 13),
                 bg=COLOR_ESCUDO_RED,
                 fg=COLOR_TEXT_MAIN).pack(side="right")

        # Fila ubicación + badge IA
        f2 = tk.Frame(header, bg=COLOR_ESCUDO_RED)
        f2.pack(fill="x", padx=14, pady=(0, 6))

        u = self.usuario_actual
        zona = u.get("zona_preferida", "Campus UCATEC / Zona Norte")
        tk.Label(f2, text=f"📍 {zona}",
                 font=("Helvetica", 8),
                 bg=COLOR_ESCUDO_RED,
                 fg="#FFCCCC").pack(side="left")

<<<<<<< Updated upstream
        tk.Label(self.frame_principal, text="Mi Perfil Two Pack", font=("Helvetica", 18, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        tk.Label(self.frame_principal, text="Tu identidad en el ecosistema urbano de Cochabamba", font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(0, 20))
=======
        tk.Label(f2,
                 text=" ⚡ IA MATCHMAKER ACTIVO ",
                 font=("Helvetica", 7, "bold"),
                 bg="#FF4400",
                 fg=COLOR_TEXT_MAIN).pack(side="right")
>>>>>>> Stashed changes

        # Barra búsqueda blanca
        f3 = tk.Frame(header, bg=COLOR_ESCUDO_RED)
        f3.pack(fill="x", padx=14, pady=(0, 8))

<<<<<<< Updated upstream
        col_izq = tk.Frame(frame_body, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D", width=220)
        col_izq.pack(side="left", fill="y", padx=(0, 15))
        col_izq.pack_propagate(False)

        canvas_av = tk.Canvas(col_izq, width=90, height=90, bg=COLOR_CARD, bd=0, highlightthickness=0)
        canvas_av.pack(pady=(25, 10))
        canvas_av.create_oval(5, 5, 85, 85, fill=COLOR_ACCENT_RED, outline="")
        inicial = u.get('nombre', 'U')[0].upper()
        canvas_av.create_text(45, 45, text=inicial, font=("Helvetica", 36, "bold"), fill=COLOR_TEXT_MAIN)

        tk.Label(col_izq, text=u.get('nombre', 'Usuario'), font=("Helvetica", 13, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, wraplength=190, justify="center").pack()

        tk.Label(col_izq, text=u.get('genero', 'No especificado'), font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=(3, 0))

        estado = 'Activo'
        color_estado = COLOR_SUCCESS if estado == 'Activo' else COLOR_ACCENT_RED
        tk.Label(col_izq, text=f"● {estado}", font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=color_estado).pack(pady=(5, 20))

        tk.Frame(col_izq, bg="#2D2D2D", height=1).pack(fill="x", padx=15, pady=(0, 15))

        stats = [
            ("⭐", str(u.get('confianza', 5.0)), "Puntuación"),
            ("🤝", "0", "Matches"),
            ("🚫", "0", "Reportes"),
        ]
        for icono, valor, etiqueta in stats:
            frame_stat = tk.Frame(col_izq, bg=COLOR_CARD)
            frame_stat.pack(fill="x", padx=15, pady=4)
            tk.Label(frame_stat, text=f"{icono}  {valor}", font=("Helvetica", 13, "bold"), bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW, anchor="w").pack(side="left")
            tk.Label(frame_stat, text=etiqueta, font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="e").pack(side="right")
=======
        barra = tk.Frame(f3, bg="#FFFFFF")
        barra.pack(fill="x")

        tk.Label(barra, text="🔍",
                 bg="#FFFFFF", fg="#999999",
                 font=("Helvetica", 10)).pack(
                 side="left", padx=(8, 2), pady=5)

        self.ent_busq = tk.Entry(
            barra, font=("Helvetica", 9),
            bg="#FFFFFF", fg="#999999",
            bd=0, insertbackground="#333")
        self.ent_busq.insert(0, "Buscar promociones, lugares o actividades...")
        self.ent_busq.pack(side="left", fill="x", expand=True, ipady=6)

        tk.Label(barra, text="⚙",
                 bg="#FFFFFF", fg=COLOR_ESCUDO_RED,
                 font=("Helvetica", 12)).pack(
                 side="right", padx=8)

        # ── CHIPS DE CATEGORÍA ───────────────────────
        frame_chips = tk.Frame(f, bg=COLOR_BG)
        frame_chips.pack(fill="x", padx=10, pady=8)

        chips = [
            ("🍔 Gastronomía",    "Gastronomía"),
            ("🎬 Entretenimiento","Entretenimiento"),
            ("💪 Bienestar",      "Deportes / Bienestar"),
            ("🎵 Eventos",        "Eventos / Conciertos"),
            ("🛍️ Tiendas",        "Otros"),
        ]
        self.chip_activo = "Gastronomía"
        self.chip_btns = {}
>>>>>>> Stashed changes

        for txt, val in chips:
            activo = val == self.chip_activo
            b = tk.Button(
                frame_chips, text=txt,
                font=("Helvetica", 7, "bold"),
                bg=COLOR_ACCENT_RED if activo else "#2A2A2A",
                fg=COLOR_TEXT_MAIN,
                bd=0, cursor="hand2",
                padx=10, pady=5, relief="flat",
                command=lambda v=val: self._chip_click(v)
            )
            b.pack(side="left", padx=3)
            self.chip_btns[val] = b

<<<<<<< Updated upstream
        card_datos = tk.Frame(col_der, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
        card_datos.pack(fill="x", pady=(0, 15))

        tk.Label(card_datos, text="INFORMACIÓN DE CUENTA", font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=20, pady=(15, 10))
=======
        # ── TÍTULO SECCIÓN ───────────────────────────
        ft = tk.Frame(f, bg=COLOR_BG)
        ft.pack(fill="x", padx=14, pady=(4, 2))

        tk.Label(ft,
                 text="Cartelera Inteligente de Anuncios 2x1",
                 font=("Helvetica", 11, "bold"),
                 bg=COLOR_BG,
                 fg=COLOR_TEXT_MAIN).pack(side="left")
>>>>>>> Stashed changes

        tk.Label(ft, text="🔥 Ver más",
                 font=("Helvetica", 8, "bold"),
                 bg=COLOR_BG,
                 fg=COLOR_ACCENT_RED).pack(side="right")

<<<<<<< Updated upstream
        campos_editables = [
            ("NOMBRE COMPLETO", 'nombre'),
            ("UNIVERSIDAD / INSTITUCIÓN", 'universidad'),
            ("GÉNERO", 'genero'),
        ]
        for label_txt, clave in campos_editables:
            tk.Label(card_datos, text=label_txt, font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=20, pady=(6, 2))
            en = tk.Entry(card_datos, font=("Helvetica", 11), bg="#2D2D2D", fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#3D3D3D")
            en.insert(0, u.get(clave, ''))
            en.pack(fill="x", padx=20, ipady=6, pady=(0, 6))
            self.entradas_perfil[clave] = en

        btn_guardar = tk.Button(card_datos, text="💾  Guardar cambios de perfil", font=("Helvetica", 10, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=self.guardar_perfil)
        btn_guardar.pack(fill="x", padx=20, ipady=9, pady=15)
        configurar_animacion_boton(btn_guardar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")

        card_seg = tk.Frame(col_der, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
        card_seg.pack(fill="x")

        tk.Label(card_seg, text="🔒  SEGURIDAD DE CUENTA", font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW).pack(anchor="w", padx=20, pady=(15, 8))
        tk.Label(card_seg, text="Tu correo universitario garantiza la autenticidad\nde tu perfil dentro del ecosistema Two Pack.\nLos perfiles verificados tienen mayor prioridad\nen el algoritmo de emparejamiento.", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, justify="left").pack(anchor="w", padx=20, pady=(0, 15))

    def guardar_perfil(self):
        messagebox.showinfo("Perfil actualizado ✓", f"Los datos de {self.usuario_actual['nombre']} han sido guardados correctamente.")

    def mostrar_detalle_promo(self, promo):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        btn_volver = tk.Button(self.frame_principal, text="← Volver al catálogo", font=("Helvetica", 9), bg=COLOR_BG, fg=COLOR_TEXT_MUTED, bd=0, cursor="hand2", command=self.mostrar_catalogo_matchmaker)
        btn_volver.pack(anchor="w", pady=(0, 15))
        btn_volver.bind("<Enter>", lambda e: btn_volver.config(fg=COLOR_ACCENT_RED))
        btn_volver.bind("<Leave>", lambda e: btn_volver.config(fg=COLOR_TEXT_MUTED))

        frame_header = tk.Frame(self.frame_principal, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
        frame_header.pack(fill="x", pady=(0, 15))

        tk.Label(frame_header, text="  2x1  ", font=("Helvetica", 10, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN).pack(anchor="ne", padx=15, pady=(15, 0))

        tk.Label(frame_header, text=promo['titulo'], font=("Helvetica", 16, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, wraplength=600, justify="left").pack(anchor="w", padx=20, pady=(10, 5))

        tk.Label(frame_header, text=f"📂  {promo['categoria']}", font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 15))

        frame_cuerpo = tk.Frame(self.frame_principal, bg=COLOR_BG)
        frame_cuerpo.pack(fill="both", expand=True)

        col_info = tk.Frame(frame_cuerpo, bg=COLOR_BG)
        col_info.pack(side="left", fill="both", expand=True, padx=(0, 15))

        card_info = tk.Frame(col_info, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
        card_info.pack(fill="x", pady=(0, 15))

        tk.Label(card_info, text="DETALLES DE LA PROMOCIÓN", font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=20, pady=(15, 10))

        detalles = [
            ("📅 Fecha Inicio", promo.get('fecha_inicio', '—').strftime("%d/%m/%Y") if promo.get('fecha_inicio') else '—'),
            ("📅 Fecha Fin", promo.get('fecha_fin', '—').strftime("%d/%m/%Y") if promo.get('fecha_fin') else '—'),
        ]
        for etiqueta, valor in detalles:
            fila = tk.Frame(card_info, bg=COLOR_CARD)
            fila.pack(fill="x", padx=20, pady=5)
            tk.Label(fila, text=etiqueta, font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, width=26, anchor="w").pack(side="left")
            tk.Label(fila, text=valor, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, anchor="w").pack(side="left")

        tk.Frame(card_info, bg="#2D2D2D", height=1).pack(fill="x", padx=20, pady=10)

        tk.Label(card_info, text="DESCRIPCIÓN COMPLETA", font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 6))

        desc_text = promo.get('descripcion', '')
        tk.Label(card_info, text=desc_text, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, wraplength=380, justify="left").pack(anchor="w", padx=20, pady=(0, 20))

        col_accion = tk.Frame(frame_cuerpo, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D", width=280)
        col_accion.pack(side="right", fill="y")
        col_accion.pack_propagate(False)

        tk.Label(col_accion, text="⚡", font=("Helvetica", 28), bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW).pack(pady=(25, 0))

        tk.Label(col_accion, text="ACTIVAR MATCH", font=("Helvetica", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(pady=5)

        tk.Label(col_accion, text="Selecciona tu disponibilidad\ny encuentra tu compañero", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, justify="center").pack(pady=(0, 20))

        tk.Frame(col_accion, bg="#2D2D2D", height=1).pack(fill="x", padx=20, pady=(0, 15))

        tk.Label(col_accion, text="DESDE LAS", font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 3))
        cb_desde_det = ttk.Combobox(col_accion, values=[str(i) for i in range(8, 24)], state="readonly", width=10)
        cb_desde_det.pack(padx=20, anchor="w", pady=(0, 10))
        cb_desde_det.set("12")

        tk.Label(col_accion, text="HASTA LAS", font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 3))
        cb_hasta_det = ttk.Combobox(col_accion, values=[str(i) for i in range(8, 24)], state="readonly", width=10)
        cb_hasta_det.pack(padx=20, anchor="w", pady=(0, 20))
        cb_hasta_det.set("14")

        btn_match_det = tk.Button(col_accion, text="🤝  Quiero este 2x1", font=("Helvetica", 11, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=lambda: self._activar_match_desde_detalle(promo, cb_desde_det, cb_hasta_det))
        btn_match_det.pack(fill="x", padx=20, ipady=12, pady=(0, 15))
        configurar_animacion_boton(btn_match_det, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        tk.Label(col_accion, text="🔒 Encuentro seguro en el local", font=("Helvetica", 8), bg=COLOR_CARD, fg=COLOR_SUCCESS).pack()

    def _activar_match_desde_detalle(self, promo, cb_desde, cb_hasta):
        self.promo_seleccionada = promo
        self.mostrar_catalogo_matchmaker()
        self.cb_desde.set(cb_desde.get())
        self.cb_hasta.set(cb_hasta.get())
        self.after(300, self.ejecutar_matchmaking)

    def mostrar_historial(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        tk.Label(self.frame_principal, text="Mis Matches Two Pack", font=("Helvetica", 18, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        tk.Label(self.frame_principal, text="Historial de experiencias compartidas en Cochabamba", font=("Helvetica", 10), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(0, 20))

        conn = get_db_connection()
        historial = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT m.id, p.titulo, m.fecha_match
                    FROM twopack_matches m
                    JOIN promociones p ON m.promocion_id = p.id
                    WHERE m.usuario_1_id = %s OR m.usuario_2_id = %s
                    ORDER BY m.fecha_match DESC
                """, (self.usuario_actual['id'], self.usuario_actual['id']))
                historial = cursor.fetchall()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                conn.close()

        if not historial:
            tk.Label(self.frame_principal, text="🤝  Aún no tienes matches.\n¡Explora las promos y activa tu primer Two Pack Match!", font=("Helvetica", 12), bg=COLOR_BG, fg=COLOR_TEXT_MUTED, justify="center").pack(expand=True)
            return

        canvas_h = tk.Canvas(self.frame_principal, bg=COLOR_BG, bd=0, highlightthickness=0)
        scroll_h = ttk.Scrollbar(self.frame_principal, orient="vertical", command=canvas_h.yview)
        frame_lista = tk.Frame(canvas_h, bg=COLOR_BG)
        frame_lista.bind("<Configure>", lambda e: canvas_h.configure(scrollregion=canvas_h.bbox("all")))
        canvas_h.create_window((0, 0), window=frame_lista, anchor="nw")
        canvas_h.configure(yscrollcommand=scroll_h.set)
        canvas_h.pack(side="left", fill="both", expand=True)
        scroll_h.pack(side="right", fill="y")

        for match in historial:
            card_m = tk.Frame(frame_lista, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
            card_m.pack(fill="x", pady=8)

            frame_mh = tk.Frame(card_m, bg=COLOR_CARD)
            frame_mh.pack(fill="x", padx=20, pady=(15, 8))

            tk.Label(frame_mh, text=match['titulo'], font=("Helvetica", 11, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, anchor="w").pack(fill="x")
            tk.Label(frame_mh, text=match['fecha_match'].strftime("%d/%m/%Y %H:%M"), font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(fill="x")

    def mostrar_catalogo_matchmaker(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        frame_catalogo = tk.Frame(self.frame_principal, bg=COLOR_BG)
        frame_catalogo.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(frame_catalogo, text="🎁 CATÁLOGO DE DESCUENTOS 2x1", font=("Helvetica", 14, "bold"), bg=COLOR_BG, fg=COLOR_RAYO_YELLOW).pack(anchor="w", pady=(0, 10))

        frame_filtros = tk.Frame(frame_catalogo, bg=COLOR_BG)
        frame_filtros.pack(fill="x", pady=(0, 15))

        tk.Label(frame_filtros, text="Categoría:", font=("Helvetica", 9, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 5))
        self.cb_categoria = ttk.Combobox(frame_filtros, values=["Todas"], state="readonly", width=20)
        self.cb_categoria.pack(side="left")
        self.cb_categoria.set("Todas")
        self.cb_categoria.bind("<<ComboboxSelected>>", lambda e: self.actualizar_catalogo())
        
        self.cargar_categorias()

        frame_scroll = tk.Frame(frame_catalogo, bg=COLOR_BG)
        frame_scroll.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(frame_scroll, bg=COLOR_BG, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLOR_BG)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
=======
        tk.Label(f,
                 text="Promociones reales. 100% Gratis para todos.",
                 font=("Helvetica", 8),
                 bg=COLOR_BG,
                 fg=COLOR_TEXT_MUTED).pack(
                 anchor="w", padx=14, pady=(0, 6))

        # ── GRID DE TARJETAS 2 COLUMNAS ──────────────
        frame_scroll = tk.Frame(f, bg=COLOR_BG)
        frame_scroll.pack(fill="both", expand=True)

        self.canvas_cards = tk.Canvas(
            frame_scroll, bg=COLOR_BG,
            bd=0, highlightthickness=0)
        sb = ttk.Scrollbar(
            frame_scroll, orient="vertical",
            command=self.canvas_cards.yview)
        self.frame_grid = tk.Frame(
            self.canvas_cards, bg=COLOR_BG)
        self.frame_grid.bind(
            "<Configure>",
            lambda e: self.canvas_cards.configure(
                scrollregion=self.canvas_cards.bbox("all")))
        self.canvas_cards.create_window(
            (0, 0), window=self.frame_grid, anchor="nw")
        self.canvas_cards.configure(yscrollcommand=sb.set)
        self.canvas_cards.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
>>>>>>> Stashed changes

        self._renderizar_grid()

        # Banner inferior
        banner = tk.Frame(f, bg=COLOR_ACCENT_RED, height=32)
        banner.pack(fill="x", side="bottom")
        banner.pack_propagate(False)
        tk.Label(banner, text="Two Pack: Tu ciudad, tus planes, tu mejor match.", font=("Helvetica", 8, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN).pack(expand=True, pady=8)

<<<<<<< Updated upstream
        frame_matchmaker = tk.Frame(self.frame_principal, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D", width=380)
        frame_matchmaker.pack(side="right", fill="y")
        frame_matchmaker.pack_propagate(False)

        lbl_icon = tk.Label(frame_matchmaker, text="⚡", font=("Helvetica", 28), bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW)
        lbl_icon.pack(pady=(20, 0))

        lbl_titulo = tk.Label(frame_matchmaker, text="MOTOR MATCHMAKER IA", font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN)
        lbl_titulo.pack(pady=5)

        lbl_sub = tk.Label(frame_matchmaker, text="Cochabamba Ciudad Inteligente", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED)
        lbl_sub.pack(pady=(0, 20))

        self.lbl_promo_seleccionada = tk.Label(frame_matchmaker, text="❌ No hay promoción seleccionada", font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=340)
        self.lbl_promo_seleccionada.pack(pady=(0, 15))
=======
    def _chip_click(self, val):
        self.chip_activo = val
        self.filtro_categoria = val
        for v, b in self.chip_btns.items():
            b.config(bg=COLOR_ACCENT_RED if v == val else "#2A2A2A")
        self._renderizar_grid()

    def _renderizar_grid(self):
        for w in self.frame_grid.winfo_children():
            w.destroy()
        self.tarjetas = []

        promos = [
            p for p in base_datos_global["promociones"]
            if self.filtro_categoria == "Todas"
            or p.get("cat") == self.filtro_categoria
        ]

        for i, promo in enumerate(promos):
            fila = i // 2
            col  = i % 2
            card = self._crear_card_foto(self.frame_grid, promo)
            card.grid(row=fila, column=col, padx=6, pady=6, sticky="nsew")
            self.frame_grid.grid_columnconfigure(col, weight=1, minsize=180)
            self.tarjetas.append(card)

    def _crear_card_foto(self, parent, promo):
        FOTO_CONFIG = {
            "Gastronomía": ("#5C1010","#CC3300","#FF6633","🍔"),
            "Pubs / Discotecas": ("#0D0D40","#1A1AFF","#6666FF","🍺"),
            "Cafeterías": ("#0D300D","#006600","#33CC33","☕"),
            "Entretenimiento": ("#0A0A40","#000099","#3333FF","🎬"),
            "Deportes / Bienestar": ("#300D30","#660066","#CC33CC","💪"),
            "Eventos / Conciertos": ("#3D1A00","#993300","#FF6600","🎵"),
            "Tiendas Locales": ("#1A1A1A","#333333","#666666","🛍️"),
            "Otros": ("#1A1A1A","#333333","#666666","🛍️"),
        }
        cat = promo.get("cat", "Otros")
        bg1, bg2, bg3, emoji = FOTO_CONFIG.get(cat, FOTO_CONFIG["Otros"])
>>>>>>> Stashed changes

        card = tk.Frame(parent, bg=COLOR_CARD, highlightthickness=0)

<<<<<<< Updated upstream
        tk.Label(frame_campos, text="TU VENTANA TEMPORAL DE DISPONIBILIDAD", font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        frame_horas = tk.Frame(frame_campos, bg=COLOR_CARD)
        frame_horas.pack(fill="x", pady=(0, 12))

        tk.Label(frame_horas, text="Desde:", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.cb_desde = ttk.Combobox(frame_horas, values=[str(i) for i in range(8, 24)], width=5, state="readonly")
        self.cb_desde.pack(side="left", padx=(0, 15))
        self.cb_desde.set("12")

        tk.Label(frame_horas, text="Hasta:", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.cb_hasta = ttk.Combobox(frame_horas, values=[str(i) for i in range(8, 24)], width=5, state="readonly")
        self.cb_hasta.pack(side="left")
        self.cb_hasta.set("14")

        self.check_genero_var = tk.BooleanVar(value=False)
        chk_genero = tk.Checkbutton(frame_campos, text="Activar restricción de seguridad (Match solo con mi mismo género)", variable=self.check_genero_var, font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, activebackground=COLOR_CARD, activeforeground=COLOR_RAYO_YELLOW, selectcolor=COLOR_BG, bd=0)
        chk_genero.pack(anchor="w", pady=(10, 25))

        self.btn_match = tk.Button(frame_matchmaker, text="🤝 Quiero aprovechar este 2x1", font=("Helvetica", 11, "bold"), bg="#333333", fg=COLOR_TEXT_MUTED, bd=0, cursor="hand2", state="disabled", command=self.ejecutar_matchmaking)
        self.btn_match.pack(fill="x", padx=25, ipady=12, pady=(0, 15))

        self.lbl_status = tk.Label(frame_matchmaker, text="Sistema Matchmaker listo. Selecciona una promoción!", font=("Helvetica", 9, "italic"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=340)
        self.lbl_status.pack(pady=(0, 15))

    def cargar_categorias(self):
        conn = get_db_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM categorias ORDER BY nombre")
            categorias = cursor.fetchall()
            self.cb_categoria['values'] = ["Todas"] + [cat['nombre'] for cat in categorias]
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    def crear_tarjeta_promo(self, parent, promo):
        frame_tarjeta = tk.Frame(parent, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#3D3D3D", padx=0, pady=0)

        banda = tk.Frame(frame_tarjeta, bg=COLOR_ESCUDO_RED, height=6)
        banda.pack(fill="x")

        inner = tk.Frame(frame_tarjeta, bg=COLOR_CARD, padx=15, pady=12)
        inner.pack(fill="x")

        fila_top = tk.Frame(inner, bg=COLOR_CARD)
        fila_top.pack(fill="x", pady=(0, 6))

        tk.Label(fila_top, text=" 2x1  ", font=("Helvetica", 8, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 8))

        tk.Label(fila_top, text=promo.get('categoria', ''), font=("Helvetica", 8), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(side="left")

        tk.Label(inner, text=promo['titulo'], font=("Helvetica", 11, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, wraplength=320, justify="left", anchor="w").pack(anchor="w", pady=(0, 4))

        tk.Frame(inner, bg="#2D2D2D", height=1).pack(fill="x", pady=(4, 10))

        fila_bot = tk.Frame(inner, bg=COLOR_CARD)
        fila_bot.pack(fill="x")

        tk.Label(fila_bot, text=f"📅  Vence: {promo['fecha_fin'].strftime('%d/%m/%Y')}", font=("Helvetica", 8), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(side="left")

        btn_sel = tk.Button(fila_bot, text="Ver detalle →", font=("Helvetica", 9, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=10, pady=4, command=lambda p=promo, f=frame_tarjeta: (self.seleccionar_promo(p, f), self.mostrar_detalle_promo(p)))
        btn_sel.pack(side="right")
        configurar_animacion_boton(btn_sel, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        frame_tarjeta.btn_seleccionar = btn_sel
        frame_tarjeta.promo = promo

        return frame_tarjeta

    def seleccionar_promo(self, promo, frame_tarjeta):
        for tarjeta in self.tarjetas:
            tarjeta.configure(highlightbackground="#3D3D3D", highlightthickness=1)
            tarjeta.btn_seleccionar.config(bg="#2D2D2D", text="✅ Seleccionar")
        
        frame_tarjeta.configure(highlightbackground=COLOR_ACCENT_RED, highlightthickness=2)
        frame_tarjeta.btn_seleccionar.config(bg=COLOR_ACCENT_RED, text="✓ SELECCIONADA")
        self.promo_seleccionada = promo
        
        self.lbl_promo_seleccionada.config(text=f"📌 {promo['titulo']}", fg=COLOR_RAYO_YELLOW)
        self.btn_match.config(state="normal", bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN)
        self.lbl_status.config(text="Promoción seleccionada! Ingresa tu disponibilidad.")
        configurar_animacion_boton(self.btn_match, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def actualizar_catalogo(self):
        try:
            if not hasattr(self, 'scrollable_frame') or not self.scrollable_frame.winfo_exists():
                return
                
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self.tarjetas = []
            
            filtro_categoria = self.cb_categoria.get()
            
            conn = get_db_connection()
            promos = []
            if conn:
                try:
                    cursor = conn.cursor()
                    if filtro_categoria == "Todas":
                        cursor.execute("""
                            SELECT p.id, p.titulo, c.nombre as categoria, p.descripcion, p.fecha_inicio, p.fecha_fin
                            FROM promociones p
                            JOIN categorias c ON p.categoria_id = c.id
                            WHERE p.estado = 'activa'
                            ORDER BY p.fecha_creacion DESC
                        """)
                    else:
                        cursor.execute("""
                            SELECT p.id, p.titulo, c.nombre as categoria, p.descripcion, p.fecha_inicio, p.fecha_fin
                            FROM promociones p
                            JOIN categorias c ON p.categoria_id = c.id
                            WHERE p.estado = 'activa' AND c.nombre = %s
                            ORDER BY p.fecha_creacion DESC
                        """, (filtro_categoria,))
                    promos = cursor.fetchall()
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    conn.close()
            
            for promo in promos:
                tarjeta = self.crear_tarjeta_promo(self.scrollable_frame, promo)
                tarjeta.pack(fill="x", pady=8)
                self.tarjetas.append(tarjeta)
            
            if self.promo_seleccionada:
                for tarjeta in self.tarjetas:
                    if tarjeta.promo['id'] == self.promo_seleccionada['id']:
                        self.seleccionar_promo(tarjeta.promo, tarjeta)
                        break
        except Exception:
            pass

    def ejecutar_matchmaking(self):
        if not self.promo_seleccionada:
            messagebox.showwarning("Promoción requerida", "Por favor selecciona una promoción primero!")
            return
            
        self.lbl_status.config(text="🤖 Escaneando base de datos urbana en tiempo real...", fg=COLOR_RAYO_YELLOW)
        self.btn_match.config(state="disabled", bg="#444444", text="Procesando algoritmo...")
        
        self.after(1500, self._procesar_match_resultado)
    
    def _procesar_match_resultado(self):
        desde = int(self.cb_desde.get())
        hasta = int(self.cb_hasta.get())
=======
        # ── FOTO SIMULADA (canvas con gradiente de color) ──
        canvas_foto = tk.Canvas(card, width=180, height=110, bg=bg1, bd=0, highlightthickness=0)
        canvas_foto.pack(fill="x")

        # Fondo degradado simulado con rectángulos
        canvas_foto.create_rectangle(0, 0, 180, 55, fill=bg1, outline="")
        canvas_foto.create_rectangle(0, 55, 180, 110, fill=bg2, outline="")

        # Emoji grande central (simula foto de comida/lugar)
        canvas_foto.create_text(90, 50, text=emoji, font=("Helvetica", 36))

        # Badge 2x1 arriba izquierda
        canvas_foto.create_rectangle(8, 8, 48, 28, fill=COLOR_ACCENT_RED, outline="")
        canvas_foto.create_text(28, 18, text="2x1", font=("Helvetica", 9, "bold"), fill=COLOR_TEXT_MAIN)

        # Badge demanda arriba derecha
        demanda = promo.get("demanda", "Alta Demanda")
        canvas_foto.create_rectangle(90, 8, 175, 28, fill="#FF6600", outline="")
        canvas_foto.create_text(132, 18, text=f"🔥 {demanda}", font=("Helvetica", 7, "bold"), fill=COLOR_TEXT_MAIN)

        # ── INFO DEBAJO DE LA FOTO ──────────────────
        info = tk.Frame(card, bg=COLOR_CARD, padx=8, pady=6)
        info.pack(fill="x")

        # Nombre del comercio (simula nombre real)
        comercio_nombre = promo.get("comercio", promo["titulo"].split()[0] + " Local")
        tk.Label(info, text=comercio_nombre, font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, anchor="w").pack(anchor="w")

        # Subtítulo
        tk.Label(info, text=promo["titulo"], font=("Helvetica", 8), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w", wraplength=165).pack(anchor="w")

        # Distancia y horario
        dist = promo.get("distancia", "800 m")
        hora = promo.get("hora_hasta", "23:00")
        tk.Label(info, text=f"📍 {dist}   🕐 Hasta {hora}", font=("Helvetica", 7), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(anchor="w", pady=(2, 6))

        # Botón Encontrar Compañero
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
        configurar_animacion_boton(btn, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        return card

    def mostrar_mapa(self):
        f = self.frame_contenido

        # Header
        header = tk.Frame(f, bg=COLOR_NAV, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
>>>>>>> Stashed changes

        tk.Label(header, text="←",
                 font=("Helvetica", 16),
                 bg=COLOR_NAV,
                 fg=COLOR_TEXT_MAIN).pack(
                 side="left", padx=15, pady=10)
        tk.Label(header,
                 text="Mapa de Promociones",
                 font=("Helvetica", 12, "bold"),
                 bg=COLOR_NAV,
                 fg=COLOR_TEXT_MAIN).pack(
                 side="left")
        tk.Label(header, text="⚙",
                 font=("Helvetica", 14),
                 bg=COLOR_NAV,
                 fg=COLOR_TEXT_MAIN).pack(
                 side="right", padx=15)

<<<<<<< Updated upstream
        self.match_encontrado = {
            'usuario': 'Usuario Compañero',
            'genero': 'No especificado'
        }
=======
        # Canvas del mapa simulado
        canvas_mapa = tk.Canvas(
            f, bg="#1A2A1A",
            bd=0, highlightthickness=0)
        canvas_mapa.pack(fill="both", expand=True)
>>>>>>> Stashed changes

        # Cuadrícula de calles
        for i in range(0, 500, 35):
            canvas_mapa.create_line(i, 0, i, 600, fill="#2A3A2A", width=1)
        for j in range(0, 700, 35):
            canvas_mapa.create_line(0, j, 500, j, fill="#2A3A2A", width=1)

<<<<<<< Updated upstream
        if self.match_encontrado:
            self.lbl_status.config(text="¡MATCH LOGRADO EXITOSAMENTE! 🎉", fg=COLOR_SUCCESS)
            messagebox.showinfo("⚡ ¡Match Two Pack Detectado!", f"¡Felicidades, {self.usuario_actual['nombre']}!\n\nHemos encontrado un compañero compatible!\nSe ha habilitado un chat temporal seguro para coordinar el encuentro.")
            self.mostrar_chat()
        else:
            self.lbl_status.config(text="Sin coincidencias inmediatas. En cola de espera.", fg=COLOR_TEXT_MUTED)
            messagebox.showwarning("Solicitud en Espera", "No hay solicitudes idénticas en este momento.\n\nTu petición se ha quedado registrada de forma inteligente en la cola de la zona. Te notificaremos de inmediato por WhatsApp en cuanto otro estudiante aplique al mismo beneficio.")
=======
        # Calles principales más anchas
        for y in [150, 300, 450]:
            canvas_mapa.create_line(0, y, 500, y, fill="#3A4A3A", width=3)
        for x in [100, 250, 380]:
            canvas_mapa.create_line(x, 0, x, 700, fill="#3A4A3A", width=3)

        # Etiqueta COCHABAMBA
        canvas_mapa.create_text(210, 290, text="COCHABAMBA", font=("Helvetica", 11, "bold"), fill="#4A6A4A")

        # Pins de ubicación de promos
        pins = [
            (160, 120, COLOR_ACCENT_RED, "001"),
            (300, 180, COLOR_ACCENT_RED, "002"),
            (100, 250, "#FF6600", "003"),
            (350, 300, COLOR_ACCENT_RED, "004"),
            (200, 380, "#FF6600", "005"),
            (280, 440, COLOR_ACCENT_RED, "006"),
        ]
        for px, py, color, pid in pins:
            canvas_mapa.create_oval(px-14, py-14, px+14, py+14, fill=color, outline="white", width=2)
            canvas_mapa.create_text(px, py, text="📍", font=("Helvetica", 12))

        # Card flotante de promo seleccionada (abajo)
        frame_card_mapa = tk.Frame(
            f, bg=COLOR_CARD,
            highlightthickness=1,
            highlightbackground="#3D3D3D")
        frame_card_mapa.pack(fill="x", padx=10, pady=8)

        promo_ejemplo = base_datos_global["promociones"][0]

        fila_card = tk.Frame(frame_card_mapa, bg=COLOR_CARD)
        fila_card.pack(fill="x", padx=10, pady=10)

        # Miniatura de color
        mini = tk.Canvas(fila_card, width=56, height=56, bg="#5C1010", bd=0, highlightthickness=0)
        mini.pack(side="left", padx=(0, 10))
        mini.create_text(28, 28, text="🍔", font=("Helvetica", 22))

        # Info promo
        info_mapa = tk.Frame(fila_card, bg=COLOR_CARD)
        info_mapa.pack(side="left", fill="x", expand=True)
        tk.Label(info_mapa, text=promo_ejemplo.get("comercio", promo_ejemplo["titulo"].split()[0]), font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, anchor="w").pack(anchor="w")
        tk.Label(info_mapa, text=promo_ejemplo["titulo"], font=("Helvetica", 8), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(anchor="w")
        tk.Label(info_mapa, text=f"📍 {promo_ejemplo.get('distancia','400 m')} 🕐 Hasta 19:00", font=("Helvetica", 7), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w")

        tk.Label(fila_card, text=" 2x1 ", font=("Helvetica", 9, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN).pack(side="right", padx=5)

    def mostrar_match_panel(self):
        f = self.frame_contenido

        # Header
        header = tk.Frame(f, bg=COLOR_CARD, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="⚡ Motor Matchmaker IA", font=("Helvetica", 13, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(side="left", padx=15, pady=14)

        # Card IA con criterios visuales
        card_ia = tk.Frame(f, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#2D2D2D")
        card_ia.pack(fill="x", padx=12, pady=10)

        tk.Label(card_ia, text="Tu mejor coincidencia", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(10, 8))

        criterios = [
            ("🎯", "Coincidencia Exacta del Anuncio", "Filtro por promo, zona y categoría", 95),
            ("📍", "Proximidad Geográfica Inmediata", "Georreferenciación en Cochabamba", 88),
            ("🕐", "Sincronización de Disponibilidad", "Ventanas de tiempo optimizadas", 90),
        ]

        for icono, titulo, subtitulo, pct in criterios:
            fila = tk.Frame(card_ia, bg=COLOR_CARD)
            fila.pack(fill="x", padx=15, pady=5)

            # Ícono círculo
            c = tk.Canvas(fila, width=36, height=36, bg=COLOR_CARD, bd=0, highlightthickness=0)
            c.pack(side="left", padx=(0, 10))
            c.create_oval(2, 2, 34, 34, fill="#2D2D2D", outline="")
            c.create_text(18, 18, text=icono, font=("Helvetica", 14))

            texto_col = tk.Frame(fila, bg=COLOR_CARD)
            texto_col.pack(side="left", fill="x", expand=True)
            tk.Label(texto_col, text=titulo, font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, anchor="w").pack(anchor="w")
            tk.Label(texto_col, text=subtitulo, font=("Helvetica", 7), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(anchor="w")

            # Barra de progreso
            barra_bg = tk.Frame(texto_col, bg="#2D2D2D", height=4)
            barra_bg.pack(fill="x", pady=(3, 0))
            ancho_pct = int(1.6 * pct)
            barra_fill = tk.Frame(barra_bg, bg=COLOR_ACCENT_RED, height=4, width=ancho_pct)
            barra_fill.pack(side="left")

            tk.Label(fila, text=f"{pct}%", font=("Helvetica", 8, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT_RED).pack(side="right")

        tk.Frame(card_ia, bg="#2D2D2D", height=1).pack(fill="x", padx=15, pady=10)

        # Stats Smart Economy
        tk.Label(card_ia, text="Smart Economy para Todos", font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(anchor="w", padx=15, pady=(0, 8))

        frame_stats = tk.Frame(card_ia, bg=COLOR_CARD)
        frame_stats.pack(fill="x", padx=15, pady=(0, 12))

        stats = [
            ("128", "Ofertas 2x1\nDisponibles"),
            ("42", "Matches\nHoy"),
            ("87", "Comercios\nLocales"),
            ("100%", "Gratis\nTodos"),
        ]
        for valor, etq in stats:
            col = tk.Frame(frame_stats, bg=COLOR_CARD)
            col.pack(side="left", fill="x", expand=True)
            tk.Label(col, text=valor, font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW).pack()
            tk.Label(col, text=etq, font=("Helvetica", 7), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, justify="center").pack()

        # Promo seleccionada
        if self.promo_seleccionada:
            tk.Label(f, text=f"📌 {self.promo_seleccionada['titulo']}", font=("Helvetica", 9, "bold"), bg=COLOR_BG, fg=COLOR_RAYO_YELLOW).pack(padx=12, pady=(8, 4), anchor="w")
        else:
            tk.Label(f, text="← Selecciona una promo en Inicio primero", font=("Helvetica", 9), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(padx=12, pady=(8, 4), anchor="w")
>>>>>>> Stashed changes

        # Horarios
        frame_horas = tk.Frame(f, bg=COLOR_BG)
        frame_horas.pack(fill="x", padx=12, pady=4)

        tk.Label(frame_horas, text="Desde:", font=("Helvetica", 9), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.cb_desde = ttk.Combobox(frame_horas, values=[str(i) for i in range(8, 24)], state="readonly", width=5)
        self.cb_desde.set("12")
        self.cb_desde.pack(side="left", padx=(0, 15))

        tk.Label(frame_horas, text="Hasta:", font=("Helvetica", 9), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.cb_hasta = ttk.Combobox(frame_horas, values=[str(i) for i in range(8, 24)], state="readonly", width=5)
        self.cb_hasta.set("14")
        self.cb_hasta.pack(side="left")

        # Botón principal
        btn_activar = tk.Button(
            f, text="🤝 Activar Two Pack Match Temporal",
            font=("Helvetica", 11, "bold"), bg=COLOR_ACCENT_RED,
            fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", relief="flat",
            command=lambda: self.buscar_match(self.promo_seleccionada)
        )
        btn_activar.pack(fill="x", padx=12, pady=12, ipady=12)
        configurar_animacion_boton(btn_activar, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        # Footer con íconos de propuesta de valor
        frame_footer = tk.Frame(f, bg="#0D0D0D")
        frame_footer.pack(fill="x", pady=(4, 0))

        footer_items = [
            ("💰", "Ahorra dinero\nen cada salida"),
            ("👥", "Conecta con personas\ncon tus mismos planes"),
            ("📍", "Descubre lugares\ncerca de ti"),
            ("⚡", "Aprovecha promociones\nreales y verificadas"),
        ]

        for icono, texto in footer_items:
            col = tk.Frame(frame_footer, bg="#0D0D0D")
            col.pack(side="left", fill="x", expand=True, pady=8)
            tk.Label(col, text=icono, font=("Helvetica", 14), bg="#0D0D0D", fg=COLOR_TEXT_MAIN).pack()
            tk.Label(col, text=texto, font=("Helvetica", 6), bg="#0D0D0D", fg=COLOR_TEXT_MUTED, justify="center").pack()

    def mostrar_chat_vacio(self):
        f = self.frame_contenido

        # Header
        header = tk.Frame(f, bg=COLOR_NAV, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Chats", font=("Helvetica", 14, "bold"), bg=COLOR_NAV, fg=COLOR_TEXT_MAIN).pack(pady=10)

        # Empty state
        empty = tk.Frame(f, bg=COLOR_BG)
        empty.pack(fill="both", expand=True)

        tk.Label(empty, text="💬", font=("Helvetica", 60), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(pady=(150, 10))
        tk.Label(empty, text="No hay chats activos", font=("Helvetica", 12), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack()
        tk.Label(empty, text="Haz un Match para comenzar", font=("Helvetica", 9), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(pady=(5, 0))

    def mostrar_perfil(self):
        f = self.frame_contenido

        # Header
        header = tk.Frame(f, bg=COLOR_ESCUDO_RED, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Mi Perfil", font=("Helvetica", 14, "bold"), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN).pack(pady=(30, 0))

        # Avatar
        avatar_canvas = tk.Canvas(f, width=100, height=100, bg=COLOR_BG, bd=0, highlightthickness=0)
        avatar_canvas.pack(pady=(20, 15))
        avatar_canvas.create_oval(10, 10, 90, 90, fill=COLOR_ACCENT_RED, outline="")
        inicial = self.usuario_actual.get("nombre", "U")[0].upper()
        avatar_canvas.create_text(50, 50, text=inicial, font=("Helvetica", 36, "bold"), fill=COLOR_TEXT_MAIN)

        # Nombre
        tk.Label(f, text=self.usuario_actual.get("nombre", "Usuario"), font=("Helvetica", 14, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(pady=(0, 5))

        # Stats
        frame_stats = tk.Frame(f, bg=COLOR_BG)
        frame_stats.pack(pady=(15, 20))

        stat_data = [
            ("⭐ Confianza", str(self.usuario_actual.get("confianza", 5.0))),
            ("🤝 Matches", str(self.usuario_actual.get("matches", 0))),
            ("🏆 Puntuación", "4.8"),
        ]

        for i, (titulo, valor) in enumerate(stat_data):
            stat_card = tk.Frame(frame_stats, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#3D3D3D", padx=20, pady=15)
            stat_card.pack(side="left", padx=5)
            tk.Label(stat_card, text=valor, font=("Helvetica", 16, "bold"), bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW).pack()
            tk.Label(stat_card, text=titulo, font=("Helvetica", 7), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack()

        # Botón cerrar sesión
        btn_logout = tk.Button(f, text="🚪 Cerrar Sesión", font=("Helvetica", 10, "bold"), bg="#2A1B1D", fg=COLOR_ACCENT_RED, bd=0, cursor="hand2", pady=8, command=self.al_cerrar_sesion)
        btn_logout.pack(fill="x", padx=30, pady=(10, 0))
        configurar_animacion_boton(btn_logout, "#2A1B1D", COLOR_ACCENT_RED, COLOR_RED_ACTIVE)

    def mostrar_historial(self):
        f = self.frame_contenido

        # Header
        header = tk.Frame(f, bg=COLOR_NAV, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Historial", font=("Helvetica", 12, "bold"), bg=COLOR_NAV, fg=COLOR_TEXT_MAIN).pack(pady=10)

        # Historial
        frame_hist = tk.Frame(f, bg=COLOR_BG)
        frame_hist.pack(fill="both", expand=True, padx=14, pady=10)

        historial = base_datos_global.get("historial_matches", [])

        if not historial:
            tk.Label(frame_hist, text="Aún no tienes matches", font=("Helvetica", 12), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(pady=100)
            return

        for match in historial:
            frame_match = tk.Frame(frame_hist, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#3D3D3D", padx=10, pady=10)
            frame_match.pack(fill="x", pady=(0, 8))

            tk.Label(frame_match, text=f"🤝 {match['usuario_match']}", font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, anchor="w").pack(anchor="w")
            tk.Label(frame_match, text=match["promo"], font=("Helvetica", 7), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(anchor="w")
            tk.Label(frame_match, text=f"📅 {match.get('fecha', 'N/A')} | ⭐ {match.get('puntuacion_dada', 'Sin calificar')}", font=("Helvetica", 7), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(anchor="w", pady=(2, 0))

    def mostrar_detalle_promo(self, promo):
        self.promo_seleccionada = promo
        for w in self.frame_contenido.winfo_children():
            w.destroy()

        f = self.frame_contenido

        # Header
        header = tk.Frame(f, bg=COLOR_ESCUDO_RED, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="←", font=("Helvetica", 16), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN, cursor="hand2").pack(side="left", padx=15, pady=10)
        tk.Label(header, text="Detalle de Promo", font=("Helvetica", 12, "bold"), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN).pack(side="left")
        tk.Label(header, text="❤️", font=("Helvetica", 14), bg=COLOR_ESCUDO_RED, fg=COLOR_TEXT_MAIN, cursor="hand2").pack(side="right", padx=15, pady=10)

        # Foto de promo
        FOTO_CONFIG = {
            "Gastronomía": ("#5C1010","#CC3300","#FF6633","🍔"),
            "Pubs / Discotecas": ("#0D0D40","#1A1AFF","#6666FF","🍺"),
            "Cafeterías": ("#0D300D","#006600","#33CC33","☕"),
            "Entretenimiento": ("#0A0A40","#000099","#3333FF","🎬"),
            "Deportes / Bienestar": ("#300D30","#660066","#CC33CC","💪"),
            "Eventos / Conciertos": ("#3D1A00","#993300","#FF6600","🎵"),
            "Tiendas Locales": ("#1A1A1A","#333333","#666666","🛍️"),
            "Otros": ("#1A1A1A","#333333","#666666","🛍️"),
        }
        cat = promo.get("cat", "Otros")
        bg1, bg2, bg3, emoji = FOTO_CONFIG.get(cat, FOTO_CONFIG["Otros"])

        canvas_foto = tk.Canvas(f, height=220, bg=bg1, bd=0, highlightthickness=0)
        canvas_foto.pack(fill="x")
        canvas_foto.create_rectangle(0, 0, 420, 110, fill=bg1, outline="")
        canvas_foto.create_rectangle(0, 110, 420, 220, fill=bg2, outline="")
        canvas_foto.create_text(210, 110, text=emoji, font=("Helvetica", 60))

        # Badge 2x1
        canvas_foto.create_rectangle(15, 15, 65, 40, fill=COLOR_ACCENT_RED, outline="")
        canvas_foto.create_text(40, 27, text="2x1", font=("Helvetica", 12, "bold"), fill=COLOR_TEXT_MAIN)

        # Info card
        frame_info = tk.Frame(f, bg=COLOR_CARD, padx=14, pady=12)
        frame_info.pack(fill="x")

        tk.Label(frame_info, text=promo["titulo"], font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, anchor="w").pack(anchor="w", pady=(0, 4))
        tk.Label(frame_info, text=f"📍 {promo['zona']} | 📅 Vence: {promo['vence']}", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(anchor="w")
        tk.Label(frame_info, text=f"💰 Ahorro estimado: Bs. {promo.get('precio_ref', 'N/A')}", font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_SUCCESS, anchor="w").pack(anchor="w", pady=(6, 0))
        tk.Label(frame_info, text=promo.get("descripcion", "Sin descripción"), font=("Helvetica", 8), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=380, anchor="w").pack(anchor="w", pady=(8, 10))

        # Botón match
        btn_match = tk.Button(
            f, text="🤝 Encontrar Compañero Ahora",
            font=("Helvetica", 11, "bold"), bg=COLOR_ACCENT_RED,
            fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2",
            pady=12, command=lambda: self.buscar_match(promo)
        )
        btn_match.pack(fill="x", padx=14, pady=(8, 10))
        configurar_animacion_boton(btn_match, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def buscar_match(self, promo):
        self.promo_seleccionada = promo
        # Simular match encontrado
        self.match_encontrado = {
            "usuario": "Ana Paredes",
            "genero": "Femenino",
            "genero_preferencia": "Cualquiera"
        }
        self.hora_fin = "14:00"
        self._mostrar_dialogo_match()

    def _mostrar_dialogo_match(self):
        ventana = tk.Toplevel(self)
        ventana.title("⚡ Match Encontrado!")
        ventana.geometry("350x450")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.grab_set()

        ventana.update_idletasks()
        x = (self.winfo_width() // 2) - 175 + self.winfo_x()
        y = (self.winfo_height() // 2) - 225 + self.winfo_y()
        ventana.geometry(f"+{x}+{y}")

        tk.Label(ventana, text="🎉", font=("Arial Black", 50), bg=COLOR_CARD).pack(pady=(20, 5))
        tk.Label(ventana, text="¡Match Encontrado!", font=("Helvetica", 18, "bold"), bg=COLOR_CARD, fg=COLOR_RAYO_YELLOW).pack(pady=(0, 10))

        # Avatar del compañero
        canvas_avatar = tk.Canvas(ventana, width=80, height=80, bg=COLOR_CARD, bd=0, highlightthickness=0)
        canvas_avatar.pack(pady=(10, 10))
        canvas_avatar.create_oval(5, 5, 75, 75, fill=COLOR_ACCENT_RED, outline="")
        canvas_avatar.create_text(40, 40, text=self.match_encontrado["usuario"][0].upper(), font=("Helvetica", 28, "bold"), fill=COLOR_TEXT_MAIN)

        tk.Label(ventana, text=self.match_encontrado["usuario"], font=("Helvetica", 13, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack()
        tk.Label(ventana, text=f"También quiere {self.promo_seleccionada['titulo']}", font=("Helvetica", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=(2, 15))

        # Botones
        def ir_chat():
            ventana.destroy()
            self.mostrar_chat()

        btn_chat = tk.Button(ventana, text="💬 Ir al Chat", font=("Helvetica", 12, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", pady=10, command=ir_chat)
        btn_chat.pack(fill="x", padx=30, pady=(0, 8))
        configurar_animacion_boton(btn_chat, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")

        btn_omitir = tk.Button(ventana, text="Cancelar", font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, bd=0, cursor="hand2", command=ventana.destroy)
        btn_omitir.pack()

    def mostrar_chat(self):
<<<<<<< Updated upstream
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        
        self.chat = SalaChatTemporal(self, self.match_encontrado, self.promo_seleccionada, self.cb_hasta.get(), on_close=self.cerrar_chat)
        self.chat.pack(fill="both", expand=True, padx=0, pady=0)
=======
        for w in self.frame_contenido.winfo_children():
            w.destroy()
>>>>>>> Stashed changes

        self.chat = SalaChatTemporal(
            self.frame_contenido,
            self.match_encontrado,
            self.promo_seleccionada,
            self.hora_fin,
            on_close=lambda: self.navegar_a("inicio")
        )
        self.chat.pack(fill="both", expand=True)

    def _mostrar_dialogo_alerta(self, titulo, mensaje):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("350x200")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.grab_set()

        tk.Label(ventana, text="⚠️", font=("Arial Black", 30), bg=COLOR_CARD).pack(pady=(15, 5))
        tk.Label(ventana, text=titulo, font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT_RED).pack(pady=(0, 8))
        tk.Label(ventana, text=mensaje, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=300, justify="center").pack(pady=(0, 15))
        btn_aceptar = tk.Button(ventana, text="Aceptar", font=("Helvetica", 11, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=ventana.destroy)
        btn_aceptar.pack(fill="x", padx=40, pady=5)
        configurar_animacion_boton(btn_aceptar, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def _mostrar_dialogo_exito(self, titulo, mensaje):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("350x200")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.grab_set()

        tk.Label(ventana, text="✅", font=("Arial Black", 30), bg=COLOR_CARD).pack(pady=(15, 5))
        tk.Label(ventana, text=titulo, font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_SUCCESS).pack(pady=(0, 8))
        tk.Label(ventana, text=mensaje, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=300, justify="center").pack(pady=(0, 15))
        btn_aceptar = tk.Button(ventana, text="¡Genial!", font=("Helvetica", 11, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=ventana.destroy)
        btn_aceptar.pack(fill="x", padx=40, pady=5)
        configurar_animacion_boton(btn_aceptar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")
