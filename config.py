
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# --- PALETA DE COLORES OFICIAL ACTUALIZADA ---
COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_MUTED = "#A0A0A0"
COLOR_SUCCESS = "#2ECC71"
COLOR_SUCCESS_HOVER = "#27AE60"
COLOR_ESCUDO_RED = "#C41430"
COLOR_ACCENT_RED = "#FF1E39"
COLOR_RED_HOVER = "#FF4D63"
COLOR_RED_ACTIVE = "#990A15"
COLOR_RAYO_YELLOW = "#FFCC00"
COLOR_CORAL_FUEGO = "#FF2A3A"  # Rojo Coral Fuego
COLOR_AZUL_ELECTRICO = "#007BFF"  # Azul Eléctrico Vivo
COLOR_AMARILLO_ORO = "#FFB800"  # Amarillo Oro
COLOR_NAV = "#1A1A1A"

# --- CONFIGURACIÓN DE POSTGRESQL ---
DB_CONFIG = {
    'dbname': 'twopack_db',
    'user': 'twopack_user',
    'password': 'twopack_password',
    'host': 'localhost',
    'port': '5432'
}

# --- BASE DE DATOS COMPARTIDA ACTUALIZADA ---
base_datos_global = {
    "promociones": [
        {
            "id": "001",
            "titulo": "2x1 en Hamburguesas Premium",
            "cat": "Gastronomía",
            "zona": "Zona Centro / Calle Comercio",
            "vence": "30/06/2026",
            "precio_ref": "55",
            "comercio": "Burger Hub",
            "distancia": "400 m",
            "hora_hasta": "22:00",
            "demanda": "Alta Demanda",
            "descripcion": (
                "Disfruta de dos combos completos de hamburguesas premium por el precio de uno. "
                "Perfecto para una reunión profesional o plan casual."
            )
        },
        {
            "id": "002",
            "titulo": "2x1 en Noches de Bowling",
            "cat": "Entretenimiento",
            "zona": "Zona Sur / Mall Las Brisas",
            "vence": "31/07/2026",
            "precio_ref": "40",
            "comercio": "Strike Zone",
            "distancia": "1.2 km",
            "hora_hasta": "23:00",
            "demanda": "Media Demanda",
            "descripcion": (
                "Paga una línea completa y juega dos. Ideal para desconectar después del trabajo "
                "con otros jóvenes profesionales."
            )
        },
        {
            "id": "003",
            "titulo": "2x1 en Café Especial",
            "cat": "Tiendas Locales",
            "zona": "Zona El Prado / Café D'Crem",
            "vence": "15/07/2026",
            "precio_ref": "28",
            "comercio": "Café D'Crem",
            "distancia": "600 m",
            "hora_hasta": "19:00",
            "demanda": "Baja Demanda",
            "descripcion": (
                "Dos cafés especiales (latte art o capuchino por el precio de uno. "
                "Para tus reuniones laborales o planificación de proyectos."
            )
        },
        {
            "id": "004",
            "titulo": "2x1 en Entradas de Cine",
            "cat": "Entretenimiento",
            "zona": "Zona Este / Cine Prime Center",
            "vence": "30/06/2026",
            "precio_ref": "35",
            "comercio": "Cine Prime",
            "distancia": "800 m",
            "hora_hasta": "23:30",
            "demanda": "Alta Demanda",
            "descripcion": (
                "Compra una entrada y lleva a un acompañante gratis en tandas de tarde. "
                "Para disfrutar de estrenos con amigos o compañeros de trabajo."
            )
        },
        {
            "id": "005",
            "titulo": "2x1 en Clases de Yoga",
            "cat": "Deportes / Bienestar",
            "zona": "Zona Norte / Wellness Center",
            "vence": "15/07/2026",
            "precio_ref": "45",
            "comercio": "Wellness Lab",
            "distancia": "1.5 km",
            "hora_hasta": "21:00",
            "demanda": "Media Demanda",
            "descripcion": (
                "Trae a un amigo y ambos entrenan por el precio de una clase. "
                "Mantén el equilibrio entre vida laboral y personal."
            )
        },
        {
            "id": "006",
            "titulo": "2x1 en Evento de Networking",
            "cat": "Eventos",
            "zona": "Zona El Prado / Hub Emprendedor",
            "vence": "31/07/2026",
            "precio_ref": "80",
            "comercio": "Hub Emprendedor",
            "distancia": "500 m",
            "hora_hasta": "20:00",
            "demanda": "Alta Demanda",
            "descripcion": (
                "Asiste a nuestro exclusivo evento de networking para jóvenes profesionales. "
                "Dos entradas por el precio de una, perfecto para conocer contactos."
            )
        }
    ],
    "historial_matches": [ 
        { 
            "id": "m001", 
            "usuario_match": "Ana Paredes", 
            "genero_match": "Femenino", 
            "promo": "2x1 en Noches de Bowling", 
            "zona": "Zona Sur / Mall Las Brisas", 
            "fecha": "18/06/2026", 
            "hora": "19:30", 
            "reseña_dada": "Muy buena experiencia, cumplidos al 100%!", 
            "puntuacion_dada": 5 
        }, 
        { 
            "id": "m002", 
            "usuario_match": "Carlos López", 
            "genero_match": "Masculino", 
            "promo": "2x1 en Café Especial", 
            "zona": "Zona El Prado / Café D'Crem", 
            "fecha": "15/06/2026", 
            "hora": "16:00", 
            "reseña_dada": "Genial para coordinar un plan laboral rápido", 
            "puntuacion_dada": 4 
        } 
    ],
    "pool_solicitudes": [
        {"usuario": "Ana Paredes", "genero": "Femenino", "oferta_id": "001", "hora_inicio": 13, "hora_fin": 15, "filtro_genero": False},
        {"usuario": "Carlos López", "genero": "Masculino", "oferta_id": "003", "hora_inicio": 16, "hora_fin": 18, "filtro_genero": False},
        {"usuario": "Daniela Uribe", "genero": "Femenino", "oferta_id": "002", "hora_inicio": 19, "hora_fin": 21, "filtro_genero": False}
    ],
    "usuarios": {
        "usuario@profesional.com": {"nombre": "María Fernández", "password": "123", "rol": "usuario", "genero": "Femenino", "profesion": "Marketing Digital", "confianza": 5.0, "matches": 3, "reportes": 0, "estado": "Activo"},
        "comercio@local.com": {"nombre": "Restaurante Sabores", "password": "123", "rol": "comercio"}
    }
}

# --- FUNCIONES DE CONEXIÓN A LA BASE DE DATOS ---
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# --- FUNCIONES DE PERSISTENCIA ---
def cargar_datos():
    global base_datos_global
    if os.path.exists("datos_app.json"):
        try:
            with open("datos_app.json", "r", encoding="utf-8") as f:
                base_datos_global = json.load(f)
        except Exception:
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

def configurar_animacion_enlace(enlace, color_normal, color_hover):
    enlace.bind("<Enter>", lambda e: enlace.config(fg=color_hover))
    enlace.bind("<Leave>", lambda e: enlace.config(fg=color_normal))
