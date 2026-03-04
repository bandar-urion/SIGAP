import os
import sys
import unittest
from unittest.mock import patch, MagicMock

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.modulos import inbox_movimientos
from scripts.modulos.inbox_movimientos import Movimiento

# --- 1. CUSTOM TEST RUNNER (FORMATO LIMPIO) ---
class SIGAPTestResult(unittest.TextTestResult):
    def getDescription(self, test):
        # Retorna SOLO el docstring, extirpando el nombre feo de la clase
        return test.shortDescription() or str(test)

class SIGAPTestRunner(unittest.TextTestRunner):
    resultclass = SIGAPTestResult
# ----------------------------------------------

class TestUiInboxMovimientos(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\n")
        mov_demo = Movimiento("2026-03-03", "DEMO", "S.I.G.A.P. MOCK ENVIRONMENT", 1500, 1)
        
        # 1. Construimos la identidad del test dinámicamente (Ruta Relativa)
        ruta_relativa = os.path.relpath(__file__, BASE_DIR)
        titulo_qa = (
            f"{inbox_movimientos.C_PURPLE}🛠️  QA TEST RUNNER | Archivo: {ruta_relativa}{inbox_movimientos.C_RESET}\n\n"
            f"{inbox_movimientos.C_CYAN}🦅 S.I.G.A.P. - Módulo Testeado: modulos/inbox_movimientos.py (Motor UI){inbox_movimientos.C_RESET}\n"
        )

        # 2. Inyectamos el título usando el nuevo parámetro
        inbox_movimientos.render_dashboard([mov_demo], 0, "TEST_RUNNER_ENV", modo_edicion=False, custom_title=titulo_qa)
        
        print("\n" + "="*80)
        print("🚀 EJECUTANDO TESTS DE UI (MODO SILENCIOSO)...")
        print("="*80 + "\n")


    def setUp(self):
        # 1. Datos base del test
        self.mov = Movimiento("2026-03-03", "REF_TEST", "COMPRA MOCK UI", 1500, 1)
        self.lista_movs = [self.mov]
        self.cursor_mock = MagicMock()

        # 2. Centralización de Mocks
        # Usamos patch().start() para activarlos y addCleanup() para apagarlos al terminar el test
        patcher_prefs = patch('scripts.modulos.inbox_movimientos.cargar_preferencias_contexto', return_value=({}, {}))
        self.mock_prefs = patcher_prefs.start()
        self.addCleanup(patcher_prefs.stop)

        patcher_dicc = patch('scripts.modulos.inbox_movimientos.cargar_diccionario', return_value=[])
        self.mock_dicc = patcher_dicc.start()
        self.addCleanup(patcher_dicc.stop)

        patcher_clear = patch('scripts.modulos.inbox_movimientos.limpiar_pantalla')
        self.mock_clear = patcher_clear.start()
        self.addCleanup(patcher_clear.stop)

        patcher_stdout = patch('sys.stdout')
        self.mock_stdout = patcher_stdout.start()
        self.addCleanup(patcher_stdout.stop)

        patcher_nav = patch('scripts.modulos.inbox_movimientos.leer_input_navegacion')
        self.mock_nav = patcher_nav.start()
        self.addCleanup(patcher_nav.stop)

        patcher_byte = patch('scripts.modulos.inbox_movimientos.leer_byte')
        self.mock_byte = patcher_byte.start()
        self.addCleanup(patcher_byte.stop)


    def test_robot_navegacion_y_salida(self):
        """[UI-MOCK] Valida aborto de sesion (Tecla X) y navegacion basica."""
        self.mock_nav.side_effect = ['DOWN', 'X']
        resultado = inbox_movimientos.iniciar_inbox_movimientos(self.lista_movs, self.cursor_mock, "MOCK_BANK")
        self.assertFalse(resultado)

    def test_robot_asignacion_cuotas_manual(self):
        """[UI-MOCK] Valida intervencion manual de cuotas (Tecla C)."""
        self.mock_nav.side_effect = ['C', 'X']
        self.mock_byte.side_effect = [b'3', b'\r']
        inbox_movimientos.iniciar_inbox_movimientos(self.lista_movs, self.cursor_mock, "MOCK_BANK")
        self.assertEqual(self.lista_movs[0].cuotas_totales, 3)

    def test_robot_maquina_estados_descarte(self):
        """[UI-MOCK] Valida Maquina de Estados: Descarte (Right) y Recuperacion (Left)."""
        
        # 1. Probamos Descarte (Flecha Derecha) y Salir
        self.mock_nav.side_effect = ['RIGHT', 'X']
        inbox_movimientos.iniciar_inbox_movimientos(self.lista_movs, self.cursor_mock, "MOCK_BANK")
        
        # Validamos que cambie internamente el estado del objeto
        self.assertEqual(self.lista_movs[0].estado, 'DESCARTADO', "El estado no cambió a DESCARTADO.")
        
        # 2. Reiniciamos el mock de teclado y probamos Recuperación (Flecha Izquierda)
        self.mock_nav.side_effect = ['LEFT', 'X']
        inbox_movimientos.iniciar_inbox_movimientos(self.lista_movs, self.cursor_mock, "MOCK_BANK")
        
        # Validamos que vuelva a su estado original
        self.assertEqual(self.lista_movs[0].estado, 'PENDIENTE', "El estado no se recuperó a PENDIENTE.")

    def test_robot_motor_hibrido_numerico(self):
        """[UI-MOCK] Valida Motor Hibrido: Seleccion numerica (Fast-Pick)."""
        
        # Simulamos que la base de datos devuelve 2 opciones válidas para elegir
        self.cursor_mock.fetchall.return_value = [(1, "OPCION_MOCK"), (2, "OTRA_OPCION")]
        
        # 1. Comandos de la Torre: Editar (Enter) y Salir (X)
        self.mock_nav.side_effect = ['\r', 'X']
        
        # 2. Secuencia dentro del modo edición (CC -> CAT -> SUBCAT -> Memorizar)
        # Selecciona la opción 1 (b'1') y confirma (b'\r') en los 3 menús.
        # Luego presiona 'n' (b'n') para rechazar la memorización de la IA.
        self.mock_byte.side_effect = [
            b'1', b'\r',   # Centro de Costo
            b'1', b'\r',   # Categoría
            b'1', b'\r',   # Subcategoría
            b'n'           # ¿Memorizar IA? (No)
        ]
        
        inbox_movimientos.iniciar_inbox_movimientos(self.lista_movs, self.cursor_mock, "MOCK_BANK")
        
        # 3. Validamos que el registro haya avanzado por todo el embudo correctamente
        tx = self.lista_movs[0]
        self.assertEqual(tx.id_cc, 1, "Fallo al asignar Centro de Costo.")
        self.assertEqual(tx.id_cat, 1, "Fallo al asignar Categoría.")
        self.assertEqual(tx.id_subcat, 1, "Fallo al asignar Subcategoría.")
        self.assertEqual(tx.estado, 'LISTO', "El registro no alcanzó el estado LISTO.")

    def test_robot_motor_hibrido_texto(self):
        """[UI-MOCK] Valida Motor Hibrido: Busqueda por texto y autocompletado."""
        
        # El Mock de la DB devuelve opciones. El usuario tipea 'S', 'U' y da Enter.
        self.cursor_mock.fetchall.return_value = [(1, "SUPERMERCADO"), (2, "FARMACIA")]
        
        self.mock_nav.side_effect = ['\r', 'X'] # Enter para editar, X para salir
        
        self.mock_byte.side_effect = [
            b'S', b'U', b'\r', # CC: Tipea SU y confirma
            b'1', b'\r',       # Cat: Selecciona rápido la opción 1
            b'1', b'\r',       # Subcat: Selecciona rápido la opción 1
            b'n'               # Memo: Rechaza
        ]
        
        inbox_movimientos.iniciar_inbox_movimientos(self.lista_movs, self.cursor_mock, "MOCK_BANK")
        
        # Validamos que el flujo avanzó
        self.assertEqual(self.lista_movs[0].id_cc, 1, "Fallo al asignar CC por búsqueda de texto.")
        self.assertEqual(self.lista_movs[0].estado, 'LISTO', "El registro no alcanzó el estado LISTO.")

    def test_robot_freno_inercia_cancelacion(self):
        """[UI-MOCK] Valida Freno de Inercia: Cancelacion de edicion (ESC)."""
        
        self.mock_nav.side_effect = ['\r', 'X'] # Enter para entrar a editar, luego X para salir del programa
        
        # Dentro del menú de Centro de Costo, el usuario tipea 'A' pero luego se arrepiente y manda ESC (\x1b)
        self.mock_byte.side_effect = [b'A', b'\x1b'] 
        
        inbox_movimientos.iniciar_inbox_movimientos(self.lista_movs, self.cursor_mock, "MOCK_BANK")
        
        # El estado debe seguir intacto (PENDIENTE) porque abortamos antes de confirmar
        self.assertEqual(self.lista_movs[0].estado, 'PENDIENTE', "El registro no abortó limpiamente la edición.")


if __name__ == '__main__':
    # 2. Reemplazamos el motor estándar por nuestro Custom Runner
    unittest.main(testRunner=SIGAPTestRunner(verbosity=2))
