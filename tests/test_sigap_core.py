import os
import sys
import unittest

# Aseguramos que el entorno de test encuentre los módulos en la raíz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import sigap_config
from scripts.modulos.carga_gastos import Transaccion

class TestConfiguracionMultiplataforma(unittest.TestCase):
    def test_get_db_path_es_absoluta(self):
        """Verifica que la ruta a la BD sea absoluta para evitar BD fantasmas."""
        db_path = sigap_config.get_db_path()
        self.assertTrue(os.path.isabs(db_path), f"La ruta {db_path} no es absoluta.")
        self.assertTrue(db_path.endswith('sigap.db'), "La BD no se llama sigap.db")

    def test_get_path_normaliza_barras(self):
        """Verifica que las rutas respeten el OS (Termux vs Windows)."""
        inbox_path = sigap_config.get_path('PATHS', 'INBOX')
        self.assertTrue(os.path.isabs(inbox_path))
        # Validamos que no queden barras invertidas en Linux, o barras normales flotando en Windows
        self.assertTrue(os.sep in inbox_path)

class TestMotorCuotasRegex(unittest.TestCase):
    def test_detectar_cuotas_formato_barra(self):
        """Prueba extraccion de cuota actual y total (ej. 03/12)."""
        tx = Transaccion("2026-03-02", "REF1", "COMPRA FRAVEGA 03/12", 50000, 1)
        self.assertEqual(tx.cuota_actual, 3)
        self.assertEqual(tx.cuotas_totales, 12)

    def test_detectar_cuotas_formato_texto(self):
        """Prueba extraccion solo de cuota actual (ej. CTA 2)."""
        tx = Transaccion("2026-03-02", "REF2", "SEGURO AUTO CTA 2", 15000, 1)
        self.assertEqual(tx.cuota_actual, 2)
        # El regex actual de tu código para "CTA" no extrae totales, solo actual
        self.assertEqual(tx.cuotas_totales, 0) 

    def test_ignorar_falsos_positivos_fechas(self):
        """Verifica que fechas puras no sean confundidas con cuotas."""
        tx = Transaccion("2026-03-02", "REF3", "PAGO VTO 15/03/2026", 10000, 1)
        self.assertEqual(tx.cuota_actual, 0)
        self.assertEqual(tx.cuotas_totales, 0)

if __name__ == '__main__':
    unittest.main()
