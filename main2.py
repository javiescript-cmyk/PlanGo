import tkinter as tk
from tkinter import ttk, messagebox
import random

# --- CONFIGURACIÓN DE ESTILO Y PALETA DE COLORES (Aesthetic Dark Mode) ---
COLOR_BG = "#121212"          # Fondo principal ultra oscuro
COLOR_CARD = "#1E1E1E"        # Fondo de las tarjetas de promociones
COLOR_ACCENT = "#FF4C65"      # Rosa/Rojo neón para resaltar el "2x1"
COLOR_TEXT_MAIN = "#FFFFFF"   # Texto blanco
COLOR_TEXT_MUTED = "#A0A0A0"  # Texto gris para detalles
COLOR_NAV = "#1A1A1A"         # Barra de navegación lateral
COLOR_BTN_HOVER = "#FF6B81"

class DobleteeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dobletee - Ciudades Inteligentes 2x1")
        self.geometry("1100x700")
        self.configure(bg=COLOR_BG)
        
        # Base de datos simulada de promociones
        self.promociones = [
            {"id": 1, "titulo": "Hamburguesa Doble Smash", "comercio": "Burger Click", "categoria": "Gastronomía", "detalles": "Dos por el precio de una. Válido Lunes y Martes.", "zona": "La Recoleta"},
            {"id": 2, "titulo": "Chaqueta de Mezclilla Oversize", "comercio": "Retro Vibes Clothing", "categoria": "Ropa", "detalles": "Lleva dos chaquetas seleccionadas y paga solo una.", "zona": "El Prado"},
            {"id": 3, "titulo": "Entrada General - Mirador Tunari", "comercio": "EcoTour Cbba", "categoria": "Lugares", "detalles": "Paseo guiado al atardecer 2x1 este fin de semana.", "zona": "Norte"},
            {"id": 4, "titulo": "Combo Popcorn + 2 Refrescos", "comercio": "Cine Prime", "categoria": "Entretenimiento", "detalles": "Aplica para funciones de tanda tarde.", "zona": "Av. América"},
            {"id": 5, "titulo": "Pizza Familiar Pepperoni", "comercio": "Pizzería Il Capo", "categoria": "Gastronomía", "detalles": "A la piedra, tamaño familiar 2x1.", "zona": "Zona Central"},
            {"id": 6, "titulo": "Poleras Urbanas Estampadas", "comercio": "Drip Store", "categoria": "Ropa", "detalles": "Diseños exclusivos de temporada.", "zona": "La Recoleta"}
        ]
        
        self.categoria_actual = "Todas"
        self.setup_ui()

    def setup_ui(self):
        # --- BARRA LATERAL DE NAVEGACIÓN ---
        self.sidebar = tk.Frame(self, bg=COLOR_NAV, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logotipo
        lbl_logo = tk.Label(self.sidebar, text="D O B L E T E E", font=("Helvetica", 16, "bold"), bg=COLOR_NAV, fg=COLOR_ACCENT)
        lbl_logo.pack(pady=30)
        
        # Botones de Categorías
        categorias = ["Todas", "Gastronomía", "Ropa", "Lugares", "Entretenimiento"]
        for cat in categorias:
            btn = tk.Button(
                self.sidebar, 
                text=cat, 
                font=("Helvetica", 11), 
                bg=COLOR_NAV, 
                fg=COLOR_TEXT_MAIN, 
                bd=0, 
                activebackground=COLOR_CARD, 
                activeforeground=COLOR_ACCENT,
                anchor="w",
                padx=20,
                command=lambda c=cat: self.filtrar_categoria(c)
            )
            btn.pack(fill="x", pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg=COLOR_ACCENT))
            btn.bind("<Leave>", lambda e, b=btn: b.config(fg=COLOR_TEXT_MAIN))

        # --- CONTENEDOR PRINCIPAL (DERECHO) ---
        self.main_container = tk.Frame(self, bg=COLOR_BG)
        self.main_container.pack(side="right", fill="both", expand=True, padx=30, pady=20)
        
        # Encabezado
        self.lbl_titulo_seccion = tk.Label(self.main_container, text="Promociones Disponibles", font=("Helvetica", 22, "bold"), bg=COLOR_BG, fg=COLOR_TEXT_MAIN)
        self.lbl_titulo_seccion.pack(anchor="w", pady=(0, 10))
        
        lbl_subtitulo = tk.Label(self.main_container, text="Encuentra ofertas 2x1 y conecta con alguien para dividir gastos.", font=("Helvetica", 11), bg=COLOR_BG, fg=COLOR_TEXT_MUTED)
        lbl_subtitulo.pack(anchor="w", pady=(0, 20))
        
        # Área escroleable para las Tarjetas
        self.canvas = tk.Canvas(self.main_container, bg=COLOR_BG, bd=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLOR_BG)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.renderizar_tarjetas()

    def renderizar_tarjetas(self):
        # Limpiar contenedor de tarjetas
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        promos_filtradas = [p for p in self.promociones if self.categoria_actual == "Todas" or p["categoria"] == self.categoria_actual]
        
        if not promos_filtradas:
            lbl_vacío = tk.Label(self.scrollable_frame, text="No hay promociones activas en esta categoría.", font=("Helvetica", 12), bg=COLOR_BG, fg=COLOR_TEXT_MUTED)
            lbl_vacío.pack(pady=40)
            return

        # Renderizar en cuadrícula (2 columnas)
        for index, promo in enumerate(promos_filtradas):
            fila = index // 2
            columna = index % 2
            
            # Tarjeta contenedor
            card = tk.Frame(self.scrollable_frame, bg=COLOR_CARD, bd=0, highlightbackground="#2D2D2D", highlightthickness=1)
            card.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")
            self.scrollable_frame.grid_columnconfigure(columna, weight=1, minsize=400)
            
            # Etiqueta Flotante "2x1"
            lbl_badge = tk.Label(card, text=" 2x1 ", font=("Helvetica", 10, "bold"), bg=COLOR_ACCENT, fg=COLOR_TEXT_MAIN)
            lbl_badge.pack(anchor="ne", padx=15, pady=10)
            
            # Título Promoción
            lbl_titulo = tk.Label(card, text=promo["titulo"], font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, wraplength=350, justify="left")
            lbl_titulo.pack(anchor="w", padx=20, pady=(0, 2))
            
            # Comercio
            lbl_comercio = tk.Label(card, text=f"🏪 {promo['comercio']} • 📍 {promo['zona']}", font=("Helvetica", 10, "italic"), bg=COLOR_CARD, fg=COLOR_ACCENT)
            lbl_comercio.pack(anchor="w", padx=20, pady=(0, 10))
            
            # Descripción
            lbl_desc = tk.Label(card, text=promo["detalles"], font=("Helvetica", 11), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=350, justify="left")
            lbl_desc.pack(anchor="w", padx=20, pady=(0, 15))
            
            # Botón Conexión Dobletee
            btn_match = tk.Button(
                card, 
                text="Quiero aprovechar este 2x1 (Match)", 
                font=("Helvetica", 11, "bold"), 
                bg="#2D2D2D", 
                fg=COLOR_TEXT_MAIN, 
                bd=0, 
                cursor="hand2",
                pady=8,
                command=lambda p=promo: self.simular_conexion(p)
            )
            btn_match.pack(fill="x", padx=20, pady=(0, 20))
            btn_match.bind("<Enter>", lambda e, b=btn_match: b.config(bg=COLOR_ACCENT))
            btn_match.bind("<Leave>", lambda e, b=btn_match: b.config(bg="#2D2D2D"))

    def filtrar_categoria(self, categoria):
        self.categoria_actual = categoria
        self.lbl_titulo_seccion.config(text=f"Categoría: {categoria}")
        self.renderizar_tarjetas()

    def simular_conexion(self, promo):
        # Simulación del algoritmo inteligente Matchmaker de Dobletee
        VentanaConexion(self, promo)

