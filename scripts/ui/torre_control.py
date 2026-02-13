import os
import sys
import shutil
import time
from core.brain import limpiar_texto, reanalizar_inteligencia

# --- CONFIGURACIÓN VISUAL ---
C_RESET = "\033[0m"; C_CYAN = "\033[96m"; C_GREEN = "\033[92m"; C_YELLOW = "\033[93m"
C_RED = "\033[91m"; C_WHITE = "\033[97m"; C_PURPLE = "\033[95m"; C_INVERT = "\033[7m"
C_GRAY = "\033[90m"; ANSI_UP = "\033[A"; ANSI_CLEAR_LINE = "\033[K"
PANEL_HEIGHT = 6

# --- CAPA DE ENTRADA ---
def leer_input_navegacion():
    if os.name == 'nt':
        import msvcrt
        ch = msvcrt.getch()
        if ch in [b'\x00', b'\xe0']:
            sc = msvcrt.getch()
            mapping = {b'H': 'UP', b'P': 'DOWN', b'K': 'LEFT', b'M': 'RIGHT'}
            return mapping.get(sc)
        if ch == b'\r': return 'ENTER'
        if ch == b'\x08': return 'BACKSPACE'
        try: return ch.decode('utf-8').upper()
        except: return None
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                seq = sys.stdin.read(2)
                mapping = {'[A': 'UP', '[B': 'DOWN', '[D': 'LEFT', '[C': 'RIGHT'}
                return mapping.get(seq)
            if ch == '\r' or ch == '\n': return 'ENTER'
            if ch == '\x7f': return 'BACKSPACE'
            return ch.upper()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# --- SELECTOR DE MATRIZ ---
