"""
test_contrato_santander.py — Contract Test: Formato Excel Santander Río

PROPÓSITO:
    Verificar que el archivo Excel descargado del banco tiene el contrato
    de formato que el parser (import_santander.py) espera antes de procesarlo.

    Santander Río modifica el formato de sus resúmenes sin aviso previo.
    Este test actúa como el primer guardián: si el banco cambió algo,
    este test falla con un mensaje claro ANTES de que el parser toque los datos.

COMPORTAMIENTO:
    - Si no hay ningún .xlsx en data/inbox/ → todos los tests se SALTEAN (skip).
      Esto permite correr la suite completa sin tener un archivo del banco presente.
    - Si hay un .xlsx → se valida el contrato completo.
    - Los lock files de Windows (~$*.xlsx) se ignoran automáticamente.

CÓMO CORRER SOLO ESTE TEST:
    python -m unittest tests.test_contrato_santander -v

CONTRATO ESPERADO (Santander Río — formato vigente):
    - skiprows=13: las primeras 13 filas son encabezado institucional
    - Columnas obligatorias: Fecha, Descripción, Referencia, Caja de Ahorro, Cuenta Corriente
    - Columnas opcionales conocidas: Sucursal origen, Saldo
    - Columna Fecha: parseable como fecha (dayfirst=True)
    - Al menos un movimiento con Monto_Real != 0
"""

import unittest
import os
import sys
import glob
import pandas as pd
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ruta relativa al inbox (compatible con ejecución desde raíz del proyecto)
INBOX_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'inbox')

# Columnas que el parser import_santander.py requiere obligatoriamente
COLUMNAS_REQUERIDAS = ['Fecha', 'Descripción', 'Referencia', 'Caja de Ahorro', 'Cuenta Corriente']

# Columnas opcionales conocidas (documentadas pero no requeridas por el parser)
COLUMNAS_OPCIONALES_CONOCIDAS = ['Sucursal origen', 'Saldo']

# Parámetro de parseo que debe mantenerse sincronizado con import_santander.py
SKIPROWS = 13


def buscar_xlsx_valido():
    """
    Busca el primer .xlsx en data/inbox/ que no sea un lock file de Windows.
    Retorna la ruta o None si no hay archivos.
    """
    archivos = glob.glob(os.path.join(INBOX_DIR, '*.xlsx'))
    validos = [a for a in archivos if not os.path.basename(a).startswith('~$')]
    return validos[0] if validos else None


def skip_si_no_hay_archivo(func):
    """
    Decorador: saltea el test con mensaje claro si no hay xlsx en inbox.
    """
    def wrapper(self, *args, **kwargs):
        if self.archivo is None:
            self.skipTest(
                f"Sin archivo en data/inbox/ — colocar Excel de Santander para activar este test"
            )
        return func(self, *args, **kwargs)
    return wrapper


