"""
test_sigap_cli.py — Cobertura para sigap.py (CLI orquestador)

PROPÓSITO:
    Verificar los contratos de la interfaz CLI de S.I.G.A.P.:
    - Argparse reconoce los subcomandos válidos.
    - show_status() no explota con DB inexistente ni con DB válida.
    - run_reset() rechaza la operación si el usuario no confirma.
    - RUTA_DB proviene de sigap_config y termina en 'sigap.db' (no nombre legacy).

ESTRATEGIA DE AISLAMIENTO:
    - show_status() usa el módulo-global RUTA_DB, mockeado via patch.object.
    - run_reset() usa input() estándar (excepción arquitectónica documentada),
      mockeado via patch('builtins.input').
    - Ningún test toca la DB real del proyecto.
"""

import unittest
import os
import sys
import sqlite3
import tempfile
import io
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import sigap


# Tablas que show_status() consulta con COUNT(*)
TABLAS_SCHEMA = [
    'movimientos',
    'param_centros_costo',
    'param_categorias',
    'param_subcategorias',
    'auditoria_movimientos',
]


class TestSigapRutaDB(unittest.TestCase):
    """Verifica que RUTA_DB proviene de sigap_config y no tiene nombre legacy."""

    def test_ruta_db_termina_en_sigap_db(self):
        """RUTA_DB en sigap.py debe terminar en 'sigap.db', no en un nombre legacy."""
        self.assertTrue(
            sigap.RUTA_DB.endswith('sigap.db'),
            f"RUTA_DB='{sigap.RUTA_DB}' no termina en 'sigap.db' — posible nombre legacy."
        )

    def test_ruta_db_es_absoluta(self):
        """RUTA_DB debe ser una ruta absoluta para evitar DB fantasmas."""
        self.assertTrue(
            os.path.isabs(sigap.RUTA_DB),
            f"RUTA_DB='{sigap.RUTA_DB}' no es absoluta."
        )


class TestSigapArgparse(unittest.TestCase):
    """Verifica que argparse despacha los subcomandos correctos."""

    def _run_main_with_argv(self, argv, mock_target):
        """Ejecuta sigap.main() con argv dado y retorna el mock del handler."""
        with patch.object(sys, 'argv', argv), \
             patch(f'sigap.{mock_target}') as mock_fn:
            sigap.main()
        return mock_fn

    def test_subcomando_status_invoca_show_status(self):
        """'python sigap.py status' debe invocar show_status() una sola vez."""
        mock_fn = self._run_main_with_argv(['sigap', 'status'], 'show_status')
        mock_fn.assert_called_once()

    def test_subcomando_reset_invoca_run_reset(self):
        """'python sigap.py reset' debe invocar run_reset() una sola vez."""
        mock_fn = self._run_main_with_argv(['sigap', 'reset'], 'run_reset')
        mock_fn.assert_called_once()


class TestShowStatus(unittest.TestCase):
    """Verifica el comportamiento de show_status() en distintos estados de la DB."""

    def setUp(self):
        self._temp_files = []

    def tearDown(self):
        for f in self._temp_files:
            if os.path.exists(f):
                os.unlink(f)

    def _crear_db_temp_con_schema(self):
        """Crea un archivo SQLite temporal con las tablas que consulta show_status()."""
        fd, temp_path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        self._temp_files.append(temp_path)
        conn = sqlite3.connect(temp_path)
        for tabla in TABLAS_SCHEMA:
            conn.execute(f"CREATE TABLE {tabla} (id INTEGER PRIMARY KEY)")
        conn.commit()
        conn.close()
        return temp_path

    # ------------------------------------------------------------------
    # DB inexistente
    # ------------------------------------------------------------------

    def test_show_status_db_inexistente_no_lanza_excepcion(self):
        """show_status() con DB inexistente imprime advertencia y retorna sin crashear."""
        ruta_falsa = os.path.join(BASE_DIR, 'data', '_test_fake_sigap_cli.db')
        salida = io.StringIO()
        with patch.object(sigap, 'RUTA_DB', ruta_falsa), \
             redirect_stdout(salida):
            try:
                sigap.show_status()
            except Exception as e:
                self.fail(
                    f"show_status() lanzó excepción con DB inexistente: "
                    f"{type(e).__name__}: {e}"
                )
        # Verificamos que imprimió la advertencia esperada
        self.assertIn('NO existe', salida.getvalue())

    # ------------------------------------------------------------------
    # DB válida
    # ------------------------------------------------------------------

    def test_show_status_db_valida_imprime_conteos(self):
        """show_status() con DB válida imprime conteos y retorna sin crashear."""
        temp_path = self._crear_db_temp_con_schema()
        salida = io.StringIO()
        with patch.object(sigap, 'RUTA_DB', temp_path), \
             redirect_stdout(salida):
            try:
                sigap.show_status()
            except Exception as e:
                self.fail(
                    f"show_status() lanzó excepción con DB válida: "
                    f"{type(e).__name__}: {e}"
                )
        # Verificamos que imprimió la conexión exitosa
        self.assertIn('CONEXIÓN EXITOSA', salida.getvalue())


class TestRunReset(unittest.TestCase):
    """Verifica el comportamiento de run_reset() ante distintas respuestas del usuario."""

    def test_run_reset_cancelado_no_llama_factory_reset(self):
        """run_reset() con input()='no' imprime cancelación y NO llama a factory_reset_normalized()."""
        salida = io.StringIO()
        with patch('builtins.input', return_value='no'), \
             patch.object(sigap.db_reset_script, 'factory_reset_normalized') as mock_reset, \
             redirect_stdout(salida):
            sigap.run_reset()

        mock_reset.assert_not_called()
        self.assertIn('cancelada', salida.getvalue().lower())


if __name__ == '__main__':
    unittest.main(verbosity=2)
