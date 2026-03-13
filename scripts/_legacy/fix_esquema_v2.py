import sqlite3
import os
import logging
from datetime import datetime

# Configuración de Logging y Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'control_gastos.db')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def fix_preferencias():
    if not os.path.exists(DB_FILE):
        logging.error(f"Base de datos no encontrada en {DB_FILE}")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    try:
        logging.info("--- INICIANDO HARD RESET DE PREFERENCIAS ---")
        
        # 1. Eliminamos para asegurar creación limpia
        cursor.execute("DROP TABLE IF EXISTS param_preferencias")
        logging.info("Tabla 'param_preferencias' eliminada para recreación.")

        # 2. Creamos con el esquema Modular-v2
        cursor.execute("""
            CREATE TABLE param_preferencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amortizacion_default TEXT DEFAULT 'SIN_AMORTIZACION',
                centro_costo_default INTEGER,
                FOREIGN KEY (centro_costo_default) REFERENCES param_centros_costo(id)
            )
        """)
        logging.info("Tabla 'param_preferencias' creada con columna 'amortizacion_default'.")

        # 3. Datos iniciales
        cursor.execute("INSERT INTO param_preferencias (amortizacion_default, centro_costo_default) VALUES ('SIN_AMORTIZACION', 1)")
        
        # 4. Auditoría Funcional
        cursor.execute("""
            INSERT INTO auditoria_movimientos (timestamp, accion, resultado)
            VALUES (?, ?, ?)
        """, (ahora, 'FIX_ESQUEMA', 'Reconstrucción total de param_preferencias'))

        conn.commit()
        logging.info("✅ PROCESO COMPLETADO EXITOSAMENTE.")

    except Exception as e:
        conn.rollback()
        logging.error(f"Fallo en la reparación: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_preferencias()