class VentanaConexion(tk.Toplevel):
    def __init__(self, parent, promo):
        super().__init__(parent)
        self.title("Buscando Conexión Dobletee...")
        self.geometry("450x300")
        self.configure(bg=COLOR_CARD)
        self.transient(parent)
        self.grab_set()
        
        self.promo = promo
        
        lbl_buscando = tk.Label(self, text="Buscando un Dobletee disponible...", font=("Helvetica", 14, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN)
        lbl_buscando.pack(pady=30)
        
        # Barra de progreso simulada
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        
        self.bytes_enviados = 0
        self.actualizar_progreso()

    def actualizar_progreso(self):
        if self.bytes_enviados < 100:
            self.bytes_enviados += random.randint(10, 25)
            self.progress['value'] = self.bytes_enviados
            self.after(400, self.actualizar_progreso)
        else:
            self.mostrar_resultado_match()

    def mostrar_resultado_match(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        # Simulación de perfiles basados en el interés del mismo anuncio
        nombres_simulados = ["Carlos M.", "Sofía R.", "Alejandro V.", "Mariana T.", "Diego L."]
        compañero = random.choice(nombres_simulados)
        
        lbl_exito = tk.Label(self, text="¡Conexión Encontrada! 🎉", font=("Helvetica", 16, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT)
        lbl_exito.pack(pady=20)
        
        info_match = f"A {compañero} también le interesa el 2x1 de:\n'{self.promo['titulo']}'\nen {self.promo['comercio']}."
        lbl_info = tk.Label(self, text=info_match, font=("Helvetica", 11), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, justify="center")
        lbl_info.pack(pady=10)
        
        lbl_aviso = tk.Label(self, text="Nota: Coordina el punto de encuentro de forma segura dentro del local.", font=("Helvetica", 9, "italic"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED)
        lbl_aviso.pack(pady=10)
        
        btn_chat = tk.Button(
            self, 
            text="Abrir Canal de Comunicación", 
            font=("Helvetica", 11, "bold"), 
            bg=COLOR_ACCENT, 
            fg=COLOR_TEXT_MAIN, 
            bd=0,
            pady=5,
            command=lambda: messagebox.showinfo("Simulación", "Aquí se abriría el chat seguro o redirección para coordinar.") or self.destroy()
        )
        btn_chat.pack(pady=10)

if __name__ == "__main__":
    app = DobleteeApp()
    app.mainloop()