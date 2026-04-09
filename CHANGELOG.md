# Changelog - S.I.G.A.P.

Todas las modificaciones notables a este proyecto serán documentadas en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [v0.8.1] — 2026-04-09

### Fixed
- `scripts/factory_reset_normalized.py`: ruta de DB hardcodeada a nombre legacy
  `control_gastos.db` corregida. Ahora usa `sigap_config.get_db_path()`.
- `scripts/factory_reset_preserve_learning.py`: mismo fix de ruta. Ambos scripts
  son ahora compatibles con `sigap.cfg` como única fuente de configuración.

### Infra
- Conector GitHub de Claude.ai deshabilitado. Claude Code cubre lectura,
  escritura y ejecución en tiempo real sobre el repo local.

## [v0.8.0] - 2026-03-15 (Hito: Auditoría Completa y Robots de QA)

### 🛡️ Auditoría & Trazabilidad
- **Flujo de `auditoria_movimientos` completado** en `scripts/import_santander.py`.
  Tres casos cubiertos con registro atómico (antes del `conn.commit()`):
  - `resultado='OK'` — movimiento insertado, `id_movimiento_ref=lastrowid`.
  - `resultado='SKIP_DUPLICADO'` — duplicado silencioso (`rowcount=0`).
  - `resultado='DESCARTADO_USUARIO'` — descarte explícito por el operador.
- **Campo `usuario`** en `auditoria_movimientos`: identifica el módulo origen
  del evento (`SIGAP_IMPORT`, `SIGAP_UI`, `SIGAP_RESET`, `SIGAP_CLI`),
  no una persona física.

### 🧪 Calidad (QA)
- **`tests/test_robots_gobernanza.py`:** 5 robots de QA para el flujo
  de alta de subcategoría:
  - `test_robot_crear_subcategoria_nueva`
  - `test_robot_rechazo_duplicado_exacto`
  - `test_robot_alerta_similitud`
  - `test_robot_justificacion_requerida`
  - `test_robot_cancelacion_por_usuario`
- **Suite final: 71/71 OK** (era 66 al inicio de la sesión).

### 🛠️ Tooling
- **Claude Code** instalado en Entorno A (Windows 11 · VSCode).
  Generado `CLAUDE.md` con configuración del proyecto para el agente.

## [v0.7.0] - 2026-03-05 (Hito: Refactor Semántico e Inbox)

### 🚀 Arquitectura y Dominio
- **Domain-Driven Design:** Transición completa de la nomenclatura "Transacciones" a "Movimientos" en todo el ecosistema.
- **Inbox Centralizado:** Consolidación del motor `inbox_movimientos.py` como único punto de entrada de datos.

### 🧪 Calidad (QA)
- **Estandarización de Mocks:** Refactor de la suite de pruebas UI (`test_ui_inbox_movimientos.py`) implementando variables de instancia (`self.`) para garantizar aislamiento entre tests.
- **Runner Personalizado:** Implementación de descripciones limpias (Docstrings) en la salida de la terminal.

## [v0.7.2] - 2026-03-14 (Patch: Seguridad y Migración de Repo)

### 🔐 Seguridad
- **Limpieza de historial:** Eliminado `scripts/credenciales.json` y
  `scripts/_legacy/credenciales.json` de los 61 commits históricos mediante
  `git filter-branch`. Las credenciales de Google Cloud (service account
  `gastos-python-485019`) fueron revocadas antes de la operación.
- **Decisión D-010:** Formalizada la regla "credenciales nunca en el repo"
  en `docs/DECISIONES.md` con contexto, acciones tomadas y regla operativa.

### 🏗️ Infraestructura
- **Migración de repo:** Repositorio remoto renombrado de `ControlGastos`
  a `SIGAP` en GitHub (`github.com/bandar-urion/SIGAP`), alineando el nombre
  del repo con la carpeta local y el nombre del sistema.
- **Credential helper:** Configurado `git credential.helper store` en Termux
  para eliminar la dependencia del socket de Code-Server (que causaba 403).
