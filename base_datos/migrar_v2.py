import sqlite3
import shutil
import os

DB_FILE = 'control_gastos.db'
BACKUP_FILE = 'control_gastos_backup_v2.db'

def inferir_tipo_pago(nombre_mp):
    """
    Intenta adivinar el tipo de medio de pago basado en su nombre
    para cumplir con el CHECK constraint de la base de datos.
    """
    nombre_lower = nombre_mp.lower()
    if any(x in nombre_lower for x in ['tarjeta', 'visa', 'amex', 'master', 'crédito', 'credito']):
        return 'TARJETA_CREDITO'
    elif 'efectivo' in nombre_lower:
        return 'EFECTIVO'
    else:
        # Ante la duda, asumimos que es una CUENTA bancaria o similar
        return 'CUENTA'

def migrar_base_datos():
    # 1. Backup de seguridad
    if os.path.exists(DB_FILE):
        shutil.copy(DB_FILE, BACKUP_FILE)
        print(f"📦 Backup creado: {BACKUP_FILE}")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        print("🔧 Iniciando Migración a 3NF (IDs) - FIX v2.1...")

        # ---------------------------------------------------------
        # PASO 1: AUTO-CURACIÓN DE MEDIOS DE PAGO HUÉRFANOS
        # ---------------------------------------------------------
        print("🔍 Buscando Medios de Pago desconocidos...")

        sql_huerfanos = """
        SELECT DISTINCT m.medio_pago
        FROM movimientos m
        LEFT JOIN param_medios_pago p ON m.medio_pago = p.nombre
        WHERE p.id IS NULL AND m.medio_pago IS NOT NULL
        """
        cursor.execute(sql_huerfanos)
        huerfanos = cursor.fetchall()

        for mp in huerfanos:
            nombre_mp = mp[0]
            # AQUI ESTA EL ARREGLO: Inferimos un tipo válido
            tipo_valido = inferir_tipo_pago(nombre_mp)

            print(f"   ⚠️ Encontrado MP nuevo: '{nombre_mp}'. Asignando tipo: '{tipo_valido}'")

            cursor.execute("""
                INSERT INTO param_medios_pago (nombre, tipo)
                VALUES (?, ?)
            """, (nombre_mp, tipo_valido))

        conn.commit()

        # ---------------------------------------------------------
        # PASO 2: CREAR LA NUEVA TABLA (V2)
        # ---------------------------------------------------------
        print("🏗️ Creando estructura de tabla 'movimientos_v2'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            descripcion TEXT,
            monto REAL NOT NULL,

            -- NUEVAS COLUMNAS (IDs)
            id_subcategoria INTEGER,
            id_centro_costo INTEGER,
            id_medio_pago INTEGER,

            -- OTROS CAMPOS MANTENIDOS
            id_referencia TEXT UNIQUE,
            es_amortizable INTEGER DEFAULT 0,
            meses_amortizacion INTEGER DEFAULT 0,
            fecha_fin_amortizacion DATE,

            -- CLAVES FORÁNEAS
            FOREIGN KEY(id_subcategoria) REFERENCES param_subcategorias(id),
            FOREIGN KEY(id_centro_costo) REFERENCES param_centros_costo(id),
            FOREIGN KEY(id_medio_pago) REFERENCES param_medios_pago(id)
        );
        """)

        # ---------------------------------------------------------
        # PASO 3: MIGRACIÓN DE DATOS
        # ---------------------------------------------------------
        print("🚀 Migrando datos y transformando Textos a IDs...")

        sql_migracion = """
        INSERT INTO movimientos_v2 (
            fecha, descripcion, monto, id_referencia,
            es_amortizable, meses_amortizacion, fecha_fin_amortizacion,
            id_subcategoria, id_centro_costo, id_medio_pago
        )
        SELECT
            m.fecha, m.descripcion, m.monto, m.id_referencia,
            m.es_amortizable, m.meses_amortizacion, m.fecha_fin_amortizacion,
            s.id, c.id, p.id
        FROM movimientos m
        LEFT JOIN param_subcategorias s ON m.subcategoria = s.nombre
        LEFT JOIN param_centros_costo c ON m.centro_costo = c.nombre
        LEFT JOIN param_medios_pago p ON m.medio_pago = p.nombre;
        """

        cursor.execute(sql_migracion)
        registros = cursor.rowcount
        print(f"✅ Se han migrado {registros} registros exitosamente.")

        # ---------------------------------------------------------
        # PASO 4: SWAP DE TABLAS
        # ---------------------------------------------------------
        print("🔄 Realizando el intercambio de tablas...")

        # Primero borramos la tabla vieja si ya existía de un intento fallido anterior
        cursor.execute("DROP TABLE IF EXISTS movimientos_old_text")

        cursor.execute("ALTER TABLE movimientos RENAME TO movimientos_old_text;")
        cursor.execute("ALTER TABLE movimientos_v2 RENAME TO movimientos;")

        conn.commit()
        print("✨ ¡MIGRACIÓN COMPLETADA! La base de datos ahora es Relacional Pura.")

    except sqlite3.Error as e:
        print(f"❌ Error crítico en la migración: {e}")
        conn.rollback()

    finally:
        conn.close()

if __name__ == "__main__":
    migrar_base_datos()