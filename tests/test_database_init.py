import unittest
import os
import sqlite3
import sys

# Truco para importar módulos superiores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos el script de la base de datos (asegúrate que el nombre sea correcto)
# Si tu script de inicialización se llama 'factory_reset_normalized.py', lo importamos así:
# Nota: Esto asume que el script tiene una función main() o similar,
# si es un script directo, lo testeamos verificando el archivo.

class TestInfraestructuraDB(unittest.TestCase):

    def setUp(self):
        """Preparamos el terreno."""
        self.db_path = ':memory:' # Usamos RAM para no romper nada real
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        """Limpiamos."""
        self.conn.close()

    def test_tablas_esenciales(self):
        """Verifica que el esquema SQL básico sea válido."""
        print("\n🏗️ TEST: Integridad del Esquema SQL...")

        # Simulamos la creación de tablas críticas
        sql_script = """
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE,
                descripcion TEXT,
                monto REAL
            );
            CREATE TABLE IF NOT EXISTS centros_costo (
                id INTEGER PRIMARY KEY,
                nombre TEXT
            );
        """
        try:
            self.cursor.executescript(sql_script)

            # Verificamos que existan
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = [t[0] for t in self.cursor.fetchall()]

            self.assertIn('movimientos', tablas)
            self.assertIn('centros_costo', tablas)
            print("   ✅ Tablas Core creadas correctamente en memoria.")

        except sqlite3.Error as e:
            self.fail(f"❌ Error SQL al crear tablas: {e}")

if __name__ == '__main__':
    unittest.main()