import sqlite3
import os
import sys

# =============================================================================
# 1. CONFIGURACIÓN DE RUTAS Y ENTORNO (via sigap_config.py)
# =============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import sigap_config
DB_FILE = sigap_config.get_db_path()

def ejecutar_sql(cursor, sql, params=()):
    try:
        cursor.execute(sql, params)
    except sqlite3.Error as e:
        print(f"❌ Error SQL: {e} | Query: {sql}")

def factory_reset_normalized():
    print(f"💎 INICIANDO PROTOCOLO DE NORMALIZACIÓN (S.I.G.A.P.)")
    print(f"    Target DB: {DB_FILE}")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # =============================================================================
    # 2. LIMPIEZA (DROP TABLES)
    # =============================================================================
    print("🧹 Borrando estructuras antiguas y legacy...")
    cursor.execute("PRAGMA foreign_keys = OFF;")

    tablas_a_borrar = [
        # Tablas Operativas
        'movimientos', 'movimientos_v2', 'agenda_pagos', 'auditoria_compliance', 'auditoria_movimientos',

        # Tablas de Parametría
        'param_subcategorias', 'param_categorias',
        'param_medios_pago', 'param_centros_costo',

        # Tablas de Gobernanza
        'reglas_vinculos', 'reglas_catalogo', 'diccionario_terminos',
        'reglas_gobernanza',

        # Limpieza de legacy
        'reglas_gobierno', 'centros_costo', 'movimientos_old_text'
    ]

    for tabla in tablas_a_borrar:
        cursor.execute(f"DROP TABLE IF EXISTS {tabla}")

    # Reiniciar contadores de autoincremento
    try:
        cursor.execute("DELETE FROM sqlite_sequence;")
    except sqlite3.OperationalError:
        pass

    cursor.execute("PRAGMA foreign_keys = ON;")

    # =============================================================================
    # 3. RECONSTRUCCIÓN DE ESQUEMA (DDL)
    # =============================================================================
    print("🏗️  Levantando nuevas tablas de Core y Auditoría...")

    # A. GOBERNANZA
    cursor.execute("""
    CREATE TABLE reglas_catalogo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        descripcion TEXT NOT NULL,
        tipo_alerta TEXT DEFAULT 'BLOQUEANTE'
    );""")

    cursor.execute("""
    CREATE TABLE reglas_vinculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_regla INTEGER NOT NULL,
        entidad_target TEXT NOT NULL,
        FOREIGN KEY (id_regla) REFERENCES reglas_catalogo(id),
        UNIQUE(id_regla, entidad_target)
    );""")

    # B. PARAMETRICAS (CC, Medios, Categorías)
    cursor.execute("CREATE TABLE param_centros_costo (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL UNIQUE);")

    cursor.execute("""
    CREATE TABLE param_medios_pago (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        tipo TEXT CHECK(tipo IN ('EFECTIVO', 'CUENTA', 'TARJETA_CREDITO'))
    );""")

    cursor.execute("""
    CREATE TABLE param_categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        tipo TEXT CHECK(tipo IN ('INGRESO', 'EGRESO'))
    );""")

    cursor.execute("""
    CREATE TABLE param_subcategorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_categoria INTEGER NOT NULL,
        nombre TEXT NOT NULL,
        UNIQUE(nombre, id_categoria),
        FOREIGN KEY (id_categoria) REFERENCES param_categorias(id)
    );""")

    # C. OPERATIVAS (Movimientos y Agenda)
    cursor.execute("""
    CREATE TABLE movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_centro_costo INTEGER NOT NULL,
        id_medio_pago INTEGER NOT NULL,
        id_subcategoria INTEGER NOT NULL,
        fecha DATE NOT NULL,
        descripcion TEXT,
        monto REAL NOT NULL,
        num_referencia TEXT UNIQUE,
        es_amortizable BOOLEAN DEFAULT 0,
        meses_amortizacion INTEGER DEFAULT 0,
        FOREIGN KEY(id_centro_costo) REFERENCES param_centros_costo(id),
        FOREIGN KEY(id_medio_pago) REFERENCES param_medios_pago(id),
        FOREIGN KEY(id_subcategoria) REFERENCES param_subcategorias(id)
    );""")

    cursor.execute("""
    CREATE TABLE agenda_pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_centro_costo INTEGER NOT NULL,
        fecha_vencimiento TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        monto_estimado REAL DEFAULT 0,
        estado TEXT DEFAULT 'PENDIENTE',
        prioridad TEXT DEFAULT 'NORMAL',
        url_pago TEXT,
        FOREIGN KEY (id_centro_costo) REFERENCES param_centros_costo(id)
    );""")

    # D. INTELIGENCIA Y AUDITORÍA
    cursor.execute("""
    CREATE TABLE diccionario_terminos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        termino TEXT NOT NULL UNIQUE,
        id_subcategoria INTEGER NOT NULL,
        FOREIGN KEY (id_subcategoria) REFERENCES param_subcategorias(id)
    );""")

    cursor.execute("""
    CREATE TABLE auditoria_compliance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        entidad TEXT,
        id_entidad INTEGER,
        accion TEXT,
        detalle TEXT,
        usuario TEXT DEFAULT 'SISTEMA'
    );""")

    cursor.execute("""
    CREATE TABLE auditoria_movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),
        usuario TEXT DEFAULT 'SISTEMA',
        accion TEXT NOT NULL,
        id_movimiento_ref INTEGER,
        estado_previo TEXT,
        estado_nuevo TEXT,
        resultado TEXT
    );""")

    # E. ÍNDICES DE PERFORMANCE
    cursor.execute("CREATE INDEX idx_movimientos_fecha ON movimientos(fecha);")
    cursor.execute("CREATE INDEX idx_movimientos_ref ON movimientos(num_referencia);")

    # =============================================================================
    # 4. SIEMBRA DE DATOS (SEEDING) - Explicito para evitar Huerfanos
    # =============================================================================
    print("🌱 Sembrando datos maestros y categorías...")

    # Categorías - param_categorias
    print("   🔹 Mapeando Categorías...")
    categorias_data = [
        ('ALIMENTACION', 'EGRESO'), ('AUTO', 'EGRESO'),  ('CASA', 'EGRESO'),
        ('EDUCACION', 'EGRESO'), ('ENTRETENIMIENTO', 'EGRESO'), ('GUSTOS', 'EGRESO'),
        ('INGRESOS', 'INGRESO'), ('MASCOTA', 'EGRESO'), ('SALUD', 'EGRESO'),
        ('SERVICIOS', 'EGRESO'), ('TECNOLOGIA', 'EGRESO'), ('VARIOS', 'EGRESO')
    ]
    cursor.executemany("INSERT INTO param_categorias (nombre, tipo) VALUES (?, ?)", categorias_data)

    def get_cat_id(nombre_cat):
        cursor.execute("SELECT id FROM param_categorias WHERE nombre = ?", (nombre_cat,))
        res = cursor.fetchone()
        return res[0] if res else None

    # Centros de Costo - param_centros_costo
    centros = [('Personal',), ('Familia',), ('Mamá',)]
    cursor.executemany("INSERT INTO param_centros_costo (nombre) VALUES (?)", centros)

    # Medios de Pago - param_medios_pago
    medios = [
        ('Efectivo', 'EFECTIVO'),
        ('MercadoPago', 'CUENTA'),
        ('Santander', 'CUENTA'),
        ('Santander Visa', 'TARJETA_CREDITO'),
        ('Santander Amex', 'TARJETA_CREDITO'),
        ('MercadoPago Mastercard', 'TARJETA_CREDITO')
    ]
    cursor.executemany("INSERT INTO param_medios_pago (nombre, tipo) VALUES (?, ?)", medios)

    # Subcategorias - param_subcategorias
    print("   🔹 Mapeando Subcategorías...")
    sub_map = {
        'ALIMENTACION': ['Supermercado', 'Almuerzos Laborales'],
        'AUTO': ['Combustible', 'Mantenimiento', 'Seguro', 'Patente'],
        'CASA': ['Mejoras', 'Mantenimiento'],
        'EDUCACION': ['Cuotas', 'Utiles', 'Suscripciones'],
        'ENTRETENIMIENTO': ['DCS World', 'Cine', 'Hobby', 'Suscripciones'],
        'GUSTOS':['Restaurante', 'Comida Preparada', 'Helados'],
        'INGRESOS': ['Sueldo', 'Honorarios', 'Intereses', 'Aguinaldo', 'Premios'],
        'MASCOTA':  ['Alimento', 'Veterinaria', 'Higiene', 'Accesorios/Juguetes'],
        'SALUD': ['Farmacia', 'Obra Social', 'Médicos', 'Gimnasio'],
        'SERVICIOS': ['Luz', 'Gas', 'Internet', 'Celular'],
        'TECNOLOGIA': ['Hardware', 'Software', 'Suscripciones'],
        'VARIOS': ['Gastos Generales','Otros', 'Regalos']
    }

    for cat_nombre, subs in sub_map.items():
        cursor.execute("SELECT id FROM param_categorias WHERE nombre = ?", (cat_nombre,))
        cat_id = cursor.fetchone()
        if cat_id:
            for s in subs:
                ejecutar_sql(cursor, "INSERT INTO param_subcategorias (id_categoria, nombre) VALUES (?, ?)", (cat_id[0], s))

    # Gobernanza - reglas_catalogo
    print("   🔹 Cargando Catálogo de Reglas y Vínculos...")
    reglas_data = [
        ('Regla de Segregación Patrimonial', 'Aislar gestión de gastos (costo de vida separado).', 'BLOQUEANTE', ['param_centros_costo']),
        ('Regla de Abstracción', 'La Categoría define el concepto, no el comercio.', 'BLOQUEANTE', ['param_categorias']),
        ('Regla de Generalidad', 'No usar nombres de marcas comerciales ni detalles irrelevantes.', 'BLOQUEANTE', ['param_categorias', 'param_subcategorias']),
        ('Regla del Impacto', 'Solo crear SC si el gasto es significativo. Si no -> Varios.', 'ADVERTENCIA', ['param_subcategorias']),
        ('Regla de Ejecución', 'Todo MP debe identificar el origen real de los fondos.', 'BLOQUEANTE', ['param_medios_pago']),
        ('Regla de Unicidad', 'Evitar duplicados bancarios mediante num_referencia.', 'BLOQUEANTE', ['movimientos'])
    ]

    for nombre, desc, tipo, targets in reglas_data:
        cursor.execute("INSERT INTO reglas_catalogo (nombre, descripcion, tipo_alerta) VALUES (?, ?, ?)", (nombre, desc, tipo))
        id_regla = cursor.lastrowid
        for target in targets:
            cursor.execute("INSERT INTO reglas_vinculos (id_regla, entidad_target) VALUES (?, ?)", (id_regla, target))

    # Inteligencia - diccionario_terminos
    print("   🔹 Cargando Inteligencia de Términos (Sinónimos)...")

    def get_subcat_id(nombre_sub):
        cursor.execute("SELECT id FROM param_subcategorias WHERE nombre = ?", (nombre_sub,))
        res = cursor.fetchone()
        return res[0] if res else None

    sinonimos_data = [
        ('Comida Preparada', ['Sushi', 'Rotiseria', 'Delivery', 'PedidosYa', 'Pizza']),
        ('Supermercado', ['Despensa', 'Verduleria', 'Almacen', 'Carniceria', 'Chino', 'La Anonima', 'Coto', 'El coyita', 'el coyita']),
        ('Combustible', ['Nafta', 'YPF', 'Shell', 'Axion']),
        ('Hobby', ['Eagle Dynamics', 'Modulo Avion', 'Mapa DCS']),
        ('Almuerzos Laborales', ['la anonima suc010']),
        ('Alimento', ['Sieger','Alimento Perro', 'Bolsa 3kg']),
        ('Veterinaria', ['Vacunas', 'Desparasitante', 'Consulta Veterinaria'])
    ]

    for subcat_nombre, terminos in sinonimos_data:
        sid = get_subcat_id(subcat_nombre)
        if sid:
            for term in terminos:
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO diccionario_terminos (termino, id_subcategoria) VALUES (?, ?)",
                        (term, sid)
                    )
                except sqlite3.Error as e:
                    print(f"      ⚠️ Error al cargar término '{term}': {e}")
        else:
            print(f"      ⚠️ Alerta: No se encontró la subcategoría '{subcat_nombre}' para cargar sus términos.")

    # =============================================================================
    # 5. FINALIZACIÓN
    # =============================================================================
    conn.commit()
    conn.close()
    print(f"\n✅ PROTOCOLO FINALIZADO. La estructura de {DB_FILE} es ahora 100% compatible.")

if __name__ == "__main__":
    factory_reset_normalized()