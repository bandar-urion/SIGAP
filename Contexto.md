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
| **Cuando Martín dice** "cerramos", "listo", "commit", "terminamos"    | Activar PROTOCOLO DE CIERRE DE SESIÓN completo sin esperar que lo pida  |
| **Cuando hay un fix de código**                                       | Verificar si corresponde nueva entrada en `docs/DECISIONES.md`          |
| **Cuando hay una decisión arquitectónica nueva**                      | Proponer D-XXX antes de continuar                                       |
| **Al detectar cualquier inconsistencia** entre código y documentación | Señalarla antes de continuar con la tarea principal                     |
| **Cada tres meses**                                                   | Recordar que corresponde Sesión de Arqueología Trimestral (Protocolo 6) |

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
├── sigap.py                          # Orquestador CLI (status / reset)
├── sigap_config.py                   # Config centralizada (lee sigap.cfg)
├── sigap.cfg                         # Parámetros: DB, rutas, UI, LOG_LEVEL
├── CLAUDE.md                         # Configuración para Claude Code
├── CHANGELOG.md                      # Historial de versiones
├── README.md                         # Documentación pública del proyecto
├── TODO.md                           # Tareas pendientes
├── Contexto.md                       # ← Este archivo (guía de sesión IA)
├── data/
│   ├── sigap.db                      # Base de datos SQLite (fuente de verdad)
│   ├── inbox/                        # Excel bancarios a procesar
│   └── processed/                    # Excel ya importados
├── scripts/
│   ├── import_santander.py           # Parser Excel Santander → Inbox UI
│   ├── factory_reset_normalized.py   # Reset + sembrado de DB
│   ├── factory_reset_preserve_learning.py
│   ├── modulos/
│   │   └── inbox_movimientos.py      # ⭐ Motor principal (UI + lógica de negocio)
│   ├── utils/
│   │   ├── config_grafica.py         # Constantes ANSI, colores, dimensiones UI
│   │   ├── auditar_db.py
│   │   ├── sesion_inicio.py          # Script de apertura de sesión
│   │   └── sesion_cierre.py          # Script de cierre de sesión
│   └── _legacy/                      # Scripts anteriores a v0.8.0 (solo referencia)
├── tests/
│   ├── test_aislamiento_cuotas.py    # Aislamiento lógica de cuotas
│   ├── test_config.py                # Configuración centralizada
│   ├── test_contrato_santander.py    # Contrato formato Excel Santander
│   ├── test_database_init.py         # Esquema SQL
│   ├── test_gobernanza_similitud.py  # Motor de Gobernanza (25 tests)
│   ├── test_gui_logic.py             # Lógica UI (mocks)
│   ├── test_importacion.py           # Integridad DB + deduplicación
│   ├── test_motor_clasificacion.py   # Motor IA (reemplaza test_cerebro.py)
│   ├── test_ui_inbox_movimientos.py  # UI mocks
│   └── test_robots_gobernanza.py     # ⭐ Robots de QA (5 robots)
├── docs/
│   ├── ADR-001-Motor-Base-Datos.md
│   ├── ADR-002-Modelo-Gobernanza.md
│   ├── GUIA_GIT.md
│   ├── DECISIONES.md                 # Decisiones arquitectónicas (D-001 a D-010)
│   ├── SESIONES.md                   # Bitácora de sesiones
│   ├── QA_UI_Checklist_inbox_movimientos.md
│   └── VIBE_CODING_SKILLS.md
└── logs/
    └── sigap_tecnico.log             # Log técnico rotativo
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

**Fecha:** 2026-04-09
**Sesión:** #17 — Auditoría de Integridad + Fix D-004 + Fix D-005 + Auditoría de Cobertura
**Entorno:** A (Windows 11 · VSCode · Claude Code)
**Branch:** `feature/importar-movimiento`

**Lo que hicimos:**
- Auditoría de integridad completa del proyecto post-Sesión #16.
- Suite baseline: 71/71 OK antes de cualquier cambio.
- FIX CRÍTICO D-004: `input()` en `inbox_movimientos.py:789` reemplazado
  por `leer_linea_inline()` — violación en el flujo UI principal del motor.
- FIX CRÍTICO D-005: `auditar_db.py` tenía rutas hardcodeadas a
  `control_gastos.db` (DB legacy inexistente). Migrado a
  `sigap_config.get_db_path()`.
- D-012 agregada a `docs/DECISIONES.md` (incidente rutas hardcodeadas
  en factory_reset, detectado en Sesión #16).
- `Contexto.md`: `manage.py` → `sigap.py` en tabla de módulos.
- `Contexto.md`: versión sincronizada a v0.8.1.
- Comentario de excepción arquitectónica en `sesion_inicio.py` y
  `sesion_cierre.py`.
- Suite post-fix: 71/71 OK ✅
- **Anexo — Auditoría de cobertura (primera ejecución trimestral):**
  - `sigap_config.py`: 90% ✅
  - `inbox_movimientos.py`: 68% ⚠️ — gaps documentados en TODO.md
  - `import_santander.py`: 0% ⚠️ — estructuralmente requiere refactor
  - `auditar_db.py`: 0% ⚠️ — testeable con SQLite en memoria
  - Protocolo 6 de VIBE_CODING_SKILLS.md actualizado: auditoría de
    cobertura incorporada como herramienta obligatoria trimestral.
    Próxima ejecución: Julio 2026.

**Estado del repo al cierre:**
- Suite: 71/71 OK ✅
- Pendiente commit de cierre de sesión
- Repo sin bugs críticos conocidos

## PRÓXIMAS TAREAS (en orden de prioridad)

1. **[DOC]** Revisión estructural completa de `ROADMAP.md`
2. **[DOC]** Documentar convención campo `usuario` en `auditoria_movimientos`
3. **[FEAT]** Desacoplar `parsear_excel_santander()` como función aislada
4. **[FEAT]** Expandir `sigap.py` como CLI unificado
5. **[FEAT]** Módulo ABM standalone de catálogo
6. **[FEAT]** Parser MercadoPago
7. **[DOC]** Diagrama/mapa de la suite de tests