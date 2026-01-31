import sqlite3
import pandas as pd
import os
import hashlib

# --- CONFIGURACIÓN ---
ruta_bd = os.path.join(os.path.dirname(__file__), '..', 'base_datos', 'control_gastos.db')
ruta_excel = os.path.join(os.path.dirname(__file__), '..', 'datos_entrada', 'santander.xlsx')

print(f"🔌 Conectando a BD: {ruta_bd}")
print(f"🏦 Leyendo Santander: {ruta_excel}")

conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

def limpiar_moneda_banco(valor):
    if pd.isna(valor): return 0.0
    texto = str(valor)
    limpio = texto.replace('$', '').replace(' ', '').strip()
    limpio = limpio.replace('.', '')
    limpio = limpio.replace(',', '.')
    try:
        return float(limpio)
    except ValueError:
        return 0.0

# --- MODIFICACIÓN CLAVE AQUÍ ---
def generar_hash(fecha, descripcion, monto, indice_fila):
    """
    Ahora incluimos 'indice_fila' en la mezcla.
    Esto asegura que dos gastos idénticos en distintas lineas tengan IDs distintos.
    """
    cadena = f"{fecha}{descripcion}{monto}{indice_fila}"
    return hashlib.md5(cadena.encode('utf-8')).hexdigest()

try:
    df = pd.read_excel(ruta_excel)

    contador_nuevos = 0
    contador_duplicados = 0

    print("🔄 Procesando movimientos...")

    cols = [c.strip() for c in df.columns]
    df.columns = cols

    for index, row in df.iterrows():
        fecha_raw = row.get('Fecha')

        if str(fecha_raw).strip() == 'Fecha': continue

        descripcion = row.get('Empresa')
        if pd.isna(descripcion):
            descripcion = row.get('Destinatario')
        if pd.isna(descripcion):
            descripcion = row.get('Concepto')

        monto_raw = row.get('Importe')
        medio_origen = row.get('Medio de pago')

        if pd.isna(fecha_raw) or pd.isna(monto_raw): continue
        if pd.isna(descripcion): continue

        try:
            fecha_dt = pd.to_datetime(fecha_raw, dayfirst=True, errors='coerce')
            if pd.isna(fecha_dt): continue
            fecha_iso = fecha_dt.strftime('%Y-%m-%d')
        except:
            continue

        monto_limpio = limpiar_moneda_banco(monto_raw)

        # --- LLAMADA ACTUALIZADA AL GENERADOR ---
        # Le pasamos 'index' (el número de fila del Excel)
        id_ref = generar_hash(fecha_iso, descripcion, monto_limpio, index)

        medio_pago_final = str(medio_origen) if not pd.isna(medio_origen) else "Santander"

        try:
            cursor.execute("""
                INSERT OR IGNORE INTO movimientos (id_referencia, fecha, descripcion, monto, medio_pago, estado)
                VALUES (?, ?, ?, ?, ?, 'CONCILIADO')
            """, (id_ref, fecha_iso, descripcion, monto_limpio, medio_pago_final))

            if cursor.rowcount > 0:
                contador_nuevos += 1
            else:
                contador_duplicados += 1

        except sqlite3.Error as e:
            print(f"❌ Error SQL: {e}")

    conn.commit()
    print("-" * 30)
    print(f"✅ Procesados Santander: {contador_nuevos}")
    print(f"♻️  Duplicados reales ignorados: {contador_duplicados}")

except Exception as e:
    print(f"❌ ERROR: {e}")
finally:
    conn.close()