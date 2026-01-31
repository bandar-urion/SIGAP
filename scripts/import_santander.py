import pandas as pd
import sqlite3
import os
import glob
from datetime import datetime

# --- CONFIGURACIÓN ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, 'control_gastos.db')
INBOX_DIR = os.path.join(BASE_DIR, 'data', 'inbox')

# --- UTILIDADES ---

def conectar():
    return sqlite3.connect(DB_FILE)

def cargar_diccionario_inteligente(cursor):
    cursor.execute("""
        SELECT d.termino, s.id, s.nombre
        FROM diccionario_terminos d
        JOIN param_subcategorias s ON d.id_subcategoria = s.id
    """)
    return cursor.fetchall()

def buscar_categoria_inteligente(descripcion, diccionario):
    desc_normalizada = descripcion.lower()
    for termino, id_sub, nombre_sub in diccionario:
        if termino.lower() in desc_normalizada:
            return id_sub, nombre_sub
    return None, None

def existe_movimiento(cursor, referencia):
    cursor.execute("SELECT id FROM movimientos WHERE num_referencia = ?", (referencia,))
    return cursor.fetchone() is not None

# --- 🆕 INTERFAZ MEJORADA (Ahora pide CC) ---

def solicitar_clasificacion_manual(cursor, descripcion, monto):
    """
    Pide al usuario:
    1. Centro de Costo (¿De quién es el gasto?)
    2. Categoría/Subcategoría (¿Qué es?)
    """
    print(f"\n❓ A REVISAR: '{descripcion}' (${monto})")

    # 1. SELECCIÓN DE CENTRO DE COSTO
    cursor.execute("SELECT id, nombre FROM param_centros_costo ORDER BY id")
    ccs = cursor.fetchall()
    print("   🏢 ¿A quién corresponde?")
    for i, (id_cc, nombre) in enumerate(ccs):
        print(f"      [{i+1}] {nombre}")

    try:
        sel_cc = int(input("      >>> Opción CC: ")) - 1
        id_cc_elegido = ccs[sel_cc][0]
        nombre_cc_elegido = ccs[sel_cc][1]
    except:
        print("   ❌ Opción inválida. Se usará 'Personal' por defecto.")
        cursor.execute("SELECT id FROM param_centros_costo WHERE nombre='Personal'")
        id_cc_elegido = cursor.fetchone()[0]

    # 2. SELECCIÓN DE CATEGORÍA
    print(f"   🏷️  ¿Qué concepto es? (CC: {nombre_cc_elegido})")
    cursor.execute("SELECT id, nombre FROM param_categorias ORDER BY nombre")
    cats = cursor.fetchall()
    for i, (cid, cnom) in enumerate(cats):
        print(f"      [{i+1}] {cnom}")

    try:
        sel_cat = int(input("      >>> Opción Categoría: ")) - 1
        id_cat = cats[sel_cat][0]

        # Subcategorías
        cursor.execute("SELECT id, nombre FROM param_subcategorias WHERE id_categoria = ? ORDER BY nombre", (id_cat,))
        subcats = cursor.fetchall()
        for j, (sid, snom) in enumerate(subcats):
            print(f"         ({j+1}) {snom}")

        sel_sub = int(input("         >>> Opción Subcategoría: ")) - 1
        id_sub = subcats[sel_sub][0]
        nombre_sub = subcats[sel_sub][1]

        # Aprendizaje
        aprender = input(f"   🧠 ¿Guardar clave de '{descripcion[:15]}...' como sinónimo de '{nombre_sub}'? (S/n): ").lower()
        if aprender == 's' or aprender == '':
            termino_nuevo = input("   Escriba la palabra clave a recordar (ej: 'Coyita'): ").strip()
            if termino_nuevo:
                try:
                    cursor.execute("INSERT INTO diccionario_terminos (termino, id_subcategoria) VALUES (?, ?)", (termino_nuevo, id_sub))
                    print(f"   ✅ ¡Aprendido! '{termino_nuevo}' -> {nombre_sub}")
                except sqlite3.IntegrityError:
                    pass

        return id_sub, id_cc_elegido # 🆕 Devolvemos AMBOS

    except (ValueError, IndexError):
        print("   ❌ Selección inválida. Se saltará este registro.")
        return None, None

