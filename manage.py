import sys
import os
import argparse

# Agregamos la ruta base para que Python encuentre la carpeta 'scripts'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts')))

def check_db():
    """Valida la existencia de la base de datos."""
    db_path = 'control_gastos.db'
    if os.path.exists(db_path):
        print(f"✅ Base de datos detectada: {db_path}")
        return True
    print(f"❌ No se encuentra la base de datos.")
    return False

def main():
    parser = argparse.ArgumentParser(description="🦅 S.I.G.A.P. - Panel de Control del Proyecto Fénix")
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')

    # Comandos Administrativos
    subparsers.add_parser('status', help='Muestra el estado actual del sistema')
    subparsers.add_parser('reset', help='Factory Reset (Limpieza Total)')
    subparsers.add_parser('reset-safe', help='Factory Reset preservando aprendizaje (Sinónimos)')

    # Comandos de Operación
    subparsers.add_parser('import-santander', help='Inicia el parser del Banco Santander')

    args = parser.parse_args()

    if args.command == 'status':
        if check_db():
            # Aquí llamaremos a una futura función de métricas en dal/db_manager.py
            print("📊 Sistema listo para auditoría.")

    elif args.command == 'reset':
        from dal.factory_reset import factory_reset_normalized
        factory_reset_normalized()

    elif args.command == 'reset-safe':
        from dal.reset_with_backup import main as safe_reset
        safe_reset()

    elif args.command == 'import-santander':
        from parsers.santander import main as import_run
        import_run()

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
