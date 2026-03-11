"""
sesion_cierre.py — S.I.G.A.P. · Proyecto Fénix
Registra el cierre de una sesión de trabajo en docs/SESIONES.md
Uso: python scripts/utils/sesion_cierre.py
"""

import os
import re
from datetime import datetime, timedelta

# ── Rutas ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SESIONES_PATH = os.path.join(BASE_DIR, 'docs', 'SESIONES.md')
TEMP_PATH = os.path.join(BASE_DIR, '.sesion_activa')

# ── Lectura del estado de apertura ─────────────────────────────────────────

def leer_sesion_activa():
    """Lee los datos de apertura guardados por sesion_inicio.py."""
    if not os.path.exists(TEMP_PATH):
        return None
    datos = {}
    with open(TEMP_PATH, 'r', encoding='utf-8') as f:
        for linea in f:
            if '=' in linea:
                clave, valor = linea.strip().split('=', 1)
                datos[clave] = valor
    return datos if datos else None

# ── Cálculo de duración ─────────────────────────────────────────────────────

def calcular_duracion(hora_inicio_str, hora_fin):
    """Calcula la duración legible entre inicio y fin."""
    try:
        hoy = hora_fin.date()
        hora_inicio = datetime.strptime(f"{hoy} {hora_inicio_str}", "%Y-%m-%d %H:%M")
        # Si fin < inicio asumimos que pasó la medianoche
        if hora_fin < hora_inicio:
            hora_inicio -= timedelta(days=1)
        delta = hora_fin - hora_inicio
        total_min = int(delta.total_seconds() // 60)
        horas = total_min // 60
        minutos = total_min % 60
        if horas > 0:
            return f"{horas}h {minutos:02d}m"
        return f"{minutos}m"
    except Exception:
        return "—"

# ── Input del usuario ───────────────────────────────────────────────────────

def solicitar_observaciones(datos_apertura, hora_fin):
    """Muestra resumen y solicita observaciones opcionales."""
    duracion = calcular_duracion(datos_apertura['hora_inicio'], hora_fin)

    print()
    print("=" * 60)
    print("  🦅 S.I.G.A.P. — CIERRE DE SESIÓN")
    print("=" * 60)
    print()
    print(f"  #️⃣  Sesión     : #{datos_apertura['n_sesion']}")
    print(f"  🎯 Objetivo   : {datos_apertura['objetivo']}")
    print(f"  ⏱️  Inicio     : {datos_apertura['hora_inicio']}")
    print(f"  ⏱️  Fin        : {hora_fin.strftime('%H:%M')}")
    print(f"  ⌛ Duración   : {duracion}")
    print()

    obs = input("  📝 Observaciones (Enter para omitir): ").strip()
    if not obs:
        obs = "—"

    print()
    print(f"  ✅ Sesión #{datos_apertura['n_sesion']} cerrada. ¡Buen trabajo, Martín!")
    print("=" * 60)
    print()

    return obs, duracion

# ── Actualización de SESIONES.md ───────────────────────────────────────────

def cerrar_fila_sesion(datos_apertura, hora_fin_str, duracion, observaciones):
    """Reemplaza la fila de apertura (con —) por la fila completa."""
    if not os.path.exists(SESIONES_PATH):
        print("  ⚠️  No se encontró docs/SESIONES.md. ¿Ejecutaste sesion_inicio.py?")
        return

    with open(SESIONES_PATH, 'r', encoding='utf-8') as f:
        contenido = f.read()

    n = datos_apertura['n_sesion']
    objetivo_escaped = re.escape(datos_apertura['objetivo'])

    # Buscamos la fila de apertura de esta sesión (tiene "| — | — |" en fin/duración)
    patron = (
        rf"(\| {n} \| {re.escape(datos_apertura['fecha'])} \| "
        rf"{re.escape(datos_apertura['hora_inicio'])} \| — \| — \| "
        rf"{objetivo_escaped.replace(' ', r'[ ]')}.*?\|.*?\|)\n"
    )

    # Construcción simple: buscamos la línea que empiece con "| n |" y tenga "| — | — |"
    lineas = contenido.splitlines(keepends=True)
    nuevas_lineas = []
    reemplazado = False

    for linea in lineas:
        if (not reemplazado and
                linea.startswith(f"| {n} |") and
                "| — | — |" in linea):
            nueva_fila = (
                f"| {n} "
                f"| {datos_apertura['fecha']} "
                f"| {datos_apertura['hora_inicio']} "
                f"| {hora_fin_str} "
                f"| {duracion} "
                f"| {datos_apertura['entorno']} "
                f"| {datos_apertura['rama']} "
                f"| {datos_apertura['objetivo']} "
                f"| {observaciones} |\n"
            )
            nuevas_lineas.append(nueva_fila)
            reemplazado = True
        else:
            nuevas_lineas.append(linea)

    if reemplazado:
        with open(SESIONES_PATH, 'w', encoding='utf-8') as f:
            f.writelines(nuevas_lineas)
        print(f"  📝 docs/SESIONES.md actualizado.")
    else:
        print("  ⚠️  No se encontró la fila de apertura para completar. Verificá SESIONES.md.")

def limpiar_temp():
    """Elimina el archivo temporal de sesión activa."""
    if os.path.exists(TEMP_PATH):
        os.remove(TEMP_PATH)

# ── Main ────────────────────────────────────────────────────────────────────

def main():
    datos_apertura = leer_sesion_activa()

    if not datos_apertura:
        print()
        print("  ⚠️  No hay sesión activa registrada.")
        print("  Ejecutá primero: python scripts/utils/sesion_inicio.py")
        print()
        return

    hora_fin = datetime.now()
    observaciones, duracion = solicitar_observaciones(datos_apertura, hora_fin)
    cerrar_fila_sesion(datos_apertura, hora_fin.strftime('%H:%M'), duracion, observaciones)
    limpiar_temp()

if __name__ == '__main__':
    main()
