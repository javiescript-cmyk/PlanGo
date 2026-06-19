from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="PlanMatch AI - Backend Core",
    description="API para el emparejamiento y citas basadas en intereses comunes.",
    version="1.0.0"
)

# --- MODELOS DE DATOS (Pydantic) ---

class UserPreferences(BaseModel):
    gender_interest: str  # "Masculino", "Femenino", "Todos"
    min_age: int = Field(default=18, ge=18)
    max_age: int = Field(default=99, le=99)
    preferred_plan_type: str  # "Fiesta", "Cena", "Viaje", "Tranquilo"

class User(BaseModel):
    id: int
    name: str
    age: int
    gender: str  # "Masculino", "Femenino", "Otro"
    city: str  # Ejemplo: "Cochabamba"
    interests: List[str]  # Ejemplo: ["Trekking", "Alitas", "Cine", "Anime"]
    preferences: UserPreferences
    bio: Optional[str] = None

# --- BASE DE DATOS SIMULADA (Para desarrollo rápido en los 5 días) ---
# Aquí simulamos usuarios registrados en la app para poder probar los matches de inmediato.
db_users = [
    User(
        id=1, name="Carlos", age=22, gender="Masculino", city="Cochabamba",
        interests=["Trekking", "Alitas", "Fotografía", "Viajes"],
        preferences=UserPreferences(gender_interest="Femenino", min_age=18, max_age=25, preferred_plan_type="Viaje"),
        bio="Buscando conocer gente para viajar el finde."
    ),
    User(
        id=2, name="Andrea", age=21, gender="Femenino", city="Cochabamba",
        interests=["Trekking", "Cine", "Viajes", "Café"],
        preferences=UserPreferences(gender_interest="Masculino", min_age=20, max_age=26, preferred_plan_type="Viaje"),
        bio="Amo viajar y conocer lugares nuevos."
    ),
    User(
        id=3, name="Sofía", age=24, gender="Femenino", city="Cochabamba",
        interests=["Fiesta", "Alitas", "Bailar", "Boliche"],
        preferences=UserPreferences(gender_interest="Masculino", min_age=18, max_age=30, preferred_plan_type="Fiesta"),
        bio="Salir por unas cervezas y bailar."
    ),
]

# --- LÓGICA DE IA / ALGORITMO DE COMPATIBILIDAD ---

def calculate_match_score(user_a: User, user_b: User) -> float:
    """
    Calcula un porcentaje de compatibilidad basado en la intersección de sus intereses.
    Utiliza el índice de Jaccard: (Intersección / Unión) * 100
    """
    set_a = set(user_a.interests)
    set_b = set(user_b.interests)
    
    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)
    
    if not union:
        return 0.0
        
    return round((len(intersection) / len(union)) * 100, 2)

# --- ENDPOINTS (API RUTAS) ---

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Core de PlanMatch AI"}

@app.get("/users", response_model=List[User])
def get_all_users():
    return db_users

@app.post("/matchmaking/{user_id}", response_model=List[dict])
def get_matches_for_user(user_id: int):
    # 1. Buscar al usuario que solicita los matches
    current_user = next((u for u in db_users if u.id == user_id), None)
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    suggestions = []
    
    # 2. Filtrar y calcular afinidad con el resto de los usuarios
    for candidate in db_users:
        if candidate.id == current_user.id:
            continue  # No emparejar consigo mismo
            
        # Filtro estricto de ubicación
        if candidate.city != current_user.city:
            continue
            
        # Filtro estricto de orientación sexual mutua
        if current_user.preferences.gender_interest != "Todos" and candidate.gender != current_user.preferences.gender_interest:
            continue
        if candidate.preferences.gender_interest != "Todos" and current_user.gender != candidate.preferences.gender_interest:
            continue
            
        # Filtro estricto de rango de edad mutuo
        if not (current_user.preferences.min_age <= candidate.age <= current_user.preferences.max_age):
            continue
        if not (candidate.preferences.min_age <= current_user.age <= candidate.preferences.max_age):
            continue
            
        # 3. Si pasa los filtros, calculamos el porcentaje de afinidad de la IA
        score = calculate_match_score(current_user, candidate)
        
        # Opcional: bonus si coinciden en el tipo de plan favorito
        if current_user.preferences.preferred_plan_type == candidate.preferences.preferred_plan_type:
            score += 10
            if score > 100: score = 100

        suggestions.append({
            "id": candidate.id,
            "name": candidate.name,
            "age": candidate.age,
            "bio": candidate.bio,
            "interests": candidate.interests,
            "match_score": f"{score}%",
            "preferred_plan": candidate.preferences.preferred_plan_type
        })
        
    # Ordenar las sugerencias de mayor a menor compatibilidad
    suggestions = sorted(suggestions, key=lambda x: float(x["match_score"].replace("%", "")), reverse=True)
    
    return suggestions