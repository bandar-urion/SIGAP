# 📋 SESIONES — S.I.G.A.P. · Proyecto Fénix

> Bitácora de sesiones de trabajo. Generado automáticamente por `sesion_inicio.py` y `sesion_cierre.py`.
> Consultar `scripts/utils/` para los scripts de apertura y cierre.

| # | Fecha | Inicio | Fin | Duración | Entorno | Rama | Objetivo | Observaciones |
|---|-------|--------|-----|----------|---------|------|----------|---------------|
| 1 | — | — | — | — | — | — | Sesiones 1-5 (pre-implementación de bitácora) | Historial previo en CHANGELOG.md |
| 6 | 2026-03-10 | 22:20 | 22:38 | 18m | A — PC Casa (Windows) | feature/metodologia-sesiones | Implementar registro de sesiones + scripts de apertura/cierre | LF/CRLF warnings normales en Windows. Guardado manual en VSCode crítico pre-commit. |

## Sesión #22 — 2026-04-12
**Entorno:** A (Windows 11 · VSCode)
**Branch:** `feature/importar-movimiento`
**Duración estimada:** 2 hs

### Trabajo realizado
- 4 archivos de tests generados vía Claude Code (89/89 OK):
  `test_factory_reset.py`, `test_auditar_db.py`, `test_sigap_cli.py`,
  `test_factory_reset_preserve.py` — cierra gaps identificados en Sesión #21.
- Fix `.gitignore`: `*.db/` → `*.db` — sigap.db no estaba siendo ignorada.
- Diagnóstico diferencial documentado en test y mensaje de fallo de
  `test_ciclo_completo_sin_perdida` (seeding vs. bug real).
- D-014 y D-015 agregadas a `DECISIONES.md`.
- `sesion_inicio/cierre.py` → `_legacy/` (métricas de reloj descartadas).

### Estado al cierre
- Suite: 89/89 OK ✅
- 2 commits pusheados

## Sesión #21 — 2026-04-12
**Entorno:** A (Windows 11 · VSCode)
**Branch:** `feature/importar-movimiento`
**Duración estimada:** 0.5 hs

### Trabajo realizado
- `docs/MAPA_TESTS.md` generado por Claude Code: mapa completo de la suite
  (10 archivos, 71 tests, descripción por método, tabla resumen).
- Gaps de cobertura identificados: `sigap.py` (0 tests), `factory_reset_normalized.py`
  (1 test mínimo, sin regresión para fix de rutas de Sesión #16),
  `auditar_db.py` (0 tests).

### Estado al cierre
- Suite: 71/71 OK ✅
- Sin cambios de código

## Sesión #18 — 2026-04-10
**Entorno:** A (Windows 11 · VSCode)
**Branch:** `feature/importar-movimiento`
**Duración estimada:** 1.5 hs

### Trabajo realizado
- Fix de protocolo de cierre: nuevo paso 1 para ejecutar tareas pendientes antes
  de generar bloques de cierre. Soluciona el problema recurrente de estado
  desincronizado en `Contexto.md`.
- Auditoría y corrección del árbol de estructura del proyecto en `Contexto.md`.
- Decisión: `sigap.py` como CLI unificado (descartado `manage.py` por ser
  convención exclusiva de Django).
- `ROADMAP.md` reescrito estructuralmente: sincronizado con v0.8.1, estructura
  limpia en cuatro secciones, sin deuda documental.

### Estado al cierre
- Suite: 71/71 OK ✅
- Sin bugs introducidos

## Sesión #17 — 2026-04-09

**Entorno:** A (Windows 11 · VSCode · Claude Code)
**Branch:** `feature/importar-movimiento`
**Tipo:** Auditoría de integridad + Fix de bugs + Auditoría de cobertura

### Resumen
Auditoría completa post-Sesión #16. Baseline 71/71 OK confirmado.
Detectados y corregidos dos bugs críticos. Suite post-fix: 71/71 OK.
Primera ejecución de auditoría de cobertura trimestral (Protocolo 6).

### Cambios realizados
- **FIX CRÍTICO (D-004):** `input()` en `inbox_movimientos.py:789`
  reemplazado por `leer_linea_inline()`.
- **FIX CRÍTICO (D-005):** `auditar_db.py` migrado a
  `sigap_config.get_db_path()`.
- **D-012** agregada a `docs/DECISIONES.md`.
- `Contexto.md`: `manage.py` → `sigap.py` + versión v0.8.1.
- Comentario de excepción arquitectónica en `sesion_inicio/cierre.py`.
- **Anexo — Cobertura:** `inbox_movimientos.py` 68%, `sigap_config.py`
  90%, `import_santander.py` 0%, `auditar_db.py` 0%. Gaps documentados
  en `TODO.md`. Protocolo 6 de VIBE_CODING_SKILLS.md actualizado.

### Estado al cierre
- Suite: 71/71 OK ✅
- Commit: pendiente

---

### Sesión #12 — 2026-03-16
**Entorno:** B (Termux · Code-Server)
**Duración estimada:** ~2hs
**Foco:** Infraestructura — Pipeline de sincronización automática repo → Google Drive

**Resumen:**
Configuración completa de rclone en Termux con autenticación OAuth. Implementación de hook
`post-commit` para sync automático del repo a `gdrive:SIGAP` tras cada commit. Verificación
exitosa desde terminal y Code-Server. Activación del conector Drive en Claude.ai para acceso
automático al código fuente del proyecto. Reset de branch por divergencia con origin.

**Pendiente para próxima sesión:**
- Hook equivalente en Entorno A (Windows).
- Retomar refactor-modular.

---

### Sesión #13 — 2026-03-16

**Entorno:** A (Windows 11 · VSCode)
**Foco:** Infraestructura — hook post-commit Drive en Windows

**Resumen:**
Configuración del hook post-commit en Entorno A usando robocopy con flags //
para compatibilidad Git Bash/Windows. Pipeline sync completo y operativo en
ambos entornos. Protocolo de cierre de sesión formalizado en Contexto.md.

---

## Sesión #16 — 2026-04-09 — Entorno A

**Branch:** `feature/importar-movimiento`

**Resumen:**
Sesión de higiene y corrección de bug crítico. Auditoría de archivos obsoletos
identificó el Showstopper: ambos `factory_reset_*.py` tenían la ruta de DB
hardcodeada al nombre legacy `control_gastos.db`. Corregidos para usar
`sigap_config.get_db_path()`. Se deshabilitó el Conector GitHub de Claude.ai
por ser redundante con Claude Code.

**Cambios:**
- Fix: `scripts/factory_reset_normalized.py` — ruta DB vía sigap_config
- Fix: `scripts/factory_reset_preserve_learning.py` — ruta DB vía sigap_config
- Infra: Conector GitHub de Claude.ai deshabilitado
- Pendiente borrado: `scripts/migration_v0_6_1_reglas_gas.py`
- Pendiente limpieza: `__pycache__` en todo el árbol