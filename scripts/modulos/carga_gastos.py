import pandas as pd
import os
import shutil
import math
import time
from datetime import datetime
import msvcrt

# --- COLORES ANSI ---
C_RESET = "\033[0m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_CYAN = "\033[96m"
C_WHITE = "\033[97m"
C_PURPLE = "\033[95m"

PAGE_SIZE = 9  # Ajustado a 9 para permitir selección 1-9 instantánea
MENU_SIZE = 9

# --- CLASE MODELO ---
class Transaccion:
    def __init__(self, fecha, referencia, descripcion, monto, id_mp):
        self.idx = 0
        self.fecha_fmt = pd.to_datetime(fecha, dayfirst=True).strftime('%Y-%m-%d')
        self.referencia = str(referencia)
        self.descripcion_original = str(descripcion).strip()
        self.monto = float(monto)
        self.id_mp = id_mp

        self.descripcion_final = self.descripcion_original
        self.estado = 'PENDIENTE'

        self.id_cc = None; self.nombre_cc = "---"
        self.id_cat = None; self.nombre_cat = "---"
        self.id_subcat = None; self.nombre_subcat = "---"

        self.ia_match = False
        self.nuevo_sinonimo = None
        self.conflictos = []

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
              "Pago de servicios", "Debito directo", "Su pago en", "Pago DEBIN", "\t"]
    limpio = texto
    for b in basura:
        limpio = limpio.replace(b, "")
        limpio = limpio.replace(b.upper(), "")
    limpio = " ".join(limpio.split())
    if limpio.startswith("-"): limpio = limpio[1:].strip()
    return limpio

# --- MOTOR DE ENTRADA (INSTANTÁNEO) ---

def leer_tecla_instante():
    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            try:
                if ch == b'\x00' or ch == b'\xe0':
                    msvcrt.getch(); return None
                return ch.decode('utf-8').upper()
            except: return None
        time.sleep(0.05)

# --- LOGICA DE APRENDIZAJE ---

def cerrar_y_aprender(tx):
    tx.estado = 'LISTO'
    if not tx.ia_match:
        clave_sugerida = limpiar_texto_visual(tx.descripcion_final)
        clave_sugerida = (clave_sugerida[:30] + '..') if len(clave_sugerida) > 30 else clave_sugerida

        print(f"\n   {C_PURPLE}🧠 INTELIGENCIA ARTIFICIAL:{C_RESET}")
        print(f"   ¿Siempre que aparezca {C_WHITE}'{clave_sugerida}'{C_RESET}")
        print(f"   asignar {C_CYAN}'{tx.nombre_subcat}'{C_RESET}?")

        print(f"   (s/N): ", end='', flush=True)
        resp = leer_tecla_instante()
        print(resp)

        if resp == 'S':
            k = input(f"   Frase clave a buscar (Enter usa '{clave_sugerida}'): ").strip()
            if not k: k = clave_sugerida
            k = k.replace("..", "").strip()
            tx.nuevo_sinonimo = k
            return (k, tx.id_subcat, tx.nombre_subcat, tx.nombre_cat, tx.id_cat)

    return None

# --- DB & LOGIC FUNCTIONS ---

def cargar_diccionario(cursor):
    cursor.execute("""
        SELECT d.termino, s.id, s.nombre, c.nombre, c.id
        FROM diccionario_terminos d
        JOIN param_subcategorias s ON d.id_subcategoria = s.id
        JOIN param_categorias c ON s.id_categoria = c.id
    """)
    return list(cursor.fetchall())

def verificar_conocimiento_previo(cursor, tx):
    if not tx.id_subcat: return False
    desc_lower = tx.descripcion_final.lower()
    cursor.execute("SELECT termino FROM diccionario_terminos WHERE id_subcategoria = ?", (tx.id_subcat,))
    terminos = cursor.fetchall()
    for (t,) in terminos:
        if t.lower() in desc_lower:
            tx.ia_match = True
            return True
    tx.ia_match = False
    return False

