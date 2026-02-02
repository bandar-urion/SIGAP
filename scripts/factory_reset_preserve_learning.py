import sqlite3
import os
import sys

# Ajuste de rutas para encontrar el script base y la DB
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, 'control_gastos.db')

# Intentamos importar el reset original para no duplicar código de esquema
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from factory_reset_normalized import factory_reset_normalized
except ImportError:
    print("❌ Error: No se encuentra 'factory_reset_normalized.py' en la carpeta scripts.")
    sys.exit(1)

def backup_inteligencia(cursor):
    """Extrae el conocimiento adquirido antes de la destrucción."""
    print("\n🧠 RESGUARDANDO INTELIGENCIA (Backup de Sinónimos)...")
    try:
        # Recuperamos por NOMBRE para evitar problemas si cambian los IDs
        sql = """
            SELECT d.termino, s.nombre, c.nombre
            FROM diccionario_terminos d
            JOIN param_subcategorias s ON d.id_subcategoria = s.id
            JOIN param_categorias c ON s.id_categoria = c.id
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        print(f"   📦 Se han resguardado {len(data)} términos en memoria RAM.")
        return data
    except sqlite3.OperationalError:
        print("   ⚠️ La tabla de diccionario no existía. Se asume inicio desde cero.")
        return []

def restaurar_inteligencia(cursor, backup_data):
    """Re-implanta el conocimiento en la nueva estructura."""
    print("\n🧠 RESTAURANDO INTELIGENCIA...")

    restaurados = 0
    ignorados = 0 # Por si ya venían en el seed base

    for termino, subcat_nombre, cat_nombre in backup_data:
        # 1. Buscamos el ID nuevo de la subcategoría (por si cambiaron)
        sql_id = """
            SELECT s.id
            FROM param_subcategorias s
            JOIN param_categorias c ON s.id_categoria = c.id
            WHERE s.nombre = ? AND c.nombre = ?
        """
        cursor.execute(sql_id, (subcat_nombre, cat_nombre))
        resultado = cursor.fetchone()

        if resultado:
            nuevo_id = resultado[0]
            try:
                # 2. Insertamos. INSERT OR IGNORE evita duplicar si el seed base ya lo traía.
                cursor.execute(
                    "INSERT OR IGNORE INTO diccionario_terminos (termino, id_subcategoria) VALUES (?, ?)",
                    (termino, nuevo_id)
                )
                if cursor.rowcount > 0:
                    restaurados += 1
                else:
                    ignorados += 1
            except Exception as e:
                print(f"   ❌ Error insertando '{termino}': {e}")
        else:
            print(f"   ⚠️ Huérfano: La categoría '{cat_nombre} > {subcat_nombre}' ya no existe. Se pierde la regla para '{termino}'.")

    print(f"   ✅ Operación completada: {restaurados} términos restaurados ( + {ignorados} ya existentes en base).")

def main():
    # 1. CONEXIÓN PARA BACKUP
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    memoria_ram = backup_inteligencia(cursor)

    conn.close() # Cerramos para liberar el archivo .db

    # 2. EL GRAN RESET (Borra todo y crea tablas limpias)
    print("\n⚡ EJECUTANDO FACTORY RESET ESTÁNDAR...")
    factory_reset_normalized()

    # 3. CONEXIÓN PARA RESTORE
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    restaurar_inteligencia(cursor, memoria_ram)

    conn.commit()
    conn.close()
    print("\n🦅 SISTEMA REINICIADO. CONOCIMIENTO PRESERVADO.")

if __name__ == "__main__":
    main()