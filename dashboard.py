
import tkinter as tk
from tkinter import ttk, messagebox
from chat import SalaChatTemporal
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
    COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_RAYO_YELLOW, COLOR_ESCUDO_RED,
    cargar_datos, guardar_datos, configurar_animacion_boton
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
        
        self.datos = cargar_datos()
        
        self.inicializar_ui()
        self._iniciar_sincronizacion()

    def inicializar_ui(self):
        frame_sidebar = tk.Frame(self, bg="#1A1A1A", width=220)
        frame_sidebar.pack(side="left", fill="y")
        frame_sidebar.pack_propagate(False)

        mini_canvas = tk.Canvas(frame_sidebar, width=160, height=70,
                            bg="#1A1A1A", bd=0, highlightthickness=0)
        mini_canvas.pack(pady=(15, 5))
        
        pts = [30, 10, 130, 10, 115, 45, 80, 65, 45, 45]
        mini_canvas.create_polygon(pts, fill=COLOR_ESCUDO_RED, outline="#800A12", width=1)
        mini_canvas.create_text(80, 30, text="2x1",
                            font=("Arial Black", 16, "bold"), fill=COLOR_TEXT_MAIN)
        mini_canvas.create_text(80, 48, text="PROMO",
                            font=("Arial Black", 7, "bold"), fill=COLOR_TEXT_MAIN)
        mini_canvas.create_polygon(
            [48, 45, 112, 45, 105, 62, 55, 62],
            fill=COLOR_TEXT_MAIN, outline="#CCCCCC", width=1)
        mini_canvas.create_text(80, 53, text="Two Pack",
                            font=("Georgia", 8, "bold", "italic"),
                            fill=COLOR_ESCUDO_RED)

        tk.Frame(frame_sidebar, bg="#2D2D2D", height=1).pack(
            fill="x", padx=15, pady=(5, 15))

        tk.Label(frame_sidebar, text="MENÚ PRINCIPAL",
                font=("Helvetica", 7, "bold"),
                bg="#1A1A1A", fg=COLOR_TEXT_MUTED).pack(
            anchor="w", padx=15, pady=(0, 8))

        nav_items = [
            ("🏠  Inicio", "inicio"),
            ("🔍  Explorar 2x1", "explorar"),
            ("⚡  Two Pack Match", "match"),
            ("📜  Historial", "historial"),
            ("👤  Mi Perfil", "perfil"),
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
                bg=COLOR_ACCENT_RED if self.seccion_actual == s else "#1A1A1A"))
            self.nav_botones[seccion] = btn

        if "inicio" in self.nav_botones:
            self.nav_botones["inicio"].config(bg=COLOR_ACCENT_RED)

        lbl_user = tk.Label(frame_sidebar, text=f"👤 {self.usuario_actual['nombre']}",
                            font=("Helvetica", 10, "bold"), bg="#1A1A1A", fg=COLOR_TEXT_MAIN)
        lbl_user.pack(pady=(20, 10))

        btn_cerrar = tk.Button(frame_sidebar, text="🚪 Cerrar Sesión",
                            font=("Helvetica", 10, "bold"), bg="#2A1B1D", fg="#E74C3C",
                            bd=0, cursor="hand2", command=self.al_cerrar_sesion)
        btn_cerrar.pack(side="bottom", fill="x", pady=10)
        configurar_animacion_boton(btn_cerrar, "#2A1B1D", COLOR_ACCENT_RED, COLOR_RED_ACTIVE)

        self.frame_principal = tk.Frame(self, bg=COLOR_BG)
        self.frame_principal.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.mostrar_catalogo_matchmaker()

    def _iniciar_sincronizacion(self):
        try:
            if self.seccion_actual in ["inicio", "explorar", "match"]:
                if (hasattr(self, 'scrollable_frame') and 
                    hasattr(self, 'cb_zona') and 
                    hasattr(self, 'cb_categoria') and 
                    self.scrollable_frame.winfo_exists() and 
                    self.cb_zona.winfo_exists() and 
                    self.cb_categoria.winfo_exists()):
                    self.actualizar_catalogo()
        except Exception:
            pass
        
        try:
            self.sync_after_id = self.after(5000, self._iniciar_sincronizacion)
        except Exception:
            pass

    def navegar_a(self, seccion):
        self.seccion_actual = seccion
        for s, btn in self.nav_botones.items():
            btn.config(bg=COLOR_ACCENT_RED if s == seccion else "#1A1A1A")
        if seccion in ["inicio", "explorar", "match"]:
            self.mostrar_catalogo_matchmaker()
        elif seccion == "perfil":
            self.mostrar_perfil()
        elif seccion == "historial":
            self.mostrar_historial()

    def mostrar_perfil(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        u = self.usuario_actual

        tk.Label(self.frame_principal,
                text="Mi Perfil Two Pack",
                font=("Helvetica", 18, "bold"),
                bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        tk.Label(self.frame_principal,
                text="Tu identidad en el ecosistema urbano de Cochabamba",
                font=("Helvetica", 10),
                bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(0, 20))

        frame_body = tk.Frame(self.frame_principal, bg=COLOR_BG)
        frame_body.pack(fill="both", expand=True)

        col_izq = tk.Frame(frame_body, bg=COLOR_CARD,
                        highlightthickness=1, highlightbackground="#2D2D2D",
                        width=220)
        col_izq.pack(side="left", fill="y", padx=(0, 15))
        col_izq.pack_propagate(False)

        canvas_av = tk.Canvas(col_izq, width=90, height=90,
                            bg=COLOR_CARD, bd=0, highlightthickness=0)
        canvas_av.pack(pady=(25, 10))
        canvas_av.create_oval(5, 5, 85, 85,
                            fill=COLOR_ACCENT_RED, outline="")
        inicial = u.get("nombre", "U")[0].upper()
        canvas_av.create_text(45, 45, text=inicial,
                            font=("Helvetica", 36, "bold"),
                            fill=COLOR_TEXT_MAIN)

        tk.Label(col_izq,
                text=u.get("nombre", "Usuario"),
                font=("Helvetica", 13, "bold"),
                bg=COLOR_CARD, fg=COLOR_TEXT_MAIN,
                wraplength=190, justify="center").pack()

        tk.Label(col_izq,
                text=u.get("genero", "No especificado"),
                font=("Helvetica", 9),
                bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=(3, 0))

        estado = u.get("estado", "Activo")
        color_estado = COLOR_SUCCESS if estado == "Activo" else COLOR_ACCENT_RED
        tk.Label(col_izq, text=f"● {estado}",
                font=("Helvetica", 9, "bold"),
                bg=COLOR_CARD, fg=color_estado).pack(pady=(5, 20))

        tk.Frame(col_izq, bg="#2D2D2D", height=1).pack(
            fill="x", padx=15, pady=(0, 15))

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

        col_der = tk.Frame(frame_body, bg=COLOR_BG)
        col_der.pack(side="right", fill="both", expand=True)

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
        configurar_animacion_boton(
            btn_guardar, COLOR_SUCCESS, COLOR_SUCCESS_HOVER, "#1E8449")

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

        frame_header = tk.Frame(self.frame_principal, bg=COLOR_CARD,
                            highlightthickness=1,
                            highlightbackground="#2D2D2D")
        frame_header.pack(fill="x", pady=(0, 15))

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

        frame_cuerpo = tk.Frame(self.frame_principal, bg=COLOR_BG)
        frame_cuerpo.pack(fill="both", expand=True)

        col_info = tk.Frame(frame_cuerpo, bg=COLOR_BG)
        col_info.pack(side="left", fill="both", expand=True, padx=(0, 15))

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

        card_mapa = tk.Frame(col_info, bg=COLOR_CARD,
                            highlightthickness=1,
                            highlightbackground="#2D2D2D")
        card_mapa.pack(fill="x")

        tk.Label(card_mapa,
                text="📍  ZONA DEL ESTABLECIMIENTO",
                font=("Helvetica", 8, "bold"),
                bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(
            anchor="w", padx=20, pady=(15, 8))

        canvas_mapa = tk.Canvas(card_mapa, width=400, height=120,
                            bg="#1A2A1A", bd=0,
                            highlightthickness=0)
        canvas_mapa.pack(padx=20, pady=(0, 15))

        for i in range(0, 420, 40):
            canvas_mapa.create_line(i, 0, i, 120,
                            fill="#2D3D2D", width=1)
        for j in range(0, 130, 30):
            canvas_mapa.create_line(0, j, 400, j,
                            fill="#2D3D2D", width=1)

        canvas_mapa.create_oval(185, 45, 215, 75,
                            fill=COLOR_ACCENT_RED, outline="")
        canvas_mapa.create_text(200, 60,
                            text="📍",
                            font=("Helvetica", 14))
        canvas_mapa.create_text(200, 95,
                            text=promo.get("zona", "Zona"),
                            font=("Helvetica", 9, "bold"),
                            fill=COLOR_RAYO_YELLOW)

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
        configurar_animacion_boton(
            btn_match_det, COLOR_ACCENT_RED,
            COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        tk.Label(col_accion,
                text="🔒 Encuentro seguro en el local",
                font=("Helvetica", 8),
                bg=COLOR_CARD, fg=COLOR_SUCCESS).pack()

    def _activar_match_desde_detalle(self, promo, cb_desde, cb_hasta):
        self.promo_seleccionada = promo
        self.mostrar_catalogo_matchmaker()
        self.cb_desde.set(cb_desde.get())
        self.cb_hasta.set(cb_hasta.get())
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

        historial = self.datos.get("historial_matches", [])

        if not historial:
            tk.Label(self.frame_principal,
                    text="🤝  Aún no tienes matches.\n"
                        "¡Explora las promos y activa tu primer Two Pack Match!",
                    font=("Helvetica", 12),
                    bg=COLOR_BG, fg=COLOR_TEXT_MUTED,
                    justify="center").pack(expand=True)
            return

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

            frame_mh = tk.Frame(card_m, bg=COLOR_CARD)
            frame_mh.pack(fill="x", padx=20, pady=(15, 8))

            canvas_mini = tk.Canvas(frame_mh, width=44, height=44,
                                    bg=COLOR_CARD, bd=0,
                                    highlightthickness=0)
            canvas_mini.pack(side="left", padx=(0, 12))
            canvas_mini.create_oval(2, 2, 42, 42,
                                    fill=COLOR_ACCENT_RED, outline="")
            ini = match["usuario_match"][0].upper()
            canvas_mini.create_text(22, 22, text=ini,
                                    font=("Helvetica", 18, "bold"),
                                    fill=COLOR_TEXT_MAIN)

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

            tk.Label(frame_mh,
                    text=f"{match['fecha']} • {match['hora']}",
                    font=("Helvetica", 9),
                    bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(side="right")

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

    def mostrar_catalogo_matchmaker(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        frame_catalogo = tk.Frame(self.frame_principal, bg=COLOR_BG)
        frame_catalogo.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(frame_catalogo, text="🎁 CATÁLOGO DE DESCUENTOS 2x1", font=("Helvetica", 14, "bold"),
                bg=COLOR_BG, fg=COLOR_RAYO_YELLOW).pack(anchor="w", pady=(0, 10))

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

        self.actualizar_catalogo()

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

        self.lbl_promo_seleccionada = tk.Label(frame_matchmaker, text="❌ No hay promoción seleccionada",
                                            font=("Helvetica", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=340)
        self.lbl_promo_seleccionada.pack(pady=(0, 15))

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

    def crear_tarjeta_promo(self, parent, promo):
        frame_tarjeta = tk.Frame(
            parent, bg=COLOR_CARD,
            highlightthickness=1,
            highlightbackground="#3D3D3D",
            padx=0, pady=0
        )
 
        # Banda superior de color con badge
        banda = tk.Frame(frame_tarjeta,
                         bg=COLOR_ESCUDO_RED, height=6)
        banda.pack(fill="x")
 
        # Contenido interno
        inner = tk.Frame(frame_tarjeta, bg=COLOR_CARD,
                         padx=15, pady=12)
        inner.pack(fill="x")
 
        # Fila superior: badge y categoría
        fila_top = tk.Frame(inner, bg=COLOR_CARD)
        fila_top.pack(fill="x", pady=(0, 6))
 
        tk.Label(fila_top,
                 text=" 2x1 ",
                 font=("Helvetica", 8, "bold"),
                 bg=COLOR_ACCENT_RED,
                 fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 8))
 
        tk.Label(fila_top,
                 text=promo.get("cat", ""),
                 font=("Helvetica", 8),
                 bg=COLOR_CARD,
                 fg=COLOR_TEXT_MUTED).pack(side="left")
 
        # Título principal
        tk.Label(inner,
                 text=promo["titulo"],
                 font=("Helvetica", 11, "bold"),
                 bg=COLOR_CARD,
                 fg=COLOR_TEXT_MAIN,
                 wraplength=320,
                 justify="left",
                 anchor="w").pack(anchor="w", pady=(0, 4))
 
        # Zona
        tk.Label(inner,
                 text=f"📍  {promo.get('zona', '—')}",
                 font=("Helvetica", 9),
                 bg=COLOR_CARD,
                 fg=COLOR_ACCENT_RED).pack(anchor="w", pady=(0, 4))
 
        # Precio referencial si existe
        precio = promo.get("precio_ref", None)
        if precio and str(precio).strip():
            frame_precio = tk.Frame(inner, bg=COLOR_CARD)
            frame_precio.pack(anchor="w", pady=(0, 8))
            tk.Label(frame_precio,
                     text=f"💰  Ahorro estimado: Bs. {precio}",
                     font=("Helvetica", 9, "bold"),
                     bg=COLOR_CARD,
                     fg=COLOR_SUCCESS).pack(side="left")
 
        # Separador
        tk.Frame(inner, bg="#2D2D2D", height=1).pack(
            fill="x", pady=(4, 10))
 
        # Fecha vencimiento y botón
        fila_bot = tk.Frame(inner, bg=COLOR_CARD)
        fila_bot.pack(fill="x")
 
        tk.Label(fila_bot,
                 text=f"📅  Vence: {promo.get('vence', '—')}",
                 font=("Helvetica", 8),
                 bg=COLOR_CARD,
                 fg=COLOR_TEXT_MUTED).pack(side="left")
 
        btn_sel = tk.Button(
            fila_bot,
            text="Ver detalle →",
            font=("Helvetica", 9, "bold"),
            bg=COLOR_ACCENT_RED,
            fg=COLOR_TEXT_MAIN,
            bd=0,
            cursor="hand2",
            padx=10, pady=4,
            command=lambda p=promo, f=frame_tarjeta: (
                self.seleccionar_promo(p, f),
                self.mostrar_detalle_promo(p)
            )
        )
        btn_sel.pack(side="right")
        configurar_animacion_boton(
            btn_sel, COLOR_ACCENT_RED,
            COLOR_RED_HOVER, COLOR_RED_ACTIVE)
 
        frame_tarjeta.btn_seleccionar = btn_sel
        frame_tarjeta.promo = promo
 
        return frame_tarjeta

    def seleccionar_promo(self, promo, frame_tarjeta):
        for tarjeta in self.tarjetas:
            tarjeta.configure(highlightbackground="#3D3D3D", highlightthickness=1)
            tarjeta.btn_seleccionar.configure(bg="#2D2D2D", text="✅ Seleccionar")
        
        frame_tarjeta.configure(highlightbackground=COLOR_ACCENT_RED, highlightthickness=2)
        frame_tarjeta.btn_seleccionar.configure(bg=COLOR_ACCENT_RED, text="✓ SELECCIONADA")
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
            
            filtro_zona = self.cb_zona.get()
            filtro_categoria = self.cb_categoria.get()
            
            for promo in self.datos["promociones"]:
                if (filtro_zona == "Todas" or promo["zona"] == filtro_zona) and \
                (filtro_categoria == "Todas" or promo["cat"] == filtro_categoria):
                    tarjeta = self.crear_tarjeta_promo(self.scrollable_frame, promo)
                    tarjeta.pack(fill="x", pady=8)
                    self.tarjetas.append(tarjeta)
            
            if self.promo_seleccionada:
                for tarjeta in self.tarjetas:
                    if tarjeta.promo["id"] == self.promo_seleccionada["id"]:
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
        for candidato in self.datos["pool_solicitudes"]:
            if candidato["oferta_id"] != id_oferta_elegida:
                continue
            inicio_comun = max(desde, candidato["hora_inicio"])
            fin_comun = min(hasta, candidato["hora_fin"])
            if inicio_comun >= fin_comun:
                continue
            if filtro_estricto and candidato["genero"] != self.usuario_actual.get("genero", ""):
                continue
            if candidato["filtro_genero"] and candidato["genero"] != self.usuario_actual.get("genero", ""):
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
        configurar_animacion_boton(self.btn_match, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

    def mostrar_chat(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        
        self.chat = SalaChatTemporal(self, self.match_encontrado, self.promo_seleccionada, self.hora_fin, on_close=self.cerrar_chat)
        self.chat.pack(fill="both", expand=True, padx=0, pady=0)

    def cerrar_chat(self):
        self.chat = None
        self.mostrar_catalogo_matchmaker()
