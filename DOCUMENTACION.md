# **PROYECTO FÉNIX**

## **S.I.G.A.P. (Sistema Inteligente de Gestión y Auditoría Patrimonial)**

### **Powered by Hybrid Intelligence (Human + AI)**

---

# **0. MANIFIESTO FÉNIX: LA VISIÓN MACRO**

### **0.1. DEFINICIÓN DEL PROYECTO**
El "Proyecto Fénix" excede el alcance de un desarrollo de software. Es un **Programa de Actualización y Transformación Profesional** cuyo objetivo principal es la reactivación técnica y motivacional del Desarrollador (Martín).

### **0.2. PILARES DEL PROYECTO**
1. **Ejercitar el uso de herramientas:** Pasar de la teoría a la práctica moderna (Python, Git, SQL, VS Code, Clean Code, 3NF).
2. **Aplicación de la Mentalidad de Ingeniero de Software:** Adherir a los estándares de industria actual (documentación viva, control de versiones, auditoría).
3. **Sinergia Humano-IA:** Establecer un flujo de trabajo pionero donde el Analista Humano aporta la Lógica de Negocio y la Ética, mientras que la IA actúa como Copiloto Técnico y consultor, potenciando la productividad sin reemplazar el criterio.
4. **El Producto como Prueba de Concepto:** El **S.I.G.A.P.** es el *vehículo práctico* para ejecutar este aprendizaje.

### **0.3. EL COMPROMISO**
No se busca solo "que funcione", se busca "que esté bien hecho". El error es el punto de aprendizaje. El objetivo final es terminar el proyecto sintiéndose un **Analista de Sistemas vigente, capaz y motivado**.

---

# **1. OBJETO Y PROPÓSITO DEL SISTEMA**

### **1.1. DEFINICIÓN TÉCNICA**
El **S.I.G.A.P.** es una plataforma de gestión financiera personal diseñada bajo una arquitectura de **Procesamiento Inteligente**. Su núcleo combina reglas de negocio estrictas (3NF) con capacidades de Inteligencia Artificial para la normalización, enriquecimiento y auditoría de datos transaccionales.

### **1.2. EL COMPONENTE "INTELIGENTE" (AI-DRIVEN PROCESSING)**
El sistema se diferencia de una base de datos tradicional por su capacidad de **Inferencia de Contexto** sobre los "Movimientos":
* **Categorización Predictiva:** El sistema utiliza modelos de lenguaje (LLMs) y reglas aprendidas para interpretar descripciones bancarias ambiguas (ej: "MP*774" → "Gastos Varios") y sugerir la categoría más probable.
* **Detección de Anomalías:** Capacidad de alertar sobre patrones de gasto inusuales que escapan a la media histórica del Centro de Costo, actuando como un auditor automatizado.

### **1.3. OBJETIVOS ESPECÍFICOS**
* **Segregación Patrimonial:** Administrar economías separadas (Personal, Familiar, Terceros) sin mezclar fondos.
* **Visibilidad Financiera Real:** Diferenciar claramente entre **Liquidez** (Caja) y **Patrimonio** (Solvencia real).
* **Soberanía de Datos:** Garantizar que la información histórica resida en un entorno local, privado y controlado (SQLite), eliminando la dependencia de la nube.

### **1.4. PROPÓSITO GENERAL (MISIÓN)**
El sistema tiene como objeto proveer una herramienta centralizada, segura y eficiente para la **Administración, Gestión y Auditoría** de los recursos financieros de múltiples entidades (Centros de Costo), permitiendo transformar datos transaccionales dispersos en información estratégica para la toma de decisiones.

### **1.5. ALCANCE DEL SISTEMA**
* **INCLUYE:** Registro de movimientos, gestión de cuentas y tarjetas, cálculo de saldos, proyección de cierres de tarjeta y generación de reportes patrimoniales.
* **EXCLUYE:** Automatización de inversiones bancarias (conexión con APIs de bancos para operar dinero real) o gestión fiscal/impositiva legal (ARCA). El sistema es para **Contabilidad de Gestión Interna**.

---

# **2. JUSTIFICACIÓN TECNOLÓGICA Y ESTRATÉGICA**

El desarrollo de un sistema a medida (**S.I.G.A.P.**) en Python/SQLite se fundamenta en las limitaciones críticas inherentes a las herramientas de ofimática tradicionales y a la volatilidad de los modelos de IA generativa para el manejo de datos históricos sensibles.

