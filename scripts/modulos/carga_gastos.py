import pandas as pd
import os
import shutil
import math
import time
import winsound
import msvcrt
from datetime import datetime

# --- CONFIGURACIÓN VISUAL ---
VIEWPORT_HEIGHT = 10
PANEL_HEIGHT = 6

C_RESET = "\033[0m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_CYAN = "\033[96m"
C_WHITE = "\033[97m"
C_PURPLE = "\033[95m"
C_INVERT = "\033[7m"
C_GRAY = "\033[90m"

# ANSI CODES
ANSI_CLEAR_LINE = "\033[K"
ANSI_UP = "\033[A"

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

# --- UI UTILS ---

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def vaciar_buffer_teclado():
    while msvcrt.kbhit():
        msvcrt.getch()

def beep_confirmacion():
    try: winsound.Beep(1000, 200)
    except: print('\a')
    vaciar_buffer_teclado()

def beep_error():
    try: winsound.Beep(500, 500)
    except: print('\a')
    vaciar_buffer_teclado()

def leer_input_navegacion():
    ch = msvcrt.getch()
    if ch in [b'\x00', b'\xe0']:
        try:
            scancode = msvcrt.getch()
            if scancode == b'H': return 'UP'
            if scancode == b'P': return 'DOWN'
            if scancode == b'K': return 'LEFT'
            if scancode == b'M': return 'RIGHT'
        except: pass
        return None
    try: return ch.decode('utf-8').upper()
    except: return None

def limpiar_texto_visual(texto):
    basura = ["Compra con tarjeta de debito", "Transferencia realizada", "Transferencia recibida",
              "Pago de servicios", "Debito directo", "Su pago en", "Pago DEBIN", "\t"]
    limpio = texto
    for b in basura:
        limpio = limpio.replace(b, "").replace(b.upper(), "")
    limpio = " ".join(limpio.split())
    if limpio.startswith("-"): limpio = limpio[1:].strip()
    return limpio

def detectar_patron_comun(tx_actual, lista_tx):
    desc_clean = limpiar_texto_visual(tx_actual.descripcion_final)
    mejor_patron = desc_clean
    for tx in lista_tx:
        if tx.idx == tx_actual.idx: continue
        otro_desc = limpiar_texto_visual(tx.descripcion_final)
        comun = os.path.commonprefix([desc_clean, otro_desc])
        if len(comun) > 10 and len(comun) < len(desc_clean):
            if ' ' in comun: comun = comun.rsplit(' ', 1)[0]
            mejor_patron = comun.strip()
            break
    return mejor_patron

# --- MOTOR INTELLISENSE ---

class SelectorInteligente:
    def __init__(self, cursor):
        self.cursor = cursor
        self.altura_total = PANEL_HEIGHT + 4

    def obtener_opciones(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def render_matrix(self, opciones, ancho_term):
        if not opciones:
            for _ in range(PANEL_HEIGHT): print(ANSI_CLEAR_LINE)
            return

        max_len = 0
        for op in opciones:
            if len(op[1]) > max_len: max_len = len(op[1])

        col_width = max_len + 4
        num_cols = max(1, ancho_term // col_width)

        capacidad = num_cols * PANEL_HEIGHT
        visibles = opciones[:capacidad]

        idx = 0
        for r in range(PANEL_HEIGHT):
            linea = ""
            for c in range(num_cols):
                if idx < len(visibles):
                    item = visibles[idx][1]
                    if len(item) > col_width - 2: item = item[:col_width-2]
                    linea += f"   {item:<{col_width-3}}"
                    idx += 1
            print(f"{linea}{ANSI_CLEAR_LINE}")

    def seleccionar(self, titulo, sql, params=(), permitir_nuevo=False):
        opciones = self.obtener_opciones(sql, params)
        buffer = ""
        primera_vez = True
        vaciar_buffer_teclado()

        while True:
            try: term_width = shutil.get_terminal_size().columns
            except: term_width = 80

            filtradas = [op for op in opciones if buffer.upper() in op[1].upper()]

            if not primera_vez:
                print(ANSI_UP * self.altura_total, end="")
            primera_vez = False

            print(f"{C_CYAN}➤ {titulo}: {C_WHITE}{buffer}{C_RESET}{ANSI_CLEAR_LINE}")
            print(f"-" * term_width + ANSI_CLEAR_LINE)

            self.render_matrix(filtradas, term_width)

            if len(filtradas) == 0:
                if permitir_nuevo: print(f"   {C_GREEN}[+] Crear '{buffer}' (Presione +){C_RESET}{ANSI_CLEAR_LINE}")
                else: print(f"   {C_RED}(Sin coincidencias){C_RESET}{ANSI_CLEAR_LINE}")
            else:
                print(f"{ANSI_CLEAR_LINE}")

            print(f"-" * term_width + ANSI_CLEAR_LINE)

            if len(filtradas) == 1 and len(buffer) >= 2:
                elegido = filtradas[0]
                print(ANSI_UP * (self.altura_total - 1), end="")
                print(f"{C_CYAN}➤ {titulo}: {C_GREEN}{elegido[1]} ✅{C_RESET}{ANSI_CLEAR_LINE}")
                print("\n" * (self.altura_total - 2))

                beep_confirmacion()
                time.sleep(0.4)
                return elegido[0], elegido[1]

            ch = msvcrt.getch()

            if ch == b'\x1b': return None, None
            elif ch == b'\r':
                if len(filtradas) == 1: return filtradas[0][0], filtradas[0][1]
                for op in filtradas:
                    if op[1].upper() == buffer.upper(): return op[0], op[1]
            elif ch == b'\x08': buffer = buffer[:-1]
            elif permitir_nuevo and ch == b'+': return 'NUEVO', buffer
            else:
                try:
                    char = ch.decode('utf-8')
                    if char.isalnum() or char in [' ', '-', '.']: buffer += char
                except: pass

# --- CORE LOGIC ---

def cargar_diccionario(cursor):
    return list(cursor.execute("""
        SELECT d.termino, s.id, s.nombre, c.nombre, c.id
        FROM diccionario_terminos d
        JOIN param_subcategorias s ON d.id_subcategoria = s.id
        JOIN param_categorias c ON s.id_categoria = c.id
    """).fetchall())

def reanalizar_inteligencia(lista_tx, diccionario, cc_hint=None):
    diccionario.sort(key=lambda x: len(x[0]), reverse=True)

    for tx in lista_tx:
        if tx.estado in ['DESCARTADO']: continue
        if tx.estado not in ['PENDIENTE']: continue

        desc_visual_lower = limpiar_texto_visual(tx.descripcion_original).lower()
        match_db = False

        for termino, id_sub, nom_sub, nom_cat, id_cat in diccionario:
            if termino.lower() in desc_visual_lower:
                tx.id_subcat = id_sub; tx.nombre_subcat = nom_sub
                tx.nombre_cat = nom_cat; tx.id_cat = id_cat
                tx.ia_match = True
                match_db = True
                break

        if cc_hint and match_db:
            termino_hint, id_cc_hint, nom_cc_hint = cc_hint
            if termino_hint in desc_visual_lower and not tx.id_cc:
                tx.id_cc = id_cc_hint; tx.nombre_cc = nom_cc_hint

        if tx.id_cc and tx.id_cat and tx.id_subcat:
            tx.estado = 'AUTO'

def flujo_edicion_inteligente(cursor, tx, selector, render_callback, lista_tx, viewport_start, mp_nombre):

    def repaint():
        render_callback(lista_tx, viewport_start, mp_nombre, idx_resaltado=tx)

    repaint(); print("\n")
    id_cc, nom_cc = selector.seleccionar("CENTRO DE COSTO", "SELECT id, nombre FROM param_centros_costo ORDER BY nombre")
    if not id_cc: return None, None
    tx.id_cc, tx.nombre_cc = id_cc, nom_cc

    repaint(); print("\n")
    id_cat, nom_cat = selector.seleccionar("CATEGORÍA", "SELECT id, nombre FROM param_categorias ORDER BY nombre")
    if not id_cat: return None, None
    tx.id_cat, tx.nombre_cat = id_cat, nom_cat

    repaint(); print("\n")
    id_sub, nom_sub = selector.seleccionar(f"SUBCATEGORÍA ({nom_cat})", "SELECT id, nombre FROM param_subcategorias WHERE id_categoria = ? ORDER BY nombre", (id_cat,), permitir_nuevo=True)

    if id_sub == 'NUEVO':
        nombre_new = nom_sub.strip().title()
        if nombre_new:
            try:
                cursor.execute("INSERT INTO param_subcategorias (id_categoria, nombre) VALUES (?, ?)", (id_cat, nombre_new))
                cursor.connection.commit()
                id_sub = cursor.lastrowid; nom_sub = nombre_new
            except: return None, None
    if not id_sub: return None, None
    tx.id_subcat, tx.nombre_subcat = id_sub, nom_sub

    tx.estado = 'LISTO'
    tx.ia_match = False

    repaint()
    clave_sugerida = detectar_patron_comun(tx, lista_tx)

    while True:
        print(f"\n{C_PURPLE}🧠 ¿Memorizar '{clave_sugerida}' como {nom_sub}? (S/n/Back){C_RESET}{ANSI_CLEAR_LINE}", end='\r')
        vaciar_buffer_teclado()
        ch = msvcrt.getch()
        if ch in [b's', b'S', b'\r', b' ']:
            return (clave_sugerida, tx.id_subcat, tx.nombre_subcat, tx.nombre_cat, tx.id_cat), (clave_sugerida.lower(), tx.id_cc, tx.nombre_cc)
        elif ch in [b'n', b'N', b'\x1b']:
            return None, None
        elif ch == b'\x08':
            while True:
                print(ANSI_CLEAR_LINE, end='\r')
                print(f"{C_YELLOW}✏️ Personalizar clave: {C_RESET}", end='')
                custom_clave = input().strip()
                if not custom_clave: break
                desc_real_lower = limpiar_texto_visual(tx.descripcion_final).lower()
                if custom_clave.lower() in desc_real_lower:
                    return (custom_clave, tx.id_subcat, tx.nombre_subcat, tx.nombre_cat, tx.id_cat), (custom_clave.lower(), tx.id_cc, tx.nombre_cc)
                else:
                    print(f"   {C_RED}❌ Error: La frase '{custom_clave}' no existe en la descripción original.{C_RESET}")
                    beep_error(); time.sleep(1.5)
            continue
        else: beep_error()

# --- DASHBOARD DINÁMICO ---

def render_dashboard(lista_tx, viewport_start, mp_nombre, idx_resaltado=None):
    limpiar_pantalla()

    total = len(lista_tx)
    viewport_end = min(total, viewport_start + VIEWPORT_HEIGHT)
    lote = lista_tx[viewport_start:viewport_end]

    try: term_width = shutil.get_terminal_size().columns
    except: term_width = 80

    col_sel = 3; col_fecha = 10; col_monto = 15
    fixed_space = col_sel + col_fecha + col_monto + 13
    available = max(10, term_width - fixed_space)

    # 1. Medir contenido
    max_desc = 0; max_clasif = 0; max_monto_len = 0
    for tx in lote:
        m_str = f"{tx.monto:,.2f}";
        if len(m_str) > max_monto_len: max_monto_len = len(m_str)

        d = len(limpiar_texto_visual(tx.descripcion_final))
        if d > max_desc: max_desc = d

        c_str = f"{tx.nombre_cc if tx.id_cc else '???'} / {tx.nombre_cat if tx.id_cat else '???'} > {tx.nombre_subcat if tx.id_subcat else '???'}"
        if len(c_str) > max_clasif: max_clasif = len(c_str)

    col_monto = max_monto_len + 4
    fixed_space = col_sel + col_fecha + col_monto + 13
    available = max(10, term_width - fixed_space)

    req_desc = max_desc + 2; req_clasif = max_clasif + 2
    if req_desc + req_clasif <= available:
        col_desc = max(20, req_desc)
        col_clasif = available - col_desc
    else:
        col_clasif = min(req_clasif, int(available * 0.5))
        col_desc = available - col_clasif

    print(f"{C_CYAN}🦅 S.I.G.A.P. - TORRE DE CONTROL ({mp_nombre}){C_RESET}")
    print(f"📊 Vista: {viewport_start+1}-{viewport_end} de {total} | ⬆⬇ Navegar | ⮕ Descartar | ⬅ Recuperar | ENTER Editar")

    print("-" * term_width)
    h = f"SEL | FECHA      | {'DESCRIPCIÓN':<{col_desc}} | {'MONTO':>{col_monto}} | {'CLASIFICACIÓN':<{col_clasif}}"
    print(h[:term_width])
    print("-" * term_width)

    for i, tx in enumerate(lote):
        key = str(viewport_start + i + 1)

        style = C_RESET
        if tx.estado == 'AUTO': style = C_GREEN
        elif tx.estado == 'LISTO': style = C_CYAN
        elif tx.estado == 'DESCARTADO': style = C_GRAY
        elif tx.estado == 'PENDIENTE': style = C_YELLOW

        cc_str = tx.nombre_cc if tx.id_cc else "???"
        safe_width = max(10, col_clasif - 6)
        w_cc = len(cc_str)
        remain = max(4, safe_width - w_cc)
        limit_cat = max(3, int(remain * 0.5))
        limit_sub = max(3, int(remain * 0.5))
        cat_str = tx.nombre_cat[:limit_cat] if tx.id_cat else "???"
        sub_str = tx.nombre_subcat[:limit_sub] if tx.id_subcat else "???"
        clasif = f"{cc_str} / {cat_str} > {sub_str}"

        if tx.estado == 'PENDIENTE':
            if not tx.id_subcat: clasif = "---"
        if tx.estado == 'DESCARTADO':
            clasif = "[DESCARTADO]"

        # --- AQUI ESTA LA MAGIA VISUAL DE ESTADO ---
        if tx == idx_resaltado:
            style = C_INVERT
            # Inyectamos el estado en el texto porque perdemos el color
            if tx.estado == 'AUTO': clasif = f"[AUTO] {clasif}"
            elif tx.estado == 'LISTO': clasif = f"[OK] {clasif}"
            elif tx.estado == 'PENDIENTE': clasif = f"[PEND] {clasif}"
            elif tx.estado == 'DESCARTADO': clasif = "[DESCARTADO]"

        f_show = tx.fecha_fmt
        desc = limpiar_texto_visual(tx.descripcion_final)
        if len(desc) > col_desc: desc = desc[:col_desc-2] + ".."

        val_str = f"{tx.monto:,.2f}"
        monto_fmt = f"$ {val_str:>{max_monto_len}}"

        print(f"{style}[{key}] | {f_show} | {desc:<{col_desc}} | {monto_fmt:>{col_monto}} | {clasif:<{col_clasif}}{C_RESET}")

    # --- FOOTER CON STATS ---
    print("-" * term_width)

    # Calcular contadores
    n_auto = sum(1 for t in lista_tx if t.estado == 'AUTO')
    n_listo = sum(1 for t in lista_tx if t.estado == 'LISTO')
    n_pend = sum(1 for t in lista_tx if t.estado == 'PENDIENTE')
    n_desc = sum(1 for t in lista_tx if t.estado == 'DESCARTADO')

    # Barra de estado tipo Excel
    stats = f"{C_YELLOW}PEND: {n_pend}{C_RESET} | {C_GREEN}AUTO: {n_auto}{C_RESET} | {C_CYAN}OK: {n_listo}{C_RESET} | {C_GRAY}🗑️: {n_desc}{C_RESET}"

    print(f"{stats} | {C_YELLOW}[G]{C_RESET} Grabar | {C_RED}[X]{C_RESET} Salir")

# --- MAIN LOOP (HYPERFLUX) ---

def iniciar_torre_control(lista_tx, cursor, mp_nombre):
    diccionario = cargar_diccionario(cursor)
    reanalizar_inteligencia(lista_tx, diccionario)
    selector = SelectorInteligente(cursor)

    cursor_idx = 0
    viewport_start = 0

    while True:
        if cursor_idx < viewport_start:
            viewport_start = cursor_idx
        if cursor_idx >= viewport_start + VIEWPORT_HEIGHT:
            viewport_start = cursor_idx - VIEWPORT_HEIGHT + 1

        tx_foco = lista_tx[cursor_idx]

        render_dashboard(lista_tx, viewport_start, mp_nombre, idx_resaltado=tx_foco)

        key = leer_input_navegacion()

        if key == 'UP':
            cursor_idx = max(0, cursor_idx - 1)
        elif key == 'DOWN':
            cursor_idx = min(len(lista_tx) - 1, cursor_idx + 1)
        elif key == 'RIGHT':
            if tx_foco.estado != 'DESCARTADO':
                tx_foco.estado = 'DESCARTADO'
                cursor_idx = min(len(lista_tx) - 1, cursor_idx + 1)
        elif key == 'LEFT':
            if tx_foco.estado == 'DESCARTADO':
                if tx_foco.id_cc and tx_foco.id_subcat: tx_foco.estado = 'AUTO'
                else: tx_foco.estado = 'PENDIENTE'
        elif key == '\r':
            if tx_foco.estado == 'DESCARTADO': continue
            aprendido, cc_hint = flujo_edicion_inteligente(cursor, tx_foco, selector, render_dashboard, lista_tx, viewport_start, mp_nombre)
            if aprendido:
                diccionario.append(aprendido)
                reanalizar_inteligencia(lista_tx, diccionario, cc_hint)
                cursor_idx = min(len(lista_tx) - 1, cursor_idx + 1)
        elif key == 'G': return True
        elif key == 'X': return False