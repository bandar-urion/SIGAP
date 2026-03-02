import os
import sys
import sqlite3
import logging
from datetime import datetime

# Inyectamos el cerebro central del SIGAP
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import sigap_config

def parchear_subcategorias():
    db_path = sigap_config.get_db_path()
    logging.info(f"🏗️ Aplicando parche quirúrgico en DB: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    try:
        # 1. Agregamos la columna a la tabla correcta (como entero)
        cursor.execute("ALTER TABLE param_subcategorias ADD COLUMN amortizacion_default INTEGER DEFAULT 0")
        logging.info("✅ Columna 'amortizacion_default' agregada a 'param_subcategorias'.")
        
        # 2. Trazabilidad: Registro en auditoría con precisión de milisegundos
        cursor.execute("""
            INSERT INTO auditoria_movimientos (timestamp, accion, resultado)
            VALUES (?, ?, ?)
        """, (ahora, 'MIGRACION_SUBCATEGORIAS', 'Añadida amortizacion_default a param_subcategorias'))
        
        conn.commit()
        logging.info("🚀 Parche aplicado y auditado con éxito.")
        
    except sqlite3.OperationalError as e:
        # Si la columna ya existía por algún motivo, lo atajamos limpio
        logging.warning(f"ℹ️ Aviso de esquema: {e}")
    except Exception as e:
        conn.rollback()
        logging.error(f"❌ Error crítico en parche: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    parchear_subcategorias()