class TestContratoSantander(unittest.TestCase):
    """
    Valida que el Excel de Santander Río cumpla el contrato esperado por el parser.
    """

    @classmethod
    def setUpClass(cls):
        """Intenta cargar el archivo una sola vez para todos los tests."""
        cls.archivo = buscar_xlsx_valido()
        cls.df = None
        cls.error_lectura = None

        if cls.archivo:
            try:
                df_raw = pd.read_excel(cls.archivo, skiprows=SKIPROWS, engine='openpyxl')
                cls.df = df_raw.dropna(how='all', axis=1)
            except Exception as e:
                cls.error_lectura = str(e)

    # ------------------------------------------------------------------
    # TEST 1: Detectar el archivo
    # ------------------------------------------------------------------

    def test_01_archivo_presente_en_inbox(self):
        """Verifica que exista al menos un .xlsx válido en data/inbox/."""
        if self.archivo is None:
            self.skipTest("Sin archivo en data/inbox/ — test informativo, no bloqueante")
        self.assertIsNotNone(
            self.archivo,
            f"No se encontró ningún .xlsx en {INBOX_DIR}\n"
            f"  → Descargá el resumen de Santander y colocalo en data/inbox/"
        )

    # ------------------------------------------------------------------
    # TEST 2: Lectura sin errores
    # ------------------------------------------------------------------

    @skip_si_no_hay_archivo
    def test_02_lectura_sin_errores(self):
        """Verifica que el archivo se pueda abrir con openpyxl y skiprows=13."""
        self.assertIsNone(
            self.error_lectura,
            f"El archivo no pudo leerse con skiprows={SKIPROWS}.\n"
            f"  → Error: {self.error_lectura}\n"
            f"  → Santander puede haber cambiado la cantidad de filas de encabezado.\n"
            f"  → Verificar y actualizar SKIPROWS en este test y en import_santander.py"
        )
        self.assertIsNotNone(self.df, "El DataFrame resultante es None")

    # ------------------------------------------------------------------
    # TEST 3: Columnas obligatorias presentes
    # ------------------------------------------------------------------

    @skip_si_no_hay_archivo
    def test_03_columnas_requeridas_presentes(self):
        """
        Verifica que todas las columnas que el parser usa estén presentes.
        Si este test falla, Santander cambió el nombre de alguna columna.
        """
        if self.df is None:
            self.skipTest("DataFrame no disponible (ver test_02)")

        columnas_reales = list(self.df.columns)
        faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in columnas_reales]

        self.assertEqual(
            len(faltantes), 0,
            f"Columnas requeridas FALTANTES en el Excel:\n"
            f"  → Faltantes: {faltantes}\n"
            f"  → Columnas reales detectadas: {columnas_reales}\n"
            f"  → Santander cambió el nombre de estas columnas.\n"
            f"  → Actualizar import_santander.py y este test."
        )

    # ------------------------------------------------------------------
    # TEST 4: Columnas nuevas desconocidas (alerta informativa)
    # ------------------------------------------------------------------

    @skip_si_no_hay_archivo
    def test_04_sin_columnas_desconocidas_nuevas(self):
        """
        Detecta si Santander agregó columnas nuevas que no conocemos.
        No es bloqueante, pero indica un cambio de formato que merece atención.
        """
        if self.df is None:
            self.skipTest("DataFrame no disponible (ver test_02)")

        todas_conocidas = COLUMNAS_REQUERIDAS + COLUMNAS_OPCIONALES_CONOCIDAS
        columnas_reales = list(self.df.columns)
        nuevas = [c for c in columnas_reales if c not in todas_conocidas]

        # Informamos pero no fallamos — el parser puede ignorarlas sin problema
        if nuevas:
            print(
                f"\n  ⚠️  AVISO: Columnas nuevas detectadas en el Excel: {nuevas}\n"
                f"     El parser las ignorará, pero conviene documentarlas\n"
                f"     en COLUMNAS_OPCIONALES_CONOCIDAS de este test."
            )
        # Test pasa siempre — es solo informativo
        self.assertTrue(True)

    # ------------------------------------------------------------------
    # TEST 5: Columna Fecha parseable
    # ------------------------------------------------------------------

    @skip_si_no_hay_archivo
    def test_05_columna_fecha_parseable(self):
        """
        Verifica que la columna Fecha contenga valores convertibles a datetime.
        Santander usa formato DD/MM/YYYY (dayfirst=True).
        """
        if self.df is None or 'Fecha' not in self.df.columns:
            self.skipTest("Columna Fecha no disponible (ver tests anteriores)")

        # Tomamos las primeras 5 filas no nulas para validar
        muestra = self.df['Fecha'].dropna().head(5)

        self.assertGreater(
            len(muestra), 0,
            "La columna Fecha está vacía en las primeras filas."
        )

        errores = []
        for val in muestra:
            try:
                pd.to_datetime(val, dayfirst=True)
            except Exception as e:
                errores.append(f"  '{val}' → {e}")

        self.assertEqual(
            len(errores), 0,
            f"Valores de Fecha no parseables (formato esperado: DD/MM/YYYY):\n"
            + "\n".join(errores) +
            f"\n  → Santander puede haber cambiado el formato de fecha."
        )

    # ------------------------------------------------------------------
    # TEST 6: Al menos un movimiento con monto real
    # ------------------------------------------------------------------

    @skip_si_no_hay_archivo
    def test_06_hay_movimientos_con_monto(self):
        """
        Verifica que la fusión de Caja de Ahorro + Cuenta Corriente
        produzca al menos un movimiento con monto != 0.
        Un archivo con todo en cero indicaría un problema de parseo.
        """
        if self.df is None:
            self.skipTest("DataFrame no disponible (ver test_02)")

        col_ca = 'Caja de Ahorro'
        col_cc = 'Cuenta Corriente'

        df_trabajo = self.df.copy()

        if col_ca in df_trabajo.columns:
            df_trabajo[col_ca] = df_trabajo[col_ca].fillna(0)
        else:
            df_trabajo[col_ca] = 0

        if col_cc in df_trabajo.columns:
            df_trabajo[col_cc] = df_trabajo[col_cc].fillna(0)
        else:
            df_trabajo[col_cc] = 0

        df_trabajo['Monto_Real'] = df_trabajo[col_ca] + df_trabajo[col_cc]
        movimientos_validos = df_trabajo[df_trabajo['Monto_Real'] != 0]

        self.assertGreater(
            len(movimientos_validos), 0,
            f"No se encontró ningún movimiento con Monto_Real != 0.\n"
            f"  → Total de filas en el archivo: {len(self.df)}\n"
            f"  → Verificar que el archivo no esté vacío o que skiprows={SKIPROWS} sea correcto."
        )

    # ------------------------------------------------------------------
    # TEST 7: Consistencia con import_santander.py (skiprows)
    # ------------------------------------------------------------------

    @skip_si_no_hay_archivo
    def test_07_skiprows_produce_cabecera_valida(self):
        """
        Verifica que después de saltar SKIPROWS filas, la primera fila
        sea efectivamente la cabecera de datos (no una fila de datos bancarios).
        La cabecera debe contener strings, no fechas ni números.
        """
        if self.df is None:
            self.skipTest("DataFrame no disponible (ver test_02)")

        columnas = list(self.df.columns)

        # Las columnas deben ser strings, no timestamps ni números
        columnas_invalidas = []
        for col in columnas:
            if not isinstance(col, str):
                columnas_invalidas.append(f"  '{col}' es de tipo {type(col).__name__}")

        self.assertEqual(
            len(columnas_invalidas), 0,
            f"Las columnas no son strings — skiprows={SKIPROWS} puede estar desajustado:\n"
            + "\n".join(columnas_invalidas) +
            f"\n  → Santander puede haber cambiado la cantidad de filas de encabezado.\n"
            f"  → Ajustar SKIPROWS en este test y en import_santander.py"
        )


