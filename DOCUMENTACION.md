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
* **Categorización Predictiva:** El sistema utiliza modelos de lenguaje (LLMs) para interpretar descripciones bancarias ambiguas (ej: "MP*774" → "Gastos Varios") y sugerir la categoría más probable basada en el historial del usuario.
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

# **3. PRINCIPIOS DE DISEÑO**

* **Persistencia:** Todo vive en SQLite local (control_gastos.db).
* **Integridad:** No se permite redundancia. Uso estricto de IDs y Foreign Keys (3NF).
* **Gobernanza:** Reglas claras para evitar la "granulación excesiva" (micro-management).

---

# **4. METODOLOGÍA DE DESARROLLO (PROTOCOLO FÉNIX)**

### **4.1. FILOSOFÍA DE TRABAJO: AI PAIR PROGRAMMING**
El desarrollo se ejecuta bajo una modalidad de **Programación de a Pares (Pair Programming)** asimétrica y colaborativa:
* **Rol Humano (Lead Architect):** Define el "Qué" y el "Por qué". Aporta la visión estratégica, la lógica de negocio, la auditoría final y la ética.
* **Rol IA (Copilot/Senior Dev):** Resuelve el "Cómo". Genera la implementación técnica (scripts, SQL), sugiere optimizaciones, detecta inconsistencias lógicas y documenta procesos.

### **4.2. CICLO DE VIDA DE UNA TAREA (EL FLOW)**
Para garantizar la calidad y evitar la degradación del código (Spaghetti Code), cada intervención sigue estrictamente estos 5 pasos:

1.  **Briefing (Definición de Misión):** Se establece un objetivo único y acotado para la sesión (Ej: "Normalizar tabla de usuarios"). No se escribe código hasta que el objetivo esté claro.
2.  **Blueprint (Pizarra de Diseño):** La IA presenta un plan lógico, estructura de datos o pseudo-código de la solución propuesta. El Humano valida la lógica y la arquitectura.
3.  **Execution (Coding & Testing):** Se generan y ejecutan los scripts. Se valida el resultado con pruebas reales en el entorno de desarrollo (Termux).
4.  **Version Control (Git Commit):** Una vez validado el funcionamiento, se consolida el cambio en el repositorio local. *“Si funciona, se commitea”*.
5.  **Debriefing (Doc Update):** Se actualiza este documento (`DOCUMENTACION.md`) para reflejar cualquier cambio estructural o de regla. *“El código es volátil, la documentación es la ley”*.

### **4.3. STACK DE HERRAMIENTAS**
* **Gestión de Versiones:** Git (Local en Termux).
* **IDE:** VS Code (Code-Server sobre Android).
* **Motor de Base de Datos:** SQLite 3.
* **Lenguaje de Scripting:** Python 3.

### **4.4. ESTÁNDARES DE VERSIONADO**
El proyecto adhiere estrictamente a **Conventional Commits** y **Semantic Versioning**.
Para ver la guía completa de tipos, alcances y ejemplos, consultar el anexo técnico:
👉 [GUIA_GIT.md](docs/GUIA_GIT.md)

---

# **5. REGLAS DE NEGOCIO (GOBERNANZA)**

## **5.1. ENTIDAD: CENTROS DE COSTO (CC)**
**Definición:** Es una Entidad (persona, grupo o proyecto) para la cual se genera el gasto o quien se beneficia del mismo.
* **Tabla DB:** `param_centros_costo`

**Reglas de Negocio:**
1. **Regla de Separación Patrimonial:** Solo se crea un Centro de Costo (CC) cuando se necesita aislar la gestión de sus gastos para analizar su "costo de vida" por separado (Ej: Familia / Mamá / Personal).
2. **Regla de Financiamiento:** Un CC puede ser **autofinanciado** (tiene ingresos propios) o ser **subsidiado** con fondos de otro CC (no tener ingresos propios).
3. **Regla de Operación:** El CC tiene uno o más Medios de Pagos asociados para operar, ya sean propios (titular) o cedidos por un tercero (propios de un CC financiador).

## **5.2. ENTIDAD: CATEGORÍAS (C)**
**Definición:** Es la clasificación de **Nivel 1 (Macro)**. Representa el "Concepto Contable" o la naturaleza mayor del gasto.
* **Tabla DB:** `param_categorias`

**Reglas de Negocio:**
1.  **Regla de Jerarquía:** Una Categoría debe ser un contenedor lógico suficientemente amplio para abarcar múltiples Subcategorías.
2.  **Regla de Abstracción:** Define el *concepto* (Ej: Alimentos), no el *consumidor* ni el *comercio*.
3.  **Regla de Segregación (Inversión vs. Gasto):**
    * **Casa (Gasto Operativo):** Fondos que se consumen para la habitabilidad diaria (Luz, Gas, Limpieza).
    * **Terreno (Inversión Patrimonial):** Fondos destinados al mantenimiento de un Activo no habitado (Impuestos, Mejoras). Se separan para no distorsionar el costo de vida mensual.

