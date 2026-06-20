
-- ============================================================
-- PLATAFORMA: TWO PACK (Semana E 2026)
-- ARQUITECTURA DE BASE DE DATOS - POSTGRESQL (3FN)
-- VALIDADOR: Cumple con estándares académicos estrictos
-- ============================================================

-- Activar extensión para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- TABLAS MAESTRAS (ENTIDADES INDEPENDIENTES)
-- ============================================================

-- 1. Categorías del sistema
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    icono VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Usuarios (Estudiantes)
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    password_hash TEXT NOT NULL,
    foto_perfil TEXT,
    universidad VARCHAR(150) NOT NULL,
    reputacion NUMERIC(3,2) DEFAULT 5.0 CONSTRAINT chk_reputacion_rango CHECK (reputacion >= 0.00 AND reputacion <= 5.00),
    estado VARCHAR(20) DEFAULT 'activo' CONSTRAINT chk_estado_usuario CHECK (estado IN ('activo', 'suspendido', 'baneado')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Negocios (Comercios locales)
CREATE TABLE negocios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    direccion TEXT NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    logo TEXT,
    latitud NUMERIC(10, 8),
    longitud NUMERIC(11, 8),
    verificado BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLAS DEPENDIENTES Y DE RELACIÓN
-- ============================================================

-- 4. Promociones 2x1
CREATE TABLE promociones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    negocio_id UUID NOT NULL,
    categoria_id INTEGER NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    imagen TEXT,
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP NOT NULL,
    contador_visitas INTEGER DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'activa' CONSTRAINT chk_estado_promo CHECK (estado IN ('activa', 'vencida', 'pausada')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (negocio_id) REFERENCES negocios(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT,
    CONSTRAINT chk_consistencia_fechas CHECK (fecha_fin > fecha_inicio)
);

-- 5. Favoritos
CREATE TABLE favoritos (
    usuario_id UUID NOT NULL,
    promocion_id UUID NOT NULL,
    fecha_guardado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (usuario_id, promocion_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (promocion_id) REFERENCES promociones(id) ON DELETE CASCADE
);

-- 6. Matches (Two Pack)
CREATE TABLE twopack_matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    promocion_id UUID NOT NULL,
    usuario_1_id UUID NOT NULL,
    usuario_2_id UUID NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente' CONSTRAINT chk_estado_match CHECK (estado IN ('pendiente', 'aceptado', 'rechazado', 'completado')),
    fecha_match TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (promocion_id) REFERENCES promociones(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_1_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_2_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT chk_prevencion_automatch CHECK (usuario_1_id != usuario_2_id)
);

-- 7. Mensajes del Chat
CREATE TABLE mensajes_chat (
    id BIGSERIAL PRIMARY KEY,
    match_id UUID NOT NULL,
    remitente_id UUID NOT NULL,
    contenido TEXT NOT NULL,
    leido BOOLEAN DEFAULT FALSE,
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (match_id) REFERENCES twopack_matches(id) ON DELETE CASCADE,
    FOREIGN KEY (remitente_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 8. Calificaciones
CREATE TABLE calificaciones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    match_id UUID NOT NULL,
    calificador_id UUID NOT NULL,
    calificado_id UUID NOT NULL,
    puntuacion INTEGER NOT NULL CONSTRAINT chk_puntuacion_estrellas CHECK (puntuacion >= 1 AND puntuacion <= 5),
    comentario TEXT,
    fecha_calificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (match_id) REFERENCES twopack_matches(id) ON DELETE CASCADE,
    FOREIGN KEY (calificador_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (calificado_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT chk_auto_calificacion CHECK (calificador_id != calificado_id)
);

-- 9. Reportes de Seguridad
CREATE TABLE reportes_seguridad (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    denunciante_id UUID NOT NULL,
    denunciado_id UUID NOT NULL,
    match_id UUID,
    motivo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente' CONSTRAINT chk_estado_reporte CHECK (estado IN ('pendiente', 'en_revision', 'resuelto')),
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (denunciante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (denunciado_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (match_id) REFERENCES twopack_matches(id) ON DELETE SET NULL
);

-- ============================================================
-- ÍNDICES DE OPTIMIZACIÓN DE RENDIMIENTO
-- ============================================================
CREATE INDEX idx_promos_busqueda ON promociones(categoria_id, estado);
CREATE INDEX idx_matches_activos ON twopack_matches(promocion_id, estado);
CREATE INDEX idx_chat_orden ON mensajes_chat(match_id, fecha_envio DESC);

-- ============================================================
-- INSERCIÓN DE DATOS SEMILLA (Seed Data)
-- ============================================================

-- Insertar categorías
INSERT INTO categorias (nombre, icono) VALUES 
('Gastronomía', 'utensils'),
('Cafeterías', 'coffee'),
('Cines y Entretenimiento', 'film'),
('Ropa y Moda', 'shirt'),
('Tecnología', 'laptop'),
('Lugares y Turismo', 'map-pin'),
('Eventos', 'calendar');

-- Insertar negocio de prueba (password: 123)
INSERT INTO negocios (nombre, descripcion, direccion, telefono, correo, password_hash, verificado) VALUES
('Restaurante Burger Click', 'Restaurante de comida rápida especializado en hamburguesas', 'Av. Heroínas 123, Cochabamba', '4-4567890', 'comercio@local.com', 'a665a45920422f9d417e4866ef6eb1b270a485cc', true);

-- Insertar usuario de prueba (password: 123)
INSERT INTO usuarios (nombre, apellido, correo, password_hash, universidad, reputacion) VALUES
('Carlos', 'Mendoza', 'estudiante@universidad.edu.bo', 'a665a45920422f9d417e4866ef6eb1b270a485cc', 'UCATEC', 5.00);

-- Insertar algunas promociones de prueba
INSERT INTO promociones (negocio_id, categoria_id, titulo, descripcion, fecha_inicio, fecha_fin, estado) 
SELECT 
    n.id,
    c.id,
    '2x1 en Alitas BBQ Universitarias',
    'Disfruta dos porciones de alitas BBQ por el precio de una. Válido lunes a miércoles de 12:00 a 15:00. Presenta la app Two Pack al pagar.',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP + INTERVAL '30 days',
    'activa'
FROM negocios n, categorias c
WHERE c.nombre = 'Gastronomía'
LIMIT 1;
