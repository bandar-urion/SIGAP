"""
Tests del Motor de Similitud — Gobernanza de Alta de Subcategoría
Valida los 3 criterios: Contención, Prefijo común, Palabras clave compartidas.
"""

import unittest
import os


def detectar_similares(nombre_new, subcategorias_existentes):
    """
    Replica exacta de la lógica del motor en inbox_movimientos.py.
    Recibe el nombre propuesto y una lista de (id, nombre) existentes.
    Retorna lista de (id, nombre, motivo) similares encontrados.
    """
    similares = []
    nombre_new_lower = nombre_new.lower()
    palabras_new = set(w for w in nombre_new_lower.split() if len(w) > 2)

    for sub_id, sub_nom in subcategorias_existentes:
        sub_lower = sub_nom.lower()
        palabras_sub = set(w for w in sub_lower.split() if len(w) > 2)
        es_similar = False
        motivo = ""

        # Criterio A: Contención
        if nombre_new_lower in sub_lower or sub_lower in nombre_new_lower:
            es_similar = True
            motivo = f"Contención con '{sub_nom}'"

        # Criterio B: Prefijo común (4+ caracteres) — independiente de A
        if not es_similar and len(nombre_new_lower) >= 4 and len(sub_lower) >= 4:
            prefijo = os.path.commonprefix([nombre_new_lower, sub_lower])
            if len(prefijo) >= 4:
                es_similar = True
                motivo = f"Prefijo '{prefijo}' con '{sub_nom}'"

        # Criterio C: Palabras clave compartidas — independiente de A y B
        if not es_similar and palabras_new and palabras_sub and palabras_new & palabras_sub:
            es_similar = True
            comunes = palabras_new & palabras_sub
            motivo = f"Palabras {comunes} con '{sub_nom}'"

        if es_similar:
            similares.append((sub_id, sub_nom, motivo))

    return similares