class TestContratoSantanderInforme(unittest.TestCase):
    """
    Test de resumen: imprime un diagnóstico completo del archivo detectado.
    Útil para ejecutar manualmente antes de una importación.
    """

    def test_00_diagnostico_general(self):
        """Imprime estado general del archivo en inbox (siempre pasa)."""
        archivo = buscar_xlsx_valido()

        if archivo is None:
            print(f"\n  📭 Inbox vacío: no hay .xlsx en {INBOX_DIR}")
            print(f"     Colocar el resumen de Santander para activar el Contract Test.")
            return

        print(f"\n  📄 Archivo: {os.path.basename(archivo)}")

        try:
            df = pd.read_excel(archivo, skiprows=SKIPROWS, engine='openpyxl')
            df = df.dropna(how='all', axis=1)

            col_ca = 'Caja de Ahorro'
            col_cc = 'Cuenta Corriente'
            df[col_ca] = df.get(col_ca, 0).fillna(0)
            df[col_cc] = df.get(col_cc, 0).fillna(0)
            df['Monto_Real'] = df[col_ca] + df[col_cc]

            validos = df[df['Monto_Real'] != 0]

            print(f"  📊 Filas totales: {len(df)} | Movimientos con monto: {len(validos)}")
            print(f"  📋 Columnas: {list(df.columns)}")

            faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
            if faltantes:
                print(f"  ❌ Columnas faltantes: {faltantes}")
            else:
                print(f"  ✅ Todas las columnas requeridas presentes")

        except Exception as e:
            print(f"  ❌ Error al leer: {e}")

        self.assertTrue(True)  # El diagnóstico siempre pasa


if __name__ == '__main__':
    unittest.main(verbosity=2)
