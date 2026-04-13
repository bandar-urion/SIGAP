# 🦅 S.I.G.A.P. — CONTEXTO DE SESIÓN
> **Instrucciones de uso:** Al iniciar una sesión nueva con Claude, pegá este archivo completo.
> Al cerrar la sesión, pedile a Claude que genere el bloque `## ÚLTIMA SESIÓN` actualizado.
> **Importante:** indicar siempre en qué entorno se está trabajando hoy.
>
> **Nota operativa:** Para cambios de texto simples en el repo (buscar/reemplazar, eliminar
> palabras, renombrar strings), pedirle al copiloto el comando bash directo en lugar de
> generar archivos de output. Ejemplo: `sed -i 's/texto_viejo/texto_nuevo/g' archivo.md`

---

## ⚡ COMPORTAMIENTO OBLIGATORIO DEL COPILOTO

> Estos triggers se activan **sin que Martín los solicite**.
> El copiloto los ejecuta por iniciativa propia en los momentos indicados.

| Momento                                                               | Acción obligatoria                                                      |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Al iniciar sesión**                                                 | Confirmar entorno (A/B) + verificar branch + leer BUGS CONOCIDOS        |
| **Cuando Martín dice** "cerramos", "hagamos cierre", "commit",        | Activar PROTOCOLO DE CIERRE DE SESIÓN completo sin esperar que lo pida  |
| "terminamos"                                                          |                                                                         |
| **Cuando hay un fix de código**                                       | Verificar si corresponde nueva entrada en `docs/DECISIONES.md`          |
| **Cuando hay una decisión arquitectónica nueva**                      | Proponer D-XXX antes de continuar                                       |
| **Al detectar cualquier inconsistencia** entre código y documentación | Señalarla antes de continuar con la tarea principal                     |
| **Cada tres meses**                                                   | Recordar que corresponde Sesión de Arqueología Trimestral (Protocolo 6) |

---
## DIVISIÓN DE ROLES: ESTE CHAT vs CLAUDE CODE

| Tarea                                                 | Dónde         |
| ----------------------------------------------------- | ------------- |
| Conceptualización, diseño, decisiones de arquitectura | ✅ Este chat   |
| Redacción de D-XXX, protocolos, documentación         | ✅ Este chat   |
| Revisión y validación del output de Claude Code       | ✅ Este chat   |
| Refactors, cambios en código fuente                   | 🤖 Claude Code |
| Análisis de impacto sobre el repo completo            | 🤖 Claude Code |
| Generación de archivos, scripts, migraciones          | 🤖 Claude Code |
| Ejecución de tests                                    | 🤖 Claude Code |

**Criterio de derivación:** si la tarea requiere acceso al repo completo
para hacerse correctamente → Claude Code.
Si solo requiere razonamiento, diseño o revisión → este chat.

> El copiloto debe señalar activamente cuando una tarea deriva a Claude Code,
> en lugar de intentar resolverla parcialmente aquí.
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

- `refactor-modular` — branch sucia del refactor anterior (otro LLM).
  No hacer merge. Usar solo como referencia de diseño modular.

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
├── .gitignore
├── sigap.py                          # Orquestador CLI (status / reset)
├── sigap_config.py                   # Config centralizada (lee sigap.cfg)
├── sigap.cfg                         # Parámetros: DB, rutas, UI, LOG_LEVEL
├── CLAUDE.md                         # Configuración para Claude Code
├── CHANGELOG.md                      # Historial de versiones
├── DOCUMENTACION.md                  # Documentación técnica del sistema
├── README.md                         # Documentación pública del proyecto
├── TODO.md                           # Tareas pendientes
├── Contexto.md                       # ← Este archivo (guía de sesión IA)
├── ROADMAP.md                        # Planificación y estado de features
├── Comprobantes Tramites/            # Extractos bancarios de referencia
│   ├── MercadoPago Gastos.csv
│   ├── MercadoPago Mastercard.csv
│   ├── Santander Gastos.csv
│   ├── Santander Visa.csv
│   └── Tablero Control.csv
├── data/
│   ├── sigap.db                      # Base de datos SQLite (fuente de verdad)
│   ├── inbox/                        # Excel bancarios a procesar
│   └── processed/                    # Excel ya importados
├── docs/
│   ├── ADR-001-Motor-Base-Datos.md
│   ├── ADR-002-Modelo-Gobernanza.md
│   ├── DECISIONES.md                 # Decisiones arquitectónicas (D-001 a D-013)
│   ├── GUIA_GIT.md
│   ├── QA_UI_Checklist_inbox_movimientos.md
│   ├── SESIONES.md                   # Bitácora de sesiones
│   └── VIBE_CODING_SKILLS.md
├── logs/
│   └── sigap_tecnico.log             # Log técnico rotativo
├── scripts/
│   ├── factory_reset_normalized.py   # Reset + sembrado de DB
│   ├── factory_reset_preserve_learning.py
│   ├── import_santander.py           # Parser XLS Santander → Inbox UI
│   ├── modulos/
│   │   └── inbox_movimientos.py      # ⭐ Motor principal (UI + lógica de negocio)
│   ├── utils/
│   │   ├── auditar_db.py
│   │   └── config_grafica.py         # Constantes ANSI, colores, dimensiones UI
│   └── _legacy/                      # Scripts anteriores a v0.8.0 (solo referencia)
        ├── sesion_inicio.py          # Descartado Sesión #22 (D-015)
        └── sesion_cierre.py          # Descartado Sesión #22 (D-015)
