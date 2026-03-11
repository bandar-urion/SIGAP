# 🦅 S.I.G.A.P. — CONTEXTO DE SESIÓN
> **Instrucciones de uso:** Al iniciar una sesión nueva con Claude, pegá este archivo completo.
> Al cerrar la sesión, pedile a Claude que genere el bloque `## ÚLTIMA SESIÓN` actualizado.
> **Importante:** indicar siempre en qué entorno se está trabajando hoy.
>
> **Nota operativa:** Para cambios de texto simples en el repo (buscar/reemplazar, eliminar
> palabras, renombrar strings), pedirle al copiloto el comando bash directo en lugar de
> generar archivos de output. Ejemplo: `sed -i 's/texto_viejo/texto_nuevo/g' archivo.md`

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

### 📱 Entorno B — Mobile
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
- `feature/importar-movimiento` — Parser + Inbox UI
- `feature/metodologia-sesiones` — pendiente merge desde Entorno A (ya pusheada a origin)

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
│       ├── auditar_db.py
│       ├── sesion_inicio.py          # Script de apertura de sesión
│       └── sesion_cierre.py          # Script de cierre de sesión
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
│   ├── GUIA_GIT.md
│   └── SESIONES.md                   # Bitácora de sesiones
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

> ✅ Sin bugs críticos conocidos al cierre de Sesión #7.
> Los bugs `tx → mov` (import_santander.py) y ruta DB (sigap.py) fueron
> resueltos en sesiones anteriores y verificados en código el 2026-03-10.

---

## PRÓXIMAS TAREAS (en orden de prioridad)

1. **[DOC]** Crear `DECISIONES.md` con primeras entradas retroactivas de decisiones clave
2. **[FEAT]** Agregar `FileHandler` al logging en `sigap_config.py`
3. **[FEAT]** Completar flujo de auditoría (`auditoria_movimientos`) en importación
4. **[FEAT]** Crear `manage.py` como CLI unificado
5. **[FEAT]** Robots de QA: `test_robot_crear_subcategoria_nueva` y `test_robot_rechazo_por_gobernanza`
6. **[FEAT]** Parser MercadoPago

---

## DECISIONES DE ARQUITECTURA INAMOVIBLES (NO DISCUTIR)

- **SQLite es la única DB.** No hay plans de migrar a Postgres/MySQL. (Ver ADR-001)
- **Sin GUI por ahora.** Terminal pura hasta que el core esté blindado.
- **Gobernanza antes que features.** No se agrega funcionalidad sin validaciones.
- **3NF estricta.** No se desnormalizan tablas por conveniencia.
- **`sigap_config.py` es el punto de entrada de configuración.** Nunca hardcodear rutas.
- **`leer_byte()` es el único lector de input.** Nunca usar `input()` estándar en flujos UI.

---

## ÚLTIMA SESIÓN

**Fecha:** 2026-03-11
**Sesión:** #7 — Metodología: Formalización del Estándar VibeCoding
**Entorno:** B (Samsung S21 Ultra · Termux)
**Branch:** `feature/metodologia-sesiones`

**Lo que hicimos:**
- Patrón D (Abogado del Diablo) aplicado sobre el VibeCoding: análisis de las críticas más fuertes al modelo Humano-IA en el contexto específico de SIGAP, con respuestas fundamentadas.
- Derivación de 6 Protocolos de Calidad a partir de las vulnerabilidades identificadas: Comentario de Intención, Paridad de Sesión, Definition of Done Financiero, Diario de Decisiones, Justificación de Complejidad, Arqueología Trimestral.
- `VIBE_CODING_SKILLS.md` reestructurado completo: Parte 1 (7 Patrones + 4 Avanzados) y Parte 2 (6 Protocolos nuevos). Apertura reformulada como estándar operativo.
- 10 ventajas del modelo Humano-IA vs. AloneCoding formalizadas: sección completa en `VIBE_CODING_SKILLS.md` y tabla comparativa en `README.md`.
- Corrección `Mobile Empresa` → `Mobile` en `Contexto.md`, `CONTEXTO__1_.md` y `README.md`.
- Nota operativa agregada al Contexto: para cambios simples de texto usar comando bash directo.

**Archivos modificados (listos para integrar al repo):**
- `VIBE_CODING_SKILLS.md` — reestructurado completo
- `README.md` — sección Humano-IA vs. AloneCoding agregada, "Empresa" eliminado
- `Contexto.md` — "Empresa" eliminado, nota operativa agregada, branch y tareas actualizadas
- `CONTEXTO__1_.md` — "Empresa" eliminado

**Pendientes antes del commit:**
- Crear `DECISIONES.md` (Protocolo 4 lo referencia, el archivo aún no existe)

**Próxima sesión (Entorno B · branch: feature/importar-movimiento):**
1. Commit de cierre sesión #7 en `feature/importar-movimiento`
2. `git fetch origin` + merge de `feature/metodologia-sesiones` sobre `feature/importar-movimiento`
3. Crear `DECISIONES.md` con primeras entradas retroactivas

---
*Actualizado por Claude Sonnet · Sesión #7 · Proyecto Fénix v0.7.0*
