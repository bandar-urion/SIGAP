# 📋 DECISIONES.md — Registro de Decisiones Arquitectónicas
**Proyecto Fénix · S.I.G.A.P.**

> **Propósito:** Este documento registra las decisiones de diseño y arquitectura
> que definen el sistema. No son opciones abiertas: son compromisos adoptados,
> con contexto y justificación. Antes de proponer una alternativa, leer la entrada
> correspondiente.
>
> **Formato:** Cada entrada tiene Fecha, Contexto, Alternativas evaluadas,
> Decisión final y Consecuencias conocidas.
>
> **Relación con ADRs:** Los ADRs en `docs/` son el registro formal de decisiones
> de motor/infraestructura. Este archivo cubre decisiones de diseño de producto,
> UX y filosofía operativa que no encajan en un ADR técnico estricto.

---

## Índice

| ID | Decisión | Fecha | Estado |
|---|---|---|---|
| D-001 | SQLite como motor de base de datos | 2026-01-28 | ✅ Activa |
| D-002 | Modelo de Gobernanza Data-Driven | 2026-01-28 | ✅ Activa |
| D-003 | Terminal pura como interfaz (sin GUI) | 2026-01-28 | ✅ Activa |
| D-004 | `leer_byte()` como único lector de input en UI | 2026-02-10 | ✅ Activa |
| D-005 | `sigap_config.py` como único punto de configuración | 2026-02-15 | ✅ Activa |
| D-006 | Doctrina HyperFlux: viewport deslizante sin menús | 2026-02-01 | ✅ Activa |
| D-007 | Renombrado semántico: Transaccion → Movimiento | 2026-03-05 | ✅ Activa |
| D-008 | 3NF estricta: no desnormalizar por conveniencia | 2026-01-28 | ✅ Activa |
| D-009 | Gobernanza de Alta de Subcategoría (6 criterios) | 2026-03-09 | ✅ Activa |

---

## D-001 — SQLite como motor de base de datos

**Fecha:** 2026-01-28
**Decisores:** Martín (Lead), IA (Copilot)
**Ver también:** `docs/ADR-001-Motor-Base-Datos.md` (documento completo)

**Contexto:** El proyecto requería almacenamiento para datos financieros históricos y transaccionales. Las herramientas previas (Excel/Sheets) mostraron fragilidad en integridad de datos, dependencia de la nube y problemas de escalabilidad.

**Alternativas evaluadas:**
- CSV/JSON planos — sin integridad referencial
- Excel/Google Sheets — frágil, sin constraints, dependencia de nube
- PostgreSQL/Firebase — costo, latencia, dependencia de internet
- **SQLite 3** — relacional, archivo único, serverless, soporte nativo Python

**Decisión:** SQLite 3 como única base de datos del sistema.

**Consecuencias:**
- Positiva: integridad ACID, FK, constraints, sin servidor, portabilidad total
- Negativa: requiere herramientas propias para visualizar/editar datos
- **Nota operativa:** las Foreign Keys deben activarse explícitamente con `PRAGMA foreign_keys = ON` en cada conexión, ya que SQLite las desactiva por defecto

---

## D-002 — Modelo de Gobernanza Data-Driven

**Fecha:** 2026-01-28
**Decisores:** Martín (Lead), IA (Copilot)
**Ver también:** `docs/ADR-002-Modelo-Gobernanza.md` (documento completo)

**Contexto:** El sistema necesitaba validar reglas de negocio complejas (ej: "no usar nombres de marcas como subcategorías"). Hardcodear estas reglas en Python las haría rígidas y costosas de cambiar.

**Alternativas evaluadas:**
- Validación en código Python — rápido pero rígido, requiere deploy ante cada cambio
- Triggers en SQLite — difíciles de depurar
- **Modelo híbrido declarativo** — reglas como datos en tablas, código las lee y aplica

**Decisión:** Dos tablas de gobernanza: `reglas_catalogo` (define la regla) y `reglas_vinculos` (asocia la regla a entidades).

**Consecuencias:**
- Positiva: reglas modificables sin tocar código, reutilizables entre entidades
- Negativa: requiere JOIN adicional para recuperar reglas aplicables

---

## D-003 — Terminal pura como interfaz (sin GUI)

**Fecha:** 2026-01-28
**Estado de revisión:** No negociable hasta que el core esté blindado

**Contexto:** El proyecto se desarrolla en dos entornos: PC Windows y Samsung S21 con Termux. Cualquier GUI requeriría dependencias de sistema, compilación nativa, o exposición a la red. El objetivo es que el sistema funcione con Python puro en cualquiera de los dos entornos.

