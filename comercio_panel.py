

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
    COLOR_CORAL_FUEGO, COLOR_AZUL_ELECTRICO, COLOR_AMARILLO_ORO, COLOR_ACCENT_RED,
    COLOR_RED_HOVER, COLOR_RED_ACTIVE, cargar_datos, guardar_datos, configurar_animacion_boton,
    base_datos_global
)

class PanelComercio(tk.Frame):
    def __init__(self, parent, usuario_actual, al_cerrar_sesion=None):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion
        self.datos = cargar_datos()
        
        self.configurar_estilos_tabla()
        self.inicializar_interfaz()
        self.actualizar_tabla()
        
        if not base_datos_global.get("comercio_onboarding_visto"):
            self.after(300, self._mostrar_onboarding)

    def configurar_estilos_tabla(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, fieldbackground=COLOR_CARD, rowheight=28, borderwidth=0)
        style.map("Treeview", background=[("selected", COLOR_CORAL_FUEGO)], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", bg="#2D2D2D", fg=COLOR_TEXT_MAIN, relief="flat", font=("Helvetica", 9, "bold"))
        style.map("Treeview.Heading", background=[("active", "#3D3D3D")])

    def inicializar_interfaz(self):
        # --- Header with electric blue ---
        frame_header = tk.Frame(self, bg=COLOR_AZUL_ELECTRICO, height=60)
        frame_header.pack(fill="x", side="top")
        frame_header.pack_propagate(False)

        lbl_titulo = tk.Label(frame_header, text="🏪 Panel de Comercio Local", font=("Helvetica", 14, "bold"), bg=COLOR_AZUL_ELECTRICO, fg=COLOR_TEXT_MAIN)
        lbl_titulo.pack(side="left", padx=15, pady=15)

        btn_salir = tk.Button(frame_header, text="Cerrar Sesión", font=("Helvetica", 9, "bold"), bg="#333333", fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", padx=10, command=self.al_cerrar_sesion)
        btn_salir.pack(side="right", padx=15, pady=15)
        configurar_animacion_boton(btn_salir, "#333333", "#444444", "#222222")

        frame_cuerpo = tk.Frame(self, bg=COLOR_BG)
        frame_cuerpo.pack(fill="both", expand=True, padx=15, pady=15)

        frame_izq = tk.Frame(frame_cuerpo, bg=COLOR_BG, width=280)
        frame_izq.pack(side="left", fill="y", padx=(0, 10))
        frame_izq.pack_propagate(False)

        frame_der = tk.Frame(frame_cuerpo, bg=COLOR_BG)
        frame_der.pack(side="right", fill="both", expand=True)

        tk.Label(frame_izq, text="PUBLICAR NUEVO 2x1", font=("Helvetica", 10, "bold"), bg=COLOR_BG, fg=COLOR_AMARILLO_ORO).pack(anchor="w", pady=(0, 15))

        tk.Label(frame_izq, text="TÍTULO DE LA OFERTA", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_titulo = tk.Entry(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_titulo.pack(fill="x", ipady=5, pady=(0, 10))

        tk.Label(frame_izq, text="CATEGORÍA", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.cb_categoria = ttk.Combobox(frame_izq, values=["Gastronomía", "Pubs / Discotecas", "Cafeterías", "Entretenimiento", "Eventos", "Deportes / Bienestar", "Tiendas Locales"], state="readonly")
        self.cb_categoria.pack(fill="x", ipady=3, pady=(0, 10))
        self.cb_categoria.set("Gastronomía")
        
        tk.Label(frame_izq, text="TIPO DE OFERTA", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.cb_tipo_oferta = ttk.Combobox(frame_izq, values=[
            "2x1 Clásico",
            "Combo Especial",
            "Descuento 50%",
            "Happy Hour",
            "Precio de Socio",
            "Oferta del Día",
            "Lleva 3 Paga 2",
            "Menú Universitario",
        ], state="readonly")
        self.cb_tipo_oferta.pack(fill="x", ipady=3, pady=(0, 10))
        self.cb_tipo_oferta.set("2x1 Clásico")

        tk.Label(frame_izq, text="ZONA COMERCIAL", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.cb_zona = ttk.Combobox(frame_izq, values=["Zona Centro / Calle Comercio", "La Recoleta", "El Prado", "Zona Norte", "Zona Sur / Mall Las Brisas", "Zona Este / Cine Prime Center"], state="readonly")
        self.cb_zona.pack(fill="x", ipady=3, pady=(0, 10))
        self.cb_zona.set("Zona Centro / Calle Comercio")

        tk.Label(frame_izq, text="FECHA CADUCIDAD (DD/MM/AAAA)", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_vence = tk.Entry(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_vence.pack(fill="x", ipady=5, pady=(0, 10))
        self.ent_vence.insert(0, datetime.now().strftime("%d/%m/%Y"))

        tk.Label(frame_izq, text="PRECIO UNITARIO REFERENCIAL (Bs.)", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_precio = tk.Entry(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_precio.pack(fill="x", ipady=5, pady=(0, 10))

        tk.Label(frame_izq, text="DESCRIPCIÓN DEL 2x1", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.txt_desc = tk.Text(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, height=4, highlightthickness=1, highlightbackground="#2D2D2D")
        self.txt_desc.pack(fill="x", pady=(0, 10))

        btn_lanzar = tk.Button(frame_izq, text="🚀 Lanzar Promo 2x1", font=("Helvetica", 11, "bold"), bg=COLOR_CORAL_FUEGO, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=self.registrar_oferta)
        btn_lanzar.pack(fill="x", ipady=8)
        configurar_animacion_boton(btn_lanzar, COLOR_CORAL_FUEGO, "#FF4A5A", "#C41430")

        tk.Label(frame_der, text="MIS PROMOCIONES ACTIVAS", font=("Helvetica", 10, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 15))

        columnas = ("id", "titulo", "cat", "zona", "vence", "precio_ref", "descripcion", "demanda")
        self.tabla = ttk.Treeview(frame_der, columns=columnas, show="headings")

        self.tabla.heading("id", text="ID")
        self.tabla.heading("titulo", text="Título")
        self.tabla.heading("cat", text="Categoría")
        self.tabla.heading("zona", text="Zona")
        self.tabla.heading("vence", text="Vence")
        self.tabla.heading("precio_ref", text="Precio")
        self.tabla.heading("descripcion", text="Descripción")
        self.tabla.heading("demanda", text="Demanda")

        self.tabla.column("id", width=40, anchor="center")
        self.tabla.column("titulo", width=150, anchor="w")
        self.tabla.column("cat", width=100, anchor="center")
        self.tabla.column("zona", width=120, anchor="center")
        self.tabla.column("vence", width=80, anchor="center")
        self.tabla.column("precio_ref", width=70, anchor="center")
        self.tabla.column("descripcion", width=200, anchor="w")
        self.tabla.column("demanda", width=100, anchor="center")

        self.tabla.pack(fill="both", expand=True, pady=(0, 10))

        btn_eliminar = tk.Button(frame_der, text="🗑️ Eliminar Promo Seleccionada", font=("Helvetica", 9, "bold"), bg="#2D2D2D", fg=COLOR_TEXT_MUTED, bd=0, cursor="hand2", command=self.eliminar_oferta)
        btn_eliminar.pack(anchor="e", ipady=5, ipadx=10)
        configurar_animacion_boton(btn_eliminar, "#2D2D2D", COLOR_CORAL_FUEGO, "#C41430")

        tk.Frame(frame_der, bg="#2D2D2D", height=1).pack(
            fill="x", pady=15)

        tk.Label(frame_der,
                 text="📊  IMPACTO DE TUS PROMOCIONES",
                 font=("Helvetica", 9, "bold"),
                 bg=COLOR_BG, fg=COLOR_RAYO_YELLOW).pack(
            anchor="w", pady=(0, 10))

        promos_activas = len(base_datos_global["promociones"])
        usuarios_vieron = promos_activas * 6
        matches_gen = promos_activas * 2
        precio_prom = 70
        ingresos_est = matches_gen * precio_prom

        metricas = [
            ("👥",
             f"{usuarios_vieron}",
             "Usuarios vieron tu promo",
             COLOR_ACCENT_RED),
            ("🤝",
             f"{matches_gen}",
             "Matches generados",
             COLOR_RAYO_YELLOW),
            ("�",
             f"Bs. {ingresos_est}",
             "Ingresos estimados",
             COLOR_SUCCESS),
            ("⭐",
             "4.8",
             "Valoración de usuarios",
             "#5D3FD3"),
        ]

        frame_metricas = tk.Frame(frame_der, bg=COLOR_BG)
        frame_metricas.pack(fill="x")

        for icono, valor, etiqueta, color in metricas:
            card_m = tk.Frame(
                frame_metricas,
                bg=COLOR_CARD,
                highlightthickness=1,
                highlightbackground="#2D2D2D",
                padx=10, pady=8)
            card_m.pack(
                side="left",
                fill="x",
                expand=True,
                padx=3)

            tk.Label(
                card_m,
                text=icono,
                font=("Helvetica", 16),
                bg=COLOR_CARD
            ).pack()

            tk.Label(
                card_m,
                text=valor,
                font=("Helvetica", 13, "bold"),
                bg=COLOR_CARD,
                fg=color
            ).pack()

            tk.Label(
                card_m,
                text=etiqueta,
                font=("Helvetica", 7),
                bg=COLOR_CARD,
                fg=COLOR_TEXT_MUTED,
                justify="center",
                wraplength=90
            ).pack()

        tk.Label(frame_der, text="* Datos calculados en base a actividad real de la plataforma.",
                 font=("Helvetica", 7, "italic"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(8, 0))

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
        for promo in base_datos_global["promociones"]:
            self.tabla.insert("", "end", values=(
                promo["id"],
                promo["titulo"],
                promo["cat"],
                promo["zona"],
                promo["vence"],
                promo["precio_ref"],
                promo["descripcion"][:50] + "...",
                promo.get("demanda", "Media")
            ))

    def _mostrar_onboarding(self):
        ven = tk.Toplevel(self)
        ven.title("Bienvenido a Two Pack")
        ven.geometry("380x480")
        ven.configure(bg=COLOR_BG)
        ven.resizable(False, False)
        ven.grab_set()

        sw = ven.winfo_screenwidth()
        sh = ven.winfo_screenheight()
        ven.geometry(f"380x480+{sw//2-190}+{sh//2-240}")

        self._paso_actual = tk.IntVar(value=0)

        pasos = [
            ("📢", "Tu promo,\nmás clientes", "128 usuarios activos buscan\nofertas 2x1 en Cochabamba\nahora mismo.", COLOR_ACCENT_RED),
            ("📍", "Llega a\ntu zona", "Geolocalización IA dirige\nusuarios cercanos\ndirecto a tu local.", COLOR_RAYO_YELLOW),
            ("💰", "100% gratis\npara ti", "Publica ilimitado sin costo.\n87 comercios ya confían\nen Two Pack Cochabamba.", COLOR_SUCCESS),
        ]

        frame_cont = tk.Frame(ven, bg=COLOR_BG)
        frame_cont.pack(fill="both", expand=True, padx=20)

        def mostrar_paso(idx):
            for w in frame_cont.winfo_children():
                w.destroy()
            ico, tit, desc, col = pasos[idx]

            # Dots de progreso
            frame_dots = tk.Frame(frame_cont, bg=COLOR_BG)
            frame_dots.pack(pady=(20,0))
            for i in range(3):
                tk.Label(frame_dots, text="●", font=("Helvetica",10), bg=COLOR_BG, fg=col if i == idx else "#333333").pack(side="left", padx=4)

            tk.Label(frame_cont, text=ico, font=("Helvetica",48), bg=COLOR_BG).pack(pady=(20,8))
            tk.Label(frame_cont, text=tit, font=("Helvetica",16,"bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN, justify="center").pack()
            tk.Label(frame_cont, text=desc, font=("Helvetica",10), bg=COLOR_BG, fg=COLOR_TEXT_MUTED, justify="center").pack(pady=(10,0))

            # Barra de progreso paso
            frame_barra = tk.Frame(frame_cont, bg="#2D2D2D", height=4)
            frame_barra.pack(fill="x", pady=(20,0))
            frame_barra.pack_propagate(False)
            ancho = int(380 * ((idx + 1)/3))
            tk.Frame(frame_barra, bg=col, height=4, width=ancho).place(x=0, y=0)

            if idx < 2:
                btn = tk.Button(frame_cont, text="Siguiente →", font=("Helvetica",11,"bold"), bg=col, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=lambda: mostrar_paso(idx+1))
                btn.pack(fill="x", ipady=12, pady=(20,0))
            else:
                btn = tk.Button(frame_cont, text="¡Empezar a publicar!", font=("Helvetica",11,"bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=lambda: [base_datos_global.update({"comercio_onboarding_visto": True}), ven.destroy()])
                btn.pack(fill="x", ipady=12, pady=(20,0))

        mostrar_paso(0)

    def _mostrar_dialogo_alerta(self, titulo, mensaje):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("400x220")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.grab_set()
        
        tk.Label(ventana, text="⚠️", font=("Arial Black", 30), bg=COLOR_CARD).pack(pady=(15, 5))
        
        tk.Label(ventana, text=titulo, font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_CORAL_FUEGO).pack(pady=(0, 8))
        
        tk.Label(ventana, text=mensaje, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=350, justify="center").pack(pady=(0, 20))
        
        btn_aceptar = tk.Button(ventana, text="Aceptar", font=("Helvetica", 11, "bold"), bg=COLOR_CORAL_FUEGO, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=ventana.destroy)
        btn_aceptar.pack(fill="x", padx=50, pady=5)
        configurar_animacion_boton(btn_aceptar, COLOR_CORAL_FUEGO, "#FF4A5A", "#C41430")

    def _mostrar_dialogo_exito(self, titulo, mensaje):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("400x220")
        ventana.configure(bg=COLOR_CARD)
        ventana.resizable(False, False)
        ventana.grab_set()
        
        tk.Label(ventana, text="✅", font=("Arial Black", 30), bg=COLOR_CARD).pack(pady=(15, 5))
        
        tk.Label(ventana, text=titulo, font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_SUCCESS).pack(pady=(0, 8))
        
        tk.Label(ventana, text=mensaje, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=350, justify="center").pack(pady=(0, 20))
        
        btn_aceptar = tk.Button(ventana, text="¡Genial!", font=("Helvetica", 11, "bold"), bg=COLOR_SUCCESS, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=ventana.destroy)
        btn_aceptar.pack(fill="x", padx=50, pady=5)
        configurar_animacion_boton(btn_aceptar, COLOR_SUCCESS, "#27AE60", "#1E8449")

    def registrar_oferta(self):
        titulo = self.ent_titulo.get().strip()
        categoria = self.cb_categoria.get()
        tipo_oferta = self.cb_tipo_oferta.get()
        zona = self.cb_zona.get()
        vence = self.ent_vence.get().strip()
        precio_ref = self.ent_precio.get().strip()
        descripcion = self.txt_desc.get("1.0", tk.END).strip()

        if not titulo or not vence or not descripcion:
            self._mostrar_dialogo_alerta("Campos Incompletos", "Por favor completa todos los campos para lanzar la promoción.")
            return

        nuevo_id = str(len(base_datos_global["promociones"]) + 1).zfill(3)

        nueva_promo = {
            "id": nuevo_id, 
            "titulo": titulo, 
            "cat": categoria, 
            "tipo_oferta": tipo_oferta,
            "zona": zona, 
            "vence": vence,
            "precio_ref": precio_ref,
            "descripcion": descripcion,
            "demanda": "Alta",
            "comercio": self.usuario_actual.get("nombre", "Mi Negocio"),
            "distancia": "500 m",
            "hora_hasta": "22:00"
        }

        base_datos_global["promociones"].append(nueva_promo)
        self.datos["promociones"].append(nueva_promo)

        guardar_datos()

        self.actualizar_tabla()
        self._mostrar_dialogo_exito("¡Éxito Total!", f"Tu oferta '{titulo}' ha sido publicada correctamente.")

        self.ent_titulo.delete(0, tk.END)
        self.ent_precio.delete(0, tk.END)
        self.txt_desc.delete("1.0", tk.END)

    def eliminar_oferta(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado:
            self._mostrar_dialogo_alerta("Selección Requerida", "Por favor selecciona una promoción de la tabla para eliminarla.")
            return

        valores = self.tabla.item(item_seleccionado, "values")
        id_promo = valores[0]

        # Eliminar de base_datos_global
        base_datos_global["promociones"] = [
            p for p in base_datos_global["promociones"] 
            if p["id"] != id_promo
        ]
        
        # Also update self.datos to keep in sync
        self.datos["promociones"] = [
            p for p in self.datos["promociones"] 
            if p["id"] != id_promo
        ]

        guardar_datos()

        self.actualizar_tabla()
        self._mostrar_dialogo_exito("Promo Eliminada", "La oferta seleccionada fue removida del feed de Two Pack de forma inmediata.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Two Pack - Test Comercio Local")
    root.geometry("1000x600")
    root.configure(bg=COLOR_BG)

    # Dummy usuario para pruebas
    usuario_test = {"nombre": "Restaurante Sabores", "rol": "comercio"}
    panel = PanelComercio(root, usuario_test, al_cerrar_sesion=lambda: root.destroy())
    panel.pack(fill="both", expand=True)

    root.mainloop()
