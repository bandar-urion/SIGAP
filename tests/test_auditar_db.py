"""
test_auditar_db.py — Cobertura para scripts/utils/auditar_db.py

PROPÓSITO:
    Verificar los contratos de la función auditar():
    - D-005: usa sigap_config.get_db_path(), no rutas hardcodeadas.
    - Resiliencia: no lanza excepciones en las tres situaciones de arranque posibles:
        a) Ruta de DB inexistente.
        b) DB existente sin la tabla param_preferencias.
        c) DB existente con la tabla param_preferencias (camino feliz).

COMPORTAMIENTO DE CADA TEST:
    - Se mockea sigap_config.get_db_path() para apuntar a una ruta controlada,
      sin tocar la DB real del proyecto.
    - Los archivos temporales se eliminan en tearDown.
"""

import unittest
import os
import sys
import sqlite3
import tempfile
from unittest.mock import patch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.utils import auditar_db

# Target del mock: el objeto sigap_config dentro del módulo auditar_db
MOCK_GET_DB_PATH = 'sigap_config.get_db_path'


class TestAuditarDbFuente(unittest.TestCase):
    """Verifica que auditar_db.py cumpla D-005 a nivel de código fuente."""

    def _leer_fuente(self):
        ruta = os.path.join(BASE_DIR, 'scripts', 'utils', 'auditar_db.py')
        with open(ruta, encoding='utf-8') as f:
            return f.read()

    def test_usa_sigap_config_para_ruta(self):
        """auditar_db.py debe obtener la ruta via sigap_config.get_db_path(), no hardcodeada (D-005)."""
        fuente = self._leer_fuente()
        self.assertIn(
            'sigap_config',
            fuente,
            "auditar_db.py no referencia sigap_config — posible violación D-005."
        )
        self.assertIn(
            'get_db_path',
            fuente,
            "auditar_db.py no llama a get_db_path() — posible violación D-005."
        )


class TestAuditarDbRuntime(unittest.TestCase):
    """Tests de comportamiento en runtime de la función auditar()."""

    def setUp(self):
        self._temp_files = []

    def tearDown(self):
        for f in self._temp_files:
            if os.path.exists(f):
                os.unlink(f)

    def _crear_db_temp(self, schema_sql=None):
        """Crea un archivo SQLite temporal y registra su path para limpieza."""
        fd, temp_path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        self._temp_files.append(temp_path)
        if schema_sql:
            conn = sqlite3.connect(temp_path)
            conn.executescript(schema_sql)
            conn.commit()
            conn.close()
        return temp_path

    # ------------------------------------------------------------------
    # TEST 1: ruta inexistente
    # ------------------------------------------------------------------

    def test_ruta_inexistente_no_lanza_excepcion(self):
        """auditar() con ruta que no existe solo loguea y retorna sin explotar."""
        ruta_falsa = os.path.join(BASE_DIR, 'data', '_test_fake_nonexistent.db')
        with patch(MOCK_GET_DB_PATH, return_value=ruta_falsa):
            try:
                auditar_db.auditar()
            except Exception as e:
                self.fail(
                    f"auditar() lanzó excepción con ruta inexistente: {type(e).__name__}: {e}"
                )

    # ------------------------------------------------------------------
    # TEST 2: DB sin param_preferencias
    # ------------------------------------------------------------------

    def test_db_sin_param_preferencias_no_lanza_excepcion(self):
        """auditar() con DB sin param_preferencias solo loguea warning, no lanza excepción."""
        temp_path = self._crear_db_temp("""
            CREATE TABLE movimientos (
                id INTEGER PRIMARY KEY,
                descripcion TEXT
            );
        """)
        with patch(MOCK_GET_DB_PATH, return_value=temp_path):
            try:
                auditar_db.auditar()
            except Exception as e:
                self.fail(
                    f"auditar() lanzó excepción cuando param_preferencias no existe: "
                    f"{type(e).__name__}: {e}"
                )

    # ------------------------------------------------------------------
    # TEST 3: DB con param_preferencias (camino feliz)
    # ------------------------------------------------------------------

    def test_db_con_param_preferencias_completa_sin_error(self):
        """auditar() con DB que tiene param_preferencias completa el ciclo sin errores."""
        temp_path = self._crear_db_temp("""
            CREATE TABLE param_preferencias (
                id    INTEGER PRIMARY KEY,
                clave TEXT NOT NULL,
                valor TEXT
            );
            INSERT INTO param_preferencias (clave, valor) VALUES ('test_clave', 'test_valor');
        """)
        with patch(MOCK_GET_DB_PATH, return_value=temp_path):
            try:
                auditar_db.auditar()
            except Exception as e:
                self.fail(
                    f"auditar() lanzó excepción con DB completa: {type(e).__name__}: {e}"
                )


if __name__ == '__main__':
    unittest.main(verbosity=2)
