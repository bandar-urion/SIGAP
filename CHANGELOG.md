# Changelog - S.I.G.A.P.

Todas las modificaciones notables a este proyecto serán documentadas en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

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