## **5.3. ENTIDAD: SUBCATEGORÍAS (SC)**
**Definición:** Es la clasificación de **Nivel 2 (Micro)**. Representa el detalle específico dentro de una Categoría padre.
* **Tabla DB:** `param_subcategorias`

**Reglas de Negocio:**
1.  **Regla del Impacto:** Solo se crea una SC si el gasto tiene un impacto significativo mensual o es crítico para la toma de decisiones. Gastos menores o esporádicos van a agrupadores genéricos.
2.  **Regla de Generalidad:** No se utilizan nombres propios de empresas o marcas (Ej: "Coto", "Shell") como nombre de Subcategoría. Se debe usar el sustantivo genérico ("Supermercado", "Combustible").
3.  **Dependencia:** Toda SC debe pertenecer obligatoriamente a una sola Categoría.

## **5.4. ENTIDAD: MEDIOS DE PAGO (MP)**
**Definición:** Es el instrumento financiero o canal utilizado para abonar una transacción.
* **Tabla DB:** `param_medios_pago`

**Reglas de Negocio:**
1. **Regla de Ejecución:** Todo movimiento debe tener asociado un Medio de Pago (MP) que identifique el origen de los fondos.
2. **Regla de Vinculación:** Un MP puede ser utilizado para financiar gastos de cualquier Centro de Costos (CC). *Ejemplo: MP propiedad de ‘Personal’ puede ser utilizado para pagar un gasto de ‘Mamá’.*
3. **Clasificación de MP por Temporalidad:**
    * **MP Líquidos (inmediatos):** El dinero sale del patrimonio en el mismo momento de la compra (Ej: cuenta bancaria, efectivo, e-commerce, broker).
    * **MP Diferidos (crédito):** El dinero sale del patrimonio en una fecha futura (fecha de vencimiento) (Ej: tarjetas de crédito - Visa, Amex).

## **5.5. ENTIDAD: MOVIMIENTO (M)**
**Definición:** Es el registro atómico de un hecho económico que altera el patrimonio de un CC.
* **Tabla DB:** `movimientos`

**Reglas de Negocio:**
1. **Regla de Integridad:** Todo movimiento debe estar triangularmente vinculado a:
    1.  **Cuándo:** Una fecha real de ocurrencia (Fecha de Compra, no de Pago).
    2.  **Qué:** Una Subcategoría (SC) que explica el **destino** de los fondos (en caso de gastos) o la fuente (en caso de ingresos).
    3.  **Cómo:** Un Medio de Pago (MP) que explica el **origen** de los fondos (en caso de gastos) o donde se depositan (en caso de ingresos).
2. **Regla de Signo (Naturaleza):** El Movimiento en sí mismo es un valor absoluto (magnitud). Si suma o resta al saldo depende del Tipo de Categoría a la que pertenece su Subcategoría (destino):
    * Si Categoría es EGRESO → El movimiento **RESTA** patrimonio.
    * Si Categoría es INGRESO → El movimiento **SUMA** patrimonio.
3. **Regla de Temporalidad (Cierre vs Caja):**
    * La fecha del movimiento es la fecha de la transacción (lo económico).
    * La fecha de salida real del dinero (lo financiero) es calculada automáticamente por las reglas del Medio de Pago, si es tarjeta de crédito.
4. **Regla de Unicidad:** Cada movimiento importado de un sistema externo (Banco/MP) debe poseer un identificador único (campo `num_referencia`) que impida su duplicación en la base de datos local durante procesos de importación masiva.
5.* **Regla de Amortización:** Los gastos de gran magnitud financiados en cuotas pueden registrarse bajo dos modalidades, siendo preferente el **Criterio Financiero** para la gestión diaria del S.I.G.A.P. (registro del flujo de caja mes a mes) sobre el Criterio Económico (devengado total al inicio).

## **5.6. ENTIDAD: PATRIMONIO (P)**
**Definición:** Es el valor neto resultante de los recursos económicos de un CC en un instante determinado. Es la "foto" de la salud financiera.

**Reglas de Negocio:**
1. **Regla de Cálculo:** Patrimonio = Activos (lo que tengo) - Pasivos (lo que debo).
    * *Activos:* Saldo en cuentas bancarias + efectivo + inversiones.
    * *Pasivos:* Saldo pendiente en tarjetas de crédito + préstamos.
2. **Regla de Segregación:** Cada CC tiene su propio Estado Patrimonial Independiente. (Ej: el patrimonio de “Personal” puede crecer mientras el de “Familia” -que es puramente deficitario por diseño- siempre es negativo).
3. **Regla de Liquidez vs. Solvencia:**
    * **Liquidez:** Dinero disponible YA en MP Líquidos (caja de ahorro).
    * **Patrimonio Real:** Liquidez menos las deudas de Tarjeta de Crédito que vencerán el mes próximo.