class SelectorInteligente:
    def __init__(self, cursor):
        self.cursor = cursor
        self.altura_total = PANEL_HEIGHT + 4

    def render_matrix(self, opciones, ancho_term):
        """Dibuja las opciones en una cuadrícula dinámica."""
        if not opciones:
            for _ in range(PANEL_HEIGHT): print(ANSI_CLEAR_LINE)
            return

        # 1. Calcular ancho de columna basado en la opción más larga
        max_len = max(len(op[1]) for op in opciones)
        col_width = max_len + 4
        num_cols = max(1, ancho_term // col_width)

        # 2. Determinar cuántos ítems entran en el panel
        capacidad = num_cols * PANEL_HEIGHT
        visibles = opciones[:capacidad]

        # 3. Renderizado por filas
        for r in range(PANEL_HEIGHT):
            linea = ""
            for c in range(num_cols):
                idx = r + (c * PANEL_HEIGHT) # Lógica de llenado por columnas
                if idx < len(visibles):
                    item = visibles[idx][1]
                    # Recorte de seguridad
                    if len(item) > col_width - 2: item = item[:col_width-2]
                    linea += f"   {item:<{col_width-3}}"
            print(f"{linea}{ANSI_CLEAR_LINE}")

    def seleccionar(self, titulo, sql, params=()):
        self.cursor.execute(sql, params)
        opciones = self.cursor.fetchall()
        buffer = ""; primera_vez = True

        while True:
            try: term_width = shutil.get_terminal_size().columns
            except: term_width = 80

            filtradas = [op for op in opciones if buffer.upper() in op[1].upper()]

            if not primera_vez: print(ANSI_UP * self.altura_total, end="")
            primera_vez = False

            # Cabecera del selector
            print(f"{C_CYAN}➤ {titulo}: {C_WHITE}{buffer}{C_RESET}{ANSI_CLEAR_LINE}")
            print("-" * term_width + ANSI_CLEAR_LINE)

            # --- LA MATRIZ ---
            self.render_matrix(filtradas, term_width)

            print("-" * term_width + ANSI_CLEAR_LINE)

            # Auto-selección inteligente (Si solo queda una opción y escribiste algo)
            if len(filtradas) == 1 and len(buffer) >= 2:
                # Feedback visual antes de cerrar
                print(ANSI_UP * (self.altura_total - 1), end="")
                print(f"{C_CYAN}➤ {titulo}: {C_GREEN}{filtradas[0][1]} ✅{C_RESET}{ANSI_CLEAR_LINE}")
                print("\n" * (self.altura_total - 2))
                time.sleep(0.3)
                return filtradas[0]

            cmd = leer_input_navegacion()
            if cmd == 'ENTER' and len(filtradas) >= 1: return filtradas[0]
            elif cmd == 'BACKSPACE': buffer = buffer[:-1]
            elif cmd == 'ESC': return None
            elif cmd and len(cmd) == 1: buffer += cmd


# --- FLUJO DE EDICIÓN ---
def flujo_edicion(cursor, tx, selector, render_callback, lista_tx, v_start, mp_nombre):
    def repaint(): render_callback(lista_tx, v_start, mp_nombre, idx_resaltado=tx)

    # 1. CC
    repaint(); print("\n")
    res_cc = selector.seleccionar("CENTRO DE COSTO", "SELECT id, nombre FROM param_centros_costo ORDER BY nombre")
    if not res_cc: return
    tx.id_cc, tx.nombre_cc = res_cc

    # 2. CATEGORÍA
    repaint(); print("\n")
    res_cat = selector.seleccionar("CATEGORÍA", "SELECT id, nombre FROM param_categorias ORDER BY nombre")
    if not res_cat: return
    tx.id_cat, tx.nombre_cat = res_cat

    # 3. SUBCATEGORÍA
    repaint(); print("\n")
    res_sub = selector.seleccionar(f"SUBCAT ({tx.nombre_cat})",
                                   "SELECT id, nombre FROM param_subcategorias WHERE id_categoria = ?", (tx.id_cat,))
    if res_sub:
        tx.id_subcat, tx.nombre_subcat = res_sub
        tx.estado = 'LISTO'

# --- DASHBOARD ---
def render_dashboard(lista_tx, viewport_start, mp_nombre, idx_resaltado=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    total = len(lista_tx)
    try: term_width = shutil.get_terminal_size().columns
    except: term_width = 80

    print(f"{C_CYAN}🦅 S.I.G.A.P. - TORRE DE CONTROL ({mp_nombre}){C_RESET}")
    print(f"📊 {viewport_start+1}-{min(total, viewport_start+10)} de {total} | ⬆⬇ Nav | ENTER Editar | G Grabar")
    print("-" * term_width)

    for i in range(viewport_start, min(total, viewport_start + 10)):
        tx = lista_tx[i]
        style = C_INVERT if tx == idx_resaltado else ""
        color = C_GREEN if tx.estado == 'AUTO' else (C_CYAN if tx.estado == 'LISTO' else C_YELLOW)
        if tx.estado == 'DESCARTADO': color = C_GRAY

        desc = (tx.descripcion_final[:30] + "..") if len(tx.descripcion_final) > 30 else tx.descripcion_final
        print(f"{style}{color}[{tx.fecha_fmt}] {desc:<32} | $ {tx.monto:>10.2f} | {tx.nombre_subcat[:15]:<15}\033[0m")

def iniciar_torre_control(lista_tx, cursor, mp_nombre):
    reanalizar_inteligencia(lista_tx, cursor)
    selector = SelectorInteligente(cursor)
    cursor_idx = 0; viewport_start = 0

    while True:
        if cursor_idx < viewport_start: viewport_start = cursor_idx
        if cursor_idx >= viewport_start + 10: viewport_start = cursor_idx - 9

        tx_foco = lista_tx[cursor_idx]
        render_dashboard(lista_tx, viewport_start, mp_nombre, idx_resaltado=tx_foco)

        cmd = leer_input_navegacion()
        if cmd == 'UP': cursor_idx = max(0, cursor_idx - 1)
        elif cmd == 'DOWN': cursor_idx = min(len(lista_tx) - 1, cursor_idx + 1)
        elif cmd == 'ENTER':
            flujo_edicion(cursor, tx_foco, selector, render_dashboard, lista_tx, viewport_start, mp_nombre)
        elif cmd == 'G': return True
        elif cmd == 'X': return False
        elif cmd == 'RIGHT': tx_foco.estado = 'DESCARTADO'
        elif cmd == 'LEFT': tx_foco.estado = 'PENDIENTE'
