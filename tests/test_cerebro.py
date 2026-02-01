import unittest
import sys
import os

# Truco ninja para importar módulos desde la carpeta superior
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.modulos import carga_gastos

class TestCerebroSIGAP(unittest.TestCase):

    def test_limpieza_texto(self):
        """Verifica que el limpiador quite la basura bancaria correctamente."""
        print("\n🧠 TEST: Higiene de Texto...")

        casos = [
            ("Compra con tarjeta de debito UBER TRIP", "UBER TRIP"),
            ("Transferencia realizada A JOSE PEREZ", "A JOSE PEREZ"),
            ("DEBITO DIRECTO GIMNASIO", "GIMNASIO"),
            ("   Espacios   Extra   ", "Espacios Extra"), # Trim y espacios dobles
            ("Pago DEBIN Netflix", "Netflix")
        ]

        for sucio, esperado in casos:
            resultado = carga_gastos.limpiar_texto_visual(sucio)
            self.assertEqual(resultado, esperado)
            print(f"   ✅ '{sucio}' -> '{resultado}'")

    def test_intellisense_match(self):
        """Verifica que la IA encuentre coincidencias en el diccionario."""
        print("\n🧠 TEST: Motor de Inteligencia...")

        # 1. Creamos un diccionario FALSO (Mock)
        # Formato: (termino, id_sub, nom_sub, nom_cat, id_cat)
        diccionario_mock = [
            ("COTO", 10, "Supermercado", "Alimentos", 1),
            ("SHELL", 20, "Combustible", "Auto", 2),
            ("TRANSFERENCIA A JOSE", 30, "Sueldo", "Ingresos", 3)
        ]

        # 2. Creamos transacciones de prueba
        tx1 = carga_gastos.Transaccion("01-01-2026", "REF1", "COMPRA COTO SUC 10", -100, 1)
        tx2 = carga_gastos.Transaccion("01-01-2026", "REF2", "CARGA SHELL", -500, 1)
        tx3 = carga_gastos.Transaccion("01-01-2026", "REF3", "TRANSFERENCIA A JOSE MARTIN", 1000, 1)
        tx4 = carga_gastos.Transaccion("01-01-2026", "REF4", "GASTO DESCONOCIDO", -10, 1)

        lista_tx = [tx1, tx2, tx3, tx4]

        # 3. Ejecutamos el cerebro
        carga_gastos.reanalizar_inteligencia(lista_tx, diccionario_mock)

        # 4. Validamos resultados
        self.assertTrue(tx1.ia_match, "❌ Coto debería ser detectado")
        self.assertEqual(tx1.nombre_subcat, "Supermercado")

        self.assertTrue(tx2.ia_match, "❌ Shell debería ser detectado")

        # Test de especificidad (La regla es 'TRANSFERENCIA A JOSE', el texto es mas largo)
        self.assertTrue(tx3.ia_match, "❌ Transferencia parcial debería funcionar")

        # Test de negativo
        self.assertFalse(tx4.ia_match, "❌ Gasto desconocido no debería tener match")

        print("   ✅ Todas las pruebas de inteligencia pasaron.")

if __name__ == '__main__':
    unittest.main()