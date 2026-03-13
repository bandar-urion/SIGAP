import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.modulos import inbox_movimientos as motor


# ==============================================================================
# BLOQUE 1: HIGIENE DE TEXTO
# Testea limpiar_texto_visual(): eliminación de prefijos bancarios genéricos.
# ==============================================================================

class TestLimpiezaTexto(unittest.TestCase):
    """Verifica que el limpiador elimine correctamente el ruido bancario."""

    def test_elimina_prefijos_bancarios(self):
        casos = [
            ("Compra con tarjeta de debito UBER TRIP", "UBER TRIP"),
            ("Transferencia realizada A JOSE PEREZ",   "A JOSE PEREZ"),
            ("DEBITO DIRECTO GIMNASIO",                "GIMNASIO"),
            ("Pago DEBIN Netflix",                     "Netflix"),
        ]
        for sucio, esperado in casos:
            with self.subTest(entrada=sucio):
                self.assertEqual(motor.limpiar_texto_visual(sucio), esperado)

    def test_normaliza_espacios(self):
        """Trim y colapso de espacios múltiples."""
        self.assertEqual(motor.limpiar_texto_visual("   Espacios   Extra   "), "Espacios Extra")


# ==============================================================================
# BLOQUE 2: MOTOR DE CUOTAS (REGEX)
# Testea detectar_cuotas_regex() vía el constructor de Movimiento.
# Se divide en: casos válidos, trampas de fechas, lógica imposible.
# ==============================================================================

class TestMotorCuotasValidos(unittest.TestCase):
    """Casos que el regex SÍ debe detectar correctamente."""

    def _cuotas(self, descripcion):
        tx = motor.Movimiento("2026-01-01", "REF", descripcion, -100, 1)
        return tx.cuota_actual, tx.cuotas_totales

    def test_formato_barra_estandar(self):
        """03/12 → cuota 3 de 12."""
        self.assertEqual(self._cuotas("COMPRA FRAVEGA 03/12"), (3, 12))

    def test_formato_barra_ultimo(self):
        """12/12 → última cuota."""
        self.assertEqual(self._cuotas("VISA CREDITO 12/12"), (12, 12))

    def test_formato_barra_primero(self):
        """01/12 → primera cuota."""
        self.assertEqual(self._cuotas("COMPRA EN COTO 01/12"), (1, 12))

    def test_formato_barra_corto(self):
        """01/03 → plan de 3 cuotas."""
        self.assertEqual(self._cuotas("PLAN V 01/03"), (1, 3))

    def test_formato_cta_solo_actual(self):
        """CTA 2 → cuota actual sin total (comportamiento documentado del regex)."""
        tx = motor.Movimiento("2026-01-01", "REF", "SEGURO AUTO CTA 2", -100, 1)
        self.assertEqual(tx.cuota_actual, 2)
        self.assertEqual(tx.cuotas_totales, 0)

    def test_formato_cta_numerico(self):
        """CTA 3 → solo actual."""
        tx = motor.Movimiento("2026-01-01", "REF", "CTA 3", -100, 1)
        self.assertEqual(tx.cuota_actual, 3)


class TestMotorCuotasTrampasFechas(unittest.TestCase):
    """Casos que PARECEN cuotas pero son fechas. El regex debe ignorarlos."""

    def _cuotas(self, descripcion):
        tx = motor.Movimiento("2026-01-01", "REF", descripcion, -100, 1)
        return tx.cuota_actual, tx.cuotas_totales

    def test_fecha_completa_con_anio(self):
        """DD/MM/AAAA no debe confundirse con cuotas."""
        self.assertEqual(self._cuotas("PAGO 01/12/2025 AUTOMATICO"), (0, 0))

    def test_fecha_completa_vto(self):
        """VTO DD/MM/AAAA no debe confundirse con cuotas."""
        self.assertEqual(self._cuotas("PAGO VTO 15/03/2026"), (0, 0))

    def test_rango_de_fechas_del_al(self):
        """PERIODO DEL 01/12 AL 31/12 → rango, no cuotas."""
        self.assertEqual(self._cuotas("PERIODO DEL 01/12 AL 31/12"), (0, 0))

    def test_vencimiento_vto(self):
        """VTO 10/05 → vencimiento, no cuotas."""
        self.assertEqual(self._cuotas("VTO 10/05 CIERRE"), (0, 0))


