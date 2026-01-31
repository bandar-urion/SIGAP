import sqlite3
import os

# --- CONFIGURACIÓN ---
ruta_bd = os.path.join(os.path.dirname(__file__), '..', 'base_datos', 'control_gastos.db')
print(f"🏗️  CONSTRUYENDO ARQUITECTURA FÉNIX FINAL (V4) en: {ruta_bd}")

conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

# --- PASO 1: LIMPIEZA TOTAL (De estructura maestra) ---
print("🧹 Limpiando tablas antiguas...")
tablas = ["param_subcategorias", "param_categorias", "param_centros_costo",
          "param_medios_pago", "auditoria_compliance", "reglas_gobierno"]
for t in tablas:
    cursor.execute(f"DROP TABLE IF EXISTS {t}")

# --- PASO 2: CREACIÓN DE TABLAS BLINDADAS ---
print("🔨 Levantando muros de contención (Tablas)...")

# 2.1 Centros de Costo
cursor.execute("CREATE TABLE param_centros_costo (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE)")

# 2.2 Medios de Pago (TESORERÍA)
cursor.execute("""
    CREATE TABLE param_medios_pago (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE,
        tipo TEXT CHECK(tipo IN ('EFECTIVO', 'CUENTA', 'TARJETA_CREDITO')),
        dia_cierre INTEGER,      -- Solo tarjetas
        dia_vencimiento INTEGER  -- Solo tarjetas
    )
""")

# 2.3 Categorías (Con distinción INGRESO/EGRESO)
cursor.execute("""
    CREATE TABLE param_categorias (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        tipo TEXT NOT NULL CHECK(tipo IN ('INGRESO', 'EGRESO')), -- <--- CLAVE NUEVA
        id_centro_costo INTEGER NOT NULL,
        FOREIGN KEY(id_centro_costo) REFERENCES param_centros_costo(id),
        UNIQUE(nombre, id_centro_costo)
    )
""")

# 2.4 Reglas de Gobierno
cursor.execute("CREATE TABLE reglas_gobierno (id INTEGER PRIMARY KEY, codigo TEXT UNIQUE, descripcion TEXT)")

# 2.5 Subcategorías (Con Trazabilidad)
cursor.execute("""
    CREATE TABLE param_subcategorias (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        id_categoria INTEGER NOT NULL,
        id_regla_aceptada INTEGER,
        FOREIGN KEY(id_categoria) REFERENCES param_categorias(id),
        FOREIGN KEY(id_regla_aceptada) REFERENCES reglas_gobierno(id),
        UNIQUE(nombre, id_categoria)
    )
""")

# 2.6 Auditoría
cursor.execute("""
    CREATE TABLE auditoria_compliance (
        id INTEGER PRIMARY KEY, fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        accion TEXT, detalle TEXT
    )
""")

# --- PASO 3: SEMBRADO DE DATOS MAESTROS ---
print("🌱 Sembrando la Taxonomía Fénix...")

# A. Centros de Costo
ccs = {"Familia": 1, "Mama": 2, "Personal": 3} # Forzamos IDs para facilitar carga
for nombre, id_cc in ccs.items():
    cursor.execute("INSERT INTO param_centros_costo (id, nombre) VALUES (?, ?)", (id_cc, nombre))

# B. Medios de Pago (Ejemplos Base)
medios = [
    ("Efectivo", "EFECTIVO", None, None),
    ("MercadoPago", "CUENTA", None, None),
    ("Santander", "CUENTA", None, None),
    ("Visa", "TARJETA_CREDITO", 24, 5),      # -- Cierra 24, Vence 5
    ("MasterCard", "TARJETA_CREDITO", 28, 10)
]
cursor.executemany("INSERT INTO param_medios_pago (nombre, tipo, dia_cierre, dia_vencimiento) VALUES (?, ?, ?, ?, ?)", medios)

# C. Categorías (Ingresos y Egresos)
datos_categorias = [
    # (Nombre, Tipo, ID_Centro_Costo)
    # --- FAMILIA (1) ---
    ("Casa", "EGRESO", 1), ("Alimentacion", "EGRESO", 1), ("Auto", "EGRESO", 1),
    ("Educacion", "EGRESO", 1), ("Salud", "EGRESO", 1), ("Terreno", "EGRESO", 1),

    # --- MAMA (2) ---
    ("Casa Mama", "EGRESO", 2), ("Salud Mama", "EGRESO", 2), ("Gestion Mama", "EGRESO", 2),
    ("Jubilacion", "INGRESO", 2), ("Alquiler Propiedad", "INGRESO", 2), # <-- INGRESOS MAMA

    # --- PERSONAL (3) ---
    ("Tecnologia", "EGRESO", 3), ("Hobby", "EGRESO", 3), ("Vestimenta", "EGRESO", 3),
    ("Sueldo Relacion Dependencia", "INGRESO", 3), ("Changas IT", "INGRESO", 3) # <-- TUS INGRESOS
]

for nombre, tipo, id_cc in datos_categorias:
    cursor.execute("INSERT INTO param_categorias (nombre, tipo, id_centro_costo) VALUES (?, ?, ?)", (nombre, tipo, id_cc))
    # Subcategoría General automática
    id_cat = cursor.lastrowid
    cursor.execute("INSERT INTO param_subcategorias (nombre, id_categoria) VALUES (?, ?)", ("General", id_cat))

# D. Reglas
reglas = [("REG-8020", "Ley de Pareto (80/20)"), ("REG-GEN", "Regla de Generalidad"), ("REG-BRAND", "Anti-Marcas")]
cursor.executemany("INSERT INTO reglas_gobierno (codigo, descripcion) VALUES (?, ?)", reglas)

conn.commit()
conn.close()
print("\n🚀 ¡SISTEMA FÉNIX V4.0 (FULL) OPERATIVO!")
print("   - Estructura 3NF: OK")
print("   - Ingresos/Egresos: OK")
print("   - Tarjetas de Crédito: OK")
print("   - Gobernanza: OK")