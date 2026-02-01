import pandas as pd
import sqlite3
import os
import glob
import shutil
from datetime import datetime
# --- CAMBIO IMPORTANTE: AHORA LLAMAMOS A CARGA_GASTOS ---
from modulos import carga_gastos

# --- CONFIGURACIÓN ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, 'control_gastos.db')
INBOX_DIR = os.path.join(BASE_DIR, 'data', 'inbox')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def main():
    # 1. SETUP
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    archivos = glob.glob(os.path.join(INBOX_DIR, '*.xlsx'))
    if not archivos: print("❌ No hay archivos .xlsx en inbox."); return
    archivo_input = archivos[0]

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # 2. IDENTIFICAR MEDIO DE PAGO
        cursor.execute("SELECT id, nombre, tipo FROM param_medios_pago WHERE nombre LIKE '%Santander%' AND tipo='CUENTA'")
        res = cursor.fetchone()
        if not res: print("❌ No existe Medio Pago Santander Cuenta."); return
        ID_MP, NOM_MP, TIPO_MP = res
        MP_FULL = f"{NOM_MP} [{TIPO_MP}]"

        # 3. PARSEO
        print(f"📂 Procesando: {os.path.basename(archivo_input)}...")
        df = pd.read_excel(archivo_input, skiprows=13, engine='openpyxl')
        df = df.dropna(how='all', axis=1)
        if 'Caja de Ahorro' not in df.columns: df['Caja de Ahorro'] = 0
        if 'Cuenta Corriente' not in df.columns: df['Cuenta Corriente'] = 0
        df = df.fillna(0)
        df['Monto_Real'] = df['Caja de Ahorro'] + df['Cuenta Corriente']

        lista_tx = []
        idx = 1
        for _, row in df.iterrows():
            if row['Monto_Real'] == 0: continue

            # Usamos la clase del nuevo módulo
            tx = carga_gastos.Transaccion(
                fecha=row['Fecha'],
                referencia=row['Referencia'],
                descripcion=row['Descripción'],
                monto=row['Monto_Real'],
                id_mp=ID_MP
            )
            tx.idx = idx

            cursor.execute("SELECT id FROM movimientos WHERE num_referencia = ?", (tx.referencia,))
            if cursor.fetchone(): continue

            lista_tx.append(tx)
            idx += 1

        if not lista_tx: print("✅ No hay movimientos nuevos."); return

        # 4. INVOCAR AL NUEVO MOTOR DE CARGA
        confirmado = carga_gastos.iniciar_torre_control(lista_tx, cursor, MP_FULL)

        # 5. GRABAR
        if confirmado:
            print("\n💾 Guardando en DB...")
            n = 0
            for tx in lista_tx:
                if tx.estado not in ['LISTO', 'AUTO']: continue

                cursor.execute("""
                    INSERT INTO movimientos (id_centro_costo, id_medio_pago, id_subcategoria, fecha, descripcion, monto, num_referencia)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (tx.id_cc, tx.id_mp, tx.id_subcat, tx.fecha_fmt, tx.descripcion_final, tx.monto, tx.referencia))

                if tx.nuevo_sinonimo:
                    try: cursor.execute("INSERT INTO diccionario_terminos (termino, id_subcategoria) VALUES (?, ?)", (tx.nuevo_sinonimo, tx.id_subcat))
                    except: pass
                n += 1

            conn.commit()

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = os.path.join(PROCESSED_DIR, f"santander_{ts}.xlsx")
            shutil.move(archivo_input, dest)
            print(f"✅ Procesado exitoso: {n} registros.")

    except Exception as e:
        print(f"❌ Error Crítico: {e}")
        import traceback; traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()