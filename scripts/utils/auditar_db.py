import sqlite3
import os
import sys
import logging
from datetime import datetime

# sigap_config como fuente única de rutas (D-005)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
import sigap_config

# Protocolo SIGAP: Logging con precisión de milisegundos
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def auditar():
    db_path = sigap_config.get_db_path()
    rutas_a_revisar = [db_path]

    logging.info("--- INICIANDO AUDITORÍA DE RUTAS SIGAP ---")

    for ruta in rutas_a_revisar:
        if os.path.exists(ruta):
            logging.info(f"🔎 Detectado archivo en: {ruta}")
            try:
                conn = sqlite3.connect(ruta)
                cursor = conn.cursor()

                # Listar todas las tablas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tablas = [t[0] for t in cursor.fetchall()]
                logging.info(f"   Tablas encontradas: {tablas}")

                if 'param_preferencias' in tablas:
                    cursor.execute("PRAGMA table_info(param_preferencias)")
                    columnas = [c[1] for c in cursor.fetchall()]
                    logging.info(f"   ✅ param_preferencias tiene columnas: {columnas}")
                else:
                    logging.warning(f"   ❌ param_preferencias NO EXISTE en esta base de datos.")

                conn.close()
            except Exception as e:
                logging.error(f"   Error al leer {ruta}: {e}")
        else:
            logging.info(f"🚫 No existe archivo en: {ruta}")

if __name__ == "__main__":
    auditar()