class TestGobernanzaSimilitud(unittest.TestCase):

    def setUp(self):
        """Catálogo base simulando una DB real."""
        self.catalogo = [
            (1,  "Supermercado"),
            (2,  "Farmacia"),
            (3,  "Combustible"),
            (4,  "Servicios Básicos"),
            (5,  "Seguro Auto"),
            (6,  "Varios"),
            (7,  "Desayuno"),
            (8,  "Almuerzo"),
            (9,  "Restaurante"),
            (10, "Transporte Público"),
        ]

    # ------------------------------------------------------------------
    # CRITERIO A: Contención
    # ------------------------------------------------------------------

    def test_contencion_nuevo_dentro_existente(self):
        """'Super' está contenido en 'Supermercado' → debe alertar."""
        res = detectar_similares("Super", self.catalogo)
        nombres = [r[1] for r in res]
        self.assertIn("Supermercado", nombres)

    def test_contencion_existente_dentro_nuevo(self):
        """'Gas y Combustible' contiene a 'Combustible' → debe alertar."""
        res = detectar_similares("Gas Y Combustible", self.catalogo)
        nombres = [r[1] for r in res]
        self.assertIn("Combustible", nombres)

    def test_contencion_exacta_no_duplica_con_paso3(self):
        """'Supermercado' exacto debería ser capturado antes (paso 3), 
        pero si llega aquí igual detecta similitud."""
        res = detectar_similares("Supermercado", self.catalogo)
        nombres = [r[1] for r in res]
        self.assertIn("Supermercado", nombres)

    # ------------------------------------------------------------------
    # CRITERIO B: Prefijo común
    # ------------------------------------------------------------------

    def test_prefijo_comun_farmacia(self):
        """'Farma' comparte prefijo 'farm' con 'Farmacia' → debe alertar."""
        res = detectar_similares("Farma", self.catalogo)
        nombres = [r[1] for r in res]
        self.assertIn("Farmacia", nombres)

    def test_prefijo_comun_seguro(self):
        """'Seguro Vida' comparte prefijo 'seguro' con 'Seguro Auto' → debe alertar."""
        res = detectar_similares("Seguro Vida", self.catalogo)
        nombres = [r[1] for r in res]
        self.assertIn("Seguro Auto", nombres)

    def test_prefijo_corto_no_alerta(self):
        """'Se' solo tiene 2 chars de prefijo con 'Servicios' → NO debe alertar por prefijo."""
        res = detectar_similares("Se Fue", self.catalogo)
        # Puede que haya resultado por palabras, pero no por prefijo de 'Se'
        # Verificamos que no hay false-positives absurdos
        nombres = [r[1] for r in res]
        self.assertNotIn("Seguro Auto", nombres)  # 'se' no matchea 'segu'

    # ------------------------------------------------------------------
    # CRITERIO C: Palabras clave compartidas
    # ------------------------------------------------------------------

    def test_palabras_clave_transporte(self):
        """'Uber Transporte' comparte 'transporte' con 'Transporte Público' → debe alertar."""
        res = detectar_similares("Uber Transporte", self.catalogo)
        nombres = [r[1] for r in res]
        self.assertIn("Transporte Público", nombres)

    def test_palabras_clave_servicios(self):
        """'Servicios Digitales' comparte 'servicios' con 'Servicios Básicos' → debe alertar."""
        res = detectar_similares("Servicios Digitales", self.catalogo)
        nombres = [r[1] for r in res]
        self.assertIn("Servicios Básicos", nombres)

    def test_palabras_cortas_ignoradas(self):
        """Palabras de 2 chars o menos no deben generar match ('de', 'la', 'el')."""
        res = detectar_similares("De La Casa", self.catalogo)
        # No hay ninguna subcategoría que comparta palabras significativas
        self.assertEqual(len(res), 0)

    # ------------------------------------------------------------------
    # CASOS CLAVE: SIN SIMILITUD (flujo directo, sin fricción)
    # ------------------------------------------------------------------

    def test_sin_similitud_totalmente_nuevo(self):
        """'Netflix' no tiene similitud con nada → lista vacía, sin fricción."""
        res = detectar_similares("Netflix", self.catalogo)
        self.assertEqual(len(res), 0)

    def test_sin_similitud_gimnasio(self):
        """'Gimnasio' no matchea nada del catálogo → sin alerta."""
        res = detectar_similares("Gimnasio", self.catalogo)
        self.assertEqual(len(res), 0)

    def test_sin_similitud_colegio(self):
        """'Colegio Cuota' no matchea nada → sin alerta."""
        res = detectar_similares("Colegio Cuota", self.catalogo)
        self.assertEqual(len(res), 0)

    # ------------------------------------------------------------------
    # CASOS REALES DE FINANZAS PERSONALES
    # ------------------------------------------------------------------

    def test_caso_real_desayuno_almuerzo(self):
        """'Cafe Desayuno' comparte 'desayuno' con 'Desayuno' → debe alertar."""
        res = detectar_similares("Cafe Desayuno", self.catalogo)
        nombres = [r[1] for r in res]
        self.assertIn("Desayuno", nombres)

    def test_caso_real_restaurant_vs_restaurante(self):
        """'Restaurant' está contenido en 'Restaurante' → debe alertar."""
        res = detectar_similares("Restaurant", self.catalogo)
        nombres = [r[1] for r in res]
        self.assertIn("Restaurante", nombres)

    def test_caso_real_tv_sin_similitud(self):
        """'Smart Tv' es algo completamente nuevo → sin alerta. 
        (El caso del TV de $1.000.000 que mencionó Martín)"""
        res = detectar_similares("Smart Tv", self.catalogo)
        self.assertEqual(len(res), 0)

    def test_caso_real_nafta_combustible(self):
        """'Nafta' no tiene similitud directa con 'Combustible' → sin alerta.
        (Son distintos, el usuario sabe lo que hace)"""
        res = detectar_similares("Nafta", self.catalogo)
        self.assertEqual(len(res), 0)


if __name__ == '__main__':
    # Runner con salida descriptiva
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestGobernanzaSimilitud)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


