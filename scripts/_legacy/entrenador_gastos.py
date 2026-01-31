import sqlite3
import os

# --- CONFIGURACIÓN ---
ruta_bd = os.path.join(os.path.dirname(__file__), '..', 'base_datos', 'control_gastos.db')
conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

def guardar_y_salir():
    print("\n💾 Guardando cambios y cerrando...")
    conn.commit()
    conn.close()
    print("👋 ¡Buen provecho con esa patamuslo! (Script finalizado)")
    exit()

print("\n" + "="*50)
print(" 🎓 ENTRENADOR DE GASTOS FÉNIX")
print("="*50)
print("Instrucciones: Escribe la categoría para cada ítem.")
print("Tip: Escribe 'salir' en cualquier momento para ir a cocinar.\n")

# 1. Buscamos descripciones únicas que NO tengan categoría aún
# Así no te pregunta 20 veces por lo mismo.
cursor.execute("""
    SELECT DISTINCT descripcion
    FROM movimientos
    WHERE categoria IS NULL OR categoria = ''
    ORDER BY descripcion ASC
""")

items_pendientes = cursor.fetchall()
total = len(items_pendientes)

if total == 0:
    print("🎉 ¡Increíble! No hay nada pendiente de clasificar.")
    guardar_y_salir()

print(f"📝 Tienes {total} descripciones nuevas para enseñar.")
print("-" * 50)

for i, fila in enumerate(items_pendientes):
    desc = fila[0]

    # Mostramos progreso
    print(f"\n[{i+1}/{total}] Ítem: 👉  {desc}")

    # --- PREGUNTA 1: CATEGORÍA ---
    cat = input("   ¿Categoría? (ej. Supermercado, Impuestos, Obra): ").strip()

    if cat.lower() == 'salir': guardar_y_salir()
    if cat == "":
        print("   ⏭️  Saltado.")
        continue # Si das Enter vacío, lo salta por ahora

    # --- PREGUNTA 2: CENTRO DE COSTO (Opcional) ---
    # Solo preguntamos si quieres hilar fino
    cc = input("   ¿Centro de Costo? (Enter para 'Personal', o: Casa Martin, Casa Mama, Terreno): ").strip()
    if cc.lower() == 'salir': guardar_y_salir()
    if cc == "": cc = "Personal" # Valor por defecto

    # --- ACTUALIZACIÓN MASIVA ---
    try:
        cursor.execute("""
            UPDATE movimientos
            SET categoria = ?, centro_costo = ?
            WHERE descripcion = ?
        """, (cat, cc, desc))

        cambios = cursor.rowcount
        print(f"   ✅ ¡Aprendido! Se etiquetaron {cambios} movimientos históricos.")
        conn.commit() # Guardamos paso a paso por si se corta la luz

    except sqlite3.Error as e:
        print(f"   ❌ Error guardando: {e}")

print("\n" + "="*50)
print("🎉 ¡Terminaste por hoy! Ya no quedan ítems pendientes.")
guardar_y_salir()