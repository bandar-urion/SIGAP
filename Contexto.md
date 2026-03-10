# 🦅 S.I.G.A.P. — CONTEXTO DE SESIÓN
> **Instrucciones de uso:** Al iniciar una sesión nueva con Claude, pegá este archivo completo.
> Al cerrar la sesión, pedile a Claude que genere el bloque `## ÚLTIMA SESIÓN` actualizado.
> **Importante:** indicar siempre en qué entorno se está trabajando hoy.

---

## QUIÉN SOY Y QUÉ ESTAMOS HACIENDO

Soy **Martín**, analista de sistemas en proceso de reactivación técnica.
Este proyecto es el **"Proyecto Fénix"**: un programa personal de actualización donde el producto
(S.I.G.A.P.) es el vehículo de aprendizaje.

**Stack:** Python 3.12+ · SQLite · Git

---

## ENTORNOS DE DESARROLLO

> Al iniciar sesión, indicar cuál se está usando. Impacta en diagnóstico de bugs de paths/terminal.

### 🖥️ Entorno A — PC Casa
- **Hardware:** Windows 11 25H2 · Intel Core i9-10900KF · 80 GB RAM
- **IDE:** VSCode
- **Terminal:** PowerShell / CMD
- **Particularidades:** Rutas con `\`, sin limitaciones de memoria, pantalla grande.

### 📱 Entorno B — Mobile Empresa
- **Hardware:** Samsung Galaxy S21 Ultra · USB Hub · KVM Switch · HDMI
- **IDE:** Code-Server (VSCode en browser)
- **Terminal:** Termux (Linux/Android)
- **Particularidades:** Rutas con `/`, terminal raw mode vía `tty`/`termios`,
  ancho de pantalla variable, sin `winsound`, sin `msvcrt`.

---

## GIT

**Branch activa:** `feature/importar-movimiento`

**Branches conocidas:**
- `main` — producción estable
- `desarrollo` — integración
- `feature/importar-movimiento` — rama actual, Parser + Inbox UI

> Recordatorio: antes de cada commit verificar que estamos en la branch correcta.
> `git branch --show-current`

---

## QUÉ ES S.I.G.A.P.

**Sistema Inteligente de Gestión y Auditoría Patrimonial.**
Plataforma de finanzas personales local (sin nube). Procesa extractos bancarios (Excel),
los categoriza con un motor de IA propio (diccionario + regex), y los almacena en SQLite.

**Filosofía clave:**
- **Soberanía del dato:** todo local, nada en la nube.
- **Gobernanza estricta:** el sistema previene errores humanos (Poka-Yoke).
- **Flow State UX:** interfaz de terminal con viewport deslizante, HyperFlux, sin menús.
- **Sinergia Humano-IA:** Martín pone la lógica de negocio, Claude es el copiloto técnico.

---

## ESTRUCTURA DEL PROYECTO

```
ControlGastos/
├── sigap.py                          # Orquestador CLI (status / reset)
├── sigap_config.py                   # Config centralizada (lee sigap.cfg)
├── sigap.cfg                         # Parámetros: DB, rutas, UI, LOG_LEVEL
├── Contexto.md                       # ← Este archivo (guía de sesión IA)
├── data/
│   ├── sigap.db                      # Base de datos SQLite (fuente de verdad)
│   ├── inbox/                        # Excel bancarios a procesar
│   ├── processed/                    # Excel ya importados
│   └── rejected/                     # Excel rechazados por validación
├── scripts/
│   ├── import_santander.py           # Parser Excel Santander → Inbox UI
│   ├── factory_reset_normalized.py   # Reset + sembrado de DB
│   ├── factory_reset_preserve_learning.py
│   ├── modulos/
│   │   └── inbox_movimientos.py      # ⭐ Motor principal (UI + lógica de negocio)
│   └── utils/
│       ├── config_grafica.py         # Constantes ANSI, colores, dimensiones UI
│       └── auditar_db.py
├── tests/
│   ├── test_cerebro.py               # Motor IA (regex + matching)
│   ├── test_importacion.py           # Integridad DB + deduplicación
│   ├── test_database_init.py         # Esquema SQL
│   ├── test_avanzado.py              # Casos extremos / tortura
│   ├── test_gobernanza_similitud.py  # ⭐ Motor de Gobernanza (25 tests)
│   └── test_ui_inbox_movimientos.py  # UI mocks
├── docs/
│   ├── ADR-001-Motor-Base-Datos.md
│   ├── ADR-002-Modelo-Gobernanza.md
│   └── GUIA_GIT.md
└── logs/
    └── sigap_tecnico.log             # Log técnico rotativo
