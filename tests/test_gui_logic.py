import unittest
import sys
from unittest.mock import MagicMock

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Simulamos la estructura que queremos testear
class SelectorSimulator:
    def __init__(self, opciones):
        self.opciones = opciones
        self.buffer = ""

    def filtrar(self, texto):
        self.buffer = texto.upper()
        return [op for op in self.opciones if self.buffer in op[1].upper()]

class TestNavegacion(unittest.TestCase):
    def setUp(self):
        # Datos de prueba: (id, nombre)
        self.opciones = [
            (1, "FAMILIA"),
            (2, "FARMACIA"),
            (3, "CASA"),
            (4, "COMIDA")
        ]
        self.selector = SelectorSimulator(self.opciones)

    def test_filtrado_letras_seguidas(self):
        """Prueba si al escribir 'FA' filtra correctamente."""
        res = self.selector.filtrar("FA")
        nombres = [r[1] for r in res]
        self.assertIn("FAMILIA", nombres)
        self.assertIn("FARMACIA", nombres)
        self.assertEqual(len(res), 2)
        print("\n✅ Test Filtrado 'FA': OK")

    def test_filtrado_sin_coincidencias(self):
        """Prueba qué pasa si el buffer tiene basura."""
        res = self.selector.filtrar("XYZ")
        self.assertEqual(len(res), 0)
        print("✅ Test Filtrado Vacío: OK")

if __name__ == '__main__':
    unittest.main()
