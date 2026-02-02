import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, 'control_gastos.db')

def migrar():
    print("🦅 MIGRACIÓN v0.6.1: Memoria de Amortización...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Agregamos campo para recordar la preferencia de cuotas por subcategoría
        print("   🔹 Agregando 'amortizacion_default' a param_subcategorias...")
        cursor.execute("ALTER TABLE param_subcategorias ADD COLUMN amortizacion_default INTEGER DEFAULT 0")

        conn.commit()
        print("✅ Éxito. Ahora el sistema puede recordar la duración de los gastos.")

    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e): print("⚠️ Ya estaba aplicado.")
        else: print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrar()