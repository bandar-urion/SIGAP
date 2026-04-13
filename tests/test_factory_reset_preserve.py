"""
test_factory_reset_preserve.py — Cobertura para scripts/factory_reset_preserve_learning.py

PROPÓSITO:
    Verificar que el ciclo backup → reset → restore no pierde datos de forma
    silenciosa. El riesgo crítico es que términos del diccionario sean
    destruidos sin aviso durante un factory reset "con preservación".

ESTRATEGIA DE AISLAMIENTO:
    - Todos los tests usan DBs temporales (tempfile.mkstemp).
    - Se mockean DOS variables para aislar factory_reset_normalized():
        · sigap_config.get_db_path   → afecta a código que llama la función en runtime
        · scripts.factory_reset_normalized.DB_FILE → afecta al módulo-global que ya
          fue evaluado al importar (necesario en Windows donde DB_FILE se resuelve
          en tiempo de carga del módulo, no en tiempo de llamada).
    - Todas las conexiones SQLite se cierran en bloques finally para evitar
      PermissionError al eliminar archivos temporales en Windows.

FUNCIONES BAJO PRUEBA:
    backup_inteligencia(cursor)              → extrae términos antes de la destrucción
    restaurar_inteligencia(cursor, backup)   → reimplanta tras el reset
    factory_reset_normalized()              → usada como paso intermedio del ciclo
"""

import unittest
import os
import sys
import sqlite3
import tempfile
from unittest.mock import patch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.factory_reset_preserve_learning import (
    backup_inteligencia,
    restaurar_inteligencia,
)
from scripts.factory_reset_normalized import factory_reset_normalized

# Mocks necesarios para redirigir factory_reset_normalized() a la DB temporal:
# · DB_FILE ya fue evaluado en tiempo de importación → hay que parcharlo directamente.
# · sigap_config.get_db_path se parchea por completitud y forward-compatibility.
MOCK_GET_DB_PATH = 'sigap_config.get_db_path'
MOCK_DB_FILE     = 'scripts.factory_reset_normalized.DB_FILE'

# Schema mínimo compatible con backup_inteligencia() (replica la estructura real)
SCHEMA_PRE_RESET = """
    CREATE TABLE param_categorias (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        tipo   TEXT NOT NULL
    );
    CREATE TABLE param_subcategorias (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre       TEXT NOT NULL,
        id_categoria INTEGER NOT NULL,
        UNIQUE(nombre, id_categoria),
        FOREIGN KEY (id_categoria) REFERENCES param_categorias(id)
    );
    CREATE TABLE diccionario_terminos (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        termino         TEXT NOT NULL UNIQUE,
        id_subcategoria INTEGER NOT NULL,
        FOREIGN KEY (id_subcategoria) REFERENCES param_subcategorias(id)
    );
"""


