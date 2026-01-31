import sqlite3
import os

# --- CONFIGURACIÓN ---
ruta_bd = os.path.join(os.path.dirname(__file__), '..', 'base_datos', 'control_gastos.db')

conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

def formato_argentino(valor):
    """ Convierte 1500.50 en $ 1.500,50 """
    if valor is None: valor = 0
    return f"$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

print("\n" + "="*50)
print(" 🚀  ESTADO ACTUAL DEL SISTEMA DE GASTOS")
print("="*50 + "\n")

# 1. CONTEO TOTAL
cursor.execute("SELECT COUNT(*) FROM movimientos")
total_filas = cursor.fetchone()[0]
print(f"📦 Total de Movimientos almacenados: {total_filas}")
print("-" * 50)

# 2. RESUMEN POR MEDIO DE PAGO (Tu primer Group By)
print(f"{'MEDIO DE PAGO':<20} | {'CANTIDAD':<10} | {'TOTAL ($)':>15}")
print("-" * 50)

cursor.execute("""
    SELECT medio_pago, COUNT(*), SUM(monto)
    FROM movimientos
    GROUP BY medio_pago
    ORDER BY SUM(monto) ASC
""")

for fila in cursor.fetchall():
    medio = fila[0]
    cantidad = fila[1]
    total = fila[2]

    # Visualización: Si es negativo (gasto) en rojo (o con signo), si es positivo en verde
    print(f"{medio:<20} | {cantidad:<10} | {formato_argentino(total):>15}")

print("-" * 50)

# 3. TOP 5 GASTOS MÁS GRANDES
print("\n💸 TOP 5 GASTOS MÁS FUERTES:")
cursor.execute("""
    SELECT fecha, descripcion, monto
    FROM movimientos
    WHERE monto < 0
    ORDER BY monto ASC
    LIMIT 5
""")

for fila in cursor.fetchall():
    fecha, desc, monto = fila
    # Cortamos la descripción si es muy larga para que entre en pantalla
    desc_corta = (desc[:25] + '..') if len(desc) > 25 else desc
    print(f"  📅 {fecha} | {desc_corta:<27} | {formato_argentino(monto)}")

print("\n" + "="*50)
conn.close()