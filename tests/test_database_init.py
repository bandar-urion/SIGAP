import pytest
import sqlite3
import os

# --- CONFIGURACIÓN (El "BeforeAll" de Pester) ---

# Calculamos la ruta absoluta a la base de datos real
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'control_gastos.db')

@pytest.fixture
def db_cursor():
    """
    Esto es una FIXTURE.
    Equivale al bloque 'BeforeEach' de Pester.
    Prepara la conexión antes del test y la cierra después.
    """
    if not os.path.exists(DB_PATH):
        pytest.fail(f"❌ CRÍTICO: No se encuentra la base de datos en {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    yield cursor  # Aquí se ejecuta el test...

    # ... y aquí se ejecuta el 'Teardown' (limpieza)
    conn.close()

# --- LOS TESTS (Los "It" de Pester) ---

def test_existen_tablas_criticas(db_cursor):
    """Verifica que las tablas maestras existan."""

    # Consultamos el catálogo interno de SQLite
    db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas_encontradas = [fila[0] for fila in db_cursor.fetchall()]

    # Los 'Should -Contain' de Python
    assert 'movimientos' in tablas_encontradas
    assert 'param_categorias' in tablas_encontradas
    assert 'diccionario_terminos' in tablas_encontradas
    assert 'agenda_pagos' in tablas_encontradas

def test_estructura_categorias_correcta(db_cursor):
    """Verifica la Regla de Segregación (Casa vs Terreno)."""

    db_cursor.execute("SELECT nombre FROM param_categorias WHERE tipo='EGRESO'")
    nombres = [fila[0] for fila in db_cursor.fetchall()]

    assert 'Casa' in nombres
    assert 'Terreno' in nombres
    assert 'Alimentos' in nombres

def test_inteligencia_sinonimos_funcionando(db_cursor):
    """
    Prueba de Integración:
    Verifica que el diccionario traduzca 'Sushi' -> 'Comida Preparada'.
    """
    termino_prueba = "Sushi"

    # Hacemos un JOIN para ver si el vínculo está sano
    query = """
        SELECT s.nombre
        FROM diccionario_terminos d
        JOIN param_subcategorias s ON d.id_subcategoria = s.id
        WHERE d.termino = ?
    """
    db_cursor.execute(query, (termino_prueba,))
    resultado = db_cursor.fetchone()

    # Verificación
    assert resultado is not None, "El término 'Sushi' debería existir en el diccionario"
    assert resultado[0] == "Comida Preparada", "Sushi debería mapear a Comida Preparada"

def test_regla_unicidad_constraints(db_cursor):
    """Verifica que la DB tenga configurada la restricción UNIQUE en movimientos."""

    # Inspeccionamos el SQL de creación de la tabla
    db_cursor.execute("SELECT sql FROM sqlite_master WHERE name='movimientos'")
    create_statement = db_cursor.fetchone()[0]

    assert "num_referencia TEXT UNIQUE" in create_statement