- **`logs/` fuera del tracking:** `logs/sigap_tecnico.log` sacado del índice
  de Git (`git rm --cached`) y agregado al `.gitignore`.


## [v0.7.1] - 2026-03-13 (Patch: Cierre Fase 1 — Deuda Técnica)

### 🛡️ Integridad & Seguridad
- **Foreign Keys activas:** Agregado `PRAGMA foreign_keys = ON` en
  `scripts/import_santander.py`. Las FK estaban declaradas en el schema
  pero inactivas en runtime (SQLite las desactiva por defecto).
- **`sigap_config.py`:** Corregido `get_db_path()` para retornar ruta
  absoluta. Antes retornaba ruta relativa, causando "DB fantasma" según
  desde qué directorio se ejecutara el script.

### 🧹 Limpieza & Organización
- **`.gitignore` corregido:** Patrón `*.db` estaba comentado y con barra
  (`# *.db/`). Corregido a `*.db`. Agregados `__pycache__/`, `*.pyc`,
  `~$*.xlsx` (lock files de Windows) y `*.zip`.
- **`__pycache__` sacados del repo:** 32 archivos `.pyc` y directorios
  de caché eliminados del tracking con `git rm --cached`.
- **Scripts huérfanos → `_legacy/`:** Movidos `fix_esquema_v2.py`
  (apuntaba a `control_gastos.db`, nombre viejo), `nivelar_data.py` y
  `parche_subcategorias.py` (migraciones ya aplicadas).
- **`test_parser_santander.py` → `_legacy/`:** Reemplazado por el
  Contract Test formal `tests/test_contrato_santander.py`.

### 📄 Documentación
- **`docs/DECISIONES.md`:** Creado con 9 decisiones arquitectónicas
  retroactivas (D-001 a D-009), cubriendo SQLite, Gobernanza Data-Driven,
  Terminal pura, `leer_byte()`, `sigap_config`, HyperFlux, renombrado
  Transaccion→Movimiento, 3NF y Gobernanza de Alta de Subcategoría.

### 🧪 Calidad (QA)
- **Refactor de suite:** `test_avanzado.py` + `test_cerebro.py` +
  `test_sigap_core.py` fusionados en dos archivos con criterio por módulo:
  - `tests/test_config.py` — valida `sigap_config.py` (rutas, normalización)
  - `tests/test_motor_clasificacion.py` — valida regex de cuotas, limpieza
    de texto e inferencia de contexto (6 clases, 18 tests)
- **`tests/test_contrato_santander.py`:** Contract Test nuevo para validar
  el formato del Excel de Santander Río antes de procesarlo. 8 tests,
  skipeo automático si inbox vacío, diagnóstico integrado. Basado en
  columnas reales del extracto (`Fecha`, `Descripción`, `Referencia`,
  `Caja de Ahorro`, `Cuenta Corriente`).
- **Suite final: 66/66 OK** (era 58 al inicio de la sesión)



## [v0.7.0-doc3] - 2026-03-10 (Patch: Mapa de Sinergia Humano-IA)

### 📄 Documentación
- **`VIBE_CODING_SKILLS.md`:** Creado en raíz del proyecto. Mapa personal
  de patrones de sinergia Humano-IA construido a partir de sesiones reales
  de SIGAP. 7 patrones activos (5 dominados, 2 en construcción) y
  4 patrones avanzados pendientes de ejercitar.

## [v0.7.0-doc2] - 2026-03-10 (Patch: Auditoría de Cobertura QA)

### 📄 Documentación
- **`TODO.md`:** FASE 0 cerrada al 100%. Ítem `QA_UI_Checklist.md` actualizado
  reflejando el documento real (`QA_UI_Checklist_inbox_movimientos.md`) y su
  cobertura automatizada: Fases 1, 2, 3, 4, 5, 7 y 8 (parcial). Fase 9
  pendiente de automatización, trazada a FASE 2 (Fábrica de Veneno).

