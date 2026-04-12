# 🗺️ ROADMAP — S.I.G.A.P.
> **Proyecto Fénix** · Última actualización: 2026-04-10 · Versión actual: v0.8.1

Este documento es la fuente de verdad sobre el estado de desarrollo y la planificación futura.
Se actualiza al cierre de cada sesión de trabajo.

---

## ✅ HITOS COMPLETADOS

### [v0.1.0] — 2026-01-28 · Infraestructura Base
- Modelo relacional SQLite en 3NF. Tablas core: `movimientos`, `agenda_pagos`, `centros_costo`.
- Tablas paramétricas: `categorias`, `subcategorias`, `medios_pago`.
- Tablas de gobernanza: `reglas_catalogo`, `reglas_vinculos`.
- `factory_reset_normalized.py` para despliegue y sembrado de DB.
- Documentación fundacional: `DOCUMENTACION.md`, `ROADMAP.md`, `ADR-001`, `ADR-002`.

### [v0.1.1] — 2026-01-30 · Modelo de Datos
- Tabla `diccionario_terminos` para mapeo de sinónimos (base del Motor IA).
- Normalización de subcategorías. Soporte de billeteras virtuales y cuentas de terceros.

### [v0.4.0] — 2026-02-01 · Torre de Control (UX Flow State)
- Filosofía Flow State: edición continua sin perder el Dashboard.
- Smart Fit Dual, Accounting View, Matrix View.
- Motor IA: Pattern Mining + Auto-Promoción PENDIENTE → AUTO.
- Gobernanza Poka-Yoke: Anti-Inercia, validación de integridad, feedback auditivo.

### [v0.5.0] — 2026-02-01 · HyperFlux & Calidad
- Viewport Deslizante: navegación vectorial por flechas, sin paginado estático.
- HUD con métricas en tiempo real. Feedback semántico por etiquetas de estado.
- Smart Import: persistencia iterativa, Deep Match, Auto-Advance.
- Suite de tests unitarios inicial (`unittest`).

### [v0.6.4] — 2026-02-01 · Financiación Inteligente
- Regex financiero para detección de cuotas (`01/12`, `Cta 3`).
- Date Guard (Negative Lookahead) para no confundir fechas con cuotas.
- Smart Suggestion para servicios sin cuotas explícitas.

### [v0.6.5] — 2026-02-02 · Cross-Platform
- Soporte Linux/Termux: detección automática de OS.
- Wrappers `leer_byte()` y `beep_confirmacion()` cross-platform.
- Parser ANSI para flechas de dirección en terminales Unix/Linux.

### [v0.7.0] — 2026-03-05 · Refactor Semántico e Inbox
- Transición completa Transacciones → Movimientos (Domain-Driven Design).
- `inbox_movimientos.py` como único punto de entrada de datos.
- Estandarización de mocks en suite UI. Runner personalizado con docstrings.

### [v0.7.1] — 2026-03-13 · Deuda Técnica Fase 1
- Foreign Keys activas en runtime (`PRAGMA foreign_keys = ON`).
- `sigap_config.get_db_path()` corregido a ruta absoluta (fix "DB fantasma").
- `.gitignore` corregido. `__pycache__` sacados del tracking.
- Scripts huérfanos movidos a `_legacy/`. Suite: 66/66 OK.

### [v0.7.2] — 2026-03-14 · Seguridad & Migración de Repo
- Limpieza de historial Git: credenciales removidas de los 61 commits históricos.
- Decisión D-010 formalizada: "credenciales nunca en el repo".
- Migración de repo remoto: `ControlGastos` → `SIGAP` en GitHub.
- `git credential.helper store` configurado en Termux.

### [v0.8.0] — 2026-03-15 · Auditoría Completa & Robots de QA
- Flujo `auditoria_movimientos` completo: OK, SKIP_DUPLICADO, DESCARTADO_USUARIO.
- Campo `modulo` documenta el módulo origen del evento (no persona física). (Renombrado desde `usuario` en Sesión #19)
- `test_robots_gobernanza.py`: 5 robots de QA para el flujo de alta de subcategoría.
- Claude Code instalado en Entorno A. `CLAUDE.md` generado.
- Suite: 71/71 OK.

### [v0.8.1] — 2026-04-09 · Fix Rutas Legacy
- `factory_reset_normalized.py` y `factory_reset_preserve_learning.py`:
  ruta de DB hardcodeada a `control_gastos.db` corregida → `sigap_config.get_db_path()`.
- Conector GitHub de Claude.ai deshabilitado (reemplazado por Claude Code).

---

## 🚧 EN CURSO — feature/importar-movimiento

### Validación Atómica de Importación
Un movimiento se considera exitosamente importado solo si se cumplen los tres pasos:
- [ ] Guardado en DB (`movimientos`).
- [ ] Registrado en log técnico (`sigap_tecnico.log`).
- [ ] Registrado en `auditoria_movimientos` con antes/después.

> **Nota:** Los dos primeros pasos están implementados. Falta la validación que los trate como unidad atómica y revierta si alguno falla.

### CLI Unificado (expansión de `sigap.py`)
- [ ] Unificar comandos: `status`, `reset`, `test`, `import` bajo `sigap.py` como único punto de entrada.
- [ ] Reemplazar scripts dispersos por subcomandos del CLI.

---

## 📋 PRÓXIMOS HITOS (en orden de prioridad)

### [DOC] Documentación pendiente
- [x] Documentar convención del campo `modulo` en `auditoria_movimientos` — D-013 (Sesión #19).
- [x] Diagrama/mapa de la suite de tests → `docs/MAPA_TESTS.md` (Sesión #21)
- [ ] Revisión de `DOCUMENTACION.md` para sincronizar con estado real v0.8.1.

### [FEAT] Desacoplar Parser Santander
- [ ] Extraer `parsear_excel_santander()` como función aislada, testeable independientemente del flujo de importación completo.

### [FEAT] Módulo ABM de Catálogo
- [ ] Alta, Baja y Modificación standalone de: Centros de Costo, Categorías, Subcategorías, Medios de Pago.
- [ ] Actualmente solo se pueden gestionar vía `factory_reset` o acceso directo a DB.

### [FEAT] Parser MercadoPago
- [ ] Equivalente al parser Santander para extractos de MercadoPago.
- [ ] Referencia: `Comprobantes Tramites/MercadoPago Gastos.csv` y `MercadoPago Mastercard.csv`.

---

## 🔮 BACKLOG

### Gobernanza Futura
- [ ] **Integridad Histórica:** migrar `DELETE` físicos a `UPDATE activo=false`. Adaptar consultas SQL para filtrar por `activo=true`.
- [ ] **Soporte Multimoneda:** columna `cotizacion_ref` en `movimientos`. Consultas históricas de Dólar/UVA.
- [ ] **Gestión de Tarjetas Avanzada:** tabla `calendario_cierres`. Algoritmo de fecha de pago real.
- [ ] **Presupuestos:** tabla `presupuestos_mensuales`. Reporte de desvío de gastos.

### Reportes & Consultas
- [ ] Reporte: "Últimos N movimientos".
- [ ] Reporte: "Saldos por Centro de Costo".
- [ ] Reporte: "Alerta de Vencimientos (Agenda)".
- [ ] Backup: exportación automática a JSON/SQL.

### Interfaz (post-core)
- [ ] Dashboard web local (Streamlit o Flask). Solo cuando el core esté blindado.