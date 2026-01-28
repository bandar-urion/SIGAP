import sqlite3

def crear_tabla_agenda():
    try:
        # Conectamos a la base de datos
        conn = sqlite3.connect('control_gastos.db')
        cursor = conn.cursor()

        print("🔌 Conectado al S.I.G.A.P...")

        # Definición de la tabla AGENDA_PAGOS
        # Usamos 'IF NOT EXISTS' para no romper nada si la corres dos veces
        sql_create = """
        CREATE TABLE IF NOT EXISTS agenda_pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_vencimiento TEXT NOT NULL,   -- Formato YYYY-MM-DD
            descripcion TEXT NOT NULL,         -- Ej: "Seguro Auto", "Expensas"
            monto_estimado REAL DEFAULT 0,     -- Previsión del gasto
            id_centro_costo INTEGER NOT NULL,  -- ¿De quién es la deuda? (Personal/Familia)
            estado TEXT DEFAULT 'PENDIENTE',   -- PENDIENTE, PAGADO, CANCELADO
            prioridad TEXT DEFAULT 'NORMAL',   -- ALTA, NORMAL, BAJA (Para saber qué pagar primero si hay poca plata)

            -- Integridad Referencial
            FOREIGN KEY (id_centro_costo) REFERENCES centros_costo(id)
        );
        """

        cursor.execute(sql_create)
        conn.commit()
        print("✅ Tabla 'agenda_pagos' desplegada con éxito.")
        print("📡 El Radar de Vencimientos está operativo.")

    except sqlite3.Error as e:
        print(f"❌ Error en el sistema: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    crear_tabla_agenda()