class TestFactoryResetPreserve(unittest.TestCase):

    def setUp(self):
        self._temp_files = []

    def tearDown(self):
        for f in self._temp_files:
            if os.path.exists(f):
                try:
                    os.unlink(f)
                except PermissionError:
                    pass  # Windows: el archivo puede seguir en uso por gc; no crítico

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _crear_db_temp(self, schema_sql=None):
        """Crea un archivo SQLite temporal registrado para limpieza en tearDown."""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        self._temp_files.append(path)
        if schema_sql:
            conn = sqlite3.connect(path)
            conn.executescript(schema_sql)
            conn.commit()
            conn.close()
        return path

    def _sembrar_terminos(self, path, terminos):
        """
        Inserta categorías, subcategorías y términos en la DB indicada.
        terminos: lista de (termino, subcat_nombre, cat_nombre).
        """
        conn = sqlite3.connect(path)
        cur  = conn.cursor()
        cat_ids    = {}
        subcat_ids = {}
        try:
            for termino, subcat_nombre, cat_nombre in terminos:
                if cat_nombre not in cat_ids:
                    cur.execute(
                        "INSERT OR IGNORE INTO param_categorias (nombre, tipo) VALUES (?, 'EGRESO')",
                        (cat_nombre,)
                    )
                    cur.execute(
                        "SELECT id FROM param_categorias WHERE nombre = ?", (cat_nombre,)
                    )
                    cat_ids[cat_nombre] = cur.fetchone()[0]

                key = (subcat_nombre, cat_nombre)
                if key not in subcat_ids:
                    cur.execute(
                        "INSERT OR IGNORE INTO param_subcategorias (nombre, id_categoria) "
                        "VALUES (?, ?)",
                        (subcat_nombre, cat_ids[cat_nombre])
                    )
                    cur.execute(
                        "SELECT id FROM param_subcategorias "
                        "WHERE nombre = ? AND id_categoria = ?",
                        (subcat_nombre, cat_ids[cat_nombre])
                    )
                    subcat_ids[key] = cur.fetchone()[0]

                cur.execute(
                    "INSERT OR IGNORE INTO diccionario_terminos "
                    "(termino, id_subcategoria) VALUES (?, ?)",
                    (termino, subcat_ids[key])
                )
            conn.commit()
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # TEST 1: ciclo completo sin pérdida de datos
    # ------------------------------------------------------------------

    def test_ciclo_completo_sin_perdida(self):
        """
        Ciclo backup → factory_reset_normalized → restore no pierde términos.

        Setup: DB temporal con schema mínimo + 3 términos que pertenecen a
        subcategorías que factory_reset_normalized recrea en su propio seeding
        (Combustible/AUTO, Supermercado/ALIMENTACION), para que el restore
        los encuentre en el nuevo schema y los reimplante.

        Verificación: los 3 términos originales están en diccionario_terminos
        al finalizar el ciclo.

        ⚠️  ADVERTENCIA PARA EL MANTENEDOR:
        Si este test falla con "PÉRDIDA SILENCIOSA", hay dos causas posibles:

          1. BUG REAL en el ciclo backup/restore → investigar
             factory_reset_preserve_learning.py.

          2. CAMBIO EN EL SEEDING de factory_reset_normalized.py → los términos
             'Nafta', 'YPF' y 'Coto' ya no están en el seeding inicial, por lo
             que el restore no puede reimplantarlos (la subcategoría destino
             no existe en el nuevo schema). En ese caso, actualizar este test
             con términos que sí estén en el seeding vigente.

        Verificar en factory_reset_normalized.py la sección "sinonimos_data"
        para confirmar cuál es la causa antes de tocar el código de producción.
        """
        temp_path = self._crear_db_temp(SCHEMA_PRE_RESET)

        terminos_originales = [
            ('Nafta', 'Combustible',  'AUTO'),
            ('YPF',   'Combustible',  'AUTO'),
            ('Coto',  'Supermercado', 'ALIMENTACION'),
        ]
        self._sembrar_terminos(temp_path, terminos_originales)

        with patch(MOCK_GET_DB_PATH, return_value=temp_path), \
             patch(MOCK_DB_FILE,     new=temp_path):

            # PASO 1: backup (antes del reset)
            conn = sqlite3.connect(temp_path)
            cur  = conn.cursor()
            try:
                backup = backup_inteligencia(cur)
            finally:
                conn.close()

            # PASO 2: factory reset sobre la DB temporal
            factory_reset_normalized()

            # PASO 3: restore + verificación
            conn = sqlite3.connect(temp_path)
            cur  = conn.cursor()
            try:
                restaurar_inteligencia(cur, backup)
                conn.commit()
                cur.execute("SELECT termino FROM diccionario_terminos")
                terminos_post = {row[0] for row in cur.fetchall()}
            finally:
                conn.close()

        terminos_esperados = {t[0] for t in terminos_originales}
        perdidos = terminos_esperados - terminos_post
        self.assertEqual(
            perdidos, set(),
            f"¡PÉRDIDA SILENCIOSA! Términos no encontrados tras el ciclo: {perdidos}\n\n"
            f"⚠️  ANTES DE TOCAR CÓDIGO DE PRODUCCIÓN, verificar dos causas posibles:\n"
            f"  1. BUG REAL en backup/restore → revisar factory_reset_preserve_learning.py\n"
            f"  2. CAMBIO EN SEEDING → los términos perdidos ya no están en 'sinonimos_data'\n"
            f"     de factory_reset_normalized.py. Si es así, actualizar este test.\n"
            f"  Confirmar cuál es la causa antes de actuar."
        )

    # ------------------------------------------------------------------
    # TEST 2: resiliencia con diccionario vacío (tabla inexistente)
    # ------------------------------------------------------------------

    def test_backup_con_diccionario_inexistente_retorna_lista_vacia(self):
        """
        backup_inteligencia() sobre una DB sin diccionario_terminos
        no lanza excepción y retorna [].

        Simula una DB recién creada o corrompida que no tiene el diccionario.
        """
        temp_path = self._crear_db_temp("""
            CREATE TABLE param_categorias    (id INTEGER PRIMARY KEY, nombre TEXT, tipo TEXT);
            CREATE TABLE param_subcategorias (id INTEGER PRIMARY KEY, nombre TEXT,
                                              id_categoria INTEGER);
        """)

        conn = sqlite3.connect(temp_path)
        cur  = conn.cursor()
        try:
            resultado = backup_inteligencia(cur)
        except Exception as e:
            self.fail(
                f"backup_inteligencia() lanzó excepción con diccionario ausente: "
                f"{type(e).__name__}: {e}"
            )
        finally:
            conn.close()

        self.assertEqual(
            resultado, [],
            f"Se esperaba [] con diccionario ausente, se obtuvo: {resultado}"
        )

    # ------------------------------------------------------------------
    # TEST 3: huérfano en restore no bloquea el resto
    # ------------------------------------------------------------------

    def test_restore_con_huerfano_no_bloquea(self):
        """
        restaurar_inteligencia() con un término huérfano (subcategoría que ya
        no existe en el nuevo schema) loguea el huérfano pero completa el
        resto de términos válidos sin lanzar excepción.

        Setup: schema real de factory_reset_normalized en la DB temporal.
        backup_data mezcla 1 término válido + 1 término huérfano.
        Verificación: 'Shell' → restaurado; 'XYZ_huerfano' → ignorado sin crash.
        """
        temp_path = self._crear_db_temp()

        # Crear el schema limpio sobre la DB temporal
        with patch(MOCK_GET_DB_PATH, return_value=temp_path), \
             patch(MOCK_DB_FILE,     new=temp_path):
            factory_reset_normalized()

        # backup_data: (termino, subcat_nombre, cat_nombre)
        # 'Shell' → 'Combustible' / 'AUTO'   → existe en el nuevo schema ✅
        # 'XYZ'   → 'SubcatFantasma' / 'CatFantasma' → huérfano ❌
        backup_data = [
            ('Shell',        'Combustible',    'AUTO'),
            ('XYZ_huerfano', 'SubcatFantasma', 'CatFantasma'),
        ]

        conn = sqlite3.connect(temp_path)
        cur  = conn.cursor()
        try:
            restaurar_inteligencia(cur, backup_data)
            conn.commit()
            cur.execute(
                "SELECT termino FROM diccionario_terminos WHERE termino = 'Shell'"
            )
            restaurado = cur.fetchone()
        except Exception as e:
            self.fail(
                f"restaurar_inteligencia() lanzó excepción ante un huérfano: "
                f"{type(e).__name__}: {e}"
            )
        finally:
            conn.close()

        self.assertIsNotNone(
            restaurado,
            "El término válido 'Shell' no fue restaurado a pesar de existir en el nuevo schema."
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
