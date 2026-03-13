import os
import sys
import sqlite3
import logging

# Inyectamos nuestro cerebro central
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import sigap_config

def nivelar_db_oficial():
    db_path = sigap_config.get_db_path()
    logging.info(f"🏗️ Iniciando nivelación en la DB oficial: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Hard Reset a preferencias
        cursor.execute("DROP TABLE IF EXISTS param_preferencias")
        cursor.execute("""
            CREATE TABLE param_preferencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amortizacion_default TEXT DEFAULT 'SIN_AMORTIZACION',
                centro_costo_default INTEGER,
                FOREIGN KEY (centro_costo_default) REFERENCES param_centros_costo(id)
            )
        """)
        cursor.execute("INSERT INTO param_preferencias (amortizacion_default, centro_costo_default) VALUES ('SIN_AMORTIZACION', 1)")
        logging.info("✅ Tabla param_preferencias recreada e inicializada.")
        
        # 2. Parche a movimientos (con Try/Except para que sea idempotente)
        try:
            cursor.execute("ALTER TABLE movimientos ADD COLUMN cuota_actual INTEGER DEFAULT 0")
            cursor.execute("ALTER TABLE movimientos ADD COLUMN cuotas_totales INTEGER DEFAULT 0")
            logging.info("✅ Columnas de cuotas agregadas a movimientos.")
        except sqlite3.OperationalError:
            logging.info("ℹ️ Las columnas de cuotas ya existían en movimientos.")
            
        conn.commit()
        logging.info("🚀 Base de datos nivelada con éxito al esquema v2.")
        
    except Exception as e:
        conn.rollback()
        logging.error(f"❌ Error crítico en nivelación: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    nivelar_db_oficial()