### 🧪 Calidad (QA)
- **Auditoría de cobertura:** Mapeadas las 9 fases del Protocolo de Certificación
  UI contra los 10 archivos de tests automatizados. Gaps identificados y
  documentados en FASE 2 del backlog táctico.

## [v0.7.0-doc] - 2026-03-10 (Patch: Auditoría Documental)

### 📄 Documentación
- **`README.md`:** Creado desde cero. Carta de presentación completa del proyecto
  con stack, estructura de directorios, guía de inicio rápido, filosofía,
  tabla de estado de módulos v0.7.0 y tabla de documentación.
- **`TODO.md`:** FASE 1 (Gobernanza de Inbox) marcada como completada.
  Refleja los 6 criterios de Gobernanza y la Trazabilidad implementados en Sesión #4.
- **`ROADMAP.md`:** Registrado el hito `test_gobernanza_similitud.py` (25/25 ✅)
  correspondiente a Sesión #4 (2026-03-09).
- **`Contexto.md`:** Árbol de estructura del proyecto corregido y sincronizado
  con el estado real del repositorio (agregados `rejected/`, `logs/`, tests completos).

## [v0.6.5] - 2026-02-02 (Patch: Cross-Platform)

### 🐧 Infraestructura & Portabilidad
- **Soporte Linux/Termux:** El sistema ahora detecta automáticamente el Sistema Operativo al iniciar.
- **Capa de Abstracción de I/O:** Se reemplazaron las llamadas directas a librerías nativas de Windows (`msvcrt`, `winsound`) por wrappers inteligentes (`leer_byte`, `beep_confirmacion`) que se adaptan al entorno.
- **Navegación ANSI:** Implementación de parser de secuencias de escape para permitir el uso de flechas de dirección en terminales Unix/Linux.

## [v0.6.4] - 2026-02-01 (Hito: Financiación Inteligente)

### 💳 Gestión de Cuotas & Amortización
- **Regex Financiero:** El sistema ahora escanea las descripciones buscando patrones de cuotas (`01/12`, `Cta 3`).
- **Date Guard:** Lógica avanzada (Negative Lookahead) para evitar confundir fechas (`01/12/2025`) con cuotas.
- **Smart Suggestion:** Para servicios sin cuotas explícitas (ej: Gas), el sistema sugiere la amortización basada en el historial, pero permite confirmación manual o edición rápida.
- **Visualización:** Nuevos indicadores visuales en la Torre de Control (`💳 [x/y]`).

### 🧪 Calidad (QA)
- **Tests de Tortura:** Se agregó `tests/test_avanzado.py` para someter al motor de Regex a casos extremos, lógicas imposibles y ambigüedades fecha/cuota.

## [v0.5.0] - 2026-02-01 (Hito: HyperFlux & Calidad)

### 🚀 UX/UI (HyperFlux)
- **Navegación Vectorial:** Abandono del paginado estático. Implementación de **Viewport Deslizante** controlado por flechas del teclado (`⬆` `⬇`).
- **Acciones Rápidas:** Tecla `Derecha` para DESCARTAR movimiento (Gris), `Izquierda` para RECUPERAR (Pendiente), `Enter` para EDITAR.
- **HUD (Heads-Up Display):** Barra de estado inferior con métricas en tiempo real (`PEND: 4 | AUTO: 12 | OK: 8`).
- **Feedback Semántico:** Inyección de etiquetas de estado (`[AUTO]`, `[PEND]`) en la fila seleccionada para mantener contexto sin depender del color.

### ⚙️ Core & Lógica (Smart Import)
- **Persistencia Iterativa:** El importador `import_santander.py` ahora detecta si quedaron movimientos pendientes. Si `PENDIENTES > 0`, guarda el progreso pero **mantiene el archivo en inbox** para continuar después.
- **Deep Match:** El motor de IA ahora aplica limpieza visual antes de comparar y prioriza las reglas más largas (específicas) sobre las cortas (genéricas).
- **Auto-Advance:** El cursor avanza automáticamente a la siguiente fila tras una edición exitosa.