class TestMotorCuotasLogicaImposible(unittest.TestCase):
    """Casos matemáticamente absurdos. El regex debe rechazarlos."""

    def _cuotas(self, descripcion):
        tx = motor.Movimiento("2026-01-01", "REF", descripcion, -100, 1)
        return tx.cuota_actual, tx.cuotas_totales

    def test_cuota_actual_mayor_al_total(self):
        """13/12 es imposible: cuota actual > total."""
        self.assertEqual(self._cuotas("ERROR DE SISTEMA 13/12"), (0, 0))

    def test_total_exagerado(self):
        """01/99 supera el límite de 60 cuotas del sistema."""
        self.assertEqual(self._cuotas("PLAN LARGO 01/99"), (0, 0))


# ==============================================================================
# BLOQUE 3: MOTOR DE CLASIFICACIÓN (DICCIONARIO + INFERENCIA DE CONTEXTO)
# Testea reanalizar_inteligencia(): matching de diccionario y relleno automático de CC.
# ==============================================================================

class TestMotorClasificacion(unittest.TestCase):
    """Verifica que el motor encuentre coincidencias en el diccionario."""

    def setUp(self):
        # Formato: (termino, id_sub, nom_sub, nom_cat, id_cat)
        self.diccionario = [
            ("COTO",                10, "Supermercado", "Alimentos", 1),
            ("SHELL",               20, "Combustible",  "Auto",      2),
            ("TRANSFERENCIA A JOSE",30, "Sueldo",       "Ingresos",  3),
        ]

    def test_match_termino_simple(self):
        """COTO en la descripción → subcategoría Supermercado."""
        tx = motor.Movimiento("2026-01-01", "REF1", "COMPRA COTO SUC 10", -100, 1)
        motor.reanalizar_inteligencia([tx], self.diccionario)
        self.assertTrue(tx.ia_match)
        self.assertEqual(tx.nombre_subcat, "Supermercado")

    def test_match_termino_compuesto(self):
        """La regla 'TRANSFERENCIA A JOSE' matchea texto más largo."""
        tx = motor.Movimiento("2026-01-01", "REF3", "TRANSFERENCIA A JOSE MARTIN", 1000, 1)
        motor.reanalizar_inteligencia([tx], self.diccionario)
        self.assertTrue(tx.ia_match)

    def test_no_match_descripcion_desconocida(self):
        """Descripción sin ningún término del diccionario → sin match."""
        tx = motor.Movimiento("2026-01-01", "REF4", "GASTO DESCONOCIDO", -10, 1)
        motor.reanalizar_inteligencia([tx], self.diccionario)
        self.assertFalse(tx.ia_match)


class TestInferenciaContexto(unittest.TestCase):
    """
    Verifica que el motor infiera el Centro de Costo a partir del historial.
    Si 'Supermercado' siempre fue de 'Familia', el nuevo movimiento debe
    heredar esa preferencia automáticamente.
    """

    def test_relleno_automatico_cc(self):
        diccionario = [("COTO", 10, "Supermercado", "Alimentos", 1)]
        prefs_cc    = {10: (5, "Familia")}

        tx = motor.Movimiento("2026-01-01", "REF", "COMPRA EN COTO", -1000, 1)
        motor.reanalizar_inteligencia([tx], diccionario, map_prefs_cc=prefs_cc)

        self.assertEqual(tx.nombre_subcat, "Supermercado")
        self.assertEqual(tx.nombre_cc,     "Familia")
        self.assertEqual(tx.estado,        "AUTO")


if __name__ == '__main__':
    unittest.main()
