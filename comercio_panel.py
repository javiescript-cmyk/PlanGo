
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_SUCCESS_HOVER,
    COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE, COLOR_RAYO_YELLOW,
    get_db_connection, configurar_animacion_boton
)

class PanelComercio(tk.Frame):
    def __init__(self, parent, usuario_actual, al_cerrar_sesion=None):
        super().__init__(parent, bg=COLOR_BG)
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion
        
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
        self.cb_categoria = ttk.Combobox(frame_izq, values=[], state="readonly")
        self.cb_categoria.pack(fill="x", ipady=3, pady=(0, 10))
        self.cargar_categorias()

        tk.Label(frame_izq, text="DESCRIPCIÓN DEL 2x1", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.txt_desc = tk.Text(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, height=4, highlightthickness=1, highlightbackground="#2D2D2D")
        self.txt_desc.pack(fill="x", pady=(0, 10))

        tk.Label(frame_izq, text="FECHA INICIO (DD/MM/AAAA)", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_fecha_inicio = tk.Entry(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_fecha_inicio.pack(fill="x", ipady=5, pady=(0, 10))
        self.ent_fecha_inicio.insert(0, datetime.now().strftime("%d/%m/%Y"))

        tk.Label(frame_izq, text="FECHA FIN (DD/MM/AAAA)", font=("Helvetica", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_fecha_fin = tk.Entry(frame_izq, font=("Helvetica", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#2D2D2D")
        self.ent_fecha_fin.pack(fill="x", ipady=5, pady=(0, 15))

        btn_lanzar = tk.Button(frame_izq, text="🚀 Lanzar Promo 2x1", font=("Helvetica", 11, "bold"), bg=COLOR_ACCENT_RED, fg=COLOR_TEXT_MAIN, bd=0, cursor="hand2", command=self.registrar_oferta)
        btn_lanzar.pack(fill="x", ipady=8)
        configurar_animacion_boton(btn_lanzar, COLOR_ACCENT_RED, COLOR_RED_HOVER, COLOR_RED_ACTIVE)

        tk.Label(frame_der, text="MIS PROMOCIONES ACTIVAS", font=("Helvetica", 10, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 15))

        columnas = ("id", "titulo", "categoria", "descripcion", "estado")
        self.tabla = ttk.Treeview(frame_der, columns=columnas, show="headings")

        self.tabla.heading("id", text="ID")
        self.tabla.heading("titulo", text="Título de la Promo")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("descripcion", text="Descripción")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("id", width=40, anchor="center")
        self.tabla.column("titulo", width=200, anchor="w")
        self.tabla.column("categoria", width=100, anchor="center")
        self.tabla.column("descripcion", width=250, anchor="w")
        self.tabla.column("estado", width=80, anchor="center")

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

        # Stats will be loaded from DB
        self.lbl_promos_activas = tk.Label(frame_stats_com, text="🎯 0 Promos activas", font=("Helvetica", 12, "bold"), bg=COLOR_RAYO_YELLOW)
        self.lbl_promos_activas.pack()

    def cargar_categorias(self):
        conn = get_db_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM categorias ORDER BY nombre")
            categorias = cursor.fetchall()
            self.cb_categoria['values'] = [cat['nombre'] for cat in categorias]
            if categorias:
                self.cb_categoria.current(0)
        except Exception as e:
            print(f"Error cargando categorías: {e}")
        finally:
            conn.close()

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
        conn = get_db_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.titulo, c.nombre as categoria, p.descripcion, p.estado
                FROM promociones p
                JOIN categorias c ON p.categoria_id = c.id
                WHERE p.negocio_id = %s
                ORDER BY p.fecha_creacion DESC
            """, (self.usuario_actual['id'],))
            promos = cursor.fetchall()
            
            for promo in promos:
                self.tabla.insert("", "end", values=(
                    promo['id'],
                    promo['titulo'],
                    promo['categoria'],
                    promo['descripcion'],
                    promo['estado']
                ))
        except Exception as e:
            print(f"Error actualizando tabla: {e}")
        finally:
            conn.close()

    def registrar_oferta(self):
        titulo = self.ent_titulo.get().strip()
        categoria_nombre = self.cb_categoria.get()
        descripcion = self.txt_desc.get("1.0", tk.END).strip()
        fecha_inicio_str = self.ent_fecha_inicio.get().strip()
        fecha_fin_str = self.ent_fecha_fin.get().strip()

        if not titulo or not categoria_nombre or not descripcion or not fecha_inicio_str or not fecha_fin_str:
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los campos para lanzar la promoción.")
            return

        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
            fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error de Formato", "Las fechas deben tener el formato DD/MM/AAAA")
            return

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

        try:
            cursor = conn.cursor()
            
            # Obtener ID de la categoría
            cursor.execute("SELECT id FROM categorias WHERE nombre = %s", (categoria_nombre,))
            categoria = cursor.fetchone()
            if not categoria:
                messagebox.showerror("Error", "Categoría no encontrada.")
                return
            
            # Insertar promoción
            cursor.execute("""
                INSERT INTO promociones (negocio_id, categoria_id, titulo, descripcion, fecha_inicio, fecha_fin, estado)
                VALUES (%s, %s, %s, %s, %s, %s, 'activa')
            """, (self.usuario_actual['id'], categoria['id'], titulo, descripcion, fecha_inicio, fecha_fin))
            conn.commit()
            
            messagebox.showinfo("¡Éxito Total!", f"Tu oferta '{titulo}' ha sido publicada correctamente.")
            self.actualizar_tabla()
            
            # Limpiar campos
            self.ent_titulo.delete(0, tk.END)
            self.txt_desc.delete("1.0", tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
            conn.rollback()
        finally:
            conn.close()

    def eliminar_oferta(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado:
            messagebox.showwarning("Selección Requerida", "Por favor selecciona una promoción de la tabla para eliminarla.")
            return

        valores = self.tabla.item(item_seleccionado, "values")
        id_promo = valores[0]
        
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM promociones WHERE id = %s", (id_promo,))
            conn.commit()
            
            messagebox.showinfo("Promo Eliminada", "La oferta seleccionada fue removida del feed de Two Pack de forma inmediata.")
            self.actualizar_tabla()
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
            conn.rollback()
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Two Pack - Test Comercio Local")
    root.geometry("900x600")
    root.configure(bg=COLOR_BG)

    # Dummy usuario para pruebas
    usuario_test = {'id': '1', 'nombre': 'Negocio Test', 'rol': 'comercio'}
    panel = PanelComercio(root, usuario_test, al_cerrar_sesion=lambda: root.destroy())
    panel.pack(fill="both", expand=True)

    root.mainloop()