def reanalizar_lista(lista_tx, diccionario):
    cambios = 0
    # Reseteamos conflictos previos para evitar fantasmas
    for tx in lista_tx:
        if tx.estado not in ['LISTO', 'DESCARTADO']:
            desc_lower = tx.descripcion_original.lower()
            coincidencias = []

            for termino, id_sub, nom_sub, nom_cat, id_cat in diccionario:
                if termino.lower() in desc_lower:
                    # CLAVE ÚNICA: ID_SUB + ID_CAT (Para diferenciar misma subcat en distinta cat si pasara)
                    identificador_unico = (id_sub, id_cat)

                    # Verificamos si ya tenemos esta opción exacta guardada
                    ya_existe = False
                    for c in coincidencias:
                        if (c[0], c[3]) == identificador_unico:
                            ya_existe = True
                            break

                    if not ya_existe:
                        coincidencias.append( (id_sub, nom_sub, nom_cat, id_cat) )

            if len(coincidencias) == 1:
                c = coincidencias[0]
                if tx.id_subcat != c[0]:
                    tx.id_subcat = c[0]; tx.nombre_subcat = c[1]
                    tx.nombre_cat = c[2]; tx.id_cat = c[3]
                    tx.ia_match = True; tx.conflictos = []; cambios += 1
            elif len(coincidencias) > 1:
                tx.conflictos = coincidencias
                tx.estado = 'PENDIENTE'
                tx.id_subcat = None
                tx.nombre_subcat = f"{C_PURPLE}AMBIGUO ({len(coincidencias)}){C_RESET}"
            else:
                # Si no hay coincidencias, limpiamos conflictos viejos
                tx.conflictos = []

# --- MENUS PAGINADOS (INSTANTÁNEOS) ---

def menu_paginado(opciones, titulo):
    total = len(opciones)
    pag = 1
    max_pag = math.ceil(total / MENU_SIZE)
    error_msg = ""

    while True:
        if error_msg: print(f"\r{' '*80}\r", end='')

        ini = (pag-1) * MENU_SIZE; fin = ini + MENU_SIZE
        lote = opciones[ini:fin]

        print(f"\n   {titulo} (Pág {pag}/{max_pag})")
        validos = []
        for i, row in enumerate(lote):
            num = i + 1
            print(f"      [{num}] {row[1]}")
            validos.append(str(num))

        if max_pag > 1:
            nav = []
            if pag > 1: nav.append("[A] Ant"); validos.append('A')
            if pag < max_pag: nav.append("[S] Sig"); validos.append('S')
            if nav: print(f"      {C_BLUE}{' '.join(nav)}{C_RESET}")

        print(f"      {C_YELLOW}[0] VOLVER ATRÁS{C_RESET}")
        validos.append('0')

        if error_msg: print(f"      {C_RED}{error_msg}{C_RESET}", end='')
        print(f"\n      >>> Opción: ", end='', flush=True)

        inp = leer_tecla_instante()
        print(inp)

        if inp in validos:
            if inp == '0': return None, None
            if inp == 'S': pag += 1; continue
            if inp == 'A': pag -= 1; continue
            sel_idx = int(inp) - 1
            return lote[sel_idx][0], lote[sel_idx][1]
        else:
            limpiar_pantalla()
            error_msg = "❌ Opción no válida." # Simplificación visual

def seleccionar_opcion_db(cursor, query, titulo, params=None):
    if params: cursor.execute(query, params)
    else: cursor.execute(query)
    opciones = cursor.fetchall()
    return menu_paginado(opciones, titulo)

