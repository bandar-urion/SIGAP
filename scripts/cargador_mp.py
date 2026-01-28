import sqlite3
import csv
import os

# --- CONFIGURACIÓN ---
ruta_bd = os.path.join(os.path.dirname(__file__), '..', 'base_datos', 'control_gastos.db')
ruta_csv = os.path.join(os.path.dirname(__file__), '..', 'datos_entrada', 'mercadopago.csv')

print(f"🔌 Conectando a BD: {ruta_bd}")
print(f"📂 Leyendo archivo: {ruta_csv}")

conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

try:
    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        print("🙈 Saltando las primeras 3 líneas...")
        for _ in range(3): next(archivo)

        lector = csv.DictReader(archivo, delimiter=',')

        contador_nuevos = 0
        contador_duplicados = 0

        for fila in lector:
            ref_id = fila.get('REFERENCE_ID')
            fecha_raw = fila.get('RELEASE_DATE')
            descripcion = fila.get('TRANSACTION_TYPE')
            monto_raw = fila.get('TRANSACTION_NET_AMOUNT')

            if not ref_id or not fecha_raw: continue

            fecha_limpia = fecha_raw.split("T")[0]
            medio = "MercadoPago"

            # --- CORRECCIÓN DE MONEDA ARGENTINA ---
            # 1. Si viene vacío, es 0.
            if not monto_raw:
                monto_limpio = 0.0
            else:
                # 2. Quitamos el punto de los miles ("1.500,00" -> "1500,00")
                temp = monto_raw.replace('.', '')
                # 3. Cambiamos la coma decimal por punto ("1500,00" -> "1500.00")
                temp = temp.replace(',', '.')
                try:
                    monto_limpio = float(temp)
                except ValueError:
                    monto_limpio = 0.0
            # --------------------------------------

            try:
                # Usamos REPLACE INTO para que si el ID ya existe, LO ACTUALICE (por si antes se cargó con 0)
                # OJO: Si prefieres no sobrescribir, usa INSERT OR IGNORE, pero ahora queremos arreglar los ceros.
                cursor.execute("""
                    INSERT OR REPLACE INTO movimientos (id, id_referencia, fecha, descripcion, monto, medio_pago, estado)
                    VALUES (
                        (SELECT id FROM movimientos WHERE id_referencia = ?),
                        ?, ?, ?, ?, ?, 'CONCILIADO'
                    )
                """, (ref_id, ref_id, fecha_limpia, descripcion, monto_limpio, medio))
                # Nota: El truco del SELECT id... es para mantener el ID numérico si ya existía y solo actualizar el monto.

                if cursor.rowcount > 0:
                    contador_nuevos += 1
                else:
                    contador_duplicados += 1

            except sqlite3.Error as e:
                print(f"❌ Error SQL en fila {ref_id}: {e}")

    conn.commit()
    print("-" * 30)
    print(f"✅ Procesados: {contador_nuevos} (Incluye actualizaciones de montos corregidos)")

except Exception as e:
    print(f"❌ ERROR: {e}")
finally:
    conn.close()