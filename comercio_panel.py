

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
                 text="📊  ESTADÍSTICAS DEL NEGOCIO",
                 font=("Helvetica", 9, "bold"),
                 bg=COLOR_BG, fg=COLOR_AMARILLO_ORO).pack(
            anchor="w", pady=(0, 10))

        frame_stats_com = tk.Frame(frame_der, bg=COLOR_BG)
        frame_stats_com.pack(fill="x")

        stats_negocio = [
            ("🎯", str(len(base_datos_global["promociones"])),
             "Promos activas"),
            ("👥", str(len(base_datos_global["pool_solicitudes"])),
             "Usuarios en espera"),
            ("⭐", "4.8", "Valoración media"),
        ]
        for icono, valor, etiqueta in stats_negocio:
            card_stat = tk.Frame(frame_stats_com, bg=COLOR_CARD,
                                 highlightthickness=1,
                                 highlightbackground="#2D2D2D",
                                 padx=15, pady=10)
            card_stat.pack(side="left", padx=(0, 10), fill="x",
                          expand=True)
            tk.Label(card_stat,
                     text=f"{icono}  {valor}",
                     font=("Helvetica", 16, "bold"),
                     bg=COLOR_CARD,
                     fg=COLOR_AMARILLO_ORO).pack()
            tk.Label(card_stat,
                     text=etiqueta,
                     font=("Helvetica", 8),
                     bg=COLOR_CARD,
                     fg=COLOR_TEXT_MUTED).pack()

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
        zona = self.cb_zona.get()
        vence = self.ent_vence.get().strip()
        precio_ref = self.ent_precio.get().strip()
        descripcion = self.txt_desc.get("1.0", tk.END).strip()

        if not titulo or not vence or not descripcion:
            self._mostrar_dialogo_alerta("Campos Incompletos", "Por favor completa todos los campos para lanzar la promoción.")
            return

        nuevo_id = str(len(base_datos_global["promociones"]) + 1).zfill(3)

        self.datos["promociones"].append({
            "id": nuevo_id, 
            "titulo": titulo, 
            "cat": categoria, 
            "zona": zona, 
            "vence": vence,
            "precio_ref": precio_ref,
            "descripcion": descripcion,
            "demanda": "Alta",
            "comercio": self.usuario_actual.get("nombre", "Mi Negocio"),
            "distancia": "500 m",
            "hora_hasta": "22:00"
        })
        
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
