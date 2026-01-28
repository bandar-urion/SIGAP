import sqlite3
import pandas as pd
import os

# --- CONFIGURACIÓN ---
ruta_bd = os.path.join(os.path.dirname(__file__), '..', 'base_datos', 'control_gastos.db')
ruta_excel = os.path.join(os.path.dirname(__file__), '..', 'datos_entrada', 'amex.xlsx')

print(f"🔌 Conectando a BD: {ruta_bd}")
print(f"📊 Leyendo Excel con Pandas: {ruta_excel}")

conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

def limpiar_moneda_amex(valor):
    """ Convierte cualquier cosa (texto, float, int) a un float limpio. """
    if pd.isna(valor): return 0.0

    # Truco: Convertimos a string primero para poder limpiar símbolos
    texto = str(valor)

    # Si ya viene como número puro (ej: -62000.0), lo devolvemos directo
    # Pero Amex suele mezclar cosas, así que limpiamos igual.
    limpio = texto.replace('$', '').replace(' ', '').strip()

    # Lógica Argentina: Quitar punto de mil, cambiar coma por punto
    limpio = limpio.replace('.', '')
    limpio = limpio.replace(',', '.')

    try:
        return float(limpio)
    except ValueError:
        return 0.0

try:
    # --- FASE 1: ENCONTRAR LA CABECERA (A PRUEBA DE BALAS) ---
    # Leemos sin cabecera (header=None) para ver los datos crudos
    df_crudo = pd.read_excel(ruta_excel, header=None)

    fila_inicio = None

    print("🔦 Escaneando archivo en busca de 'Fecha' y 'Descripción'...")

    for indice, fila in df_crudo.iterrows():
        # AQUÍ ESTABA EL ERROR ANTES:
        # En vez de unir todo a lo bruto, revisamos celda por celda convertida a texto.
        valores_fila = [str(x).strip() for x in fila.values]

        if "Fecha" in valores_fila and "Descripción" in valores_fila:
            fila_inicio = indice
            print(f"✅ Cabecera encontrada en la fila {indice + 1}")
            break

    if fila_inicio is None:
        raise Exception("❌ No encontré la fila de encabezados. Revisa que el Excel tenga 'Fecha' y 'Descripción'.")

    # --- FASE 2: CARGAR DATOS REALES ---
    # Recargamos usando la fila detectada como cabecera
    df = pd.read_excel(ruta_excel, header=fila_inicio)

    contador_nuevos = 0
    contador_duplicados = 0

    print("🔄 Procesando filas...")

    for index, row in df.iterrows():
        # 1. EXTRACCIÓN
        fecha_raw = row['Fecha']
        descripcion = row['Descripción']
        id_ref = row['Comprobante']
        monto_raw = row['Monto en pesos']

        # --- FILTROS DE BASURA ---
        if pd.isna(fecha_raw) or pd.isna(descripcion): continue
        if "Subtotal" in str(descripcion) or "Consumido" in str(descripcion): continue
        if str(fecha_raw).strip() == "Fecha": continue # Cabecera repetida

        # 2. TRANSFORMACIÓN
        try:
            fecha_dt = pd.to_datetime(fecha_raw, dayfirst=True, errors='coerce')
            if pd.isna(fecha_dt): continue
            fecha_iso = fecha_dt.strftime('%Y-%m-%d')
        except:
            continue

        monto_limpio = limpiar_moneda_amex(monto_raw)

        # ID Sintético
        if pd.isna(id_ref) or str(id_ref).strip() == '':
            id_ref = f"AMEX-{fecha_iso}-{abs(monto_limpio)}"
        else:
            id_ref = str(id_ref).replace('.0', '') # Quita decimales de IDs numéricos

        # 3. INYECCIÓN
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO movimientos (id, id_referencia, fecha, descripcion, monto, medio_pago, estado)
                VALUES (
                    (SELECT id FROM movimientos WHERE id_referencia = ?),
                    ?, ?, ?, ?, 'Tarjeta Amex', 'CONCILIADO'
                )
            """, (id_ref, id_ref, fecha_iso, descripcion, monto_limpio))

            if cursor.rowcount > 0:
                contador_nuevos += 1
            else:
                contador_duplicados += 1

        except sqlite3.Error as e:
            print(f"❌ Error SQL: {e}")

    conn.commit()
    print("-" * 30)
    print(f"✅ Procesados Amex: {contador_nuevos}")

except Exception as e:
    print(f"❌ ERROR CRÍTICO: {e}")
    import traceback
    traceback.print_exc() # Esto nos dará más detalles si vuelve a fallar
finally:
    conn.close()