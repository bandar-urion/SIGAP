import os
import sys
import unittest
from unittest.mock import patch, MagicMock

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.modulos import carga_gastos
from scripts.modulos.carga_gastos import Transaccion

# --- 1. CUSTOM TEST RUNNER (FORMATO LIMPIO) ---
class SIGAPTestResult(unittest.TextTestResult):
    def getDescription(self, test):
        # Retorna SOLO el docstring, extirpando el nombre feo de la clase
        return test.shortDescription() or str(test)

class SIGAPTestRunner(unittest.TextTestRunner):
    resultclass = SIGAPTestResult
# ----------------------------------------------

class TestTorreControlUI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\n")
        tx_demo = Transaccion("2026-03-03", "DEMO", "S.I.G.A.P. MOCK ENVIRONMENT", 1500, 1)
        
        # 1. Construimos la identidad del test dinámicamente (Ruta Relativa)
        ruta_relativa = os.path.relpath(__file__, BASE_DIR)
        titulo_qa = (
            f"{carga_gastos.C_PURPLE}🛠️  QA TEST RUNNER | Archivo: {ruta_relativa}{carga_gastos.C_RESET}\n\n"
            f"{carga_gastos.C_CYAN}🦅 S.I.G.A.P. - Módulo Testeado: modulos/carga_gastos.py (Motor UI){carga_gastos.C_RESET}\n"
        )

        # 2. Inyectamos el título usando el nuevo parámetro
        carga_gastos.render_dashboard([tx_demo], 0, "TEST_RUNNER_ENV", modo_edicion=False, custom_title=titulo_qa)
        
        print("\n" + "="*80)
        print("🚀 EJECUTANDO TESTS DE UI (MODO SILENCIOSO)...")
        print("="*80 + "\n")


    def setUp(self):
        self.tx = Transaccion("2026-03-03", "REF_TEST", "COMPRA MOCK UI", 1500, 1)
        self.lista_tx = [self.tx]
        self.cursor_mock = MagicMock()

    @patch('scripts.modulos.carga_gastos.cargar_preferencias_contexto', return_value=({}, {}))
    @patch('scripts.modulos.carga_gastos.cargar_diccionario', return_value=[])
    @patch('scripts.modulos.carga_gastos.limpiar_pantalla')
    @patch('scripts.modulos.carga_gastos.leer_input_navegacion')
    @patch('sys.stdout')
    def test_robot_navegacion_y_salida(self, mock_stdout, mock_nav, mock_clear, mock_dicc, mock_prefs):
        """[UI-MOCK] Valida aborto de sesion (Tecla X) y navegacion basica."""
        mock_nav.side_effect = ['DOWN', 'X']
        resultado = carga_gastos.iniciar_torre_control(self.lista_tx, self.cursor_mock, "MOCK_BANK")
        self.assertFalse(resultado)

    @patch('scripts.modulos.carga_gastos.cargar_preferencias_contexto', return_value=({}, {}))
    @patch('scripts.modulos.carga_gastos.cargar_diccionario', return_value=[])
    @patch('scripts.modulos.carga_gastos.limpiar_pantalla')
    @patch('scripts.modulos.carga_gastos.leer_byte')
    @patch('scripts.modulos.carga_gastos.leer_input_navegacion')
    @patch('sys.stdout')
    def test_robot_asignacion_cuotas_manual(self, mock_stdout, mock_nav, mock_byte, mock_clear, mock_dicc, mock_prefs):
        """[UI-MOCK] Valida intervencion manual de cuotas (Tecla C)."""
        mock_nav.side_effect = ['C', 'X']
        mock_byte.side_effect = [b'3', b'\r']
        carga_gastos.iniciar_torre_control(self.lista_tx, self.cursor_mock, "MOCK_BANK")
        self.assertEqual(self.lista_tx[0].cuotas_totales, 3)

if __name__ == '__main__':
    # 2. Reemplazamos el motor estándar por nuestro Custom Runner
    unittest.main(testRunner=SIGAPTestRunner(verbosity=2))
