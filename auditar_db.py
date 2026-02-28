import sqlite3
import os
import logging
from datetime import datetime

# Protocolo SIGAP: Logging con precisión de milisegundos
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def auditar():
    # Simulamos la lógica de rutas de import_santander.py
    # Siendo que estamos en la raíz:
    db_root = os.path.abspath("control_gastos.db")
    db_scripts = os.path.abspath("scripts/control_gastos.db") # Posible duplicado
    
    rutas_a_revisar = [db_root, db_scripts]
    
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