**Alternativas evaluadas:**
- Tkinter — no disponible fácilmente en Termux, requiere display
- PyQt/Kivy — dependencias nativas, setup complejo en Android
- Streamlit/Flask — requiere browser, introduce dependencia de red local
- **Terminal pura** — funciona en cualquier entorno con Python, sin dependencias extra

**Decisión:** Interfaz de terminal pura hasta que el core esté blindado (tests, integridad, auditoría). GUI puede evaluarse en Fase 3 como capa encima del core existente.

**Consecuencias:**
- Positiva: portabilidad total Termux/Windows, sin dependencias extra
- Negativa: curva de UX más alta, requiere diseño deliberado de la interfaz

---

## D-004 — `leer_byte()` como único lector de input en UI

**Fecha:** 2026-02-10 (aprox.)
**Contexto emergente:** Durante el desarrollo de la UI en Termux, `input()` estándar de Python causó comportamientos impredecibles: el Enter se "clavaba" (double-enter), el buffer de teclado no se vaciaba entre pantallas, y las secuencias de escape de flechas se perdían.

**Alternativas evaluadas:**
- `input()` estándar — produce doble-enter, no detecta flechas, no funciona en modo raw
- `msvcrt.getch()` en Windows / `tty + termios` en Linux — específicos de plataforma
- **`leer_byte()` como wrapper cross-platform** — encapsula ambas implementaciones en una sola función, abstrae el sistema operativo

**Decisión:** Toda lectura de input en flujos UI pasa obligatoriamente por `leer_byte()`. Prohibido usar `input()` en cualquier módulo de interfaz.

**Consecuencias:**
- Positiva: comportamiento predecible en Termux y Windows, detección de flechas y secuencias especiales
- Negativa: la función `leer_linea_inline()` también debe construirse sobre `leer_byte()`, no sobre `input()`

---

## D-005 — `sigap_config.py` como único punto de configuración

**Fecha:** 2026-02-15 (aprox.)
**Contexto emergente:** Varios scripts tenían rutas hardcodeadas a la DB (`control_gastos.db`, `sigap.db`), lo que causaba que al renombrar o mover el archivo, múltiples scripts fallaran en cascada.

**Alternativas evaluadas:**
- Variables de entorno del OS — requiere configuración del entorno, frágil en Termux
- Constantes hardcodeadas en cada script — rompe cuando cambia la estructura
- **`sigap_config.py` centralizado** — lee `sigap.cfg`, construye rutas absolutas, expone funciones `get_db_path()` y `get_path()`

**Decisión:** Toda ruta y parámetro de configuración se obtiene exclusivamente vía `sigap_config`. Prohibido hardcodear rutas o nombres de archivos en cualquier otro módulo.

**Consecuencias:**
- Positiva: un solo lugar para cambiar la ruta de la DB, compatible con Termux y Windows
- Negativa: `sigap_config.py` ejecuta `cargar_configuracion()` al importarse — los módulos que lo importan disparan el logging automáticamente

---

## D-006 — Doctrina HyperFlux: viewport deslizante sin menús

**Fecha:** 2026-02-01
**Ver también:** Sección 3.1 de `DOCUMENTACION.md`

**Contexto:** La primera versión de la UI usaba paginación clásica (página 1, página 2) y menús numerados. En el uso real resultó lenta: el usuario perdía el contexto al cambiar de página, y la navegación por menús interrumpía el flujo de clasificación masiva de movimientos.

**Alternativas evaluadas:**
- Menús numerados clásicos — interrumpen el flujo, requieren memorizar opciones
- Paginación fija — pérdida de contexto al cambiar página
- **Viewport deslizante con navegación vectorial** — el dashboard nunca desaparece, la edición ocurre in-situ

**Decisión:** La interfaz implementa un viewport de N filas que se desliza sobre el total de movimientos. Las acciones son vectoriales (flechas del teclado). No hay menús: las opciones disponibles se muestran siempre en el pie del dashboard.

**Consecuencias:**
- Positiva: Flow State real — el usuario no pierde contexto, la clasificación masiva es fluida
- Negativa: la implementación del manejo de terminal raw es más compleja

---

## D-007 — Renombrado semántico: Transaccion → Movimiento

**Fecha:** 2026-03-05
**Sesión:** #3 (aprox.)

**Contexto:** La clase principal del dominio se llamaba `Transaccion` y el módulo `carga_gastos.py`. A medida que el sistema creció, el lenguaje del dominio (DOCUMENTACION.md, reglas de negocio) habla de "Movimientos", no de "Transacciones". La divergencia entre el lenguaje del dominio y el código generaba fricción cognitiva y errores en los tests.

