import sqlite3
import os

# --- CONFIGURACIÓN ---
ruta_bd = os.path.join(os.path.dirname(__file__), '..', 'base_datos', 'control_gastos.db')
conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

def mostrar_titulo(texto):
    print("\n" + "="*60)
    print(f" 🛡️  GESTOR DE ESTRUCTURA FÉNIX: {texto}")
    print("="*60)

def elegir_opcion(lista_tuplas, titulo="Opciones"):
    """Ayuda a elegir de una lista de tuplas (id, nombre, ...)"""
    print(f"\n--- {titulo} ---")
    for i, item in enumerate(lista_tuplas):
        # item[1] debería ser el nombre
        print(f"[{i+1}] {item[1]}")

    while True:
        op = input("\nSelecciona número (0 para cancelar): ")
        if op == '0': return None
        if op.isdigit() and 1 <= int(op) <= len(lista_tuplas):
            return lista_tuplas[int(op)-1]
        print("❌ Opción inválida.")

def alta_subcategoria():
    mostrar_titulo("NUEVA SUBCATEGORÍA (Flujo Blindado)")

    # PASO 1: Elegir Centro de Costo
    cursor.execute("SELECT id, nombre FROM param_centros_costo ORDER BY id")
    ccs = cursor.fetchall()
    cc_elegido = elegir_opcion(ccs, "PASO 1: ¿A qué Centro de Costo pertenece?")
    if not cc_elegido: return

    # PASO 2: Elegir Categoría (Filtrada por CC)
    cursor.execute("""
        SELECT id, nombre FROM param_categorias
        WHERE id_centro_costo = ?
        ORDER BY nombre
    """, (cc_elegido[0],))
    cats = cursor.fetchall()

    if not cats:
        print("❌ No hay categorías en este Centro de Costo. Crea una primero.")
        return

    cat_elegida = elegir_opcion(cats, f"PASO 2: Categorías de '{cc_elegido[1]}'")
    if not cat_elegida: return

    # PASO 3: Verificación de Duplicados (Mostrar lo que ya existe)
    print(f"\n🔍 Revisando qué ya existe en '{cat_elegida[1]}'...")
    cursor.execute("SELECT nombre FROM param_subcategorias WHERE id_categoria = ? ORDER BY nombre", (cat_elegida[0],))
    existentes = cursor.fetchall()

    if existentes:
        print("   YA EXISTEN: " + ", ".join([e[0] for e in existentes]))
    else:
        print("   (Está vacío)")

    # PASO 4: Input y Reglas
    nombre_nuevo = input("\n✍️  Nombre de la NUEVA Subcategoría: ").strip().title()
    if not nombre_nuevo: return

    # Validar si ya existe
    if any(e[0].lower() == nombre_nuevo.lower() for e in existentes):
        print("❌ ERROR: Ya existe esa subcategoría.")
        return

    # PASO 5: Compliance (La Regla de Oro)
    print("\n⚠️  REQUISITO DE GOBERNANZA:")
    print("   [Regla Pareto]: ¿Este concepto justifica su propia subcategoría?")
    print("   (Debe ser un gasto significativo mensual o crítico para decisiones).")
    confirmacion = input("   ¿Confirmas que CUMPLE la regla? (S/N): ").upper()

    if confirmacion == 'S':
        try:
            # Buscamos el ID de la regla para guardar la evidencia
            cursor.execute("SELECT id FROM reglas_gobierno WHERE codigo = 'REG-8020'")
            id_regla = cursor.fetchone()
            id_regla = id_regla[0] if id_regla else None

            cursor.execute("""
                INSERT INTO param_subcategorias (nombre, id_categoria, id_regla_aceptada)
                VALUES (?, ?, ?)
            """, (nombre_nuevo, cat_elegida[0], id_regla))

            # Auditoría
            cursor.execute("""
                INSERT INTO auditoria_compliance (accion, detalle) VALUES (?, ?)
            """, ("ALTA_SUBCATEGORIA", f"Creó '{nombre_nuevo}' en '{cat_elegida[1]}' aceptando Pareto."))

            conn.commit()
            print(f"\n✅ ¡ÉXITO! '{nombre_nuevo}' creada correctamente.")
        except Exception as e:
            print(f"❌ Error de Base de Datos: {e}")
    else:
        print("\n🚫 Cancelado por el usuario (Regla de Oro). Usa 'General'.")

# --- MENÚ PRINCIPAL ---
while True:
    mostrar_titulo("MENÚ PRINCIPAL")
    print("[1] Ver Estructura Actual")
    print("[2] Crear Categoría (Rubro)")
    print("[3] Crear Subcategoría (Detalle)")
    print("[0] Salir")

    op = input("\nOpción: ")
    if op == '3': alta_subcategoria()
    elif op == '0': break
    else: print("🚧 Opción en construcción o no necesaria por ahora.")

conn.close()