### **2.1. S.I.G.A.P. VS. HOJAS DE CÁLCULO (Excel - Google Sheets)**
Si bien las hojas de cálculo son flexibles, carecen de integridad referencial y seguridad de datos a largo plazo.
* **Integridad Referencial (3NF):** En Excel, un error de tipeo puede dar origen a la creación de una categoría nueva (ej: "Súper" vs "Super"). SIGAP utiliza una base de datos relacional (SQLite) que impide físicamente cargar datos huérfanos o mal escritos, asegurando la calidad del dato desde el origen.
* **Separación Lógica/Datos:** En Excel, la fórmula vive en la celda junto al dato. Borrar una celda por error puede acarrear la destrucción en cadena de la lógica. En SIGAP, la lógica del negocio (Python) está desacoplada de los datos (SQL), blindando el sistema contra errores de usuario que afecten a la lógica del sistema.
* **Escalabilidad:** A medida que crecen los registros (años de historia), las planillas se vuelven lentas e inestables. SQLite soporta Gigabytes de información sin degradación de la performance.

### **2.2. S.I.G.A.P. VS. SOLICITUD DIRECTA A LA IA (LLMs)**
Los Modelos de Lenguaje (como Gemini/GPT) son excelentes razonadores pero pésimos almacenes de datos.
* **Alucinación Numérica:** Las IAs son probabilísticas, no determinísticas. Pueden "inventar" un número o fallar en una suma simple si el contexto es muy largo. SIGAP es determinístico: 2 + 2 siempre es 4.
* **Falta de Memoria Persistente:** Una IA no "recuerda" con precisión una transacción de hace 6 meses a menos que se le vuelva a alimentar toda la información (Context Windows Limit). SIGAP actúa como la **"Fuente de la Verdad" (Ground Truth)**; la IA se utiliza solo como consultora para analizar los datos que el SIGAP custodia.
* **Privacidad:** Cargar resúmenes bancarios completos en un chat en la nube expone datos sensibles. SIGAP procesa y anonimiza la información localmente.

### **2.3. CONCLUSIÓN: EL ECOSISTEMA HÍBRIDO**
La justificación final del desarrollo no es reemplazar a la IA, sino **potenciarla**.
* **Rol del SIGAP:** Custodio de los datos, ejecutor de reglas matemáticas estrictas y garante de la integridad histórica.
* **Rol de la IA:** Analista financiero que consume reportes generados por SIGAP para ofrecer consejos o detectar patrones.
* **Rol de la Hoja de Cálculo:** Descartada como sistema de registro, relegada únicamente a visualización temporal o borradores.

---

# **3. PRINCIPIOS DE DISEÑO Y DOCTRINA UX**

* **Persistencia:** Todo vive en SQLite local (control_gastos.db).
* **Integridad:** No se permite redundancia. Uso estricto de IDs y Foreign Keys (3NF).
* **Gobernanza:** Reglas claras para evitar la "granulación excesiva" (micro-management).

## **3.1. DOCTRINA UX: FLOW STATE (v4.0)**
El objetivo es superar la practicidad de Excel manteniendo la integridad de una Base de Datos. El usuario no debe sentir que "entra y sale" de menús, sino que fluye a través de los datos.

### **Doctrina HyperFlux (v5.0)**
La interfaz evoluciona de "Paginada" a "Flujo Continuo".
1.  **Viewport Deslizante:** El usuario navega una ventana de n registros que se desplaza sobre el total de datos.
2.  **Navegación Vectorial:** El uso del teclado es natural (Flechas direccionales).
3.  **Acciones Binarias:** Las decisiones de descarte o recuperación son inmediatas (Teclas laterales).
4.  **HUD de Estado:** El usuario siempre conoce el "Saldo de trabajo restante" mediante contadores en pantalla.

### **Filosofía de "Flujo Continuo"**
La interfaz debe reducir la carga cognitiva del usuario, permitiendo la clasificación masiva de datos sin interrupciones visuales ni cambios de contexto.

### **Principios de Interacción**
1.  **Visibilidad Permanente:** El Dashboard (Tabla de datos) nunca desaparece. La edición ocurre "in-situ", resaltando la fila activa mientras el resto del contexto permanece visible.
2.  **Pantalla Dividida (Split Screen):**
    * **Zona Superior (Estática):** Visualización de la planilla de movimientos (Dashboard).
    * **Zona Inferior (Dinámica):** Área de IntelliSense, mensajes y opciones de filtrado.
3.  **IntelliSense Táctil:**
    * El usuario no memoriza IDs numéricos.
    * El usuario escribe las primeras letras del concepto (ej: "Sup" para Supermercado).
    * **Auto-Selección:** En el momento exacto en que la búsqueda arroja un único resultado, el sistema:
        * Emite una señal auditiva (Bip).
        * Bloquea el input brevemente (0.5s) para frenar la inercia de escritura.
        * Auto-completa el campo y salta al siguiente.
