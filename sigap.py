import sys
import os
import sqlite3
import argparse

# Configuración
DB_FILE = 'sigap.db'

# Importamos los módulos de la carpeta scripts/
# Asegúrate de que el archivo 'factory_reset_normalized.py' esté en la carpeta 'scripts/'
# y que exista el archivo '__init__.py' en esa carpeta.
try:
    from scripts import factory_reset_normalized as db_reset_script
except ImportError as e:
    print(f"❌ Error de Importación: {e}")
    print("⚠️ Asegúrate de tener 'scripts/__init__.py' y 'scripts/factory_reset_normalized.py'")
    sys.exit(1)

def show_status():
    """Verifica la salud de la base de datos y muestra métricas básicas."""
    if not os.path.exists(DB_FILE):
        print(f"⚠️  La base de datos '{DB_FILE}' NO existe.")
        print("💡 Tip: Ejecuta 'python manage.py reset' para inicializarla.")
        return

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        print(f"✅ CONEXIÓN EXITOSA: {DB_FILE}")
        print("-" * 30)

        # Conteo rápido de tablas clave
        tablas = {
            'Movimientos': 'movimientos',
            'Centros de Costo': 'param_centros_costo',
            'Reglas de Gobierno': 'reglas_catalogo',
            'Auditoría': 'auditoria_compliance'
        }

        for nombre, tabla in tablas.items():
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"   📊 {nombre:<20}: {count} registros")
            except sqlite3.OperationalError:
                print(f"   ❌ {nombre:<20}: Error (¿Tabla no existe?)")

        conn.close()
        print("-" * 30)
        print("🟢 Sistema OPERATIVO.")

    except Exception as e:
        print(f"❌ Error crítico al conectar: {e}")

def run_reset():
    """Ejecuta el protocolo de reseteo de fábrica."""
    print("⚠️  ATENCIÓN: Estás a punto de ejecutar el PROTOCOLO DE REINICIO.")
    confirm = input("   ¿Confirmar borrado total y reconstrucción? (si/no): ")

    if confirm.lower() == 'si':
        # Llamamos a la función principal del script que creamos ayer
        db_reset_script.factory_reset_normalized()
    else:
        print("   🛑 Operación cancelada por el usuario.")

def main():
    parser = argparse.ArgumentParser(description="Orquestador S.I.G.A.P. - Proyecto Fénix")

    # Definimos los comandos disponibles
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')

    # Comando: status
    subparsers.add_parser('status', help='Muestra el estado de la base de datos')

    # Comando: reset
    subparsers.add_parser('reset', help='Reinicia la base de datos (Factory Reset)')

    # Leemos los argumentos
    args = parser.parse_args()

    # Ejecutamos según el comando
    if args.command == 'status':
        show_status()
    elif args.command == 'reset':
        run_reset()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()