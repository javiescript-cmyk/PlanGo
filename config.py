
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

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

# --- CONFIGURACIÓN DE POSTGRESQL ---
DB_CONFIG = {
    'dbname': 'twopack_db',
    'user': 'twopack_user',
    'password': 'twopack_password',
    'host': 'localhost',
    'port': '5432'
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

# --- FUNCIONES DE ANIMACIÓN DE BOTONES ---
def configurar_animacion_boton(boton, color_normal, color_hover, color_active):
    boton.bind("&lt;Enter&gt;", lambda e: boton.config(bg=color_hover))
    boton.bind("&lt;Leave&gt;", lambda e: boton.config(bg=color_normal))
    boton.bind("&lt;ButtonPress-1&gt;", lambda e: boton.config(bg=color_active))
    boton.bind("&lt;ButtonRelease-1&gt;", lambda e: boton.config(bg=color_hover))

def configurar_animacion_enlace(boton, color_normal, color_hover):
    boton.bind("&lt;Enter&gt;", lambda e: boton.config(fg=color_hover))
    boton.bind("&lt;Leave&gt;", lambda e: boton.config(fg=color_normal))