def seleccionar_o_crear_subcategoria(cursor, id_cat):
    cursor.execute("SELECT id, nombre FROM param_subcategorias WHERE id_categoria = ? ORDER BY nombre", (id_cat,))
    opciones = cursor.fetchall()

    total = len(opciones); pag = 1
    max_pag = math.ceil(total / MENU_SIZE) if total > 0 else 1

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        ini = (pag-1) * MENU_SIZE; fin = ini + MENU_SIZE
        lote = opciones[ini:fin]

        print(f"\n   📦 SUBCATEGORÍA (Pág {pag}/{max_pag})")
        for i, row in enumerate(lote):
            print(f"      [{i+1}] {row[1]}")

        nav = []
        if pag > 1: nav.append("[A] Ant")
        if pag < max_pag: nav.append("[S] Sig")
        if nav: print(f"      {C_BLUE}{' '.join(nav)}{C_RESET}")

        print(f"      {C_GREEN}[+] CREAR NUEVA{C_RESET}")
        print(f"      {C_YELLOW}[0] VOLVER ATRÁS{C_RESET}")
        print(f"\n      >>> Opción: ", end='', flush=True)

        inp = leer_tecla_instante()
        print(inp)

        if inp == '0': return None, None
        if inp == 'S' and pag < max_pag: pag += 1; continue
        if inp == 'A' and pag > 1: pag -= 1; continue

        if inp == '+':
            nueva = input(f"   ✨ Nombre nueva Subcategoría: ").strip()
            if nueva:
                try:
                    cursor.execute("INSERT INTO param_subcategorias (id_categoria, nombre) VALUES (?, ?)", (id_cat, nueva))
                    cursor.connection.commit()
                    return cursor.lastrowid, nueva
                except Exception as e:
                    print(f"Error: {e}"); time.sleep(1); return None, None
            continue

        try:
            val = int(inp)
            if 1 <= val <= len(lote):
                return lote[val-1][0], lote[val-1][1]
        except: pass
        print(f"   {C_RED}❌ Opción inválida{C_RESET}"); time.sleep(0.3)

def intentar_autodetectar_ingreso(cursor, tx):
    if tx.monto > 0:
        cursor.execute("SELECT id, nombre FROM param_categorias WHERE nombre LIKE 'Ingresos%' LIMIT 1")
        res = cursor.fetchone()
        if res:
            tx.id_cat = res[0]; tx.nombre_cat = res[1]
            return True
    return False

