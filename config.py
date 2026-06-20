
import json
import os

# --- PALETA DE COLORES OFICIAL ---
COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_MUTED = "#A0A0A0"
COLOR_ACCENT_RED = "#FF1E39"
COLOR_RED_HOVER = "#FF4D63"
COLOR_RED_ACTIVE = "#990A15"
COLOR_RAYO_YELLOW = "#FFCC00"
COLOR_SUCCESS = "#2ECC71"
COLOR_SUCCESS_HOVER = "#27AE60"
COLOR_ESCUDO_RED = "#C41430"

# --- BASE DE DATOS COMPARTIDA ---
base_datos_global = {
    "promociones": [
        {
            "id": "001",
            "titulo": "2x1 en Alitas BBQ Universitarias",
            "cat": "Gastronomía",
            "zona": "Zona UCATEC",
            "vence": "30/06/2026",
            "precio_ref": "45",
            "descripcion": (
                "Disfruta dos porciones de alitas BBQ "
                "por el precio de una. Válido lunes a "
                "miércoles de 12:00 a 15:00. "
                "Presenta la app Two Pack al pagar."
            )
        },
        {
            "id": "002",
            "titulo": "Fernet con Cola 2x1 — Jueves de Frater",
            "cat": "Pubs / Discotecas",
            "zona": "La Recoleta",
            "vence": "31/07/2026",
            "precio_ref": "55",
            "descripcion": (
                "Cada jueves de frater, lleva dos "
                "Fernet con Cola y paga solo uno. "
                "Válido de 20:00 a 23:00 hrs. "
                "Solo para universitarios con carnet."
            )
        },
        {
            "id": "003",
            "titulo": "Milkshake Premium 2x1",
            "cat": "Cafeterías",
            "zona": "El Prado",
            "vence": "15/07/2026",
            "precio_ref": "38",
            "descripcion": (
                "Elige dos milkshakes de cualquier sabor "
                "de nuestra carta premium y paga solo el "
                "más caro. Válido toda la semana "
                "de 14:00 a 19:00 hrs."
            )
        },
        {
            "id": "004",
            "titulo": "Combo Burger Doble Smash 2x1",
            "cat": "Gastronomía",
            "zona": "Av. América",
            "vence": "30/06/2026",
            "precio_ref": "65",
            "descripcion": (
                "Dos combos completos (burger + papas "
                "+ refresco) por el precio de uno. "
                "Válido martes y miércoles al mediodía."
            )
        },
        {
            "id": "005",
            "titulo": "Entrada Doble — Cine Prime Tarde",
            "cat": "Entretenimiento",
            "zona": "Centro Comercial Las Vegas",
            "vence": "31/07/2026",
            "precio_ref": "30",
            "descripcion": (
                "Compra una entrada y lleva a un "
                "acompañante gratis en tandas de tarde "
                "(antes de 18:00). Cualquier película "
                "en cartelera."
            )
        },
        {
            "id": "006",
            "titulo": "Clase de CrossFit 2x1",
            "cat": "Deportes / Bienestar",
            "zona": "Zona Norte",
            "vence": "15/07/2026",
            "precio_ref": "40",
            "descripcion": (
                "Trae a un amigo y los dos entrenan "
                "por el precio de una clase. Incluye "
                "acceso a vestuarios y casilleros. "
                "Lunes, miércoles y viernes."
            )
        },
        {
            "id": "007",
            "titulo": "2x1 en Pizzas Medianas",
            "cat": "Gastronomía",
            "zona": "Zona Central",
            "vence": "30/06/2026",
            "precio_ref": "58",
            "descripcion": (
                "Pide dos pizzas medianas de cualquier "
                "sabor y paga solo una. Válido domingos "
                "de 18:00 a 21:00. No incluye delivery."
            )
        },
        {
            "id": "008",
            "titulo": "Tour Gastronómico Cbba 2x1",
            "cat": "Eventos / Conciertos",
            "zona": "Cancha y Mercado",
            "vence": "31/07/2026",
            "precio_ref": "80",
            "descripcion": (
                "Recorre 5 puntos gastronómicos "
                "emblemáticos de Cochabamba con guía "
                "incluido. Dos personas por el precio "
                "de una. Sábados 10:00 a 13:00."
            )
        }
    ],
    "historial_matches": [ 
        { 
            "id": "m001", 
            "usuario_match": "Alejandro Gómez", 
            "genero_match": "Masculino", 
            "promo": "2x1 en Alitas Universitarias", 
            "zona": "Zona UCATEC", 
            "fecha": "15/06/2026", 
            "hora": "13:00", 
            "reseña_dada": None, 
            "puntuacion_dada": None 
        }, 
        { 
            "id": "m002", 
            "usuario_match": "Sofía Claros", 
            "genero_match": "Femenino", 
            "promo": "Fernet 2x1 Jueves de Frater", 
            "zona": "La Recoleta", 
            "fecha": "10/06/2026", 
            "hora": "20:00", 
            "reseña_dada": "Muy puntual y simpática", 
            "puntuacion_dada": 5 
        } 
    ],
    "pool_solicitudes": [
        {"usuario": "Alejandro Gómez", "genero": "Masculino", "oferta_id": "001", "hora_inicio": 12, "hora_fin": 14, "filtro_genero": False},
        {"usuario": "Sofía Claros", "genero": "Femenino", "oferta_id": "002", "hora_inicio": 12, "hora_fin": 14, "filtro_genero": False},
        {"usuario": "Diego Torrico", "genero": "Masculino", "oferta_id": "001", "hora_inicio": 18, "hora_fin": 20, "filtro_genero": False},
        {"usuario": "Valeria Rocha", "genero": "Femenino", "oferta_id": "001", "hora_inicio": 12, "hora_fin": 14, "filtro_genero": True}
    ],
    "usuarios": {
        "estudiante@universidad.edu.bo": {"nombre": "Carlos Mendoza", "password": "123", "rol": "estudiante", "genero": "Masculino", "universidad": "UCATEC", "confianza": 5.0, "matches": 0, "reportes": 0, "estado": "Activo"},
        "comercio@local.com": {"nombre": "Restaurante Burger Click", "password": "123", "rol": "comercio"}
    }
}

# --- FUNCIONES DE PERSISTENCIA ---
def cargar_datos():
    global base_datos_global
    if os.path.exists("datos_app.json"):
        try:
            with open("datos_app.json", "r", encoding="utf-8") as f:
                base_datos_global = json.load(f)
        except:
            pass
    return base_datos_global

def guardar_datos():
    with open("datos_app.json", "w", encoding="utf-8") as f:
        json.dump(base_datos_global, f, ensure_ascii=False, indent=2)

# --- FUNCIONES DE ANIMACIÓN DE BOTONES ---
def configurar_animacion_boton(boton, color_normal, color_hover, color_active):
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))
    boton.bind("<ButtonPress-1>", lambda e: boton.config(bg=color_active))
    boton.bind("<ButtonRelease-1>", lambda e: boton.config(bg=color_hover))

def configurar_animacion_enlace(boton, color_normal, color_hover):
    boton.bind("<Enter>", lambda e: boton.config(fg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(fg=color_normal))

