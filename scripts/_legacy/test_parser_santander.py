import pandas as pd
import os
import glob

# Configuración
INBOX_DIR = 'data/inbox'

def buscar_archivo_excel():
    # Busca cualquier .xlsx en la carpeta inbox
    archivos = glob.glob(os.path.join(INBOX_DIR, '*.xlsx'))
    if not archivos:
        return None
    return archivos[0] # Devuelve el primero que encuentre

def probar_lectura():
    print("🦅 CALIBRACIÓN DE LECTURA (SANTANDER - MODO EXCEL)...")

    archivo = buscar_archivo_excel()
    if not archivo:
        print(f"❌ Error: No encuentro ningún archivo .xlsx en {INBOX_DIR}")
        print("   -> Por favor, descarga el Excel del banco y ponlo ahí.")
        return

    print(f"📄 Archivo detectado: {os.path.basename(archivo)}")

    try:
        # LECTURA DE EXCEL (SANTANDER)
        # skiprows=13 -> Las primeras 13 filas suelen ser logo y resumen de cuenta
        # header=0 -> La fila 14 (índice 0 después del skip) es la cabecera
        df = pd.read_excel(
            archivo,
            skiprows=13,
            engine='openpyxl'
        )

        # 1. LIMPIEZA DE COLUMNAS VACÍAS
        # Santander a veces deja columnas sin nombre al principio o final
        df = df.dropna(how='all', axis=1) # Borra columnas donde todo es NaN

        print(f"✅ Lectura Exitosa. Filas encontradas: {len(df)}")
        print("\n--- COLUMNAS DETECTADAS ---")
        print(list(df.columns))

        # 2. FUSIÓN DE MONTOS
        # Santander separa en 'Caja de Ahorro' y 'Cuenta Corriente'.
        # Necesitamos una sola columna 'Monto'.

        col_ca = 'Caja de Ahorro'
        col_cc = 'Cuenta Corriente'

        # Rellenar NaNs con 0 para poder sumar
        if col_ca in df.columns:
            df[col_ca] = df[col_ca].fillna(0)
        else:
            df[col_ca] = 0

        if col_cc in df.columns:
            df[col_cc] = df[col_cc].fillna(0)
        else:
            df[col_cc] = 0

        # Crear columna unificada
        df['Monto_Real'] = df[col_ca] + df[col_cc]

        # 3. MUESTRA DE DATOS
        print("\n--- MUESTRA PROCESADA (Primeras 5 filas) ---")
        cols_mostrar = ['Fecha', 'Descripción', 'Referencia', 'Monto_Real']

        # Filtramos solo las columnas que existen para no dar error
        cols_finales = [c for c in cols_mostrar if c in df.columns]

        print(df[cols_finales].head(5))

    except Exception as e:
        print(f"❌ FALLA CRÍTICA: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    probar_lectura()
