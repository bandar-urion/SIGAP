# scripts/modulos/editor_gastos.py
import pandas as pd
import os
import shutil
import math
import time
from datetime import datetime

# --- COLORES ANSI ---
C_RESET = "\033[0m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_CYAN = "\033[96m"
C_WHITE = "\033[97m"

PAGE_SIZE = 10

# --- CLASE MODELO UNIFICADA ---
class Transaccion:
    def __init__(self, fecha, referencia, descripcion, monto, id_mp):
        # Datos inmutables (origen)
        self.idx = 0 # Se asigna al listar
        self.fecha_fmt = pd.to_datetime(fecha, dayfirst=True).strftime('%Y-%m-%d')
        self.referencia = str(referencia)
        self.descripcion_original = str(descripcion).strip()
        self.monto = float(monto)
        self.id_mp = id_mp # ID Medio Pago en DB

        # Datos mutables (trabajo)
        self.descripcion_final = self.descripcion_original
        self.estado = 'PENDIENTE'

        # Clasificación
        self.id_cc = None; self.nombre_cc = "---"
        self.id_cat = None; self.nombre_cat = "---"
        self.id_subcat = None; self.nombre_subcat = "---"

        # Inteligencia
        self.ia_match = False
        self.nuevo_sinonimo = None

# --- UI HELPER FUNCTIONS ---

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado(titulo, screen_id):
    limpiar_pantalla()
    try: width = shutil.get_terminal_size().columns
    except: width = 80
    header_txt = f"🦅 S.I.G.A.P. - {titulo}"
    espacios = width - len(header_txt) - len(screen_id) - 2
    if espacios < 1: espacios = 1
    print(f"{C_CYAN}{header_txt}{' ' * espacios}{C_YELLOW}[{screen_id}]{C_RESET}")
    print("="*width)

def limpiar_texto_visual(texto):
    basura = ["Compra con tarjeta de debito", "Transferencia realizada", "Transferencia recibida",
              "Pago de servicios", "Debito directo", "\t"]
    limpio = texto
    for b in basura:
        limpio = limpio.replace(b, "")
    limpio = " ".join(limpio.split())
    if limpio.startswith("-"): limpio = limpio[1:].strip()
    return limpio

# --- DB & LOGIC FUNCTIONS ---

def cargar_diccionario(cursor):
    cursor.execute("""
        SELECT d.termino, s.id, s.nombre, c.nombre, c.id
        FROM diccionario_terminos d
        JOIN param_subcategorias s ON d.id_subcategoria = s.id
        JOIN param_categorias c ON s.id_categoria = c.id
    """)
    return list(cursor.fetchall())

def reanalizar_lista(lista_tx, diccionario):
    cambios = 0
    print(f"\n{C_BLUE}🔄 Re-escaneando movimientos pendientes...{C_RESET}")
    for tx in lista_tx:
        if tx.estado not in ['LISTO', 'DESCARTADO']:
            desc_lower = tx.descripcion_original.lower()
            for termino, id_sub, nom_sub, nom_cat, id_cat in diccionario:
                if termino.lower() in desc_lower:
                    if tx.id_subcat != id_sub:
                        tx.id_subcat = id_sub
                        tx.nombre_subcat = nom_sub
                        tx.nombre_cat = nom_cat
                        tx.id_cat = id_cat
                        tx.ia_match = True
                        cambios += 1
                    break
    if cambios > 0:
        print(f"{C_GREEN}   ✨ {cambios} movimientos actualizados.{C_RESET}")
        time.sleep(1)

def seleccionar_opcion_db(cursor, query, titulo, params=None):
    if params: cursor.execute(query, params)
    else: cursor.execute(query)
    opciones = cursor.fetchall()
    print(f"\n   {titulo}")
    for i, row in enumerate(opciones):
        print(f"      [{i+1}] {row[1]}")
    print(f"      {C_YELLOW}[0] VOLVER ATRÁS{C_RESET}")
    try:
        sel = int(input("      >>> Opción: "))
        if sel == 0: return None, None
        return opciones[sel-1][0], opciones[sel-1][1]
    except: return None, None

def seleccionar_o_crear_subcategoria(cursor, id_cat):
    cursor.execute("SELECT id, nombre FROM param_subcategorias WHERE id_categoria = ? ORDER BY nombre", (id_cat,))
    opciones = cursor.fetchall()
    print(f"\n   📦 SUBCATEGORÍA:")
    for i, row in enumerate(opciones):
        print(f"      [{i+1}] {row[1]}")
    print(f"      {C_GREEN}[+] CREAR NUEVA SUBCATEGORÍA{C_RESET}")
    print(f"      {C_YELLOW}[0] VOLVER ATRÁS{C_RESET}")
    inp = input("      >>> Opción: ").strip()

    if inp == '0': return None, None
    if inp == '+':
        nueva = input(f"   ✨ Nombre nueva Subcategoría: ").strip()
        if nueva:
            try:
                cursor.execute("INSERT INTO param_subcategorias (id_categoria, nombre) VALUES (?, ?)", (id_cat, nueva))
                cursor.connection.commit()
                return cursor.lastrowid, nueva
            except Exception as e:
                print(f"Error: {e}"); time.sleep(1); return None, None
        return None, None
    try: return opciones[int(inp)-1][0], opciones[int(inp)-1][1]
    except: return None, None

def editar_transaccion(cursor, tx, nombre_mp_completo):
    while True:
        mostrar_encabezado(f"EDICIÓN #{tx.idx}", "SCR-EDIT")
        f_latam = datetime.strptime(tx.fecha_fmt, '%Y-%m-%d').strftime('%d/%m/%Y')
        cc_disp = tx.nombre_cc if tx.id_cc else f"{C_RED}SIN ASIGNAR ⚠️{C_RESET}"

        print(f"\n   💳 MP: {C_WHITE}{nombre_mp_completo}{C_RESET} | 📅 {C_WHITE}{f_latam}{C_RESET} | 💰 {C_WHITE}${tx.monto:,.2f}{C_RESET}")
        print(f"   📝 {C_YELLOW}{tx.descripcion_final}{C_RESET}")
        print("-" * 60)
        print(f"   🏢 CC: {cc_disp} | 🏷️ CAT: {tx.nombre_cat} | 📦 SUB: {tx.nombre_subcat}")
        print("-" * 60)
        print("   1. 🏢 Cambiar Centro Costo (+Smart)")
        print("   2. 🏷️  Cambiar Categoría")
        print("   3. 📦 Cambiar SubCategoría")
        print("   4. ✏️  Editar Descripción")
        print("-" * 30)
        print(f"   D. 🗑️  DESCARTAR")
        print(f"\n   {C_GREEN}C. ✅ CONFIRMAR{C_RESET}   {C_RED}Esc. ❌ CANCELAR{C_RESET}")

        opc = input("\n   >>> Acción: ").strip().upper()

        if opc == '1': # CC + Smart
            paso = 0
            while 0 <= paso <= 3:
                if paso == 0:
                    id_cc, nom_cc = seleccionar_opcion_db(cursor, "SELECT id, nombre FROM param_centros_costo ORDER BY id", "🏢 CENTRO DE COSTO:")
                    if not id_cc: break
                    tx.id_cc, tx.nombre_cc = id_cc, nom_cc
                    paso = 1
                elif paso == 1:
                    if tx.id_cat:
                        print(f"\n   🤖 Clasif. actual: {tx.nombre_cat} > {tx.nombre_subcat}")
                        if input("   ¿Mantener? (S/n): ").upper() in ['S','']: break
                    paso = 2
                elif paso == 2:
                    id_cat, nom_cat = seleccionar_opcion_db(cursor, "SELECT id, nombre FROM param_categorias ORDER BY nombre", "🏷️  CATEGORÍA:")
                    if not id_cat: paso=0; continue
                    tx.id_cat, tx.nombre_cat = id_cat, nom_cat
                    paso = 3
                elif paso == 3:
                    id_sub, nom_sub = seleccionar_o_crear_subcategoria(cursor, tx.id_cat)
                    if not id_sub: paso=2; continue
                    tx.id_subcat, tx.nombre_subcat = id_sub, nom_sub; tx.ia_match = False; break

        elif opc == '2': # Cat -> Sub
            id_cat, nom_cat = seleccionar_opcion_db(cursor, "SELECT id, nombre FROM param_categorias ORDER BY nombre", "🏷️  CATEGORÍA:")
            if id_cat:
                tx.id_cat, tx.nombre_cat = id_cat, nom_cat
                id_sub, nom_sub = seleccionar_o_crear_subcategoria(cursor, tx.id_cat)
                if id_sub: tx.id_subcat, tx.nombre_subcat = id_sub, nom_sub; tx.ia_match = False

        elif opc == '3': # Solo Sub
            if not tx.id_cat:
                print(f"⚠️ Defina Categoría primero."); time.sleep(1)
            else:
                id_sub, nom_sub = seleccionar_o_crear_subcategoria(cursor, tx.id_cat)
                if id_sub: tx.id_subcat, tx.nombre_subcat = id_sub, nom_sub; tx.ia_match = False

        elif opc == '4':
            n = input("   Nueva descripción: ").strip()
            if n: tx.descripcion_final = n

        elif opc == 'D':
            if input(f"   {C_RED}¿DESCARTAR? (S/n): {C_RESET}").upper() == 'S':
                tx.estado = 'DESCARTADO'; return None

        elif opc == 'C':
            if not tx.id_cc or not tx.id_subcat:
                print(f"⛔ Faltan datos (CC o Subcat)"); time.sleep(1)
            else:
                tx.estado = 'LISTO'
                if not tx.ia_match:
                    if input(f"   🧠 ¿Aprender '{tx.nombre_subcat}'? (s/N): ").lower() == 's':
                        k = input("   Clave: ").strip()
                        if k:
                            tx.nuevo_sinonimo = k
                            return (k, tx.id_subcat, tx.nombre_subcat, tx.nombre_cat, tx.id_cat)
                return None

        elif opc in ['ESC', '0']: return None

def render_dashboard(lista_tx, pag, mp_nombre):
    total = len(lista_tx); pags = math.ceil(total / PAGE_SIZE)
    ini = (pag-1)*PAGE_SIZE; fin = ini+PAGE_SIZE

    mostrar_encabezado(f"TORRE DE CONTROL ({mp_nombre})", "SCR-MAIN")
    print(f"📄 Pág {pag}/{pags} | Total: {total}")
    print("-" * 80)
    print(f"{'#':<3} | {'FECHA':<10} | {'DESCRIPCIÓN':<25} | {'MONTO':>10} | {'ESTADO':<8} | {'CLASIF'}")
    print("-" * 80)

    for tx in lista_tx[ini:fin]:
        c = C_RESET; est = "PEND"; clas = f"{tx.nombre_cc[:1]}/{tx.nombre_cat[:8]}>{tx.nombre_subcat[:8]}"
        if tx.estado == 'AUTO': c = C_GREEN; est = "AUTO"
        elif tx.estado == 'LISTO': c = C_CYAN; est = "LISTO"
        elif tx.estado == 'DESCARTADO': c = C_RED; est = "NO"; clas = "---"
        elif tx.estado == 'PENDIENTE': c = C_YELLOW; clas = "INCOMPLETO"

        desc = limpiar_texto_visual(tx.descripcion_final)
        desc = (desc[:23] + '..') if len(desc) > 23 else desc
        print(f"{c}{tx.idx:<3} | {tx.fecha_fmt:<10} | {desc:<25} | {tx.monto:>10.0f} | {est:<8} | {clas}{C_RESET}")

    print("-" * 80)
    print(f" [#] Editar | [S] Sig | [A] Ant | {C_GREEN}[G] GRABAR{C_RESET} | {C_RED}[X] SALIR{C_RESET}")

def iniciar_torre_control(lista_tx, cursor, mp_nombre):
    diccionario = cargar_diccionario(cursor)

    # Análisis inicial
    reanalizar_lista(lista_tx, diccionario)

    pag = 1
    while True:
        render_dashboard(lista_tx, pag, mp_nombre)
        cmd = input(">>> Acción: ").strip().upper()

        if cmd == 'S' and pag < math.ceil(len(lista_tx)/PAGE_SIZE): pag += 1
        elif cmd == 'A' and pag > 1: pag -= 1
        elif cmd == 'X': return False # Cancelar
        elif cmd == 'G':
            pend = [t for t in lista_tx if t.estado == 'PENDIENTE']
            if pend:
                print(f"❌ {len(pend)} Incompletos."); time.sleep(1.5); continue
            return True # Proceder a grabar
        else:
            try:
                idx = int(cmd)
                tx = next((t for t in lista_tx if t.idx == idx), None)
                if tx:
                    aprendido = editar_transaccion(cursor, tx, mp_nombre)
                    if aprendido:
                        diccionario.append(aprendido)
                        reanalizar_lista(lista_tx, diccionario)
            except: pass