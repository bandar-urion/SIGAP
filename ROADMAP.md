# 🗺️ ROADMAP S.I.G.A.P.

Este documento rastrea el progreso del desarrollo del Proyecto Fénix.
Actúa como la única fuente de verdad sobre el estado de las tareas y la planificación futura.

---
- [x] **Documentación Core**
    - [x] Manifiesto y Filosofía.
    - [x] Metodología de Desarrollo (Protocolo Fénix).
    - [x] Reglas de Negocio detalladas.
- [x] **Control de Versiones (Git Local)** ⬅️ *PRIORIDAD ALTA*
    - [x] Inicializar repositorio (`git init`).
    - [x] Configurar `.gitignore` (Ignorar DBs, temporales y sensibles).
    - [x] Primer Commit (Base Line).
- [ ] **Orquestación (Tooling)**
    - [ ] Crear `manage.py` (CLI unificado para administrar el sistema).
    - [ ] Integrar funciones de reset y test en el orquestador.
    - [x] Suite de Tests Unitarios (`tests/`).
    - [x] `test_gobernanza_similitud.py` — 25 tests (Sesión #4 · 2026-03-09).

---

## [Requisito] Sistema de Trazabilidad y Control
- [ ] **Módulo Logging (Registro Tecnico):**

    <u>*Alcance</u>:* sistema - funcional/administrativo - tecnico/desarrollador.  
    <u>*Implementacion</u>:* modular.  
    <u>*Objetivo</u>:* capturar el comportamiento interno del software para facilitar el mantenimiento y la resolución de errores técnicos.  
    <u>*​Valor para el Proyecto</u>:* elimina la "incertidumbre" ante un fallo. En lugar de adivinar por qué no cargó un archivo, el log brinda la causa técnica.  
    <u>*Funcionalidades Clave</u>:*  
    - [ ] ​Niveles de Gravedad: diferenciar entre información general (INFO), advertencias (WARNING) y errores críticos (ERROR).  
    - [ ] Persistencia: guardado automático en un archivo físico (.log) con rotación (para que el archivo no crezca infinitamente).
    - [ ] ​Contexto de Ejecución: registrar la hora exacta, el módulo donde ocurrió el evento y la línea de código (si es un error).

- [ ] **Módulo Auditoría (Funcional):** 

    <u>​*Alcance</u>*: sistema - funcional/administrativo - usuario final.  
    <u>*​Objetivo</u>*: mantener un historial inalterable de las acciones realizadas sobre los datos del sistema.  
    <u>*Implementacion</u>:* modular.  
    <u>*​Valor para el Proyecto</u>:* seguridad y transparencia. Es lo que te permite reconstruir la historia de tus finanzas o agenda si algo parece no cuadrar.  
    <u>*Funcionalidades Clave</u>:*  
    - [ ] Crear tabla `auditoria_movimientos` para registrar cada proceso de importación y acciones del usuario en SIGAP V2.  
    - [ ] ​Trazabilidad de Movimientos: Registrar quién, cuándo y qué se modificó (ej: "Importación de 50 registros desde Excel realizada con éxito").  
    - [ ] ​Integridad de Datos: Guardar el estado "antes" y "después" en caso de ediciones críticas.  
    - [ ] ​Reporte de Discrepancias: Si un movimiento no pudo ser auditado o importado por reglas de negocio, debe quedar marcado en una tabla específica de la base de datos.  
    - [ ] Validación en Importar_Movimiento: el módulo debe reportar éxito/falla tanto en el log técnico como en la exacto (incluyendo milisegundos) de cada entrada para asegurar el orden cronológico absoluto, vital en procesos de importación masiva.

---

---

## 🚀 HITO 2: OPERATORIA MANUAL (v0.2 - MVP)
**Objetivo:** Lograr que el sistema sea funcional para la carga y consulta diaria vía Terminal.

- [ ] **Carga de Datos (Input)**
    - [ ] Desarrollar función de alta de Movimiento (INSERT).
    - [ ] Implementar validaciones de Gobernanza en tiempo real (Python).
- [ ] **Consultas Básicas (Output)**
    - [ ] Reporte: "Últimos 10 movimientos".
    - [ ] Reporte: "Saldos por Centro de Costo".
    - [ ] Reporte: "Alerta de Vencimientos (Agenda)".
- ​[ ] **Implementar carga inteligente con sinónimos (diccionario_terminos)**

---

## ⚙️ HITO 3: AUTOMATIZACIÓN & MASIVIDAD (v0.3 - v0.5)
**Objetivo:** Reducir la carga manual procesando archivos bancarios.

- [ ] **Branch: feature/importar-movimiento**
    - [ ] Definir formato estándar de importación (CSV Intermedio).
    - [x] Parser para Santander (XLS/CSV -> DB).
    - [ ] Parser para MercadoPago.
    - [x] Lógica de Deduplicación (`num_referencia`).
    - [x] Lógica de "Smart Archive" (Gestión de Pendientes).
    - [ ] Validacion atomica de carga de movimientos:  
    el proceso de importación no se dará por "exitoso" si para cada movimiento no se cumplieron tres pasos:  
        - [ ] se guardó el movimiento en la DB.  
        - [ ] se registró el evento en el archivo de Log (técnico).  
        - [ ] se guardó el "antes y después" en la tabla "auditoria_movimientos" (funcional).
    - [ ] **Portabilidad**
    - [ ] Soporte Cross-Platform (Windows/Linux/Termux).
    - [ ] Carga de CC - C - SC si no existen para el movimiento actual?
    ​

---

## 🔮 BACKLOG (Ideas Futuras)
- [ ] **Interfaz Gráfica:** migrar de Terminal a Web (Streamlit o Flask local).
- [ ] **Inteligencia Artificial:** asistente para categorización automática de gastos.
- [ ] **Auditoría Presupuestaria:** reporte de desvíos de presupuesto.
- [ ] **Backup:** script de exportación automática a JSON/SQL.

## 🔮 BACKLOG (Gobernanza Futura)
*Implementación técnica de las reglas definidas en la Sección 6 de DOCUMENTACION.md*

- [ ] **Soporte Multimoneda (Regla 6.1)**
    - [ ] Agregar columna `cotizacion_ref` en tabla movimientos.
    - [ ] Integrar API de Dólar/UVA para consultas históricas.
- [ ] **Gestión de Tarjetas Avanzada (Regla 6.2)**
    - [ ] Crear tabla `calendario_cierres`.
    - [ ] Algoritmo de cálculo de fecha de pago real.
- [ ] **Integridad Histórica (Regla 6.3)**
    - [ ] Migrar `DELETE` físicos a `UPDATE activo=false`.
    - [ ] Adaptar todas las consultas SQL para filtrar por `activo=true`.
- [ ] **Presupuestos (Regla 6.4)**
    - [ ] Crear tabla `presupuestos_mensuales`.
    - [ ] Reporte de desvío de gastos.
