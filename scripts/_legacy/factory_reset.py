import sqlite3

DB_FILE = 'control_gastos.db'

def ejecutar_sql(cursor, sql, params=()):
    try:
        cursor.execute(sql, params)
    except sqlite3.Error as e:
        print(f"❌ Error SQL: {e} | Query: {sql}")

def factory_reset_normalized():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print("💎 INICIANDO PROTOCOLO DE NORMALIZACIÓN (RELATIONAL GOVERNANCE)...")

    # ---------------------------------------------------------
    # 1. DESTRUCCIÓN (DROP)
    # ---------------------------------------------------------
    cursor.execute("PRAGMA foreign_keys = OFF;")

    tablas = [
        # Tablas Operativas
        'movimientos', 'movimientos_v2', 'agenda_pagos',

        # Tablas de Parametría
        'param_subcategorias', 'param_categorias',
        'param_medios_pago', 'param_centros_costo',

        # Tablas de Gobernanza (NUEVAS)
        'reglas_vinculos', 'reglas_catalogo',

        # Limpieza de legacy
        'reglas_gobierno', 'centros_costo', 'movimientos_old_text',

        # Tabla de Auditoria (log interno)
        'auditoria_compliance'
    ]

    for tabla in tablas:
        cursor.execute(f"DROP TABLE IF EXISTS {tabla}")

    try:
        cursor.execute("DELETE FROM sqlite_sequence;")
    except sqlite3.OperationalError:
        pass

    cursor.execute("PRAGMA foreign_keys = ON;")

    # ---------------------------------------------------------
    # 2. RECONSTRUCCIÓN (CREATE)
    # ---------------------------------------------------------
    print("🏗️  LEVANTANDO ESTRUCTURA NORMALIZADA...")

    # --- A. GOBERNANZA (EL NUEVO CEREBRO) ---

    # 1. El Catálogo de Leyes (Definición única)
    cursor.execute("""
    CREATE TABLE reglas_catalogo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        descripcion TEXT NOT NULL,
        tipo_alerta TEXT DEFAULT 'BLOQUEANTE' -- BLOQUEANTE / ADVERTENCIA
    );
    """)

    # 2. La Tabla Intermedia (Dónde aplica cada ley)
    cursor.execute("""
    CREATE TABLE reglas_vinculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_regla INTEGER NOT NULL,
        entidad_target TEXT NOT NULL, -- Nombre de la tabla destino (Ej: 'param_categorias')

        FOREIGN KEY (id_regla) REFERENCES reglas_catalogo(id),
        UNIQUE(id_regla, entidad_target) -- Evita vincular la misma regla 2 veces a la misma tabla
    );
    """)

    # --- B. PARAMÉTRICAS ---
    cursor.execute("""
    CREATE TABLE param_centros_costo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE param_medios_pago (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        tipo TEXT CHECK(tipo IN ('EFECTIVO', 'CUENTA', 'TARJETA_CREDITO'))
    );
    """)

    cursor.execute("""
    CREATE TABLE param_categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        tipo TEXT CHECK(tipo IN ('INGRESO', 'EGRESO'))
    );
    """)

    cursor.execute("""
    CREATE TABLE param_subcategorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_categoria INTEGER NOT NULL,
        nombre TEXT NOT NULL,
        UNIQUE(nombre, id_categoria),
        FOREIGN KEY (id_categoria) REFERENCES param_categorias(id)
    );
    """)

    # --- C. OPERATIVAS ---
    cursor.execute("""
    CREATE TABLE agenda_pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_centro_costo INTEGER NOT NULL,
        fecha_vencimiento TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        monto_estimado REAL DEFAULT 0,
        estado TEXT DEFAULT 'PENDIENTE',
        prioridad TEXT DEFAULT 'NORMAL',
        FOREIGN KEY (id_centro_costo) REFERENCES param_centros_costo(id)
    );
    """)

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
        es_amortizable BOOLEAN DEFAULT 0 CHECK (es_amortizable IN (0, 1)),
        meses_amortizacion INTEGER DEFAULT 0,
        fecha_fin_amortizacion DATE,
        FOREIGN KEY(id_centro_costo) REFERENCES param_centros_costo(id),
        FOREIGN KEY(id_medio_pago) REFERENCES param_medios_pago(id),
        FOREIGN KEY(id_subcategoria) REFERENCES param_subcategorias(id)
    );
    """)

    print("✅ Estructura Normalizada Desplegada.")

    # --- D. AUDITORÍA (La Caja Negra) ---
    cursor.execute("""
    CREATE TABLE auditoria_compliance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        entidad TEXT,      -- Ej: 'movimientos', 'param_subcategorias'
        id_entidad INTEGER,-- ID del registro afectado
        accion TEXT,       -- Ej: 'ALTA', 'BLOQUEO_REGLA', 'MODIFICACION'
        detalle TEXT,      -- Ej: 'Se rechazó por Regla de Generalidad'
        usuario TEXT DEFAULT 'SISTEMA' -- Por si el día de mañana usas usuarios
    );
    """)

    print("✅ Tabla de Auditoría desplegada.")

    # ---------------------------------------------------------
    # 3. SEMBRADO DE DATOS (SEED INTELIGENTE)
    # ---------------------------------------------------------
    print("🌱 SEMBRANDO DATOS...")

    # --- SEED DE GOBERNANZA ---
    print("   🔹 Cargando Catálogo de Reglas y Vínculos...")

    # Definimos las reglas únicas
    # Formato: (Nombre, Descripcion, Tipo, [Lista de Tablas donde aplica])
    reglas_data = [
        ('Regla de Segregación Patrimonial', 'Aislar gestión de gastos (costo de vida separado).', 'BLOQUEANTE', ['param_centros_costo']),
        ('Regla de Abstracción', 'La Categoría define el concepto, no el comercio.', 'BLOQUEANTE', ['param_categorias']),
        ('Regla de Generalidad', 'No usar nombres de marcas comerciales ni detalles irrelevantes.', 'BLOQUEANTE', ['param_categorias', 'param_subcategorias']),
        ('Regla del Impacto', 'Solo crear SC si el gasto es significativo. Si no -> Varios.', 'ADVERTENCIA', ['param_subcategorias']),
        ('Regla de Ejecución', 'Todo MP debe identificar el origen real de los fondos.', 'BLOQUEANTE', ['param_medios_pago'])
    ]

    for nombre, desc, tipo, targets in reglas_data:
        # 1. Insertamos la Regla en el Catálogo
        cursor.execute("INSERT INTO reglas_catalogo (nombre, descripcion, tipo_alerta) VALUES (?, ?, ?)", (nombre, desc, tipo))

        # 2. Recuperamos el ID recién generado (last_insert_rowid)
        id_regla = cursor.lastrowid

        # 3. Creamos los vínculos en la tabla intermedia
        for target in targets:
            cursor.execute("INSERT INTO reglas_vinculos (id_regla, entidad_target) VALUES (?, ?)", (id_regla, target))


    # --- DATOS MAESTROS (Bancos y Rubros) ---
    for cc in ['Personal', 'Familia', 'Mamá']:
        ejecutar_sql(cursor, "INSERT INTO param_centros_costo (nombre) VALUES (?)", (cc,))

    mps = [
        ('Efectivo', 'EFECTIVO'),
        ('MercadoPago', 'CUENTA'),
        ('Santander', 'CUENTA'),
        ('Santander Visa', 'TARJETA_CREDITO'),
        ('Santander Amex', 'TARJETA_CREDITO'),
        ('MercadoPago Mastercard', 'TARJETA_CREDITO')
    ]
    for n, t in mps:
        ejecutar_sql(cursor, "INSERT INTO param_medios_pago (nombre, tipo) VALUES (?, ?)", (n, t))

    cats = [
        ('Ingresos', 'INGRESO'), ('Vivienda', 'EGRESO'), ('Transporte', 'EGRESO'),
        ('Alimentos', 'EGRESO'), ('Salud', 'EGRESO'), ('Servicios', 'EGRESO'),
        ('Educación', 'EGRESO'), ('Tecnología', 'EGRESO'), ('Varios', 'EGRESO')
    ]
    for n, t in cats:
        ejecutar_sql(cursor, "INSERT INTO param_categorias (nombre, tipo) VALUES (?, ?)", (n, t))

    def get_cat_id(nombre_cat):
        cursor.execute("SELECT id FROM param_categorias WHERE nombre = ?", (nombre_cat,))
        res = cursor.fetchone()
        return res[0] if res else None

    subcats_map = {
        'Ingresos': ['Sueldo', 'Honorarios', 'Intereses'],
        'Vivienda': ['Alquiler', 'Expensas', 'Mantenimiento'],
        'Transporte': ['Combustible', 'Seguro Auto', 'Patente', 'Uber/Taxi'],
        'Alimentos': ['Supermercado', 'Restaurante', 'Delivery'],
        'Salud': ['Farmacia', 'Obra Social', 'Médico/Dentista', 'Gimnasio'],
        'Servicios': ['Luz', 'Gas', 'Internet', 'Celular'],
        'Tecnología': ['Hardware', 'Software', 'Suscripciones'],
        'Varios': ['Gastos Generales']
    }

    for cat_nombre, lista_subcats in subcats_map.items():
        cat_id = get_cat_id(cat_nombre)
        if cat_id:
            for sub in lista_subcats:
                ejecutar_sql(cursor, "INSERT INTO param_subcategorias (id_categoria, nombre) VALUES (?, ?)", (cat_id, sub))

    conn.commit()
    conn.close()
    print("🚀 ¡S.I.G.A.P. BASE DE DATOS OPTIMIZADA (V2)! LISTO.")

if __name__ == "__main__":
    factory_reset_normalized()