4.  **Alias de Descripción (Beautifier):** El sistema "limpia" visualmente las descripciones bancarias crudas (ej: *"DEBIN-Supermercado 22344"*) transformándolas en nombres amigables (ej: *"Supermercado Coto"*) para facilitar el reconocimiento futuro.

### **Reglas de Clasificación Acelerada**
1.  **Pre-Carga Total:** Si el sistema reconoce un patrón, pre-carga los 3 pilares: Centro de Costo (CC), Categoría (C) y Subcategoría (SC).
2.  **Orden de Llenado (Embudo):** CC -> C -> SC. El filtrado de cada paso depende de la selección anterior.

---

# **4. METODOLOGÍA DE DESARROLLO (PROTOCOLO FÉNIX)**

### **4.1. FILOSOFÍA DE TRABAJO: AI PAIR PROGRAMMING**
El desarrollo se ejecuta bajo una modalidad de **Programación de a Pares (Pair Programming)** asimétrica y colaborativa:
* **Rol Humano (Lead Architect):** Define el "Qué" y el "Por qué". Aporta la visión estratégica, la lógica de negocio, la auditoría final y la ética.
* **Rol IA (Copilot/Senior Dev):** Resuelve el "Cómo". Genera la implementación técnica (scripts, SQL), sugiere optimizaciones, detecta inconsistencias lógicas y documenta procesos.

### **4.2. CICLO DE VIDA DE UNA TAREA (EL FLOW)**
Para garantizar la calidad y evitar la degradación del código (Spaghetti Code), cada intervención sigue estrictamente estos 5 pasos:

1.  **Briefing (Definición de Misión):** Se establece un objetivo único y acotado para la sesión.
2.  **Blueprint (Pizarra de Diseño):** La IA presenta un plan lógico o pseudo-código.
3.  **Execution (Coding & Testing):** Se generan y ejecutan los scripts en el entorno local.
4.  **Version Control (Git Commit):** Se consolida el cambio en el repositorio local.
5.  **Debriefing (Doc Update):** Se actualiza la documentación para reflejar cambios.

### **4.3. STACK DE HERRAMIENTAS**
* **Gestión de Versiones:** Git (Local en Termux).
* **IDE:** VS Code (Code-Server sobre Android).
* **Motor de Base de Datos:** SQLite 3.
* **Lenguaje de Scripting:** Python 3.

### **4.4. ESTÁNDARES DE VERSIONADO**
El proyecto adhiere estrictamente a **Conventional Commits** y **Semantic Versioning**.
Para ver la guía completa de tipos, alcances y ejemplos, consultar el anexo técnico:
👉 [GUIA_GIT.md](docs/GUIA_GIT.md)

### **4.5. ESTÁNDARES DE CALIDAD (UNIT TESTING)**
Para garantizar la robustez financiera, se aplica una política de **Tolerancia Cero** a la regresión.
* **Infraestructura:** Uso de `unittest` nativo de Python.
* **Cobertura:**
    * **Integridad de Datos:** Tests que simulan inserción de duplicados y validan constraints SQL.
    * **Lógica de Negocio:** Tests que validan la limpieza de strings y el matcheo de reglas.
* **Ejecución:** Todo cambio en la lógica del "Cerebro" debe ser validado corriendo `python -m unittest discover tests`.

---

# **5. REGLAS DE NEGOCIO (GOBERNANZA)**

## **5.1. ENTIDAD: CENTROS DE COSTO (CC)**
**Definición:** Es una Entidad (persona, grupo o proyecto) para la cual se genera el gasto o quien se beneficia del mismo.
* **Tabla DB:** `param_centros_costo`

**Reglas de Negocio:**
1. **Regla de Separación Patrimonial:** Solo se crea un Centro de Costo (CC) cuando se necesita aislar la gestión de sus gastos.
2. **Regla de Financiamiento:** Un CC puede ser **autofinanciado** o **subsidiado**.
3. **Regla de Operación:** El CC tiene uno o más Medios de Pagos asociados.

## **5.2. ENTIDAD: CATEGORÍAS (C)**
**Definición:** Es la clasificación de **Nivel 1 (Macro)**. Representa el "Concepto Contable".
* **Tabla DB:** `param_categorias`

**Reglas de Negocio:**
1.  **Regla de Jerarquía:** Una Categoría debe ser un contenedor lógico amplio.
2.  **Regla de Abstracción:** Define el *concepto* (Ej: Alimentos), no el *consumidor*.
3.  **Regla de Segregación (Inversión vs. Gasto):** Casa (Gasto Operativo) vs. Terreno (Inversión Patrimonial).

## **5.3. ENTIDAD: SUBCATEGORÍAS (SC)**
**Definición:** Es la clasificación de **Nivel 2 (Micro)**.
* **Tabla DB:** `param_subcategorias`

