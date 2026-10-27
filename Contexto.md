# 🦅 S.I.G.A.P. — CONTEXTO DE SESIÓN
> **Instrucciones de uso:** Al iniciar una sesión nueva con Claude, pegá este archivo completo.
> Al cerrar la sesión, pedile a Claude que genere el bloque `## ÚLTIMA SESIÓN

**Fecha:** 2026-10-27
**Sesión:** #23 — Desacople del parser Santander + límites de Claude Code
**Entorno:** S21 (Termux · DeX · Claude Code)
**Branch:** `feature/importar-movimiento`

**Lo que hicimos:**
- Entorno S21 puesto a punto: Python 3.14, pytest instalado,
  `requirements.txt` ahora incluye pytest.
- `parsear_excel_santander()` desacoplada en `scripts/import_santander.py`:
  solo parseo, sin DB ni prints. 2 tests nuevos en `tests/test_import_santander.py`.
- `except: pass` en el alta de sinónimo reemplazado por captura de
  `sqlite3.IntegrityError` + warning. Cualquier otro error ahora se propaga.
- `CLAUDE.md`: sección "Límites de operación" (Claude Code no commitea,
  alcance acotado, suite en verde) y entornos renombrados a PC / S21.
- D-016 registrada. Versión v0.8.2.
- Termux:API instalado: `comando | termux-clipboard-set` pasa salidas al chat.

**Estado del repo al cierre:**
- Suite: 91/91 OK ✅
- 4 commits pusheados + commit de cierre

## PRÓXIMAS TAREAS (en orden de prioridad)

1. **[FEAT]** Expandir `sigap.py` como CLI unificado
2. **[FEAT]** Módulo ABM standalone de catálogo
3. **[FEAT]** Parser MercadoPago
4. **[DOC]** `Contexto.md`: renombrar Entorno A/B → PC/S21, actualizar lista
   de branches (solo quedan `main`, `desarrollo`, `feature/importar-movimiento`)
   y árbol de `tests/`.