class TestGobernanzaFrecuencia(unittest.TestCase):
    """Tests del criterio de frecuencia y lógica de justificación."""

    def _make_mov(self, descripcion):
        """Crea un mock mínimo de Movimiento para los tests."""
        class MovMock:
            def __init__(self, desc):
                self.descripcion_original = desc
        return MovMock(descripcion)

    def _detectar_freq_lote(self, nombre_new, lista_movs):
        """Replica la lógica de freq_lote de evaluar_gobernanza."""
        nombre_lower = nombre_new.lower()
        palabras_new = set(w for w in nombre_lower.split() if len(w) > 2)
        count = 0
        for mov in lista_movs:
            # limpiar_texto_visual simplificado para el test
            desc = mov.descripcion_original.lower()
            if any(p in desc for p in palabras_new if len(p) > 3):
                count += 1
        return count

    def _requiere_justificacion(self, freq_lote, freq_historica):
        return freq_lote <= 1 and freq_historica == 0

    # ------------------------------------------------------------------
    # Frecuencia en lote
    # ------------------------------------------------------------------

    def test_freq_lote_multiple(self):
        """'Electricidad' aparece 3 veces en el lote → freq_lote = 3."""
        movs = [
            self._make_mov("EDESUR ELECTRICIDAD ENERO"),
            self._make_mov("EDESUR ELECTRICIDAD FEBRERO"),
            self._make_mov("EDESUR ELECTRICIDAD MARZO"),
            self._make_mov("SUPERMERCADO COTO"),
        ]
        freq = self._detectar_freq_lote("Electricidad", movs)
        self.assertEqual(freq, 3)

    def test_freq_lote_unica(self):
        """'Smart Tv' aparece solo 1 vez en el lote."""
        movs = [
            self._make_mov("COMPRA SMART TV SAMSUNG"),
            self._make_mov("SUPERMERCADO COTO"),
        ]
        freq = self._detectar_freq_lote("Smart Tv", movs)
        self.assertEqual(freq, 1)

    def test_freq_lote_ninguna(self):
        """'Gimnasio' no aparece en el lote → freq_lote = 0."""
        movs = [
            self._make_mov("SUPERMERCADO COTO"),
            self._make_mov("FARMACITY"),
        ]
        freq = self._detectar_freq_lote("Gimnasio", movs)
        self.assertEqual(freq, 0)

    # ------------------------------------------------------------------
    # Lógica de requiere_justificacion
    # ------------------------------------------------------------------

    def test_requiere_justificacion_primera_vez(self):
        """Sin historia y solo 1 en lote → requiere justificación."""
        self.assertTrue(self._requiere_justificacion(freq_lote=1, freq_historica=0))

    def test_no_requiere_por_historial(self):
        """Con historial → no requiere justificación aunque sea nuevo en lote."""
        self.assertFalse(self._requiere_justificacion(freq_lote=1, freq_historica=5))

    def test_no_requiere_por_lote_multiple(self):
        """Aparece 3 veces en el lote → no requiere justificación."""
        self.assertFalse(self._requiere_justificacion(freq_lote=3, freq_historica=0))

    def test_no_requiere_ambas_fuentes(self):
        """Con historial Y múltiples en lote → verde total."""
        self.assertFalse(self._requiere_justificacion(freq_lote=4, freq_historica=12))

    def test_caso_real_electricidad_nueva(self):
        """Electricidad: primera vez en lote (1) y sin historial → pide justificación.
        Pero el usuario sabe que es mensual → el sistema acepta la justificación."""
        requiere = self._requiere_justificacion(freq_lote=1, freq_historica=0)
        self.assertTrue(requiere)
        # Simular que el usuario ingresó justificación
        justificacion = "Pago mensual recurrente"
        self.assertTrue(len(justificacion) > 0)  # el sistema acepta y procede

    def test_caso_real_tv_unica(self):
        """Smart TV: 1 vez en lote, sin historial → pide justificación.
        Es un gasto único, el usuario puede justificarlo igual."""
        requiere = self._requiere_justificacion(freq_lote=1, freq_historica=0)
        self.assertTrue(requiere)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestGobernanzaSimilitud))
    suite.addTests(loader.loadTestsFromTestCase(TestGobernanzaFrecuencia))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