```

---

## VERSIÓN ACTUAL: v0.7.0

| Módulo | Estado |
|---|---|
| Parser Santander (XLS → Inbox) | ✅ Funcional |
| Inbox UI (viewport, navegación, edición) | ✅ Funcional |
| Motor IA (diccionario + regex) | ✅ Funcional |
| Detección de cuotas (regex financiero) | ✅ Funcional |
| Cross-platform Termux/Windows | ✅ Funcional |
| Gobernanza Alta Subcategoría (Panel + 6 criterios) | ✅ Funcional |
| Sistema de logging (consola) | ⚠️ Parcial (falta FileHandler) |
| Auditoría en DB (`auditoria_movimientos`) | ⚠️ Parcial |
| `manage.py` unificado | ❌ Pendiente |
| Parser MercadoPago | ❌ Pendiente |
| Dashboard Streamlit | 🔮 Backlog |

---

## BUGS CONOCIDOS (PENDIENTES DE FIX)

### 🐛 BUG CRÍTICO — `import_santander.py` ~línea 95
```python
# INCORRECTO (rompe con NameError al grabar):
elif tx.estado == 'PENDIENTE':
elif tx.estado == 'DESCARTADO':

# CORRECTO (la variable del loop se llama 'mov'):
elif mov.estado == 'PENDIENTE':
elif mov.estado == 'DESCARTADO':
```

### ⚠️ INCONSISTENCIA — `sigap.py` línea 6
`DB_FILE = 'control_gastos.db'` apunta a DB incorrecta.
La DB real es `data/sigap.db` vía `sigap_config.get_db_path()`.
`sigap.py` debe usar `sigap_config` para obtener la ruta.

---

## PRÓXIMAS TAREAS (en orden de prioridad)

1. **[FIX]** Corregir bug `tx` → `mov` en `import_santander.py` ← CRÍTICO
2. **[FIX]** Corregir ruta DB en `sigap.py`
3. **[FEAT]** Agregar `FileHandler` al logging en `sigap_config.py`
4. **[FEAT]** Completar flujo de auditoría (`auditoria_movimientos`) en importación
5. **[FEAT]** Crear `manage.py` como CLI unificado

---

## DECISIONES DE ARQUITECTURA INAMOVIBLES (NO DISCUTIR)

- **SQLite es la única DB.** No hay plans de migrar a Postgres/MySQL. (Ver ADR-001)
- **Sin GUI por ahora.** Terminal pura hasta que el core esté blindado.
- **Gobernanza antes que features.** No se agrega funcionalidad sin validaciones.
- **3NF estricta.** No se desnormalizan tablas por conveniencia.
- **`sigap_config.py` es el punto de entrada de configuración.** Nunca hardcodear rutas.
- **leer_byte() es el único lector de input.** Nunca usar input() estándar en flujos UI.

---

## ÚLTIMA SESIÓN

**Fecha:** 2026-03-09
**Sesión:** #5 — Hardening de Seguridad y Limpieza del Repositorio
**Entorno:** Entorno A (PC Casa · Windows 11 · PowerShell)
**Branch:** `feature/importar-movimiento`

**Lo que hicimos:**
- Fixes críticos del backlog (realizados en Entorno B a la mañana):
  - `fix(importador)`: corregido NameError `tx→mov` en `import_santander.py`
  - `fix(core)`: corregida ruta DB en `sigap.py` para usar `sigap_config`
- Análisis completo del repositorio (zip) para identificar archivos a eliminar.
- Identificación de `credenciales.json` con Service Account Key de Google Cloud expuesta.
- Revocación de la key en Google Cloud Console (proyecto `gastos-python-485019`).
- Limpieza del historial Git completo con `git filter-repo` (35 commits reescritos).
- Force push a las 3 branches en GitHub (`desarrollo`, `feature/importar-movimiento`, `refactor-modular`).
- Eliminación de `scripts/_legacy/` (9 archivos de la era pre-SIGAP).
- Actualización y reestructuración del `.gitignore` con protección de credenciales, caché Python y datos externos.
- Reestablecimiento del tracking remoto post-filter-repo (`--set-upstream`).

**Archivos modificados:**
- `scripts/import_santander.py` — fix `tx→mov`
- `sigap.py` — fix ruta DB
- `.gitignore` — expandido y reestructurado
- Eliminados: `scripts/_legacy/` (completo), scripts de migración y parche one-shot

**Pendientes identificados (no atacados esta sesión):**
- `sigap.db` duplicada en raíz del proyecto (verificar si es residuo)
- `docs/Gemini.md` y `docs/Gemini_Config.md` (evaluar si tienen valor de referencia)
- `tests/test_gui_logic.py` y `tests/test_sigap_core.py` (verificar cobertura antes de borrar)

**Próxima sesión sugerida:**
Revisión y actualización de toda la documentación: `CHANGELOG.md` (agregar entradas
de fixes v0.7.x y hardening de seguridad), `README.md`, `ROADMAP.md`, `TODO.md`,
`DOCUMENTACION.md` y este `Contexto.md`. Sesión dedicada a dejar la documentación
en sincronía con el estado real del proyecto.

---
*Actualizado por Claude Sonnet · Sesión #5 · Proyecto Fénix v0.7.0*
