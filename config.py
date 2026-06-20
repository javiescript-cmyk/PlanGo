
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
            "id": "P000",
            "titulo": "Combo Alitas 2x1 Expira Hoy",
            "cat": "Gastronomía",
            "zona": "Zona Centro",
            "vence": "20/06/2026",
            "precio_ref": "45",
            "comercio": "Alitas Express",
            "distancia": "400 m",
            "hora_hasta": "22:00",
            "demanda": "Muy Alta Demanda",
            "descripcion": "¡¡Combo de alitas 2x1 que vence HOY!! ¡No te lo pierdas! 🔥🔥🔥"
        },
        {
            "id": "P001",
            "titulo": "Combo Universitario 2x1",
            "cat": "Gastronomía",
            "zona": "Zona Norte / UCATEC",
            "vence": "30/06/2026",
            "precio_ref": "45",
            "comercio": "Pizza Campus",
            "distancia": "300 m",
            "hora_hasta": "22:00",
            "demanda": "Alta Demanda",
            "descripcion": "Combo 2x1 de pizza grande + bebidas para estudiantes de UCATEC. ¡Perfecto para entre clases!"
        },
        {
            "id": "P002",
            "titulo": "Balde de Alitas 2x1",
            "cat": "Gastronomía",
            "zona": "La Recoleta / Calle 21",
            "vence": "28/06/2026",
            "precio_ref": "75",
            "comercio": "Wing Station",
            "distancia": "800 m",
            "hora_hasta": "23:00",
            "demanda": "Muy Alta Demanda",
            "descripcion": "2x1 en baldes de 20 alitas BBQ o picantes. ¡Ideal para ver partidos con amigos!"
        },
        {
            "id": "P003",
            "titulo": "2x1 Hamburguesas Gourmet",
            "cat": "Gastronomía",
            "zona": "El Prado / Av. Ballivián",
            "vence": "30/06/2026",
            "precio_ref": "65",
            "comercio": "BurgerLab",
            "distancia": "700 m",
            "hora_hasta": "21:30",
            "demanda": "Media Demanda",
            "descripcion": "2x1 en hamburguesas de res premium con papas fritas y salsa especial."
        },
        {
            "id": "E001",
            "titulo": "2x1 Entradas Miércoles Estreno",
            "cat": "Entretenimiento",
            "zona": "Zona Centro / Cine Center",
            "vence": "31/07/2026",
            "precio_ref": "40",
            "comercio": "Cine Center",
            "distancia": "500 m",
            "hora_hasta": "23:30",
            "demanda": "Alta Demanda",
            "descripcion": "2x1 en entradas de cine los miércoles para todos los estrenos del mes!"
        },
        {
            "id": "E002",
            "titulo": "2x1 en Prime Cinemas",
            "cat": "Entretenimiento",
            "zona": "Zona Norte / Av. América",
            "vence": "31/07/2026",
            "precio_ref": "45",
            "comercio": "Prime Cinemas",
            "distancia": "1.2 km",
            "hora_hasta": "23:00",
            "demanda": "Media Demanda",
            "descripcion": "2x1 entradas 2D de lunes a jueves. Incluye combo de palomitas!"
        },
        {
            "id": "A001",
            "titulo": "Tarifa Pack Fin de Semana 2x1",
            "cat": "Alojamientos",
            "zona": "Cala Cala / Hotel Boutique",
            "vence": "31/08/2026",
            "precio_ref": "350",
            "comercio": "Cala Cala Suites",
            "distancia": "2.5 km",
            "hora_hasta": "24:00",
            "demanda": "Baja Demanda",
            "descripcion": "2x1 en habitaciones dobles para fin de semana. Incluye desayuno buffet!"
        },
        {
            "id": "A002",
            "titulo": "2x1 Noche en Hostal",
            "cat": "Alojamientos",
            "zona": "El Prado / Hostal Central",
            "vence": "30/06/2026",
            "precio_ref": "120",
            "comercio": "Hostal El Prado",
            "distancia": "600 m",
            "hora_hasta": "24:00",
            "demanda": "Media Demanda",
            "descripcion": "2x1 en habitaciones compartidas o privadas. Perfecto para viajeros!"
        },
        {
            "id": "D001",
            "titulo": "Pase Libre 2x1 Mensual",
            "cat": "Deportes",
            "zona": "Zona Norte / SmartFit",
            "vence": "30/06/2026",
            "precio_ref": "180",
            "comercio": "SmartFit Zona Norte",
            "distancia": "1.1 km",
            "hora_hasta": "22:00",
            "demanda": "Alta Demanda",
            "descripcion": "2x1 en membresías mensuales de gimnasio. Incluye clases grupales!"
        },
        {
            "id": "D002",
            "titulo": "2x1 Clases de CrossFit",
            "cat": "Deportes",
            "zona": "Av. América / CrossFit CBBA",
            "vence": "15/07/2026",
            "precio_ref": "90",
            "comercio": "CrossFit Cochabamba",
            "distancia": "1.5 km",
            "hora_hasta": "21:00",
            "demanda": "Media Demanda",
            "descripcion": "2x1 en paquetes de 10 clases de CrossFit. ¡Ponte en forma con un amigo!"
        },
        {
            "id": "S001",
            "titulo": "2x1 Packs de Snacks/Bebidas",
            "cat": "Supermercados",
            "zona": "Zona Centro / Fidalga",
            "vence": "30/06/2026",
            "precio_ref": "30",
            "comercio": "Fidalga Centro",
            "distancia": "450 m",
            "hora_hasta": "21:00",
            "demanda": "Alta Demanda",
            "descripcion": "2x1 en packs de snacks, bebidas y galletas. ¡Stocka tu nevera!"
        },
        {
            "id": "S002",
            "titulo": "2x1 en Frutas y Verduras",
            "cat": "Supermercados",
            "zona": "Zona Sur / Mercado 25 de Mayo",
            "vence": "28/06/2026",
            "precio_ref": "25",
            "comercio": "Mercado 25 de Mayo",
            "distancia": "1.8 km",
            "hora_hasta": "18:00",
            "demanda": "Media Demanda",
            "descripcion": "2x1 en kg de frutas y verduras frescas todos los días!"
        },
        {
            "id": "F001",
            "titulo": "2x1 Manillas de Ingreso",
            "cat": "Fiestas",
            "zona": "Pasaje Aranjuez / Club XYZ",
            "vence": "30/06/2026",
            "precio_ref": "50",
            "comercio": "Club Aranjuez",
            "distancia": "900 m",
            "hora_hasta": "03:00",
            "demanda": "Muy Alta Demanda",
            "descripcion": "2x1 en manillas de ingreso los sábados. Incluye una bebida gratis!"
        },
        {
            "id": "F002",
            "titulo": "2x1 Covers en Discoteca",
            "cat": "Fiestas",
            "zona": "Av. América / The Roof",
            "vence": "31/07/2026",
            "precio_ref": "60",
            "comercio": "The Roof Skybar",
            "distancia": "1.4 km",
            "hora_hasta": "04:00",
            "demanda": "Alta Demanda",
            "descripcion": "2x1 en covers de discoteca con vista 360° de la ciudad!"
        },
        {
            "id": "C001",
            "titulo": "2x1 Café Especial",
            "cat": "Cafeterías",
            "zona": "Zona El Prado / Café D'Crem",
            "vence": "15/07/2026",
            "precio_ref": "28",
            "comercio": "Café D'Crem",
            "distancia": "600 m",
            "hora_hasta": "19:00",
            "demanda": "Media Demanda",
            "descripcion": "2x1 en cafés especiales (latte, capuchino, flat white). Perfecto para reuniones!"
        },
        {
            "id": "C002",
            "titulo": "2x1 Tés y Pastel",
            "cat": "Cafeterías",
            "zona": "Zona Centro / Tea & Co",
            "vence": "30/06/2026",
            "precio_ref": "35",
            "comercio": "Tea & Co",
            "distancia": "550 m",
            "hora_hasta": "18:30",
            "demanda": "Baja Demanda",
            "descripcion": "2x1 en tés selectos + porción de pastel de queso!"
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
        {"usuario": "ana@universidad.edu.bo", "genero": "Femenino", "oferta_id": "P001", "hora_inicio": 13, "hora_fin": 15, "filtro_genero": False},
        {"usuario": "carlos@universidad.edu.bo", "genero": "Masculino", "oferta_id": "P002", "hora_inicio": 16, "hora_fin": 18, "filtro_genero": False},
        {"usuario": "daniela@universidad.edu.bo", "genero": "Femenino", "oferta_id": "P000", "hora_inicio": 19, "hora_fin": 21, "filtro_genero": False}
    ],
    "usuarios": {
        "ana@universidad.edu.bo": {"nombre": "Ana Paredes", "password": "123", "rol": "estudiante", "genero": "Femenino", "confianza": 5.0, "matches": 4, "reportes": 0, "estado": "Activo"},
        "carlos@universidad.edu.bo": {"nombre": "Carlos López", "password": "123", "rol": "estudiante", "genero": "Masculino", "confianza": 4.5, "matches": 2, "reportes": 0, "estado": "Activo"},
        "daniela@universidad.edu.bo": {"nombre": "Daniela Uribe", "password": "123", "rol": "estudiante", "genero": "Femenino", "confianza": 4.8, "matches": 3, "reportes": 0, "estado": "Activo"},
        "usuario@profesional.com": {"nombre": "María Fernández", "password": "123", "rol": "usuario", "genero": "Femenino", "profesion": "Marketing Digital", "confianza": 5.0, "matches": 3, "reportes": 0, "estado": "Activo"},
        "comercio@local.com": {"nombre": "Restaurante Sabores", "password": "123", "rol": "comercio"},
        "xydarkodayx@ucatec.edu.bo": {"nombre": "karlo dante pacheco valencia", "password": "1008", "rol": "estudiante", "genero": "Masculino", "confianza": 5.0, "matches": 0, "reportes": 0, "estado": "Activo"},
        "oscarmusic@ucatec.edu.bo": {"nombre": "oscar abasto", "password": "oscar1234", "rol": "estudiante", "genero": "Masculino", "confianza": 5.0, "matches": 0, "reportes": 0, "estado": "Activo"}
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