**Decisión:** Renombrar `Transaccion` → `Movimiento`, `carga_gastos.py` → `inbox_movimientos.py`. Actualizar todos los imports, tests y documentación. El módulo `editor_gastos.py` queda reemplazado conceptualmente por el flujo de inbox.

**Consecuencias:**
- Positiva: el código habla el mismo idioma que las reglas de negocio (Domain-Driven Design)
- Negativa: los tests que importaban el nombre viejo rompieron — fueron corregidos en Sesión #8

---

## D-008 — 3NF estricta: no desnormalizar por conveniencia

**Fecha:** 2026-01-28

**Contexto:** En sistemas de finanzas personales es tentador desnormalizar para simplificar las consultas (ej: guardar `nombre_categoria` en la tabla `movimientos` junto con `id_categoria`). Esto elimina un JOIN pero introduce redundancia y riesgo de inconsistencia.

**Decisión:** El schema mantiene Tercera Forma Normal (3NF) de forma estricta. Todo dato derivable de una clave foránea se obtiene mediante JOIN, nunca se almacena redundantemente.

**Consecuencias:**
- Positiva: consistencia garantizada — cambiar el nombre de una categoría impacta automáticamente en todos los movimientos
- Negativa: las consultas de reporte requieren JOINs explícitos, los scripts de utilidad son más verbosos

---

## D-009 — Gobernanza de Alta de Subcategoría (6 criterios)

**Fecha:** 2026-03-09
**Sesión:** #4

**Contexto:** El sistema permite al usuario crear nuevas subcategorías durante el proceso de clasificación de movimientos. Sin validación, el usuario podría crear subcategorías duplicadas, con nombres de marcas, de una sola palabra o sin evidencia de recurrencia, degradando la calidad del catálogo.

**Decisión:** Implementar un motor de evaluación con 6 criterios antes de confirmar cualquier alta:
1. Sin duplicado exacto en la DB
2. Sin subcategorías similares detectadas (contención, prefijo, palabras clave)
3. Formato Title Case
4. Nombre descriptivo (más de una palabra)
5. Frecuencia en el lote actual (¿aparece más de una vez?)
6. Frecuencia histórica en la DB (¿ya existía en movimientos pasados?)

**Flujos resultantes:**
- Duplicado exacto → **bloqueo total**
- Similar detectada → advertencia + opción de adoptar existente
- Sin evidencia de recurrencia → requiere justificación explícita del usuario
- Todo OK → confirmación directa

**Consecuencias:**
- Positiva: catálogo de subcategorías mantenido limpio desde el origen (Poka-Yoke)
- Negativa: el flujo de alta es más largo para casos nuevos legítimos — mitigado por las opciones de justificación predefinidas (M/A/R)

---

*DECISIONES.md — Proyecto Fénix · Martín · Creado Sesión #8 · 2026-03-13*

---

## D-010 — Archivos de credenciales nunca en el repositorio

**Fecha:** 2026-03-14
**Sesión:** #8 (cierre)
**Contexto emergente:** Durante el push inicial al repo `SIGAP` en GitHub, el Secret
Scanning de GitHub bloqueó el push porque el historial contenía
`scripts/credenciales.json` — una service account key de Google Cloud commiteada
en los primeros commits del proyecto (enero 2026), cuando el proyecto usaba
Google Sheets como backend.

El archivo había sido movido a `scripts/_legacy/` en un refactor posterior,
pero seguía presente en el historial de Git en ambas rutas.

**Acciones tomadas:**
1. Service account revocada en Google Cloud Console (proyecto `gastos-python-485019`)
2. Historial reescrito con `git filter-branch` para eliminar el archivo de los 61 commits
3. Push forzado (`--force`) a todas las branches del repo `SIGAP`

**Decisión:** Ningún archivo de credenciales, tokens, API keys o secrets
se commitea al repositorio bajo ninguna circunstancia. El patrón
`*credencial*.json` ya estaba en `.gitignore` — la falla ocurrió antes
de que ese patrón existiera.

**Regla operativa:** Antes de hacer el primer commit de un archivo nuevo,
verificar que no contenga ningún tipo de credencial o secret. Si hay dudas:
`git diff --cached` antes de `git commit`.

**Consecuencias:**
- Positiva: historial limpio, credencial revocada, GitHub Secret Scanning activo como guardia
- Negativa: los hashes de todos los commits cambiaron por la reescritura — cualquier
  referencia externa a commits anteriores queda inválida

*Nota: el repo anterior `ControlGastos` en GitHub fue reemplazado por `SIGAP`
como parte de esta sesión.*