# --- MOTOR PRINCIPAL ---

def procesar_importacion():
    print("🦅 IMPORTADOR SANTANDER (IA + CC SELECTOR)...")

    archivos = glob.glob(os.path.join(INBOX_DIR, '*.xlsx'))
    if not archivos:
        print("❌ No hay archivos .xlsx en /data/inbox")
        return
    archivo_input = archivos[0]

    conn = conectar()
    cursor = conn.cursor()

    try:
        df = pd.read_excel(archivo_input, skiprows=13, engine='openpyxl')
        df = df.dropna(how='all', axis=1)

        col_ca = 'Caja de Ahorro'
        col_cc = 'Cuenta Corriente'
        if col_ca not in df.columns: df[col_ca] = 0
        if col_cc not in df.columns: df[col_cc] = 0
        df[col_ca] = df[col_ca].fillna(0)
        df[col_cc] = df[col_cc].fillna(0)
        df['Monto_Real'] = df[col_ca] + df[col_cc]

        cursor.execute("SELECT id FROM param_medios_pago WHERE nombre LIKE '%Santander%' AND tipo='CUENTA'")
        mp_res = cursor.fetchone()
        if not mp_res:
            print("❌ Falta MP Santander en DB.")
            return
        ID_MP_SANTANDER = mp_res[0]

        # 🆕 Default CC (por si la IA lo encuentra solo, asumimos Personal por ahora)
        cursor.execute("SELECT id FROM param_centros_costo WHERE nombre = 'Personal'")
        ID_CC_DEFAULT = cursor.fetchone()[0]

        diccionario = cargar_diccionario_inteligente(cursor)
        nuevos = 0

        for index, row in df.iterrows():
            referencia = str(row['Referencia'])
            descripcion = str(row['Descripción']).strip()
            fecha_raw = row['Fecha']
            monto = float(row['Monto_Real'])

            if pd.isna(monto) or monto == 0: continue
            if existe_movimiento(cursor, referencia): continue

            print(f"\n🔄 Procesando: {descripcion} | ${monto}")

            # 1. INTENTO AUTOMÁTICO
            id_subcat, nombre_subcat = buscar_categoria_inteligente(descripcion, diccionario)

            # Variables finales para el insert
            id_sub_final = None
            id_cc_final = None

            if id_subcat:
                print(f"   🤖 Auto-detectado: {nombre_subcat}")
                # 🆕 Si es auto-detectado, usamos el DEFAULT (Personal).
                # (Mejora futura: agregar CC al diccionario)
                id_sub_final = id_subcat
                id_cc_final = ID_CC_DEFAULT
            else:
                # 2. INTERVENCIÓN MANUAL (Aquí eliges CC)
                id_sub_final, id_cc_final = solicitar_clasificacion_manual(cursor, descripcion, monto)
                diccionario = cargar_diccionario_inteligente(cursor)

            if id_sub_final and id_cc_final:
                # Le decimos explícitamente: "El día va primero"
                fecha_str = pd.to_datetime(fecha_raw, dayfirst=True).strftime('%Y-%m-%d')
                sql = """
                    INSERT INTO movimientos (id_centro_costo, id_medio_pago, id_subcategoria, fecha, descripcion, monto, num_referencia)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                # 🆕 Usamos id_cc_final en lugar del hardcodeado
                cursor.execute(sql, (id_cc_final, ID_MP_SANTANDER, id_sub_final, fecha_str, descripcion, monto, referencia))
                conn.commit()
                nuevos += 1
                print("   ✅ Guardado.")

    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    procesar_importacion()
