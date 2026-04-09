import sys
import os
import sqlite3
import argparse

# 1. 🏛️ IMPORTACIÓN CENTRALIZADA DE LA RUTA
from sigap_config import get_db_path

# Ejecutamos tu función para obtener la ruta dinámica y segura
RUTA_DB = get_db_path()

# Importamos los módulos de la carpeta scripts/
try:
    from scripts import factory_reset_normalized as db_reset_script
except ImportError as e:
    print(f"❌ Error de Importación: {e}")
    print("⚠️ Asegúrate de tener 'scripts/__init__.py' y 'scripts/factory_reset_normalized.py'")
    sys.exit(1)

def show_status():
    """Verifica la salud de la base de datos y muestra métricas básicas."""
    # 2. 🏛️ USAMOS RUTA_DB EN LUGAR DEL HARDCODEO
    if not os.path.exists(RUTA_DB):
        print(f"⚠️ La base de datos '{RUTA_DB}' NO existe.")
        print("💡 Tip: Ejecuta 'python sigap.py reset' para inicializarla.")
        return

    try:
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()

        print(f"✅ CONEXIÓN EXITOSA: {RUTA_DB}")
        print("-" * 30)

        # 3. 🏛️ ACTUALIZAMOS A LOS NOMBRES REALES DE TU ARQUITECTURA
        tablas = {
            'Movimientos': 'movimientos',
            'Centros de Costo': 'param_centros_costo',
            'Categorías': 'param_categorias',
            'Subcategorías': 'param_subcategorias',
            'Auditoría': 'auditoria_movimientos'
        }

        for nombre, tabla in tablas.items():
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f" 📊 {nombre:<20}: {count} registros")
            except sqlite3.OperationalError:
                print(f" ❌ {nombre:<20}: Error (¿Tabla no existe?)")

        conn.close()
        print("-" * 30)
        print("🟢 Sistema OPERATIVO.")

    except Exception as e:
        print(f"❌ Error crítico al conectar: {e}")

def run_reset():
    """Ejecuta el protocolo de reseteo de fábrica."""
    print("⚠️ ATENCIÓN: Estás a punto de ejecutar el PROTOCOLO DE REINICIO.")
    # EXCEPCIÓN ARQUITECTÓNICA: input() permitido aquí.
    # run_reset() es comando admin destructivo, fuera del flujo UI.
    # leer_byte() aplica solo a flujos de inbox/viewport. Ver DECISIONES.md.
    confirm = input(" ¿Confirmar borrado total y reconstrucción? (si/no): ")

    if confirm.lower() == 'si':
        db_reset_script.factory_reset_normalized()
    else:
        print(" 🛑 Operación cancelada por el usuario.")

def main():
    parser = argparse.ArgumentParser(description="Orquestador S.I.G.A.P. - Proyecto Fénix")
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    subparsers.add_parser('status', help='Muestra el estado de la base de datos')
    subparsers.add_parser('reset', help='Reinicia la base de datos (Factory Reset)')

    args = parser.parse_args()

    if args.command == 'status':
        show_status()
    elif args.command == 'reset':
        run_reset()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
