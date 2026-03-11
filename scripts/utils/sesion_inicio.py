"""
sesion_inicio.py — S.I.G.A.P. · Proyecto Fénix
Registra el inicio de una sesión de trabajo en docs/SESIONES.md
Uso: python scripts/utils/sesion_inicio.py
"""

import os
import sys
import subprocess
from datetime import datetime

# ── Rutas ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SESIONES_PATH = os.path.join(BASE_DIR, 'docs', 'SESIONES.md')

# ── Detección automática ────────────────────────────────────────────────────

def detectar_entorno():
    """Detecta el entorno de ejecución por OS."""
    if os.name == 'nt':
        return 'A — PC Casa (Windows)'
    else:
        # Distingue Termux de Linux genérico
        if 'com.termux' in os.environ.get('PREFIX', '') or \
           'termux' in os.environ.get('HOME', '').lower():
            return 'B — Mobile Empresa (Termux)'
        return 'Linux'

def detectar_rama():
    """Lee la rama Git activa."""
    try:
        rama = subprocess.check_output(
            ['git', 'branch', '--show-current'],
            cwd=BASE_DIR,
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return rama if rama else 'desconocida'
    except Exception:
        return 'desconocida'

def obtener_numero_sesion():
    """Lee SESIONES.md y devuelve el número de la próxima sesión."""
    if not os.path.exists(SESIONES_PATH):
        return 1
    with open(SESIONES_PATH, 'r', encoding='utf-8') as f:
        contenido = f.read()
    # Contamos filas de datos (líneas que empiezan con | y tienen un número)
    sesiones = [l for l in contenido.splitlines()
                if l.startswith('|') and l.split('|')[1].strip().isdigit()]
    return len(sesiones) + 1

# ── Input del usuario ───────────────────────────────────────────────────────

def solicitar_objetivo():
    """Solicita el objetivo de la sesión al usuario."""
    print()
    print("=" * 60)
    print("  🦅 S.I.G.A.P. — APERTURA DE SESIÓN")
    print("=" * 60)
    print()

    entorno = detectar_entorno()
    rama = detectar_rama()
    timestamp = datetime.now()
    n_sesion = obtener_numero_sesion()

    print(f"  📅 Fecha/Hora : {timestamp.strftime('%Y-%m-%d %H:%M')}")
    print(f"  💻 Entorno    : {entorno}")
    print(f"  🌿 Rama       : {rama}")
    print(f"  #️⃣  Sesión     : #{n_sesion}")
    print()

    objetivo = input("  🎯 Objetivo de la sesión: ").strip()
    if not objetivo:
        objetivo = "(sin definir)"

    print()
    print("  ✅ Sesión iniciada. ¡Buena sesión, Martín!")
    print("=" * 60)
    print()

    return {
        'n_sesion': n_sesion,
        'fecha': timestamp.strftime('%Y-%m-%d'),
        'hora_inicio': timestamp.strftime('%H:%M'),
        'entorno': entorno,
        'rama': rama,
        'objetivo': objetivo,
    }

# ── Escritura en SESIONES.md ────────────────────────────────────────────────

def escribir_apertura(datos):
    """Crea o actualiza docs/SESIONES.md con la fila de apertura."""
    os.makedirs(os.path.dirname(SESIONES_PATH), exist_ok=True)

    # Si el archivo no existe, lo creamos con el encabezado
    if not os.path.exists(SESIONES_PATH):
        with open(SESIONES_PATH, 'w', encoding='utf-8') as f:
            f.write("# 📋 SESIONES — S.I.G.A.P. · Proyecto Fénix\n\n")
            f.write("> Bitácora de sesiones de trabajo. Generado automáticamente.\n\n")
            f.write("| # | Fecha | Inicio | Fin | Duración | Entorno | Rama | Objetivo | Observaciones |\n")
            f.write("|---|-------|--------|-----|----------|---------|------|----------|---------------|\n")

    # Fila de apertura con fin y duración pendientes
    fila = (
        f"| {datos['n_sesion']} "
        f"| {datos['fecha']} "
        f"| {datos['hora_inicio']} "
        f"| — "
        f"| — "
        f"| {datos['entorno']} "
        f"| {datos['rama']} "
        f"| {datos['objetivo']} "
        f"| — |\n"
    )

    with open(SESIONES_PATH, 'a', encoding='utf-8') as f:
        f.write(fila)

    # Guardamos datos de apertura en archivo temporal para que cierre los lea
    temp_path = os.path.join(BASE_DIR, '.sesion_activa')
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(f"n_sesion={datos['n_sesion']}\n")
        f.write(f"fecha={datos['fecha']}\n")
        f.write(f"hora_inicio={datos['hora_inicio']}\n")
        f.write(f"entorno={datos['entorno']}\n")
        f.write(f"rama={datos['rama']}\n")
        f.write(f"objetivo={datos['objetivo']}\n")

    print(f"  📝 Registrado en: docs/SESIONES.md")

# ── Main ────────────────────────────────────────────────────────────────────

def main():
    datos = solicitar_objetivo()
    escribir_apertura(datos)

if __name__ == '__main__':
    main()
