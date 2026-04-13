# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

S.I.G.A.P. (Sistema Inteligente de Gestión y Auditoría Patrimonial) — local personal finance platform. Python 3.12+ · SQLite · Terminal UI. No cloud services, no web framework. See `Contexto.md` for full session context including current bugs, priorities, and last session state.

## Commands

```bash
# Run all tests
python -m unittest discover tests

# Run a single test file (verbose)
python -m unittest tests.test_gobernanza_similitud -v

# System status
python sigap.py status

# Factory reset (interactive confirmation required)
python sigap.py reset

# Reset with fresh schema (drops and recreates all tables)
python scripts/factory_reset_normalized.py

# Import Santander Excel (place .xlsx in data/inbox/ first)
python scripts/import_santander.py

```

No build step. No linter configured.

## Architecture

**Entry points:**
- `sigap.py` — CLI orchestrator (argparse, `status`/`reset` commands)
- `sigap_config.py` — single source of truth for all paths, logging setup, reads `sigap.cfg`
- `scripts/modulos/inbox_movimientos.py` — core UI + business logic engine (600+ lines)

**Data flow for movement import:**
```
data/inbox/*.xlsx → import_santander.py (Pandas) → deduplication (num_referencia)
  → inbox_movimientos.py (HyperFlux viewport UI + governance panel)
  → SQLite INSERT → auditoria_movimientos table → file moved to data/processed/
```

**Cross-platform I/O:** `inbox_movimientos.py` detects `IS_WINDOWS` and switches between `msvcrt` (Windows) and `termios/tty` (Termux/Linux). The function `leer_byte()` is the only permitted input reader — never use standard `input()` in UI flows.

**Configuration:** All paths come from `sigap_config.py` reading `sigap.cfg`. Never hardcode paths.

**Database:** SQLite only (`data/sigap.db`). Schema defined in `scripts/factory_reset_normalized.py` (20+ tables, strict 3NF). Key tables: `movimientos`, `param_categorias`, `param_subcategorias`, `param_centros_costo`, `param_medios_pago`, `reglas_catalogo`, `auditoria_movimientos`, `diccionario_terminos`.

**ANSI/UI constants:** `scripts/utils/config_grafica.py` — viewport height, panel height, color codes.

## Immutable Architectural Constraints

- **SQLite only** — no Postgres/MySQL migration (see `docs/ADR-001-Motor-Base-Datos.md`)
- **Terminal UI only** — no GUI until core is hardened
- **`sigap_config.py` for all paths** — never hardcode
- **`leer_byte()` for all input** — never use `input()` in UI flows
- **Governance before features** — no functionality without validation rules
- **3NF strict** — no denormalization for convenience

## Git

Conventional Commits + Semantic Versioning. See `docs/GUIA_GIT.md`. Main branch is `main`; integration branch is `desarrollo`. Always verify current branch before committing (`git branch --show-current`).

## Dev Environments

| Env | Platform | Terminal | Path separator |
|-----|----------|----------|----------------|
| A (primary) | Windows 11 · VSCode | PowerShell/CMD | `\` |
| B (secondary) | Samsung S21 · Termux | Code-Server browser | `/` |

Cross-platform bugs are common — check `IS_WINDOWS` flag when debugging terminal I/O or path issues.

## Comportamiento Obligatorio del Agente

El agente activa estos comportamientos por iniciativa propia, sin que Martín los solicite:

| Momento                                | Acción obligatoria                                                                       |
| -------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Al iniciar cualquier tarea**         | Leer `Contexto.md` completo. Confirmar entorno + branch activa.                          |
| **Al detectar `input()` en flujos UI** | Señalar violación D-004 antes de continuar.                                              |
| **Al detectar rutas hardcodeadas**     | Señalar violación D-005 antes de continuar.                                              |
| **Al modificar lógica de negocio**     | Verificar si corresponde nueva entrada en `docs/DECISIONES.md`.                          |
| **Antes de cada commit**               | Ejecutar `python -m unittest discover tests`. Si falla → no commitear.                   |
| **Al cierre de sesión**                | Ejecutar el PROTOCOLO DE CIERRE DE SESIÓN de `Contexto.md` completo. Nunca omitir pasos. |