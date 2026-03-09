import pandas as pd
import os
import shutil
import math
import time
import re
import sqlite3
import sys
from datetime import datetime
from scripts.utils.config_grafica import *


# ==========================================
# 🐧 CAPA DE ABSTRACCIÓN (CROSS-PLATFORM)
# ==========================================

IS_WINDOWS = os.name == 'nt'

if IS_WINDOWS:
    import msvcrt
    import winsound
else:
    # Librerías estándar de Unix para manejo de terminal
    import tty
    import termios

    def getch_unix():
        """Lee un caracter crudo en Unix/Linux."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# --- FUNCIONES PUENTE (WRAPPERS) ---

def leer_byte():
    """Devuelve un objeto BYTES de la tecla presionada (ej: b'a', b'\r')."""
    if IS_WINDOWS:
        return msvcrt.getch()
    else:
        char = getch_unix()
        return char.encode('utf-8')

def limpiar_pantalla():
    os.system('cls' if IS_WINDOWS else 'clear')

def vaciar_buffer_teclado():
    """Limpia pulsaciones pendientes para evitar 'doble enter'."""
    if IS_WINDOWS:
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        # En Linux/Termux el flush es complejo y puede bloquear.
        # Por seguridad y simplicidad en Termux, lo omitimos (no suele ser crítico).
        pass

def beep_confirmacion():
    if IS_WINDOWS:
        try: winsound.Beep(1000, 200)
        except: print('\a')
    else:
        # En Linux imprimimos el carácter BELL
        print('\a', end='', flush=True)

def beep_error():
    if IS_WINDOWS:
        try: winsound.Beep(500, 500)
        except: print('\a')
    else:
        print('\a', end='', flush=True)

def leer_input_navegacion():
    """Detecta flechas y teclas especiales en ambos sistemas."""
    ch = leer_byte()

    if IS_WINDOWS:
        # Windows usa secuencias de 2 bytes: \x00 o \xe0 + código
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
    else:
        # Linux usa secuencias ANSI: \x1b + [ + Letra
        if ch == b'\x1b':
            # Es un escape, leemos los siguientes bytes para ver si es flecha
            seq1 = leer_byte()
            if seq1 == b'[':
                seq2 = leer_byte()
                if seq2 == b'A': return 'UP'
                if seq2 == b'B': return 'DOWN'
                if seq2 == b'D': return 'LEFT'
                if seq2 == b'C': return 'RIGHT'
            return None # Fue solo la tecla ESC

        if ch == b'\r': return '\r' # Enter
        if ch == b'\n': return '\r'

        try: return ch.decode('utf-8').upper()
        except: return None

# ==========================================
# 🦅 LÓGICA DE NEGOCIO (CORE)
# ==========================================

class Movimiento:
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

        self.cuota_actual = 0
        self.cuotas_totales = 0
        self.detectar_cuotas_regex()

    def detectar_cuotas_regex(self):
        texto = self.descripcion_original.upper()
        texto_limpio = re.sub(r'\b(DEL|AL|VTO|FECHA)\s+\d{1,2}[\/-]\d{1,2}([\/-]\d{2,4})?', ' ', texto)
        match = re.search(r'\b(\d{1,2})[\/](\d{1,2})\b(?!\/)', texto_limpio)

        if not match:
            match = re.search(r'(?:CTA|CUOTA)\s?(\d{1,2})', texto_limpio)
            if match:
                self.cuota_actual = int(match.group(1))
                return

        if match:
            try:
                c_act = int(match.group(1))
                c_tot = int(match.group(2))
                if c_act > c_tot: return
                if c_tot > 60: return
                if 20 <= c_tot <= 30 and c_act <= 12: return
                self.cuota_actual = c_act
                self.cuotas_totales = c_tot
            except: pass

def limpiar_texto_visual(texto):
    basura = ["Compra con tarjeta de debito", "Transferencia realizada", "Transferencia recibida",
            "Pago de servicios", "Debito directo", "Su pago en", "Pago DEBIN", "\t"]
    limpio = texto
    for b in basura:
        limpio = limpio.replace(b, "").replace(b.upper(), "")
    limpio = " ".join(limpio.split())
    if limpio.startswith("-"): limpio = limpio[1:].strip()
    return limpio

def detectar_patron_comun(tx_actual, lista_movs):
    desc_clean = limpiar_texto_visual(tx_actual.descripcion_final)
    mejor_patron = desc_clean
    for tx in lista_movs:
        if tx.idx == tx_actual.idx: continue
        otro_desc = limpiar_texto_visual(tx.descripcion_final)
        comun = os.path.commonprefix([desc_clean, otro_desc])
        if len(comun) > 10 and len(comun) < len(desc_clean):
            if ' ' in comun: comun = comun.rsplit(' ', 1)[0]
            mejor_patron = comun.strip()
            break
    return mejor_patron

def cargar_diccionario(cursor):
    return list(cursor.execute("""
        SELECT d.termino, s.id, s.nombre, c.nombre, c.id
        FROM diccionario_terminos d
        JOIN param_subcategorias s ON d.id_subcategoria = s.id
        JOIN param_categorias c ON s.id_categoria = c.id
    """).fetchall())

def cargar_preferencias_contexto(cursor):
    sql_cc = """
        SELECT id_subcategoria, id_centro_costo, cc.nombre, COUNT(*) as uso
        FROM movimientos m
        JOIN param_centros_costo cc ON m.id_centro_costo = cc.id
        GROUP BY id_subcategoria, id_centro_costo
        ORDER BY id_subcategoria, uso DESC
    """
    cursor.execute(sql_cc)
    prefs_cc = {}
    for row in cursor.fetchall():
        sub_id, cc_id, cc_nom, _ = row
        if sub_id not in prefs_cc: prefs_cc[sub_id] = (cc_id, cc_nom)

    sql_amort = "SELECT id, amortizacion_default FROM param_subcategorias WHERE amortizacion_default > 0"
    cursor.execute(sql_amort)
    prefs_amort = {row[0]: row[1] for row in cursor.fetchall()}

    return prefs_cc, prefs_amort

def reanalizar_inteligencia(lista_movs, diccionario, cc_hint=None, map_prefs_cc=None, map_prefs_amort=None):
    diccionario.sort(key=lambda x: len(x[0]), reverse=True)

    for tx in lista_movs:
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

        if match_db and not tx.id_cc and map_prefs_cc:
            if tx.id_subcat in map_prefs_cc:
                tx.id_cc, tx.nombre_cc = map_prefs_cc[tx.id_subcat]

        if tx.id_cc and tx.id_cat and tx.id_subcat:
            tx.estado = 'AUTO'

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
        # Agregamos el número de índice visual [1], [2], etc.
        for i, op in enumerate(opciones):
            item_str = f"[{i+1}] {op[1]}"
            if len(item_str) > max_len: max_len = len(item_str)

        col_width = max_len + 4
        num_cols = max(1, ancho_term // col_width)

        capacidad = num_cols * PANEL_HEIGHT
        visibles = opciones[:capacidad]

        idx = 0
        for r in range(PANEL_HEIGHT):
            linea = ""
            for c in range(num_cols):
                if idx < len(visibles):
                    item = f"[{idx+1}] {visibles[idx][1]}"
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

            # 1. HÍBRIDO: Si el buffer es número, muestra todo (menú). Si es texto, filtra.
            if buffer.isdigit():
                filtradas = opciones
            else:
                filtradas = [op for op in opciones if buffer.upper() in op[1].upper()]

            if not primera_vez:
                print(ANSI_UP * self.altura_total, end="")
            primera_vez = False

            print(f"{C_CYAN}➤ {titulo}: {C_WHITE}{buffer}{C_RESET}{ANSI_CLEAR_LINE}")
            print(f"-" * term_width + ANSI_CLEAR_LINE)

            self.render_matrix(filtradas, term_width)

            if len(filtradas) == 0:
                if permitir_nuevo and not buffer.isdigit(): 
                    print(f"   {C_GREEN}[+] Crear '{buffer}' (Presione +){C_RESET}{ANSI_CLEAR_LINE}")
                else: 
                    print(f"   {C_RED}(Sin coincidencias o índice inválido){C_RESET}{ANSI_CLEAR_LINE}")
            else:
                print(f"{ANSI_CLEAR_LINE}")

            print(f"-" * term_width + ANSI_CLEAR_LINE)

            ch = leer_byte()

            if ch == b'\x1b': return None, None
            elif ch == b'\r':
                # -- CONFIRMACIÓN ESTRICTA CON ENTER --
                
                # A) Modo Numérico
                if buffer.isdigit():
                    idx = int(buffer) - 1
                    if 0 <= idx < len(opciones):
                        elegido = opciones[idx]
                        print(ANSI_UP * (self.altura_total - 1), end="")
                        print(f"{C_CYAN}➤ {titulo}: {C_GREEN}{elegido[1]} ✅{C_RESET}{ANSI_CLEAR_LINE}")
                        print("\n" * (self.altura_total - 2))
                        beep_confirmacion(); time.sleep(0.4)
                        return elegido[0], elegido[1]
                    else:
                        beep_error()
                        continue
                
                # B) Modo Texto (Filtro único)
                if len(filtradas) == 1:
                    elegido = filtradas[0]
                    print(ANSI_UP * (self.altura_total - 1), end="")
                    print(f"{C_CYAN}➤ {titulo}: {C_GREEN}{elegido[1]} ✅{C_RESET}{ANSI_CLEAR_LINE}")
                    print("\n" * (self.altura_total - 2))
                    beep_confirmacion(); time.sleep(0.4)
                    return elegido[0], elegido[1]
                
                # C) Modo Texto (Coincidencia exacta entre varias)
                for op in filtradas:
                    if op[1].upper() == buffer.upper():
                        print(ANSI_UP * (self.altura_total - 1), end="")
                        print(f"{C_CYAN}➤ {titulo}: {C_GREEN}{op[1]} ✅{C_RESET}{ANSI_CLEAR_LINE}")
                        print("\n" * (self.altura_total - 2))
                        beep_confirmacion(); time.sleep(0.4)
                        return op[0], op[1]
                
                # Si aprieta Enter sin coincidencia válida
                beep_error() 

            elif ch == b'\x08' or ch == b'\x7f':
                buffer = buffer[:-1]
            elif permitir_nuevo and ch == b'+' and not buffer.isdigit(): 
                return 'NUEVO', buffer
            else:
                try:
                    char = ch.decode('utf-8')
                    if char.isalnum() or char in [' ', '-', '.']: buffer += char
                except: pass


def flujo_edicion_inteligente(cursor, tx, selector, render_callback, lista_movs, viewport_start, mp_nombre, diccionario, prefs_cc, prefs_amort):

    historial_edicion = []

    def repaint():
        render_callback(lista_movs, viewport_start, mp_nombre, idx_resaltado=tx, modo_edicion=True)
        print("\n")
        for paso in historial_edicion:
            print(paso)

    # 1. CC
    repaint()
    id_cc, nom_cc = selector.seleccionar("CENTRO DE COSTO", "SELECT id, nombre FROM param_centros_costo ORDER BY nombre")
    if not id_cc: return None, None
    tx.id_cc, tx.nombre_cc = id_cc, nom_cc
    historial_edicion.append(f"{C_CYAN}➤ CENTRO DE COSTO: {C_GREEN}{nom_cc} ✅{C_RESET}")

    # 2. CAT
    repaint()
    id_cat, nom_cat = selector.seleccionar("CATEGORÍA", "SELECT id, nombre FROM param_categorias ORDER BY nombre")
    if not id_cat: return None, None
    tx.id_cat, tx.nombre_cat = id_cat, nom_cat
    historial_edicion.append(f"{C_CYAN}➤ CATEGORÍA: {C_GREEN}{nom_cat} ✅{C_RESET}")

    # 3. SUBCAT
    repaint()
    id_sub, nom_sub = selector.seleccionar(f"SUBCATEGORÍA ({nom_cat})", "SELECT id, nombre FROM param_subcategorias WHERE id_categoria = ? ORDER BY nombre", (id_cat,), permitir_nuevo=True)

    if id_sub == 'NUEVO':
        # 1. Si presionaste '+' sin texto previo en el buffer, te pedimos el nombre
        if not nom_sub.strip():
            print("\n" + "="*50)
            print("🏛️  GOBERNANZA: ALTA DE SUBCATEGORÍA")
            print("="*50)
            nom_sub = input(f"Ingrese el nombre de la nueva Subcategoría para '{nom_cat}' (o ENTER para cancelar): ")
            
        nombre_new = nom_sub.strip().title()
        
        # 2. Si te arrepentiste o lo dejaste vacío, ABORTAMOS y volvemos al buscador
        if not nombre_new:
            print("⚠️  Operación cancelada. Volviendo al buscador...")
            time.sleep(1) # Pequeña pausa para que leas el mensaje
            return None, None 
            
        # --- 🏛️ GOBERNANZA 1: Fricción Psicológica (Alerta de Micro-management) ---
        umbral_alerta = 5000
        if abs(tx.monto) < umbral_alerta:
            print(f"\n⚠️  ALERTA DE GOBERNANZA: El monto asociado es bajo (${abs(tx.monto):.2f}).")
            print(f"Crear la subcategoría '{nombre_new}' puede generar 'micro-management' si no es un gasto recurrente.")
            print("💡 Sugerencia: ¿Podés agruparlo en algo más global (ej: 'Varios' o 'Gastos Menores')?")
            
            confirmacion = input(f"\n¿Estás seguro de forzar la creación de '{nombre_new}'? (S/N): ").strip().upper()
            if confirmacion != 'S':
                print("🚫 Creación abortada. Seleccione una subcategoría existente.")
                time.sleep(1.5)
                return None, None # Volvemos al buscador
        
        try:
            # --- 🏛️ GOBERNANZA 2: Inserción Atómica ---
            cursor.execute("INSERT INTO param_subcategorias (id_categoria, nombre) VALUES (?, ?)", (id_cat, nombre_new))
            id_sub = cursor.lastrowid
            nom_sub = nombre_new
            
            # --- 🏛️ GOBERNANZA 3: Trazabilidad Absoluta (Milisegundos) ---
            timestamp_ms = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            
            # Adaptamos el Alta de Subcategoría a tu estructura de auditoría
            cursor.execute(
                """INSERT INTO auditoria_movimientos 
                (timestamp, usuario, accion, estado_previo, estado_nuevo, resultado) 
                VALUES (?, ?, ?, ?, ?, ?)""", 
                (
                    timestamp_ms, 
                    'SIGAP_UI', 
                    'ALTA_SUBCAT', 
                    'INEXISTENTE', 
                    f"ID: {id_sub} | Nombre: '{nombre_new}' | Padre: {id_cat}", 
                    'OK'
                )
            )

            # Commiteamos ambas operaciones juntas
            cursor.connection.commit()
            
        except Exception as e: 
            print(f"\n❌ [LOG TÉCNICO] Error crítico al insertar en DB: {e}")
            input("Presione ENTER para abortar...")
            return None, None

    if not id_sub: return None, None

    tx.id_subcat, tx.nombre_subcat = id_sub, nom_sub
    historial_edicion.append(f"{C_CYAN}➤ SUBCATEGORÍA: {C_GREEN}{nom_sub} ✅{C_RESET}")

    #     # --- 4. PREGUNTA DE AMORTIZACIÓN (APLICACIÓN SILENCIOSA) ---
    if tx.cuotas_totales <= 1 and id_sub in prefs_amort:
        meses = prefs_amort[id_sub]
        if meses > 1:
            tx.cuotas_totales = meses
            tx.cuota_actual = 1
            historial_edicion.append(f"{C_CYAN}➤ AMORTIZACIÓN: {C_GREEN}Autocompletado {meses} cuotas ✅{C_RESET}")

    tx.estado = 'LISTO'
    tx.ia_match = False

    prefs_cc[id_sub] = (id_cc, nom_cc)

    repaint()
    clave_sugerida = detectar_patron_comun(tx, lista_movs)

    while True:
        print(f"\n{C_PURPLE}🧠 ¿Memorizar '{clave_sugerida}' como {nom_sub}? (S/n/Back){C_RESET}{ANSI_CLEAR_LINE}", end='\r')
        vaciar_buffer_teclado()
        ch = leer_byte() # <--- WRAPPER

        if ch in [b's', b'S', b'\r', b' ']:
            tx.nuevo_sinonimo = clave_sugerida
            return (clave_sugerida, tx.id_subcat, tx.nombre_subcat, tx.nombre_cat, tx.id_cat), (clave_sugerida.lower(), tx.id_cc, tx.nombre_cc)
        elif ch in [b'n', b'N', b'\x1b']:
            return None, None
        elif ch == b'\x08' or ch == b'\x7f':
            while True:
                print(ANSI_CLEAR_LINE, end='\r')
                print(f"{C_GRAY}   (Original: {clave_sugerida}){C_RESET}")
                print(f"{C_YELLOW}✏️ Escribe nueva clave: {C_RESET}", end='')
                custom_clave = input().strip()
                if not custom_clave: break
                desc_real_lower = limpiar_texto_visual(tx.descripcion_final).lower()
                if custom_clave.lower() in desc_real_lower:
                    tx.nuevo_sinonimo = custom_clave
                    return (custom_clave, tx.id_subcat, tx.nombre_subcat, tx.nombre_cat, tx.id_cat), (custom_clave.lower(), tx.id_cc, tx.nombre_cc)
                else:
                    print(f"   {C_RED}❌ Error: La frase '{custom_clave}' no existe en la descripción original.{C_RESET}")
                    beep_error(); time.sleep(1.5)
            continue
        else: beep_error()

def render_dashboard(lista_movs, viewport_start, mp_nombre, idx_resaltado=None, modo_edicion=False, custom_title=None):
    limpiar_pantalla()

    total = len(lista_movs)
    viewport_end = min(total, viewport_start + VIEWPORT_HEIGHT)
    lote = lista_movs[viewport_start:viewport_end]

    try: term_width = shutil.get_terminal_size().columns
    except: term_width = 80

    col_sel = 3; col_fecha = 10; col_monto = 15
    fixed_space = col_sel + col_fecha + col_monto + 13
    available = max(10, term_width - fixed_space)

    max_desc = 0; max_clasif = 0; max_monto_len = 0
    for tx in lote:
        m_str = f"{tx.monto:,.2f}";
        if len(m_str) > max_monto_len: max_monto_len = len(m_str)

        tag_cuota = ""
        if tx.cuotas_totales > 1: tag_cuota = f"💳 [{tx.cuota_actual}/{tx.cuotas_totales}] "

        d = len(tag_cuota + limpiar_texto_visual(tx.descripcion_final))
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

    if custom_title:
        print(custom_title)
    else:
        print(f"{C_CYAN}🦅 S.I.G.A.P. - INBOX MOVIMIENTOS ({mp_nombre}){C_RESET}")

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

        desc_visual = limpiar_texto_visual(tx.descripcion_final)
        if tx.cuotas_totales > 1:
            tag_cuota = f"💳 [{tx.cuota_actual}/{tx.cuotas_totales}]"
            desc_visual = f"{tag_cuota} {desc_visual}"

        if tx == idx_resaltado:
            style = C_INVERT
            if tx.estado == 'AUTO': clasif = f"[AUTO] {clasif}"
            elif tx.estado == 'LISTO': clasif = f"[OK] {clasif}"
            elif tx.estado == 'PENDIENTE': clasif = f"[PEND] {clasif}"
            elif tx.estado == 'DESCARTADO': clasif = "[DESCARTADO]"

        f_show = tx.fecha_fmt
        if len(desc_visual) > col_desc: desc_visual = desc_visual[:col_desc-2] + ".."

        val_str = f"{tx.monto:,.2f}"
        monto_fmt = f"$ {val_str:>{max_monto_len}}"

        print(f"{style}[{key}] | {f_show} | {desc_visual:<{col_desc}} | {monto_fmt:>{col_monto}} | {clasif:<{col_clasif}}{C_RESET}")

    print("-" * term_width)

    n_auto = sum(1 for t in lista_movs if t.estado == 'AUTO')
    n_listo = sum(1 for t in lista_movs if t.estado == 'LISTO')
    n_pend = sum(1 for t in lista_movs if t.estado == 'PENDIENTE')
    n_desc = sum(1 for t in lista_movs if t.estado == 'DESCARTADO')

    stats = f"{C_YELLOW}PEND: {n_pend}{C_RESET} | {C_GREEN}AUTO: {n_auto}{C_RESET} | {C_CYAN}OK: {n_listo}{C_RESET} | {C_GRAY}🗑️: {n_desc}{C_RESET}"

    if modo_edicion:
        # Menú contextual: Modo Edición de Rubros
        print(f"{stats} | {C_YELLOW}[G]{C_RESET} Grabar | {C_RED}[X]{C_RESET} Salir")
        print() # Separador limpio
        print(f"{C_WHITE}[⬆⬇ ⬅⮕] Cancela Edición{C_RESET}")
    else:
        # Menú contextual: Modo Navegación (Torre de Control)
        print(f"{stats} | [Enter] Selecciona | {C_PURPLE}[C]{C_RESET} Cuotas | {C_YELLOW}[G]{C_RESET} Grabar | {C_RED}[X]{C_RESET} Salir")

def iniciar_inbox_movimientos(lista_movs, cursor, mp_nombre):
    diccionario = cargar_diccionario(cursor)
    prefs_cc, prefs_amort = cargar_preferencias_contexto(cursor)

    reanalizar_inteligencia(lista_movs, diccionario, map_prefs_cc=prefs_cc, map_prefs_amort=prefs_amort)

    selector = SelectorInteligente(cursor)
    cursor_idx = 0
    viewport_start = 0

    while True:
        if cursor_idx < viewport_start: viewport_start = cursor_idx
        if cursor_idx >= viewport_start + VIEWPORT_HEIGHT: viewport_start = cursor_idx - VIEWPORT_HEIGHT + 1

        mov_foco = lista_movs[cursor_idx]
        render_dashboard(lista_movs, viewport_start, mp_nombre, idx_resaltado=mov_foco, modo_edicion=False)

        key = leer_input_navegacion()

        if key == 'UP': cursor_idx = max(0, cursor_idx - 1)
        elif key == 'DOWN': cursor_idx = min(len(lista_movs) - 1, cursor_idx + 1)
        elif key == 'RIGHT':
            if mov_foco.estado != 'DESCARTADO':
                mov_foco.estado = 'DESCARTADO'
                cursor_idx = min(len(lista_movs) - 1, cursor_idx + 1)
        elif key == 'LEFT':
            if mov_foco.estado == 'DESCARTADO':
                if mov_foco.id_cc and mov_foco.id_subcat: mov_foco.estado = 'AUTO'
                else: mov_foco.estado = 'PENDIENTE'
        elif key == '\r':
            if mov_foco.estado == 'DESCARTADO': continue
            aprendido, cc_hint = flujo_edicion_inteligente(cursor, mov_foco, selector, render_dashboard, lista_movs, viewport_start, mp_nombre, diccionario, prefs_cc, prefs_amort)
            if aprendido:
                diccionario.append(aprendido)
                reanalizar_inteligencia(lista_movs, diccionario, cc_hint, prefs_cc, prefs_amort)
                cursor_idx = min(len(lista_movs) - 1, cursor_idx + 1)
        elif key == 'G': return True
        elif key == 'X': return False
        elif key == 'C':
            if mov_foco.estado == 'DESCARTADO': continue
            
            print(f"\n{C_YELLOW}📅 Modificando cuotas para: {mov_foco.descripcion_final}{C_RESET}")
            print(f"{C_YELLOW}➤ Ingrese cantidad de cuotas (0 o 1 = Sin cuotas): {C_RESET}", end='', flush=True)
            
            vaciar_buffer_teclado()
            buffer_cuotas = ""
            while True:
                ch = leer_byte()
                if ch == b'\r': break
                if ch == b'\x1b': buffer_cuotas = ""; break # Esc cancela
                if ch.isdigit():
                    buffer_cuotas += ch.decode('utf-8')
                    print(f"\r{C_YELLOW}➤ Ingrese cantidad de cuotas (0 o 1 = Sin cuotas): {C_WHITE}{buffer_cuotas}{C_RESET}", end='', flush=True)
            
            if buffer_cuotas:
                meses = int(buffer_cuotas)
                if meses > 1:
                    mov_foco.cuotas_totales = meses
                    mov_foco.cuota_actual = 1
                    # Si tiene subcategoría y la regla es nueva, ofrecemos memorizar
                    if mov_foco.id_subcat and (mov_foco.id_subcat not in prefs_amort or prefs_amort[mov_foco.id_subcat] != meses):
                        print(f"\n{C_PURPLE}🧠 ¿Recordar que '{mov_foco.nombre_subcat}' por defecto son {meses} meses? (S/n){C_RESET}", end='\r')
                        ch_mem = leer_byte()
                        if ch_mem in [b's', b'S', b'\r']:
                            cursor.execute("UPDATE param_subcategorias SET amortizacion_default = ? WHERE id = ?", (meses, mov_foco.id_subcat))
                            cursor.connection.commit()
                            prefs_amort[mov_foco.id_subcat] = meses
                            print(f"{ANSI_CLEAR_LINE}✅ Regla aprendida/actualizada.      ")
                            time.sleep(0.5)
                else:
                    mov_foco.cuotas_totales = 0
                    mov_foco.cuota_actual = 0