## **5.7. ENTIDAD: AGENDA DE PAGOS (AP)**
**Definición:** Es el registro de obligaciones futuras ciertas o estimadas (Pasivos Transitorios). Actúa como un "Radar de Vencimientos".
* **Tabla DB:** `agenda_pagos`

**Reglas de Negocio:**
1. **Regla de Previsión:** Todo gasto recurrente o compromiso asumido debe ingresarse en la Agenda con una fecha de vencimiento y un monto estimado, permitiendo calcular el "Cash Flow" futuro.
2. **Regla de Prioridad:** En situaciones de déficit de liquidez, la Agenda debe permitir clasificar pagos por prioridad (Alta/Normal/Baja) para decidir qué obligaciones cubrir primero (Gestión de Crisis).

## **5.8. ENTIDAD: DICCIONARIO DE TÉRMINOS (SINÓNIMOS)**
**Definición:** Es una capa de traducción semántica que vincula términos coloquiales o comerciales con una Subcategoría oficial.
* **Tabla DB:** `diccionario_terminos`

**Funcionalidad:**
1. Actúa como un "Middleware" en la entrada de datos.
2. Permite al usuario ingresar lo que recuerda (Ej: *"Sushi"*, *"Nafta"*, *"Piyito"*) y el sistema lo normaliza automáticamente (`Comida Preparada`, `Combustible`, `Mascotas`).
3. Reduce la fricción en la carga de datos y evita errores de clasificación.

**Reglas de Negocio:**
1. **Regla de Aprendizaje:** El sistema debe permitir agregar nuevos sinónimos sobre la marcha sin alterar la estructura de Categorías.

# **6. REGLAS FUTURAS (ROADMAP DE GOBERNANZA)**
*Nota: Estas reglas definen el estándar objetivo para las versiones v0.3 y superiores. No son bloqueantes para el MVP actual, pero guían la evolución de la arquitectura.*

## **6.1. REGLA DE HOMOGENEIZACIÓN MONETARIA (FACTOR INFLACIÓN)**
**Contexto:** Dada la inestabilidad de la moneda local (ARS), los valores nominales pierden representatividad histórica rápidamente.
* **Definición:** Para análisis de largo plazo (> 3 meses), el sistema no debe comparar nominales.
* **Implementación Futura:** Todo movimiento en Pesos debe registrar, al momento de la transacción, una **Cotización de Referencia** (Dólar Blue/MEP o Índice UVA) que permita normalizar la serie histórica.

## **6.2. REGLA DE IMPUTACIÓN FINANCIERA (CIERRE DE TARJETA)**
**Contexto:** El "Gasto Económico" (cuando compro) y el "Gasto Financiero" (cuando pago) están desfasados en los Medios de Pago Diferidos.
* **Definición:** Para el cálculo de liquidez (Cash Flow), la fecha de egreso de fondos de una compra con Tarjeta de Crédito no es la fecha del ticket, sino la **Fecha de Vencimiento del Resumen** correspondiente.
* **Implementación Futura:** Incorporación de una tabla `calendario_cierres` para proyectar automáticamente cuándo impactará realmente el gasto en la cuenta bancaria.

## **6.3. REGLA DE INMUTABILIDAD HISTÓRICA (SOFT DELETE)**
**Contexto:** Eliminar físicamente un registro maestro (ej: borrar una Categoría vieja) rompe la integridad referencial de los movimientos históricos asociados.
* **Definición:** Está prohibido el uso de `DELETE` en tablas paramétricas que hayan tenido uso.
* **Implementación Futura:** Se aplicará el patrón de **Borrado Lógico**. Las tablas tendrán un campo `activo = False`. El ítem deja de aparecer en los selectores de carga, pero sigue existiendo para los reportes históricos.

## **6.4. REGLA DE APROPIACIÓN PRESUPUESTARIA**
**Contexto:** El registro de gastos es reactivo. La gestión financiera requiere proactividad.
* **Definición:** El sistema debe permitir definir "Topes de Gasto" (Presupuesto) por Categoría/Subcategoría mensual.
* **Implementación Futura:** Comparativa automática entre `Gasto Real` vs `Presupuesto`. El sistema alertará mediante un semáforo de cumplimiento (Verde/Amarillo/Rojo) cuando la ejecución se acerque al límite definido.



## [2026-01-31] Hito 3.1: Refactorización Modular (S.I.G.A.P.)
**Estado:** EN PROCESO DE ESTABILIZACIÓN
**Cambios:**
- Se implementó arquitectura Núcleo/Adaptador.
- `scripts/modulos/editor_gastos.py`: Contiene toda la lógica de UI, IA y Menús.
- `scripts/import_santander.py`: Adaptador ligero ETL.
**Próximos Pasos:**
- 🛠️ Continuar con Testing exhaustivo de `import_santander` y `editor_gastos`.
- Validar casos de borde (Excepciones, reversión de cambios, persistencia de IA).
- No avanzar a nuevos módulos hasta garantizar robustez del núcleo.