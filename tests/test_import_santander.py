"""
test_import_santander.py — Tests unitarios de parsear_excel_santander()

PROPÓSITO:
    Verificar que la función de parseo del Excel de Santander Río:
      - Lee el archivo con skiprows=13 y engine='openpyxl'.
      - Calcula Monto_Real = Caja de Ahorro + Cuenta Corriente.
      - Filtra filas con Monto_Real == 0.
      - Tolera la ausencia de la columna 'Cuenta Corriente' sin romper.

A diferencia de test_contrato_santander.py (que valida un .xlsx real del
banco si existe en data/inbox/), este test genera sus propios .xlsx
sintéticos en un tempdir, sin tocar el filesystem del usuario.
"""

import unittest
import os
import sys
import tempfile
import shutil

from openpyxl import Workbook

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.import_santander import parsear_excel_santander


def _crear_xlsx(ruta: str, encabezado: list, filas: list):
    """
    Crea un .xlsx con 13 filas de relleno (como el header institucional de
    Santander), seguidas por el encabezado y las filas de datos.
    """
    wb = Workbook()
    ws = wb.active

    # 13 filas de relleno → el parser las saltea con skiprows=13
    for i in range(13):
        ws.append([f"relleno_{i}"])

    ws.append(encabezado)
    for fila in filas:
        ws.append(fila)

    wb.save(ruta)


class TestParsearExcelSantander(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="sigap_test_")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_formato_completo_filtra_monto_cero_y_calcula_monto_real(self):
        """
        Excel con las 5 columnas estándar y 3 filas:
          - una con monto en Caja de Ahorro
          - una con monto en Cuenta Corriente
          - una con 0 en ambas (debe ser filtrada)
        """
        ruta = os.path.join(self.tmpdir, "santander_full.xlsx")
        encabezado = ['Fecha', 'Referencia', 'Descripción', 'Caja de Ahorro', 'Cuenta Corriente']
        filas = [
            ['01/10/2026', 'REF-CA-1', 'Compra en CA', -1500.50, 0],
            ['02/10/2026', 'REF-CC-1', 'Compra en CC', 0, 2300.75],
            ['03/10/2026', 'REF-ZERO', 'Fila a descartar', 0, 0],
        ]
        _crear_xlsx(ruta, encabezado, filas)

        df = parsear_excel_santander(ruta)

        self.assertEqual(len(df), 2, "La fila con Monto_Real==0 no fue filtrada.")

        for col in ['Fecha', 'Referencia', 'Descripción', 'Monto_Real']:
            self.assertIn(col, df.columns, f"Falta la columna '{col}' en el DataFrame.")

        fila_ca = df[df['Referencia'] == 'REF-CA-1'].iloc[0]
        fila_cc = df[df['Referencia'] == 'REF-CC-1'].iloc[0]

        self.assertAlmostEqual(fila_ca['Monto_Real'], -1500.50)
        self.assertAlmostEqual(fila_cc['Monto_Real'], 2300.75)

    def test_sin_columna_cuenta_corriente_usa_solo_caja_de_ahorro(self):
        """
        Si Santander no exporta la columna 'Cuenta Corriente' (p. ej. cuenta
        que solo tiene CA), el parser no debe fallar y Monto_Real debe ser
        igual a Caja de Ahorro.
        """
        ruta = os.path.join(self.tmpdir, "santander_sin_cc.xlsx")
        encabezado = ['Fecha', 'Referencia', 'Descripción', 'Caja de Ahorro']
        filas = [
            ['05/10/2026', 'REF-SOLO-CA', 'Movimiento CA único', -800.00],
        ]
        _crear_xlsx(ruta, encabezado, filas)

        df = parsear_excel_santander(ruta)

        self.assertEqual(len(df), 1)
        self.assertAlmostEqual(df.iloc[0]['Monto_Real'], -800.00)
        self.assertEqual(df.iloc[0]['Referencia'], 'REF-SOLO-CA')


if __name__ == '__main__':
    unittest.main(verbosity=2)
