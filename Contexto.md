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
SIGAP/
├── sigap.py                          # Orquestador CLI (status / reset)
├── sigap_config.py                   # Config centralizada (lee sigap.cfg)
├── sigap.cfg                         # Parámetros: DB, rutas, UI, LOG_LEVEL
├── CLAUDE.md                         # Configuración para Claude Code
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
│   ├── test_gobernanza_similitud.py  # Motor de Gobernanza (25 tests)
│   ├── test_ui_inbox_movimientos.py  # UI mocks
│   └── test_robots_gobernanza.py     # ⭐ Robots de QA (5 robots)
├── docs/
│   ├── ADR-001-Motor-Base-Datos.md
│   ├── ADR-002-Modelo-Gobernanza.md
│   ├── GUIA_GIT.md
│   ├── DECISIONES.md                 # Decisiones arquitectónicas (D-001 a D-010)
│   ├── SESIONES.md                   # Bitácora de sesiones
│   └── VIBE_CODING_SKILLS.md
└── logs/
    └── sigap_tecnico.log             # Log técnico rotativo
```

---

## VERSIÓN ACTUAL: v0.8.0

| Módulo | Estado |
|---|---|
| Parser Santander (XLS → Inbox) | ✅ Funcional |
| Inbox UI (viewport, navegación, edición) | ✅ Funcional |
| Motor IA (diccionario + regex) | ✅ Funcional |
| Detección de cuotas (regex financiero) | ✅ Funcional |
| Cross-platform Termux/Windows | ✅ Funcional |
| Gobernanza Alta Subcategoría (Panel + 6 criterios) | ✅ Funcional |
| Sistema de logging (consola + archivo) | ✅ Funcional |
| Auditoría en DB (`auditoria_movimientos`) | ✅ Funcional |
| `manage.py` unificado | ❌ Pendiente |
| Parser MercadoPago | ❌ Pendiente |
| Dashboard Streamlit | 🔮 Backlog |

---

## BUGS CONOCIDOS (PENDIENTES DE FIX)

> ✅ Sin bugs críticos conocidos al cierre de Sesión #10.

---

## DECISIONES DE ARQUITECTURA INAMOVIBLES (NO DISCUTIR)

- **SQLite es la única DB.** No hay plans de migrar a Postgres/MySQL. (Ver ADR-001)
- **Sin GUI por ahora.** Terminal pura hasta que el core esté blindado.
- **Gobernanza antes que features.** No se agrega funcionalidad sin validaciones.
- **3NF estricta.** No se desnormalizan tablas por conveniencia.
- **`sigap_config.py` es el punto de entrada de configuración.** Nunca hardcodear rutas.
- **`leer_byte()` es el único lector de input.** Nunca usar `input()` estándar en flujos UI.

---

## PROTOCOLO DE CIERRE DE SESIÓN

> Ejecutar en orden al finalizar cada sesión de trabajo.

### 1. Revisión documental (copiloto)
El copiloto revisa el trabajo de la sesión y determina qué documentos requieren actualización:

| Documento          | Actualizar cuando...                                       |
| ------------------ | ---------------------------------------------------------- |
| `Contexto.md`      | **Siempre** — bloque ÚLTIMA SESIÓN + PRÓXIMAS TAREAS       |
| `docs/SESIONES.md` | **Siempre** — entrada de la sesión                         |
| `CHANGELOG.md`     | Se agregó feature, fix o cambio de versión                 |
| `DOCUMENTACION.md` | Cambió arquitectura, esquema DB o comportamiento de módulo |
| `ROADMAP.md`       | Se completó un hito o cambió la planificación              |
| `TODO.md`          | Se completaron o agregaron tareas                          |
| `CLAUDE.md`        | Cambió configuración relevante para Claude Code            |

### 2. Generación de bloques de cierre
El copiloto genera el texto actualizado para cada documento que corresponda.

### 3. Commit de cierre
Mensaje estándar:
```
docs: cierre Sesión #NN — <resumen de una línea>
```

### 4. Verificar sync a Drive
Confirmar que el hook `post-commit` disparó correctamente en el entorno activo.

---

## ÚLTIMA SESIÓN

**Fecha:** 2026-03-17
**Sesión:** #12, #13 y #14 — Pipeline Drive + Conector GitHub + Baja hooks
**Entornos:** B → A → B
**Branch:** `feature/importar-movimiento`

**Lo que hicimos:**
- Instalación y configuración de `rclone` en Termux con autenticación OAuth a Google Drive.
- Creación de carpeta `gdrive:SIGAP` como espejo del repo en Drive.
- Hook `post-commit` en Entorno B y A: creados y luego dados de baja.
- Skill `sigap` creada y empaquetada como `sigap.skill` (209 líneas).
- Conector GitHub habilitado en Claude para el proyecto SIGAP.
- Hook GDrive dado de baja en Entorno A y Entorno B. ✅
- `refactor-modular` diagnosticada: branch sucia, solo referencia de diseño.
- Confirmado: repo local limpio. Carpetas `.git (1)/.git (2)` en GitHub son artefacto visual.
- Protocolo de cierre de sesión formalizado.

**Estado del repo al cierre:**
- Suite: 71/71 OK ✅
- Hook GDrive eliminado en ambos entornos ✅
- Conector GitHub activo e indexando ✅

## PRÓXIMAS TAREAS (en orden de prioridad)

1. **[INFRA]** Verificar indexación GitHub en Claude.ai al inicio de próxima sesión.
2. **[REFACTOR]** Retomar `refactor-modular`: descomposición atómica de módulos .py por función.
3. **[DOC]** Revisión estructural completa de `ROADMAP.md`.
4. **[DOC]** Documentar convención del campo `usuario` en `auditoria_movimientos`.
5. **[FEAT]** Desacoplar `parsear_excel_santander()` como función aislada.
6. **[FEAT]** Expandir `sigap.py` como CLI unificado.
7. **[FEAT]** Módulo ABM standalone de catálogo.
8. **[FEAT]** Parser MercadoPago.
9. **[DOC]** Diagrama/mapa de la suite de tests.

---
*Actualizado por Claude Sonnet · Sesión #14 · Proyecto Fénix v0.8.0*