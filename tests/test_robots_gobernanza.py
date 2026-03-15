import unittest
import sqlite3
import sys
import os
from unittest.mock import patch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.modulos.inbox_movimientos import evaluar_gobernanza, render_panel_gobernanza

MODULE = 'scripts.modulos.inbox_movimientos'

SCHEMA_SQL = """
    CREATE TABLE param_categorias (
        id   INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        tipo   TEXT NOT NULL
    );
    CREATE TABLE param_subcategorias (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre       TEXT NOT NULL,
        id_categoria INTEGER NOT NULL
    );
    CREATE TABLE auditoria_movimientos (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp         TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),
        usuario           TEXT DEFAULT 'SISTEMA',
        accion            TEXT NOT NULL,
        id_movimiento_ref INTEGER,
        estado_previo     TEXT,
        estado_nuevo      TEXT,
        resultado         TEXT
    );
    CREATE TABLE movimientos (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT
    );
"""


class TestRobotsGobernanza(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.executescript(SCHEMA_SQL)
        self.cursor.execute(
            "INSERT INTO param_categorias (id, nombre, tipo) VALUES (1, 'Alimentos', 'EGRESO')"
        )
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    # ------------------------------------------------------------------
    # ROBOT 1 — Crear subcategoría nueva, confirmación con ENTER
    # ------------------------------------------------------------------
    def test_robot_crear_subcategoria_nueva(self):
        """Setup: cat id=1 'Alimentos', sin subcategorias.
        Un registro histórico en movimientos garantiza requiere_justificacion=False
        para que ENTER active la rama de confirmación directa."""
        self.cursor.execute(
            "INSERT INTO movimientos (descripcion) VALUES ('Compra Supermercado')"
        )

        gov = evaluar_gobernanza(self.cursor, 'Supermercado', 1, 'Alimentos', [])

        self.assertIsNone(gov['duplicado'])
        self.assertEqual(gov['similares'], [])
        self.assertTrue(gov['title_case'])

        with patch(f'{MODULE}.leer_byte', return_value=b'\r'), \
             patch(f'{MODULE}.vaciar_buffer_teclado'), \
             patch(f'{MODULE}.beep_error'), \
             patch('builtins.print'):
            decision, justificacion = render_panel_gobernanza(gov, 80)

        self.assertEqual(decision, 'CONFIRMAR')

    # ------------------------------------------------------------------
    # ROBOT 2 — Rechazo por duplicado exacto
    # ------------------------------------------------------------------
    def test_robot_rechazo_duplicado_exacto(self):
        """Setup: 'Supermercado' ya existe en param_subcategorias.
        evaluar_gobernanza detecta duplicado; render devuelve CANCELAR
        sin importar la tecla presionada."""
        self.cursor.execute(
            "INSERT INTO param_subcategorias (nombre, id_categoria) VALUES ('Supermercado', 1)"
        )

        gov = evaluar_gobernanza(self.cursor, 'Supermercado', 1, 'Alimentos', [])

        self.assertIsNotNone(gov['duplicado'])

        with patch(f'{MODULE}.leer_byte', return_value=b'\r'), \
             patch(f'{MODULE}.vaciar_buffer_teclado'), \
             patch(f'{MODULE}.beep_error'), \
             patch('builtins.print'):
            decision, _ = render_panel_gobernanza(gov, 80)

        self.assertEqual(decision, 'CANCELAR')

    # ------------------------------------------------------------------
    # ROBOT 3 — Alerta de similitud, adoptar similar con [1]
    # ------------------------------------------------------------------
    def test_robot_alerta_similitud(self):
        """Setup: 'Supermercado' existe. Buscar 'Super' activa la detección
        de similitud por substring ('super' ⊂ 'supermercado').
        Presionar [1] adopta el similar existente."""
        self.cursor.execute(
            "INSERT INTO param_subcategorias (nombre, id_categoria) VALUES ('Supermercado', 1)"
        )

        gov = evaluar_gobernanza(self.cursor, 'Super', 1, 'Alimentos', [])

        self.assertGreater(len(gov['similares']), 0)

        with patch(f'{MODULE}.leer_byte', return_value=b'1'), \
             patch(f'{MODULE}.vaciar_buffer_teclado'), \
             patch(f'{MODULE}.beep_error'), \
             patch('builtins.print'):
            decision, _ = render_panel_gobernanza(gov, 80)

        self.assertTrue(decision.startswith('ADOPTAR:'))

    # ------------------------------------------------------------------
    # ROBOT 4 — Justificación requerida, confirmar con [M]
    # ------------------------------------------------------------------
    def test_robot_justificacion_requerida(self):
        """Setup: sin subcategorias, sin historial en movimientos.
        'Gimnasio' activa requiere_justificacion=True.
        Presionar [M] devuelve CONFIRMAR con justificación mensual."""
        gov = evaluar_gobernanza(self.cursor, 'Gimnasio', 1, 'Alimentos', [])

        self.assertTrue(gov['requiere_justificacion'])

        with patch(f'{MODULE}.leer_byte', return_value=b'm'), \
             patch(f'{MODULE}.vaciar_buffer_teclado'), \
             patch(f'{MODULE}.beep_error'), \
             patch(f'{MODULE}.time.sleep'), \
             patch('builtins.print'):
            decision, justificacion = render_panel_gobernanza(gov, 80)

        self.assertEqual(decision, 'CONFIRMAR')
        self.assertEqual(justificacion, 'Pago mensual recurrente')

    # ------------------------------------------------------------------
    # ROBOT 5 — Cancelación por usuario con ESC
    # ------------------------------------------------------------------
    def test_robot_cancelacion_por_usuario(self):
        """Setup: sin subcategorias. 'Verduras' pasa validaciones básicas.
        Presionar ESC cancela sin importar el estado de justificación."""
        gov = evaluar_gobernanza(self.cursor, 'Verduras', 1, 'Alimentos', [])

        self.assertIsNone(gov['duplicado'])

        with patch(f'{MODULE}.leer_byte', return_value=b'\x1b'), \
             patch(f'{MODULE}.vaciar_buffer_teclado'), \
             patch(f'{MODULE}.beep_error'), \
             patch('builtins.print'):
            decision, justificacion = render_panel_gobernanza(gov, 80)

        self.assertEqual(decision, 'CANCELAR')
        self.assertIsNone(justificacion)


if __name__ == '__main__':
    unittest.main()
