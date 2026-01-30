import sqlite3
import os

# Ajustamos la ruta para que siempre apunte a la raíz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, 'control_gastos.db')

def ejecutar_sql(cursor, sql, params=()):
    try:
        cursor.execute(sql, params)
    except sqlite3.Error as e:
        print(f"❌ Error SQL: {e} | Query: {sql}")

def factory_reset_normalized():
    print(f"💎 INICIANDO PROTOCOLO DE NORMALIZACIÓN V2.0 (S.I.G.A.P.)...")
    print(f"    Target DB: {DB_FILE}")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # 1. DESTRUCCIÓN (DROP)
    # ---------------------------------------------------------
    cursor.execute("PRAGMA foreign_keys = OFF;")

    tablas = [
        'movimientos', 'agenda_pagos', 'auditoria_compliance',
        'param_subcategorias', 'param_categorias',
        'param_medios_pago', 'param_centros_costo',
        'reglas_vinculos', 'reglas_catalogo',
        'diccionario_terminos' # <--- NUEVA TABLA DE SINÓNIMOS
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

    # --- A. GOBERNANZA ---
    cursor.execute("""
    CREATE TABLE reglas_catalogo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        descripcion TEXT NOT NULL,
        tipo_alerta TEXT DEFAULT 'BLOQUEANTE'
    );
    """)

    cursor.execute("""
    CREATE TABLE reglas_vinculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_regla INTEGER NOT NULL,
        entidad_target TEXT NOT NULL,
        FOREIGN KEY (id_regla) REFERENCES reglas_catalogo(id),
        UNIQUE(id_regla, entidad_target)
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

    # --- C. INTELIGENCIA (SINÓNIMOS) ---
    cursor.execute("""
    CREATE TABLE diccionario_terminos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        termino TEXT NOT NULL UNIQUE, -- Ej: 'Sushi', 'Rotiseria'
        id_subcategoria INTEGER NOT NULL,
        FOREIGN KEY (id_subcategoria) REFERENCES param_subcategorias(id)
    );
    """)

    # --- D. OPERATIVAS ---
    cursor.execute("""
    CREATE TABLE agenda_pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_centro_costo INTEGER NOT NULL,
        fecha_vencimiento TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        monto_estimado REAL DEFAULT 0,
        estado TEXT DEFAULT 'PENDIENTE', -- PENDIENTE, PAGADO, ANULADO
        prioridad TEXT DEFAULT 'NORMAL',
        url_pago TEXT, -- Para guardar link de pago
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
        es_amortizable BOOLEAN DEFAULT 0,
        meses_amortizacion INTEGER DEFAULT 0,
        FOREIGN KEY(id_centro_costo) REFERENCES param_centros_costo(id),
        FOREIGN KEY(id_medio_pago) REFERENCES param_medios_pago(id),
        FOREIGN KEY(id_subcategoria) REFERENCES param_subcategorias(id)
    );
    """)

    # --- E. AUDITORÍA ---
    cursor.execute("""
    CREATE TABLE auditoria_compliance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        entidad TEXT,
        id_entidad INTEGER,
        accion TEXT,
        detalle TEXT,
        usuario TEXT DEFAULT 'SISTEMA'
    );
    """)

    print("✅ Estructura Normalizada Desplegada.")

    # ---------------------------------------------------------
    # 3. SEMBRADO DE DATOS (SEED FINAL)
    # ---------------------------------------------------------
    print("🌱 SEMBRANDO DATOS...")

    # --- GOBERNANZA BÁSICA ---
    cursor.execute("INSERT INTO reglas_catalogo (nombre, descripcion, tipo_alerta) VALUES (?, ?, ?)",
                   ('Regla de Unicidad', 'Evitar duplicados bancarios.', 'BLOQUEANTE'))
    cursor.execute("INSERT INTO reglas_vinculos (id_regla, entidad_target) VALUES (?, ?)",
                   (cursor.lastrowid, 'movimientos'))

    # --- CENTROS DE COSTO ---
    for cc in ['Personal', 'Familia', 'Mamá']:
        ejecutar_sql(cursor, "INSERT INTO param_centros_costo (nombre) VALUES (?)", (cc,))

    # --- MEDIOS DE PAGO ---
    mps = [
        ('Efectivo', 'EFECTIVO'),
        ('Efectivo USD', 'EFECTIVO'), # Caja chica en dolares
        ('MercadoPago', 'CUENTA'),
        ('Santander', 'CUENTA'),
        ('Santander Mama', 'CUENTA'), # ¡NUEVO!
        ('BPN', 'CUENTA'),            # ¡NUEVO!
        ('Lemon Cash', 'CUENTA'),     # ¡NUEVO!
        ('Santander Visa', 'TARJETA_CREDITO'),
        ('Santander Amex', 'TARJETA_CREDITO'),
        ('MercadoPago Mastercard', 'TARJETA_CREDITO')
    ]
    for n, t in mps:
        ejecutar_sql(cursor, "INSERT INTO param_medios_pago (nombre, tipo) VALUES (?, ?)", (n, t))

    # --- CATEGORÍAS ---
    cats = [
        ('Ingresos', 'INGRESO'),
        ('Casa', 'EGRESO'),           # Ex Vivienda
        ('Terreno', 'EGRESO'),        # ¡NUEVO! Separado de Casa
        ('Auto', 'EGRESO'),           # Ex Transporte
        ('Alimentos', 'EGRESO'),
        ('Salud', 'EGRESO'),
        ('Tecnología', 'EGRESO'),
        ('Entretenimiento', 'EGRESO'), # Ex Ocio
        ('Indumentaria', 'EGRESO'),
        ('Educación', 'EGRESO'),
        ('Impuestos', 'EGRESO'),      # Personales (AFIP)
        ('Movimientos Internos', 'EGRESO'),
        ('Varios', 'EGRESO')
    ]
    for n, t in cats:
        ejecutar_sql(cursor, "INSERT INTO param_categorias (nombre, tipo) VALUES (?, ?)", (n, t))

    def get_cat_id(nombre_cat):
        cursor.execute("SELECT id FROM param_categorias WHERE nombre = ?", (nombre_cat,))
        res = cursor.fetchone()
        return res[0] if res else None

    # --- SUBCATEGORÍAS ---
    subcats_map = {
        'Ingresos': [
            'Sueldo', 'Aguinaldo', 'Honorarios',
            'Jubilación', 'Acreditación Benef. Prev.', # Mamá
            'Ayuda Estatal', 'Colaboración Eny',       # Familia
            'Alquiler', 'Rentas',
            'Devoluciones', 'Reintegro Adicional OSDE', 'Venta Dólares'
        ],
        'Casa': [
            'Luz', 'Gas', 'Agua', 'Internet', # Servicios Granulares
            'Impuesto Inmobiliario', 'Tasas Municipales',
            'Expensas', 'Seguro Hogar',
            'Mantenimiento', 'Mejoras',
            'Mascotas' # ¡Movido aquí!
        ],
        'Terreno': [ # Categoría Nueva para separar gastos de inversión
            'Impuesto Inmobiliario', 'Tasas Municipales',
            'Expensas', 'Mantenimiento', 'Mejoras'
        ],
        'Auto': [
            'Combustible', 'Seguro', 'Patente',
            'Mecánica/Service', 'Repuestos', 'Limpieza',
            'Peajes/Estacionamiento'
        ],
        'Alimentos': [
            'Supermercado',
            'Comida Preparada', # Ex Delivery
            'Bebidas/Kiosco', 'Almuerzos Laborales'
        ],
        'Salud': [
            'Farmacia', 'Obra Social', 'Consulta Médica',
            'Psicólogo', 'Psiquiatra', 'Médico/Dentista',
            'Gimnasio',
            'Pañales/Cuidados' # Mamá
        ],
        'Tecnología': [
            'Celular', 'Hardware', 'Software',
            'Suscripciones Digitales', 'Seguro Equipos'
        ],
        'Entretenimiento': [
            'DCS World', # ¡Específico!
            'Videojuegos', 'Streaming', 'Salidas', 'Vacaciones'
        ],
        'Indumentaria': ['Ropa', 'Calzado', 'Accesorios'],
        'Educación': ['Cuota Escolar', 'Útiles/Libros', 'Cursos/Capacitación'],
        'Impuestos': ['AFIP', 'Ingresos Brutos', 'Bienes Personales'],
        'Movimientos Internos': ['Transferencia Propia', 'Pago Tarjeta', 'Inversión'],
        'Varios': ['Regalos', 'Donaciones', 'Costos Bancarios']
    }

    for cat_nombre, lista_subcats in subcats_map.items():
        cat_id = get_cat_id(cat_nombre)
        if cat_id:
            for sub in lista_subcats:
                try:
                    ejecutar_sql(cursor, "INSERT INTO param_subcategorias (id_categoria, nombre) VALUES (?, ?)", (cat_id, sub))
                except sqlite3.IntegrityError:
                    pass # Evitar error si duplicamos nombre en listas
        else:
            print(f"⚠️ Alerta: Categoría '{cat_nombre}' no encontrada.")

    # --- SEMBRADO DE SINÓNIMOS (EJEMPLO) ---
    # Aquí cargamos tu lógica de inteligencia
    print("   🔹 Cargando Sinónimos Inteligentes...")

    # Helper para buscar ID de subcategoria
    def get_subcat_id(nombre_sub):
        cursor.execute("SELECT id FROM param_subcategorias WHERE nombre = ?", (nombre_sub,))
        res = cursor.fetchone()
        return res[0] if res else None

    sinonimos = [
        ('Comida Preparada', ['Sushi', 'Rotiseria', 'Delivery', 'PedidosYa', 'Pizza']),
        ('Supermercado', ['Despensa', 'Verduleria', 'Chino', 'La Anonima', 'Coto']),
        ('Combustible', ['Nafta', 'YPF', 'Shell', 'Axion']),
        ('Mascotas', ['Veterinaria', 'Alimento Perro', 'Piyito']),
        ('DCS World', ['Eagle Dynamics', 'Modulo Avion', 'Mapa DCS'])
    ]

    for subcat, terms in sinonimos:
        sid = get_subcat_id(subcat)
        if sid:
            for term in terms:
                try:
                    ejecutar_sql(cursor, "INSERT INTO diccionario_terminos (termino, id_subcategoria) VALUES (?, ?)", (term, sid))
                except sqlite3.IntegrityError:
                    pass

    conn.commit()
    conn.close()
    print("🚀 ¡S.I.G.A.P. BASE DE DATOS RESTAURADA (VERSION 2.0 DIAMOND)! LISTO.")

if __name__ == "__main__":
    factory_reset_normalized()
