"""
Migración D-011: renombrar columna `usuario` → `modulo` en `auditoria_movimientos`.

SQLite no soporta ALTER TABLE ... RENAME COLUMN (hasta 3.25.0).
Se usa el patrón clásico: CREATE nueva tabla → INSERT SELECT → DROP → RENAME.

El script es idempotente: si la columna `modulo` ya existe, no hace nada.
Al completar escribe una entrada en `auditoria_movimientos` con
accion='MIGRACION_CAMPO' y modulo='SISTEMA'.

Uso:
    python scripts/migrate_auditoria_usuario_to_modulo.py
"""

import sqlite3
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ruta DB via sigap_config (nunca hardcodeada)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sigap_config

DB_PATH = sigap_config.get_db_path()


def migrar(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    # ── Idempotencia: verificar si ya fue migrado ──────────────────────────
    cursor.execute("PRAGMA table_info(auditoria_movimientos)")
    columnas = [row[1] for row in cursor.fetchall()]

    if "modulo" in columnas and "usuario" not in columnas:
        print("[MIGRACIÓN] Ya aplicada: columna 'modulo' existe, 'usuario' ausente. Sin cambios.")
        return

    if "modulo" in columnas and "usuario" in columnas:
        print("[MIGRACIÓN] Estado inconsistente: ambas columnas existen. Revisar manualmente.")
        sys.exit(1)

    if "usuario" not in columnas:
        print("[MIGRACIÓN] Columna 'usuario' no encontrada. ¿Tabla incorrecta? Revisar.")
        sys.exit(1)

    print("[MIGRACIÓN] Iniciando: usuario → modulo en auditoria_movimientos...")

    cursor.executescript("""
        PRAGMA foreign_keys = OFF;

        BEGIN;

        -- 1. Crear tabla nueva con columna renombrada
        CREATE TABLE auditoria_movimientos_new (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp         TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),
            modulo            TEXT DEFAULT 'SISTEMA',
            accion            TEXT NOT NULL,
            id_movimiento_ref INTEGER,
            estado_previo     TEXT,
            estado_nuevo      TEXT,
            resultado         TEXT
        );

        -- 2. Copiar datos existentes
        INSERT INTO auditoria_movimientos_new
            (id, timestamp, modulo, accion, id_movimiento_ref, estado_previo, estado_nuevo, resultado)
        SELECT
            id, timestamp, usuario, accion, id_movimiento_ref, estado_previo, estado_nuevo, resultado
        FROM auditoria_movimientos;

        -- 3. Eliminar tabla original
        DROP TABLE auditoria_movimientos;

        -- 4. Renombrar nueva tabla
        ALTER TABLE auditoria_movimientos_new RENAME TO auditoria_movimientos;

        COMMIT;

        PRAGMA foreign_keys = ON;
    """)

    # 5. Verificar
    cursor.execute("PRAGMA table_info(auditoria_movimientos)")
    columnas_post = [row[1] for row in cursor.fetchall()]
    assert "modulo" in columnas_post, "Error post-migración: columna 'modulo' no encontrada"
    assert "usuario" not in columnas_post, "Error post-migración: columna 'usuario' aún presente"

    # 6. Entrada de auditoría
    cursor.execute("""
        INSERT INTO auditoria_movimientos (accion, modulo, estado_previo, estado_nuevo, resultado)
        VALUES ('MIGRACION_CAMPO', 'SISTEMA', 'usuario TEXT DEFAULT SISTEMA', 'modulo TEXT DEFAULT SISTEMA', 'OK')
    """)
    conn.commit()

    print(f"[MIGRACIÓN] Completada. {len(columnas_post)} columnas verificadas.")
    print(f"[MIGRACIÓN] Columnas actuales: {columnas_post}")


def main() -> None:
    print(f"[MIGRACIÓN] DB: {DB_PATH}")
    with sqlite3.connect(DB_PATH) as conn:
        migrar(conn)


if __name__ == "__main__":
    main()
