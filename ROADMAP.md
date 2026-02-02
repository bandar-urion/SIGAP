# 🗺️ ROADMAP S.I.G.A.P.

Este documento rastrea el progreso del desarrollo del Proyecto Fénix.
Actúa como la única fuente de verdad sobre el estado de las tareas y la planificación futura.

---

## 🎯 HITO 1: INFRAESTRUCTURA & CIMIENTOS (v0.1)
**Objetivo:** Establecer un entorno de desarrollo profesional, seguro y versionado.

- [x] **Arquitectura de Datos**
    - [x] Definición de Modelo Relacional (3NF).
    - [x] Script de Inicialización (`factory_reset_normalized.py`).
    - [x] Definición de Reglas de Gobernanza (Constraints & Triggers lógicos).
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

- [ ] **Importador Bancario**
    - [x] Definir formato estándar de importación (CSV Intermedio).
    - [x] Parser para Santander (XLS/CSV -> DB).
    - [ ] Parser para MercadoPago.
    - [x] Lógica de Deduplicación (`num_referencia`).
    - [x] Lógica de "Smart Archive" (Gestión de Pendientes).
    - [x] **Portabilidad**
    - [x] Soporte Cross-Platform (Windows/Linux/Termux).


---

## 🔮 BACKLOG (Ideas Futuras)
- [ ] **Interfaz Gráfica:** Migrar de Terminal a Web (Streamlit o Flask local).
- [ ] **Inteligencia Artificial:** Asistente para categorización automática de gastos.
- [ ] **Auditoría:** Reporte de desvíos de presupuesto.
- [ ] **Backup:** Script de exportación automática a JSON/SQL.

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