└── tests/
    ├── test_aislamiento_cuotas.py    # Aislamiento lógica de cuotas
    ├── test_config.py                # Configuración centralizada
    ├── test_contrato_santander.py    # Contrato formato Excel Santander
    ├── test_database_init.py         # Esquema SQL
    ├── test_gobernanza_similitud.py  # Motor de Gobernanza (25 tests)
    ├── test_gui_logic.py             # Lógica UI (mocks)
    ├── test_importacion.py           # Integridad DB + deduplicación
    ├── test_motor_clasificacion.py   # Motor IA
    ├── test_robots_gobernanza.py     # ⭐ Robots de QA (5 robots)
    └── test_ui_inbox_movimientos.py  # UI mocks
```

---

## VERSIÓN ACTUAL: v0.8.1

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
| `sigap.py` como CLI unificado | ❌ Pendiente |
| Parser MercadoPago | ❌ Pendiente |
| Dashboard Streamlit | 🔮 Backlog |

---

## BUGS CONOCIDOS (PENDIENTES DE FIX)

> ✅ Sin bugs críticos conocidos al cierre de Sesión #16.

---

## DECISIONES DE ARQUITECTURA INAMOVIBLES (NO DISCUTIR)

- **SQLite es la única DB.** No hay plans de migrar a Postgres/MySQL. (Ver ADR-001)
- **Sin GUI por ahora.** Terminal pura hasta que el core esté blindado.
- **Gobernanza antes que features.** No se agrega funcionalidad sin validaciones.
- **3NF estricta.** No se desnormalizan tablas por conveniencia.
- **`sigap_config.py` es el punto de entrada de configuración.** Nunca hardcodear rutas.
- **`leer_byte()` es el único lector de input.** Nunca usar `input()` estándar en flujos UI.

---

## PROTOCOLO DE INICIO DE SESIÓN

> Ejecutar en orden al comenzar cada sesión de trabajo.

### 1. Actualizar Archivos de Memoria del Proyecto en Claude.ai
Reemplazar con las últimas versiones commiteadas del repo local:

| Archivo              | Por qué                                                                   |
| -------------------- | ------------------------------------------------------------------------- |
| `Contexto.md`        | Estado del proyecto, entornos, arquitectura, tareas                       |
| `SESIONES.md`        | Número de sesión correcto (fuente de verdad)                              |
| `docs/DECISIONES.md` | Historial de decisiones para no repetir ni contradecir                    |
| `ROADMAP.md`         | Estado real de features: qué está hecho, qué no                           |
| `CLAUDE.md`          | Verificar consistencia con `Contexto.md` si hubo                          |
|                      | cambios estructurales (arquitectura, entornos, constraints). Claude Code  |
|                      | lo lee automáticamente — no se adjunta aquí.                              |
| `TODO.md`            | Backlog táctico: verificar prioridades y registrar descubrimientos nuevos |

> **Tip:** actualizar la Memoria de Claude *después* de commitear,
> no antes. La fuente de verdad es siempre Git.

> **Nota `CLAUDE.md`:** leído automáticamente por Claude Code al abrir el repo. No requiere
> acción en este chat. Solo actualizar si cambió arquitectura, comandos clave o constraints.
> El estado de sesión vive en `Contexto.md`, no aquí.

> **Advertencia sobre `/mnt/project`:** el snapshot montado en el entorno del copiloto
> puede estar desactualizado o ser parcial. **No es fuente de verdad.**
> Cualquier dato sobre el estado actual del repo (estructura, contenido de archivos,
> resultado de tests, logs) debe provenir de Martin o ClaudeCode: ejecutar el comando correspondiente
> y pegar la salida, o adjuntar el archivo directamente en el chat.

### 2. Adjuntar archivos en el primer mensaje del chat
Para garantizar que el copiloto pueda leerlos con herramientas,
adjuntar en el primer mensaje:
`Contexto.md` · `SESIONES.md` · `ROADMAP.md` · `docs/DECISIONES.md` . `CLAUDE.md`

### 3. Informar al copiloto al abrir el chat
En el primer mensaje indicar siempre:
Sesión #NN — Entorno A|B — Branch: nombre-de-la-branch

### 4. El copiloto confirma al iniciar
Sin que Martín lo pida, el copiloto debe:
1. Leer `Contexto.md`, `SESIONES.md`, `ROADMAP.md` y `docs/DECISIONES.md`.
2. Confirmar entorno y branch activa.
3. Revisar `BUGS CONOCIDOS` en este archivo.
4. Listar `PRÓXIMAS TAREAS` y preguntar por dónde arrancamos.

---
## PROTOCOLO DE CIERRE DE SESIÓN

> Ejecutar en orden al finalizar cada sesión de trabajo.

### 1. Ejecutar tareas pendientes (Martín)
Antes de generar ningún bloque de cierre, ejecutar todas las tareas pendientes del repo
(borrados, limpiezas, commits intermedios). El Contexto.md se commitea **último**.

### 2. Revisión documental (copiloto)
El copiloto revisa el trabajo de la sesión y determina qué documentos requieren actualización:

### 3. Generación de bloques de cierre
El copiloto genera el texto actualizado para cada documento que corresponda.

### 4. Commit de cierre
Mensaje estándar:
```
docs: cierre Sesión #NN — <resumen de una línea>
```

### 5. Verificar push a GitHub
Confirmar que el push al remoto fue exitoso:
```
git push origin feature/importar-movimiento
```

---

## ÚLTIMA SESIÓN

**Fecha:** 2026-04-12
**Sesión:** #22 — Cobertura de tests + higiene de scripts
**Entorno:** A (Windows 11 · VSCode)
**Branch:** `feature/importar-movimiento`

**Lo que hicimos:**
- Generados 4 archivos de tests nuevos (18 tests): `test_factory_reset.py`,
  `test_auditar_db.py`, `test_sigap_cli.py`, `test_factory_reset_preserve.py`.
- Fix `.gitignore`: `*.db/` → `*.db` (sigap.db no estaba siendo ignorada).
- `test_factory_reset_preserve.py`: docstring + mensaje de fallo con diagnóstico
  diferencial para detectar pérdida silenciosa vs. cambio de seeding.
- D-014 documentada: `DB_FILE` se resuelve en tiempo de importación — doble
  mock necesario en tests de Windows.
- `sesion_inicio.py` y `sesion_cierre.py` movidos a `_legacy/` (D-015):
  métricas de tiempo de reloj descartadas por no reflejar trabajo real.
- `CLAUDE.md` y `docs/DECISIONES.md` actualizados.

**Estado del repo al cierre:**
- Suite: 89/89 OK ✅
- 2 commits pusheados a `feature/importar-movimiento`

## PRÓXIMAS TAREAS (en orden de prioridad)

1. **[TEST]** Tests faltantes — generar `tests/test_sigap_cli.py`,
   `tests/test_auditar_db.py` y `tests/test_factory_reset.py`.
   Detalle por módulo:

   **`tests/test_factory_reset.py`** — regresión fix Sesión #16:
   - Verificar que `factory_reset_normalized.py` y
     `factory_reset_preserve_learning.py` NO hardcodean rutas:
     el string `"control_gastos.db"` no debe aparecer en el código fuente.
   - Verificar que la ruta de DB usada en runtime termina en `sigap.db`
     (obtenida via `sigap_config.get_db_path()`).

   **`tests/test_auditar_db.py`** — cobertura desde cero:
   - Verificar que `auditar()` usa `sigap_config.get_db_path()` para
     obtener la ruta (D-005), no rutas hardcodeadas.
   - Verificar que con una DB en memoria que NO tiene `param_preferencias`,
     la función no lanza excepción (solo loguea warning).
   - Verificar que con una ruta inexistente, la función no lanza excepción
     (rama `os.path.exists() == False`).
   - Verificar que con una DB que SÍ tiene `param_preferencias`,
     la función completa sin errores.

   **`tests/test_sigap_cli.py`** — cobertura desde cero:
   - Verificar que argparse reconoce `status` y `reset` como subcomandos
     válidos (sin ejecutarlos).
   - Verificar que `show_status()` con DB inexistente imprime advertencia
     y retorna sin crashear (mockear `RUTA_DB` a ruta falsa).
   - Verificar que `show_status()` con DB válida (en memoria con tablas
     del schema) imprime conteos y retorna sin crashear.
   - Verificar que `run_reset()` con `input()` mockeado a `"no"` imprime
     mensaje de cancelación y NO llama a `factory_reset_normalized()`.
   - Verificar que `RUTA_DB` en `sigap.py` proviene de `sigap_config`
     y termina en `sigap.db` (no nombre legacy).

2. **[FEAT]** Desacoplar `parsear_excel_santander()` como función aislada
3. **[FEAT]** Expandir `sigap.py` como CLI unificado
4. **[FEAT]** Módulo ABM standalone de catálogo
5. **[FEAT]** Parser MercadoPago