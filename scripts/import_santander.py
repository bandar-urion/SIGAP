import pandas as pd
import sqlite3
import os
import sys
import glob
import shutil
from datetime import datetime

# 1. Aseguramos que Python encuentre el módulo sigap_config en la raíz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import sigap_config
from scripts.modulos import inbox_movimientos as carga_movimientos

# 2. Rutas dinámicas desde sigap.cfg (Compatibles con Termux S21 y Windows)
DB_FILE = sigap_config.get_db_path()
INBOX_DIR = sigap_config.get_path('PATHS', 'INBOX')
PROCESSED_DIR = sigap_config.get_path('PATHS', 'PROCESSED')
# -----------------------------------------------------


def main():
    # 1. SETUP
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    archivos = glob.glob(os.path.join(INBOX_DIR, '*.xlsx'))
    if not archivos: print("❌ No hay archivos .xlsx en inbox."); return
    archivo_input = archivos[0]

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

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

        lista_movs = []
        idx = 1
        skipped_count = 0

        for _, row in df.iterrows():
            if row['Monto_Real'] == 0: continue

            referencia = str(row['Referencia'])

            # Chequeo previo en la DB
            cursor.execute("SELECT id FROM movimientos WHERE num_referencia = ?", (referencia,))
            if cursor.fetchone():
                skipped_count += 1
                continue

            mov = carga_movimientos.Movimiento(
                fecha=row['Fecha'],
                referencia=referencia,
                descripcion=row['Descripción'],
                monto=row['Monto_Real'],
                id_mp=ID_MP
            )
            mov.idx = idx
            lista_movs.append(mov)
            idx += 1

        if not lista_movs:
            if skipped_count > 0:
                print(f"✅ Todos los movimientos ({skipped_count}) ya estaban cargados.")
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                dest = os.path.join(PROCESSED_DIR, f"santander_{ts}.xlsx")
                shutil.move(archivo_input, dest)
                print("📂 Archivo movido a procesados.")
            else:
                print("ℹ️ Archivo vacío.")
            return

        print(f"ℹ️ {skipped_count} omitidos. 🚀 Carga para {len(lista_movs)} nuevos.\n")

        # 4. Invocamos INBOX_MOVIMIENTOS
        confirmado = carga_movimientos.iniciar_inbox_movimientos(lista_movs, cursor, MP_FULL)

        # 5. GRABAR BLINDADO
        if confirmado:
            print("\n💾 Sincronizando con Base de Datos...")
            n_guardados = 0
            n_pendientes = 0
            n_descartados = 0

            _AUDIT_SQL = """
                INSERT INTO auditoria_movimientos (accion, modulo, id_movimiento_ref, estado_previo, estado_nuevo, resultado)
                VALUES (?, ?, ?, ?, ?, ?)
            """

            for mov in lista_movs:
                _estado_nuevo = f'ref:{mov.referencia} | fecha:{mov.fecha_fmt} | monto:{mov.monto} | desc:{mov.descripcion_final}'

                if mov.estado in ['LISTO', 'AUTO']:
                    cursor.execute("""
                        INSERT OR IGNORE INTO movimientos
                        (id_centro_costo, id_medio_pago, id_subcategoria, fecha, descripcion, monto, num_referencia, cuota_actual, cuotas_totales)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (mov.id_cc, mov.id_mp, mov.id_subcat, mov.fecha_fmt, mov.descripcion_final, mov.monto, mov.referencia, mov.cuota_actual, mov.cuotas_totales))

                    # Verificamos si se insertó realmente (rowcount > 0)
                    if cursor.rowcount > 0:
                        n_guardados += 1
                        _mov_id = cursor.lastrowid
                        if mov.nuevo_sinonimo:
                            try: cursor.execute("INSERT INTO diccionario_terminos (termino, id_subcategoria) VALUES (?, ?)", (mov.nuevo_sinonimo, mov.id_subcat))
                            except: pass
                        cursor.execute(_AUDIT_SQL, ('IMPORTAR_MOV', 'SIGAP_IMPORT', _mov_id, 'INEXISTENTE', _estado_nuevo, 'OK'))
                    else:
                        cursor.execute(_AUDIT_SQL, ('IMPORTAR_MOV', 'SIGAP_IMPORT', None, 'EXISTENTE', _estado_nuevo, 'SKIP_DUPLICADO'))

                elif mov.estado == 'PENDIENTE':
                    n_pendientes += 1
                elif mov.estado == 'DESCARTADO':
                    n_descartados += 1
                    cursor.execute(_AUDIT_SQL, ('IMPORTAR_MOV', 'SIGAP_IMPORT', None, 'PENDIENTE', _estado_nuevo, 'DESCARTADO_USUARIO'))

            conn.commit()

            print(f"✅ Guardados: {n_guardados} registros.")

            if n_pendientes == 0:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                dest = os.path.join(PROCESSED_DIR, f"santander_{ts}.xlsx")
                shutil.move(archivo_input, dest)
                print(f"📂 Archivo procesado y movido.")
            else:
                print(f"⚠️ Quedan {n_pendientes} PENDIENTES. Archivo se mantiene en INBOX.")

    except Exception as e:
        print(f"❌ Error Crítico: {e}")
        import traceback; traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()