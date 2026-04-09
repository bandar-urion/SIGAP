# 📋 SESIONES — S.I.G.A.P. · Proyecto Fénix

> Bitácora de sesiones de trabajo. Generado automáticamente por `sesion_inicio.py` y `sesion_cierre.py`.
> Consultar `scripts/utils/` para los scripts de apertura y cierre.

| # | Fecha | Inicio | Fin | Duración | Entorno | Rama | Objetivo | Observaciones |
|---|-------|--------|-----|----------|---------|------|----------|---------------|
| 1 | — | — | — | — | — | — | Sesiones 1-5 (pre-implementación de bitácora) | Historial previo en CHANGELOG.md |
| 6 | 2026-03-10 | 22:20 | 22:38 | 18m | A — PC Casa (Windows) | feature/metodologia-sesiones | Implementar registro de sesiones + scripts de apertura/cierre | LF/CRLF warnings normales en Windows. Guardado manual en VSCode crítico pre-commit. |


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