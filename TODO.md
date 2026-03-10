# 🎯 S.I.G.A.P. - BACKLOG TÁCTICO UNIFICADO

Este documento reemplaza temporalmente las listas dispersas y establece el orden estricto de ejecución para evitar el "Overkill" arquitectónico.

## 🧹 FASE 0: DEUDA TÉCNICA DOCUMENTAL (INMEDIATO)
- [x] **Actualizar `DOCUMENTACION.md`:** Reemplazar toda mención de `carga_gastos.py` y `editor_gastos.py` por `inbox_movimientos.py` (Reflejo del Domain-Driven Design).
- [x] **Actualizar `CHANGELOG.md`:** Crear la entrada `[v0.7.0] - Refactor Semántico e Inbox`, documentando el paso de "Transacción" a "Movimiento" y la estandarización de Mocks.
- [ ] **Crear `docs/QA_UI_Checklist.md`:** Documentar las 9 fases de certificación manual (Estrés KVM, Máquina de Estados, Edge Cases).

## 🛡️ FASE 1: GOBERNANZA DE INBOX Y AUDITORÍA (ACTUAL)
*Objetivo: Blindar la base de datos (SQLite) contra errores humanos durante la carga rápida en Terminal.*
- [x] **Gobernanza de Alta (Tecla `+`):** *(Sesión #4 — 2026-03-09)*
    - [x] Interceptar tecla `+` en `inbox_movimientos.py` pausando el renderizado de la UI.
    - [x] Check 1 (Sintaxis): Aplicar `.strip().title()` para normalizar Nombres.
    - [x] Check 2 (Similitud): Detección de subcategorías similares.
    - [x] Check 3 (Descriptividad): Validar longitud y calidad del nombre.
    - [x] Check 4 (Frecuencia en lote): Detectar si el término ya aparece en el lote actual.
    - [x] Check 5 (Frecuencia histórica): Consultar DB para detectar patrones históricos.
    - [x] Check 6 (Duplicado exacto): Bloquear altas de subcategorías ya existentes.
    - [x] Panel de Gobernanza con 3 flujos: directo (ENTER), con similares, con justificación.
- [x] **Trazabilidad (Módulo Auditoría):** *(Sesión #4 — 2026-03-09)*
    - [x] Disparar `INSERT` en `auditoria_movimientos` con justificación del usuario tras cada alta.
- [ ] **Suite de QA (Robots de Prueba):** *(pendiente)*
    - [ ] Crear `test_robot_crear_subcategoria_nueva`.
    - [ ] Crear `test_robot_rechazo_por_gobernanza`.

## 🧠 FASE 2: INTELIGENCIA Y PROYECCIÓN (PRÓXIMO HITO)
*Objetivo: Dotar al sistema de inferencia financiera y ampliar la ingesta de datos.*
- [ ] **Desacoplamiento del Parser:** Extraer la lógica de Pandas en `import_santander.py` a una función aislada (`parsear_excel_santander`) para permitir testing sin UI.
- [ ] **Fábrica de Veneno (QA):** - [ ] Crear `scripts/utils/generar_mocks_xlsx.py` para generar Excels corruptos (NaN, formatos rotos, duplicados).
- [ ] Crear motor de pruebas `tests/test_stress_ingesta.py` para automatizar la validación y logueo de errores.
- [ ] **Sugerencia de Amortización Dinámica:** Si el sistema lee "Seguro" (Categoría), sugerir "12 cuotas" por defecto en la interfaz.
- [ ] **Vista Virtual de Proyección de Cuotas:** Script de reporte que calcule el peso de las cuotas a futuro sin escribir "movimientos fantasma" en la DB.
- [ ] **Ingesta Nivel 2 (Parser PDF):** Implementar `pdfplumber` o Regex avanzado para leer resúmenes de MasterCard/MercadoPago.

## 🚀 FASE 3: S.I.G.A.P. 2.0 (BACKLOG ESTRATÉGICO)
*Objetivo: Sacar al sistema de la Terminal y conectarlo a la red neuronal externa.*
- [ ] **Dashboard Streamlit:** Migrar la visualización a una interfaz web local (Gráficos, KPIs, Presupuestos).
- [ ] **Integración Gemini API:** Reemplazar el motor de Regex estático por llamadas a LLM para categorización semántica difusa.
- [ ] **Contenerización (Docker):** Crear `Dockerfile` y `docker-compose.yml` para aislar el entorno de Python/SQLite y hacerlo 100% agnóstico del SO (Termux/Windows).
