import os
import sys
import unittest

# Aseguramos que el entorno de test encuentre los módulos en la raíz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import sigap_config


class TestConfiguracionMultiplataforma(unittest.TestCase):
    """Tests de sigap_config.py: rutas absolutas y compatibilidad cross-platform."""

    def test_get_db_path_es_absoluta(self):
        """Verifica que la ruta a la BD sea absoluta para evitar BD fantasmas."""
        db_path = sigap_config.get_db_path()
        self.assertTrue(os.path.isabs(db_path), f"La ruta {db_path} no es absoluta.")
        self.assertTrue(db_path.endswith('sigap.db'), "La BD no se llama sigap.db")

    def test_get_path_normaliza_barras(self):
        """Verifica que las rutas respeten el separador del OS (Termux vs Windows)."""
        inbox_path = sigap_config.get_path('PATHS', 'INBOX')
        self.assertTrue(os.path.isabs(inbox_path))
        self.assertTrue(os.sep in inbox_path)


if __name__ == '__main__':
    unittest.main()
