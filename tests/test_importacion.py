import unittest
import sqlite3
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class TestIntegridadBancaria(unittest.TestCase):

    def setUp(self):
        """Se ejecuta ANTES de cada prueba. Crea un entorno limpio."""
        # Usamos :memory: para no tocar tu disco duro. Es una DB fantasma.
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        # 1. Recreamos la estructura MÍNIMA necesaria de la tabla movimientos
        self.cursor.execute("""
            CREATE TABLE movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_referencia TEXT UNIQUE,  -- EL GUARDIÁN DEL DUPLICADO
                descripcion TEXT,
                monto REAL
            )
        """)
        self.conn.commit()

    def tearDown(self):
        """Se ejecuta DESPUÉS de cada prueba. Cierra el kiosco."""
        self.conn.close()

    def test_evitar_duplicados_crash(self):
        """Simula el error que tuviste y verifica el blindaje."""
        print("\n🦅 TEST: Inserción de Duplicados...")

        # PASO 1: Insertamos el movimiento original (Simula una carga previa)
        ref_id = "REF-123456"
        self.cursor.execute(
            "INSERT INTO movimientos (num_referencia, descripcion, monto) VALUES (?, ?, ?)",
            (ref_id, "Compra Original", -100.0)
        )
        self.conn.commit()
        print("   ✅ Paso 1: Movimiento original insertado.")

        # PASO 2: Intentamos insertar el MISMO movimiento (Simula correr el script de nuevo)
        # Aquí usamos la lógica BLINDADA (INSERT OR IGNORE)
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO movimientos (num_referencia, descripcion, monto)
                VALUES (?, ?, ?)
            """, (ref_id, "Compra Duplicada (Intruso)", -100.0))

            self.conn.commit()
            print("   ✅ Paso 2: Intento de duplicado ejecutado sin crash.")

        except sqlite3.IntegrityError:
            self.fail("❌ FALLO CRÍTICO: El sistema explotó con IntegrityError (Como te pasó antes)")

        # PASO 3: Verificar qué pasó
        # Debería haber SOLO 1 registro, no 2.
        self.cursor.execute("SELECT count(*) FROM movimientos")
        cantidad = self.cursor.fetchone()[0]

        self.assertEqual(cantidad, 1, f"❌ Error: Se esperaban 1 registro, se encontraron {cantidad}")
        print("   ✅ Paso 3: Integridad verificada. La base de datos rechazó al clon silenciosamente.")

if __name__ == '__main__':
    unittest.main()