def editar_transaccion(cursor, tx, nombre_mp_completo):
    if tx.monto > 0 and not tx.id_cat: intentar_autodetectar_ingreso(cursor, tx)
    verificar_conocimiento_previo(cursor, tx)

    while True:
        mostrar_encabezado(f"EDICIÓN #{tx.idx}", "SCR-EDIT")
        f_latam = datetime.strptime(tx.fecha_fmt, '%Y-%m-%d').strftime('%d/%m/%Y')
        cc_disp = tx.nombre_cc if tx.id_cc else f"{C_RED}SIN ASIGNAR ⚠️{C_RESET}"
        color_monto = C_GREEN if tx.monto > 0 else C_WHITE

        print(f"\n   💳 MP: {C_WHITE}{nombre_mp_completo}{C_RESET} | 📅 {C_WHITE}{f_latam}{C_RESET} | 💰 {color_monto}${tx.monto:,.2f}{C_RESET}")
        print(f"   📝 {C_YELLOW}{tx.descripcion_final}{C_RESET}")
        print("-" * 60)
        print(f"   🏢 CC: {cc_disp} | 🏷️ CAT: {tx.nombre_cat} | 📦 SUB: {tx.nombre_subcat}")
        print("-" * 60)

        valid_keys = ['1', '2', '3', '4', 'D', 'C', '0']

        if tx.conflictos:
            print(f"   {C_PURPLE}🧠 OPCIONES APRENDIDAS:{C_RESET}")
            for idx, conf in enumerate(tx.conflictos):
                # Asignamos letras A, B, C... para selección rápida
                letra_opcion = chr(65 + idx) # A, B, C
                valid_keys.append(letra_opcion)
                print(f"   [{C_PURPLE}{letra_opcion}{C_RESET}] {conf[2]} > {conf[1]}")
            print("-" * 30)

        print("   1. 🏢 Cambiar Centro Costo (+Smart)")
        print("   2. 🏷️  Cambiar Categoría")
        print("   3. 📦 Cambiar SubCategoría")
        print("   4. ✏️  Editar Descripción")
        print("-" * 30)
        print(f"   D. 🗑️  DESCARTAR")
        print(f"\n   {C_GREEN}C. ✅ CONFIRMAR{C_RESET}   {C_RED}0. ❌ CANCELAR{C_RESET}")

        print("\n   >>> Acción: ", end='', flush=True)
        opc = leer_tecla_instante()
        print(opc)

        # RESOLUCIÓN DE AMBIGÜEDADES (A, B, C...)
        if tx.conflictos:
            try:
                # Convertir letra A, B, C a indice 0, 1, 2
                idx_conf = ord(opc) - 65
                if 0 <= idx_conf < len(tx.conflictos):
                    sel = tx.conflictos[idx_conf]
                    tx.id_subcat = sel[0]; tx.nombre_subcat = sel[1]
                    tx.nombre_cat = sel[2]; tx.id_cat = sel[3]
                    tx.ia_match = True; tx.conflictos = []
                    continue
            except: pass

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
                        sub_str = tx.nombre_subcat if tx.id_subcat else "---"
                        print(f"\n   🤖 Clasif. actual: {tx.nombre_cat} > {sub_str}")
                        print(f"   ¿Mantener? (S/n): ", end='', flush=True)
                        mantener = leer_tecla_instante()
                        print(mantener)
                        if mantener in ['S', ' ', '\r']:
                            if not tx.id_subcat:
                                print(f"   {C_YELLOW}⚠️ Falta definir Subcategoría.{C_RESET}"); time.sleep(0.5)
                                paso = 3; continue
                            return cerrar_y_aprender(tx)
                    paso = 2
                elif paso == 2:
                    id_cat, nom_cat = seleccionar_opcion_db(cursor, "SELECT id, nombre FROM param_categorias ORDER BY nombre", "🏷️  CATEGORÍA:")
                    if not id_cat: paso=0; continue
                    tx.id_cat, tx.nombre_cat = id_cat, nom_cat
                    paso = 3
                elif paso == 3:
                    id_sub, nom_sub = seleccionar_o_crear_subcategoria(cursor, tx.id_cat)
                    if not id_sub: paso=2; continue
                    tx.id_subcat, tx.nombre_subcat = id_sub, nom_sub; tx.ia_match = False
                    return cerrar_y_aprender(tx)

        elif opc == '2': # Cat -> Sub
            id_cat, nom_cat = seleccionar_opcion_db(cursor, "SELECT id, nombre FROM param_categorias ORDER BY nombre", "🏷️  CATEGORÍA:")
            if id_cat:
                tx.id_cat, tx.nombre_cat = id_cat, nom_cat
                id_sub, nom_sub = seleccionar_o_crear_subcategoria(cursor, tx.id_cat)
                if id_sub:
                    tx.id_subcat, tx.nombre_subcat = id_sub, nom_sub; tx.ia_match = False
                    if tx.id_cc: return cerrar_y_aprender(tx)

        elif opc == '3': # Solo Sub
            if not tx.id_cat: print(f"⚠️ Defina Categoría primero."); time.sleep(1)
            else:
                id_sub, nom_sub = seleccionar_o_crear_subcategoria(cursor, tx.id_cat)
                if id_sub:
                    tx.id_subcat, tx.nombre_subcat = id_sub, nom_sub; tx.ia_match = False
                    if tx.id_cc: return cerrar_y_aprender(tx)

        elif opc == '4':
            n = input("   Nueva descripción: ").strip()
            if n: tx.descripcion_final = n

        elif opc == 'D':
            print(f"   {C_RED}¿DESCARTAR? (S/n): {C_RESET}", end='', flush=True)
            if leer_tecla_instante() == 'S':
                tx.estado = 'DESCARTADO'; return None

        elif opc == 'C':
            if not tx.id_cc or not tx.id_subcat:
                print(f"⛔ Faltan datos (CC o Subcat)"); time.sleep(1)
            else:
                return cerrar_y_aprender(tx)

        elif opc == '0': return None