### 🛡️ Calidad (Ingeniería de Software)
- **Unit Testing Suite:** Implementación de pruebas automatizadas con `unittest`.
    - `test_cerebro.py`: Valida la limpieza de texto y la lógica de matcheo de la IA.
    - `test_importacion.py`: Valida la integridad de la DB y el rechazo de duplicados (`INSERT OR IGNORE`).
    - `test_database_init.py`: Valida la estructura del esquema SQL.


## [v0.4.0] - 2026-02-01 (Hito: La Torre de Control)

### 🚀 UX/UI (Revolución de Interfaz)
- **Nuevo Módulo:** Se consolida `carga_gastos.py` como el núcleo de imputación, reemplazando los menús numéricos por una interfaz de alto rendimiento ("Torre de Control").
- **Filosofía Flow State:** Edición continua sin perder visualización del Dashboard.
- **Visualización Inteligente:**
    - **Smart Fit Dual:** Las columnas se auto-ajustan milimétricamente midiendo la longitud real del texto en pantalla.
    - **Accounting View:** Formato monetario contable (`$ - #,###.##`) con alineación derecha estricta.
    - **Matrix View:** El selector de categorías utiliza todo el ancho de pantalla en columnas dinámicas.

### 🧠 Inteligencia Artificial (Lógica)
- **Pattern Mining:** El sistema analiza las descripciones del lote actual y detecta patrones repetitivos (prefijos comunes) para sugerir reglas de aprendizaje "limpias".
- **Auto-Promoción:** Los movimientos completados (CC+C+SC) ascienden automáticamente de estado `PENDIENTE` a `AUTO`.

### 🛡️ Gobernanza & Seguridad (Poka-Yoke)
- **Anti-Inercia:** Limpieza de buffer de teclado tras confirmaciones auditivas (Bip) para evitar errores por velocidad.
- **Validación de Integridad:** Al crear una regla personalizada, el sistema impide guardar claves que no existan matemáticamente en la descripción original.
- **Feedback Auditivo:** Diferenciación de tonos para Éxito (Agudo) y Error (Grave).

### 🔧 Mantenimiento
- **Refactorización:** Eliminación de código muerto de versiones v1/v2/v3.
- **Base de Datos:** Sembrado de categorías optimizado en `factory_reset_normalized.py`.


## [v0.1.1] - 2026-01-30 (Mejora de Modelo de Datos)
### 💎 Base de Datos
- **Refactorización de Categorías:** Separación de `Terreno` (Inversión) y `Casa` (Gasto).
- **Inteligencia de Datos:** Implementación de tabla `diccionario_terminos` para mapeo de sinónimos.
- **Normalización:** Ajuste de Subcategorías basado en análisis de CSVs históricos (Regla de Abstracción).
- **Medios de Pago:** Inclusión de Billeteras Virtuales (Lemon) y Cuentas de Terceros (Santander Mamá).


## [v0.1.0] - 2026-01-28 (Hito: Infraestructura)

### 🚀 Inicial
- **Lanzamiento del Proyecto Fénix:** Definición de objetivos, manifiesto y alcance.
- **Estructura de Base de Datos (SQLite):**
    - Implementación de modelo relacional en 3ra Forma Normal (3NF).
    - Tablas Core: `movimientos`, `agenda_pagos`, `centros_costo`.
    - Tablas Paramétricas: `categorias`, `subcategorias`, `medios_pago`.
    - Sistema de Gobernanza: Tablas `reglas_catalogo` y `reglas_vinculos`.
    - Tabla de Auditoría: `auditoria_compliance`.
- **Scripting:**
    - Creación de `factory_reset_normalized.py` para despliegue y sembrado (Seeding) de la base de datos.

### 📄 Documentación
- Creación de `DOCUMENTACION.md` (Constitución del Sistema).
- Creación de `ROADMAP.md` (Hoja de Ruta).
- Creación de `ADR-001` y `ADR-002` (Decisiones Arquitectónicas).



