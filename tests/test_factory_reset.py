"""
test_factory_reset.py — Regresión D-005: sin rutas hardcodeadas en scripts de factory reset.

PROPÓSITO:
    Verificar que ninguno de los dos scripts de reset hardcodee la ruta de DB.
    Regresión del fix de Sesión #16, donde "control_gastos.db" fue reemplazado
    por el acceso dinámico via sigap_config.get_db_path().

QUÉ SE VERIFICA:
    1. factory_reset_normalized.py   — no contiene el string legacy "control_gastos.db"
    2. factory_reset_preserve_learning.py — ídem
    3. La ruta de DB obtenida en runtime termina en "sigap.db"
    4. La ruta de DB obtenida en runtime es absoluta (sin DB fantasmas)
"""

import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import sigap_config

SCRIPTS_DIR   = os.path.join(BASE_DIR, 'scripts')
SCRIPT_NORM   = os.path.join(SCRIPTS_DIR, 'factory_reset_normalized.py')
SCRIPT_PRES   = os.path.join(SCRIPTS_DIR, 'factory_reset_preserve_learning.py')
LEGACY_DB_NAME = 'control_gastos.db'


class TestFactoryResetSinRutasHardcodeadas(unittest.TestCase):
    """Regresión fix Sesión #16: ningún script de reset puede hardcodear la ruta legacy."""

    def _leer_fuente(self, ruta):
        with open(ruta, encoding='utf-8') as f:
            return f.read()

    # ------------------------------------------------------------------
    # TEST 1 y 2: inspección de código fuente
    # ------------------------------------------------------------------

    def test_factory_reset_normalized_sin_legacy_db(self):
        """factory_reset_normalized.py no debe contener el string 'control_gastos.db'."""
        fuente = self._leer_fuente(SCRIPT_NORM)
        self.assertNotIn(
            LEGACY_DB_NAME,
            fuente,
            f"¡REGRESIÓN D-005! '{LEGACY_DB_NAME}' está hardcodeado en factory_reset_normalized.py"
        )

    def test_factory_reset_preserve_sin_legacy_db(self):
        """factory_reset_preserve_learning.py no debe contener el string 'control_gastos.db'."""
        fuente = self._leer_fuente(SCRIPT_PRES)
        self.assertNotIn(
            LEGACY_DB_NAME,
            fuente,
            f"¡REGRESIÓN D-005! '{LEGACY_DB_NAME}' está hardcodeado en factory_reset_preserve_learning.py"
        )

    # ------------------------------------------------------------------
    # TEST 3 y 4: verificación de la ruta en runtime
    # ------------------------------------------------------------------

    def test_ruta_db_runtime_termina_en_sigap_db(self):
        """La ruta obtenida via sigap_config.get_db_path() debe terminar en 'sigap.db'."""
        db_path = sigap_config.get_db_path()
        self.assertTrue(
            db_path.endswith('sigap.db'),
            f"La ruta '{db_path}' no termina en 'sigap.db' — posible regresión de rutas."
        )

    def test_ruta_db_runtime_es_absoluta(self):
        """La ruta obtenida en runtime debe ser absoluta para evitar DB fantasmas."""
        db_path = sigap_config.get_db_path()
        self.assertTrue(
            os.path.isabs(db_path),
            f"La ruta '{db_path}' no es absoluta — riesgo de DB fantasma."
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