def render_dashboard(lista_tx, pag, mp_nombre):
    try: term_width = shutil.get_terminal_size().columns
    except: term_width = 80

    total = len(lista_tx); pags = math.ceil(total / PAGE_SIZE)
    ini = (pag-1)*PAGE_SIZE; fin = ini+PAGE_SIZE
    lote = lista_tx[ini:fin]

    mostrar_encabezado(f"TORRE DE CONTROL ({mp_nombre})", "SCR-MAIN")
    print(f"📄 Pág {pag}/{pags} | Total: {total}")

    col_sel = 5; col_id = 4; col_fecha = 10; col_monto = 11; col_est = 8; col_clasif = 25
    used = col_sel + col_id + col_fecha + col_monto + col_est + col_clasif + 20
    desc_width = term_width - used
    if desc_width < 10: desc_width = 10

    print("-" * term_width)
    h = f"{'SEL':<{col_sel}} | {'ID':<{col_id}} | {'FECHA':<{col_fecha}} | {'DESCRIPCIÓN':<{desc_width}} | {'MONTO':>{col_monto}} | {'EST':<{col_est}} | {'CLASIF'}"
    print(h[:term_width])
    print("-" * term_width)

    validos = []
    for i, tx in enumerate(lote):
        key = str(i + 1)
        validos.append(key)

        c = C_RESET; est = "PEND"; clas = f"{tx.nombre_cc[:1]}/{tx.nombre_cat[:8]}>{tx.nombre_subcat[:8]}"
        if tx.estado == 'AUTO': c = C_GREEN; est = "AUTO"
        elif tx.estado == 'LISTO': c = C_CYAN; est = "LISTO"
        elif tx.estado == 'DESCARTADO': c = C_RED; est = "NO"; clas = "---"
        elif tx.estado == 'PENDIENTE':
            c = C_YELLOW
            if tx.conflictos: clas = f"{C_PURPLE}AMBIGUO (?){C_RESET}"
            else: clas = "INCOMPLETO"

        try: f_show = datetime.strptime(tx.fecha_fmt, '%Y-%m-%d').strftime('%d/%m/%Y')
        except: f_show = tx.fecha_fmt

        desc = limpiar_texto_visual(tx.descripcion_final)
        if len(desc) > desc_width: desc = desc[:desc_width-2] + ".."

        sel_str = f"[{key}]"
        linea = f"{c}{sel_str:<{col_sel}} | {tx.idx:<{col_id}} | {f_show:<{col_fecha}} | {desc:<{desc_width}} | {tx.monto:>{col_monto}.0f} | {est:<{col_est}} | {clas}{C_RESET}"
        print(linea)

    print("-" * term_width)
    print(f" [1-9] Editar | [S] Sig | [A] Ant | {C_GREEN}[G] GRABAR{C_RESET} | {C_RED}[X] SALIR{C_RESET}")
    return lote

def iniciar_torre_control(lista_tx, cursor, mp_nombre):
    diccionario = cargar_diccionario(cursor)
    reanalizar_lista(lista_tx, diccionario)

    pag = 1
    while True:
        lote_actual = render_dashboard(lista_tx, pag, mp_nombre)

        print(f"\n>>> Acción: ", end='', flush=True)
        cmd = leer_tecla_instante()
        print(cmd)

        if cmd == 'S' and pag < math.ceil(len(lista_tx)/PAGE_SIZE): pag += 1
        elif cmd == 'A' and pag > 1: pag -= 1
        elif cmd == 'X': return False
        elif cmd == 'G':
            pend = [t for t in lista_tx if t.estado == 'PENDIENTE']
            if pend:
                print(f"❌ {len(pend)} Incompletos."); time.sleep(1.5); continue
            return True

        # Selección Rápida 1-9
        if cmd in [str(x) for x in range(1, 10)]:
            idx_pag = int(cmd) - 1
            if idx_pag < len(lote_actual):
                tx = lote_actual[idx_pag]
                aprendido = editar_transaccion(cursor, tx, mp_nombre)
                if aprendido:
                    diccionario.append(aprendido)
                    reanalizar_lista(lista_tx, diccionario)