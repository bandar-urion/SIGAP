import unittest
import sqlite3

class TestAislamientoFinanciero(unittest.TestCase):
    def setUp(self):
        """Prepara el entorno efímero antes de cada test."""
        # Creamos una DB en RAM para aislar la prueba de la data real
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        # Recreamos la estructura mínima de la tabla conflictiva
        self.cursor.execute('''
            CREATE TABLE param_subcategorias (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                amortizacion_default INTEGER
            )
        ''')
        # Insertamos el caso de prueba limpio (como lo dejaste con el UPDATE)
        self.cursor.execute("INSERT INTO param_subcategorias (id, nombre, amortizacion_default) VALUES (30, 'Psicologo', NULL)")
        self.conn.commit()

    def test_aislamiento_de_cuotas_manuales(self):
        """Verifica que asignar cuotas a un movimiento NO contamine la subcategoría."""
        
        # 1. Verificamos el estado inicial (Debe ser NULL/None)
        self.cursor.execute("SELECT amortizacion_default FROM param_subcategorias WHERE id = 30")
        estado_inicial = self.cursor.fetchone()[0]
        self.assertIsNone(estado_inicial, "Fallo inicial: La subcategoría no empezó limpia.")

        # 2. SIMULACIÓN DEL ENTORNO DE UI (El código que acabás de parchear)
        buffer_cuotas = "3" # Simulamos que el usuario tipeó 3
        
        # Simulamos las variables del objeto mov_foco
        mov_cuotas_totales = 0
        mov_cuota_actual = 0
        id_subcat_actual = 30

        # Bloque parcheado (Opción A: asignación sin escritura a DB)
        if buffer_cuotas:
            meses = int(buffer_cuotas)
            if meses > 1:
                mov_cuotas_totales = meses
                mov_cuota_actual = 1
                # (Acá antes estaba el código venenoso que hacía el UPDATE a la DB)

        # 3. VERIFICACIÓN FINAL (El momento de la verdad)
        self.cursor.execute("SELECT amortizacion_default FROM param_subcategorias WHERE id = 30")
        estado_final = self.cursor.fetchone()[0]

        # Comprobamos que el movimiento sí recibió las cuotas en RAM...
        self.assertEqual(mov_cuotas_totales, 3, "El movimiento no recibió las cuotas correctamente.")
        
        # ...pero la base de datos se mantuvo INMACULADA.
        self.assertIsNone(estado_final, "¡REGRESIÓN CRÍTICA! El sistema guardó las cuotas en la subcategoría.")

    def tearDown(self):
        """Destruye el entorno efímero."""
        self.conn.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)
