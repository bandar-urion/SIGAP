import os
import configparser
import logging
from datetime import datetime

# Detectamos la raíz del proyecto dinámicamente
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'sigap.cfg')

# Inicializamos el parser
config = configparser.ConfigParser()

def cargar_configuracion():
    """Lee sigap.cfg y configura el entorno general."""
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ CRÍTICO: No se encontró el archivo de configuración en {CONFIG_FILE}")
        raise FileNotFoundError(f"Falta {CONFIG_FILE}")

    config.read(CONFIG_FILE)
    
    # 1. Configurar Logging Centralizado según sigap.cfg
    log_level_str = config.get('SYSTEM', 'LOG_LEVEL', fallback='INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    os.makedirs('logs', exist_ok=True)
    
    # Reseteamos handlers por si otro script ya inició logging
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/sigap_tecnico.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logging.info("S.I.G.A.P. - Configuración base cargada con éxito.")
    return config

def get_db_path():
    """Construye la ruta absoluta y segura a la base de datos."""
    db_dir = config.get('DATABASE', 'DIR', fallback='data')
    db_name = config.get('DATABASE', 'NAME', fallback='sigap.db')
    ruta_completa = os.path.join(BASE_DIR, db_dir, db_name)
    return ruta_completa

def get_path(seccion, clave):
    """Obtiene cualquier ruta del cfg asegurando compatibilidad OS."""
    ruta_relativa = config.get(seccion, clave)
    # Reemplazamos barras por si venimos de un cfg editado en Windows
    ruta_relativa = ruta_relativa.replace('/', os.sep).replace('\\', os.sep)
    return os.path.join(BASE_DIR, ruta_relativa)

# Ejecutamos la carga al importar el módulo
cargar_configuracion()