**Reglas de Negocio:**
1.  **Regla del Impacto:** Solo se crea una SC si el gasto tiene un impacto significativo.
2.  **Regla de Generalidad:** No se utilizan nombres propios de empresas como nombre de Subcategoría.
3.  **Dependencia:** Toda SC debe pertenecer obligatoriamente a una sola Categoría.

## **5.4. ENTIDAD: MEDIOS DE PAGO (MP)**
**Definición:** Es el instrumento financiero utilizado para abonar una transacción.
* **Tabla DB:** `param_medios_pago`

**Reglas de Negocio:**
1. **Regla de Ejecución:** Todo movimiento debe tener asociado un Medio de Pago (MP).
2. **Regla de Vinculación:** Un MP puede ser utilizado para financiar gastos de cualquier Centro de Costos (CC).
3. **Clasificación:** MP Líquidos (inmediatos) vs. MP Diferidos (crédito).

## **5.5. ENTIDAD: MOVIMIENTO (M)**
**Definición:** Es el registro atómico de un hecho económico.
* **Tabla DB:** `movimientos`

**Reglas de Negocio:**
1. **Regla de Integridad:** Vinculación triangular (Cuándo, Qué, Cómo).
2. **Regla de Signo (Naturaleza):** Depende del Tipo de Categoría (Ingreso suma, Egreso resta).
3. **Regla de Temporalidad:** Fecha de Compra vs Fecha de Pago (automática).
4. **Regla de Unicidad:** Identificador único (`num_referencia`) para evitar duplicados.
5. **Regla de Amortización:** Preferencia del Criterio Financiero (cuotas mes a mes).

## **5.6. ENTIDAD: PATRIMONIO (P)**
**Definición:** Valor neto resultante (Activos - Pasivos) de un CC.

**Reglas de Negocio:**
1. **Regla de Cálculo:** Patrimonio = Activos - Pasivos.
2. **Regla de Segregación:** Estado Patrimonial Independiente por CC.
3. **Regla de Liquidez vs. Solvencia:** Diferenciación entre dinero disponible YA y patrimonio real.

## **5.7. ENTIDAD: AGENDA DE PAGOS (AP)**
**Definición:** Registro de obligaciones futuras (Radar de Vencimientos).
* **Tabla DB:** `agenda_pagos`

**Reglas de Negocio:**
1. **Regla de Previsión:** Todo gasto recurrente debe ingresarse para calcular Cash Flow.
2. **Regla de Prioridad:** Clasificación para Gestión de Crisis.

## **5.8. ENTIDAD: DICCIONARIO DE TÉRMINOS (SINÓNIMOS)**
**Definición:** Capa de traducción semántica y limpieza de datos.
* **Tabla DB:** `diccionario_terminos`

**Funcionalidad:**
1. Actúa como "Middleware" en la entrada de datos.
2. Normaliza términos coloquiales (`Sushi` -> `Comida Preparada`).
3. **Beautifier:** Almacena descripciones amigables para el usuario, reemplazando los textos crudos del banco.

**Reglas de Negocio:**
1. **Regla de Aprendizaje:** El sistema aprende nuevos sinónimos y clasificaciones completas (CC-C-SC) sobre la marcha.

# **6. REGLAS FUTURAS (ROADMAP DE GOBERNANZA)**
*Nota: Estas reglas definen el estándar objetivo para las versiones futuras.*

## **6.1. REGLA DE HOMOGENEIZACIÓN MONETARIA**
Normalización por Cotización de Referencia para análisis histórico en moneda inestable.

## **6.2. REGLA DE IMPUTACIÓN FINANCIERA**
Cálculo exacto de fecha de egreso de fondos según vencimiento de tarjeta.

## **6.3. REGLA DE INMUTABILIDAD HISTÓRICA (SOFT DELETE)**
Prohibido `DELETE` físico. Uso de `activo = False`.

## **6.4. REGLA DE APROPIACIÓN PRESUPUESTARIA**
Definición de Topes de Gasto y alertas de desvío presupuestario.

---

## [2026-02-01] Hito 4.0: Doctrina UX & IntelliSense (Planificación)
**Estado:** EN DISEÑO
**Cambios:**
- Definición de la "Doctrina UX v4.0" (Flow State).
- Renombrado de `inbox_movimientos.py` a `inbox_movimientos.py`.
- Diseño de arquitectura de pantalla dividida (Dashboard Estático / Input Dinámico).
- Especificación de IntelliSense con feedback auditivo.
**Próximos Pasos:**
- Refactorizar `inbox_movimientos.py` implementando la nueva UI.
- Implementar búsqueda incremental en base de datos.