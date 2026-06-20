
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
    COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_RAYO_YELLOW,
    cargar_datos, guardar_datos, configurar_animacion_boton
)

class PanelComercio(tk.Frame):
    def __init__(self, parent, al_cerrar_sesion=None):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.al_cerrar_sesion = al_cerrar_sesion
        
        self.datos = cargar_datos()
        
        self.configurar_estilos_tabla()
        self.inicializar_interfaz()
        self.actualizar_tabla()

    def configurar_estilos_tabla(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, fieldbackground=COLOR_CARD, rowheight=28, borderwidth=0)
        style.map("Treeview", background=[("selected", COLOR_ACCENT_RED)], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", bg="#2D2D2D", fg=COLOR_TEXT_MAIN, relief="flat", font=("Helvetica", 9, "bold"))
        style.map("Treeview.Heading", background=[("active", "#3D3D3D")])

    def inicializar_interfaz(self):
        frame_header = tk.Frame(self, bg=COLOR_CARD, height=60)
        frame_header.pack(fill="x", side="top")
        frame_header.pack_propagate(False)

        lbl_titulo = tk.Label(frame_header, text="🏪 Panel de Comercio Local", font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN)
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

        tk.Label(frame_izq, text="PUBLICAR NUEVO 2x1", font=("Helvetica", 10, "bold"), bg=COLOR_BG, fg=COLOR_RAYO_YELLOW).pack(anchor="w", pady=(0, 15))

        tk.Label(frame_izq, text="TÍTULO DE LA OFERTA", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_titulo = tk.Entry(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_titulo.pack(fill="x", ipady=5, pady=(0, 10))

        tk.Label(frame_izq, text="CATEGORÍA", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.cb_categoria = ttk.Combobox(frame_izq, values=["Gastronomía", "Pubs / Discotecas", "Cafeterías", "Eventos / Conciertos", "Otros"], state="readonly")
        self.cb_categoria.pack(fill="x", ipady=3, pady=(0, 10))
        self.cb_categoria.set("Gastronomía")

        tk.Label(frame_izq, text="ZONA COMERCIAL", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.cb_zona = ttk.Combobox(frame_izq, values=["La Recoleta", "El Prado", "Zona UCATEC", "Zona Central", "América Oeste"], state="readonly")
        self.cb_zona.pack(fill="x", ipady=3, pady=(0, 10))
        self.cb_zona.set("Zona UCATEC")

        tk.Label(frame_izq, text="FECHA CADUCIDAD (DD/MM/AAAA)", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_vence = tk.Entry(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_vence.pack(fill="x", ipady=5, pady=(0, 10))
        self.ent_vence.insert(0, datetime.now().strftime("%d/%m/%Y"))

        tk.Label(frame_izq, text="PRECIO UNITARIO REFERENCIAL (Bs.)", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_precio = tk.Entry(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_precio.pack(fill="x", ipady=5, pady=(0, 10))

        tk.Label(frame_izq, text="DESCRIPCIÓN DEL 2x1", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.txt_desc = tk.Text(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, height=4, highlightthickness=1, highlightbackground="#2D2D2D")
        self.txt_desc.pack(fill="x", pady=(0, 15))

        btn_lanzar = tk.Button(frame_izq, text="🚀 Lanzar Promo 2x1", font=("Helvetica", 11, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=self.registrar_oferta)
        btn_lanzar.pack(fill="x", ipady=8)
        configurar_animacion_boton(btn_lanzar, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        tk.Label(frame_der, text="MIS PROMOCIONES ACTIVAS EN COCHABAMBA", font=("Helvetica", 10, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 15))

        columnas = ("id", "titulo", "categoria", "zona", "vence", "precio_ref")
        self.tabla = ttk.Treeview(frame_der, columns=columnas, show="headings")

        self.tabla.heading("id", text="ID")
        self.tabla.heading("titulo", text="Título de la Promo")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("zona", text="Ubicación / Zona")
        self.tabla.heading("vence", text="Vence el")
        self.tabla.heading("precio_ref", text="Precio (Bs.)")

        self.tabla.column("id", width=40, anchor="center")
        self.tabla.column("titulo", width=160, anchor="w")
        self.tabla.column("categoria", width=100, anchor="center")
        self.tabla.column("zona", width=90, anchor="center")
        self.tabla.column("vence", width=80, anchor="center")
        self.tabla.column("precio_ref", width=70, anchor="center")

        self.tabla.pack(fill="both", expand=True, pady=(0, 10))

        btn_eliminar = tk.Button(frame_der, text="🗑️ Eliminar Promo Seleccionada", font=("Helvetica", 9, "bold"), bg="#2D2D2D", fg=COLOR_TEXT_MUTED, bd=0, cursor="hand2", command=self.eliminar_oferta)
        btn_eliminar.pack(anchor="e", ipady=5, ipadx=10)
        configurar_animacion_boton(btn_eliminar, "#2D2D2D", COLOR_ACCENT_RED, COLOR_RED_ACTIVE)

        tk.Frame(frame_der, bg="#2D2D2D", height=1).pack(
            fill="x", pady=15)

        tk.Label(frame_der,
                 text="📊  ESTADÍSTICAS DEL NEGOCIO",
                 font=("Helvetica", 9, "bold"),
                 bg=COLOR_BG, fg=COLOR_RAYO_YELLOW).pack(
            anchor="w", pady=(0, 10))

        frame_stats_com = tk.Frame(frame_der, bg=COLOR_BG)
        frame_stats_com.pack(fill="x")

        from config import base_datos_global
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
                     fg=COLOR_RAYO_YELLOW).pack()
            tk.Label(card_stat,
                     text=etiqueta,
                     font=("Helvetica", 8),
                     bg=COLOR_CARD,
                     fg=COLOR_TEXT_MUTED).pack()

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for promo in self.datos["promociones"]:
            self.tabla.insert("", "end", values=(
                promo["id"], 
                promo["titulo"], 
                promo["cat"], 
                promo["zona"], 
                promo["vence"],
                promo.get("precio_ref", "")
            ))

    def registrar_oferta(self):
        titulo = self.ent_titulo.get().strip()
        categoria = self.cb_categoria.get()
        zona = self.cb_zona.get()
        vence = self.ent_vence.get().strip()
        precio_ref = self.ent_precio.get().strip()
        descripcion = self.txt_desc.get("1.0", tk.END).strip()

        if not titulo or not vence or not descripcion:
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los campos para lanzar la promoción.")
            return

        try:
            datetime.strptime(vence, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error de Formato", "La fecha de caducidad debe tener el formato DD/MM/AAAA\nEjemplo: 25/06/2026")
            return

        nuevo_id = f"{len(self.datos['promociones']) + 1:03d}"

        self.datos["promociones"].append({
            "id": nuevo_id, 
            "titulo": titulo, 
            "cat": categoria, 
            "zona": zona, 
            "vence": vence,
            "precio_ref": precio_ref
        })
        
        guardar_datos()

        self.actualizar_tabla()
        messagebox.showinfo("¡Éxito Total!", f"Tu oferta '{titulo}' ha sido desplegada con éxito en la zona {zona}.")

        self.ent_titulo.delete(0, tk.END)
        self.ent_precio.delete(0, tk.END)
        self.txt_desc.delete("1.0", tk.END)

    def eliminar_oferta(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado:
            messagebox.showwarning("Selección Requerida", "Por favor selecciona una promoción de la tabla para eliminarla.")
            return

        valores = self.tabla.item(item_seleccionado, "values")
        id_promo = valores[0]

        self.datos["promociones"] = [p for p in self.datos["promociones"] if p["id"] != id_promo]
        
        guardar_datos()

        self.actualizar_tabla()
        messagebox.showinfo("Promo Eliminada", "La oferta seleccionada fue removida del feed de Two Pack de forma inmediata.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Two Pack - Test Comercio Local")
    root.geometry("900x600")
    root.configure(bg=COLOR_BG)

    panel = PanelComercio(root, al_cerrar_sesion=lambda: root.destroy())
    panel.pack(fill="both", expand=True)

    root.mainloop()
