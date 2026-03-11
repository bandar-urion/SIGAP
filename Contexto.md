# 🦅 S.I.G.A.P. — CONTEXTO DE SESIÓN
> **Instrucciones de uso:** Al iniciar una sesión nueva con Claude, pegá este archivo completo.
> Al cerrar la sesión, pedile a Claude que genere el bloque `## ÚLTIMA SESIÓN` actualizado.
> **Importante:** indicar siempre en qué entorno se está trabajando hoy.

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

### 📱 Entorno B — Mobile Empresa
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
- `feature/importar-movimiento` — rama actual, Parser + Inbox UI

> Recordatorio: antes de cada commit verificar que estamos en la branch correcta.
> `git branch --show-current`

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
ControlGastos/
├── sigap.py                          # Orquestador CLI (status / reset)
├── sigap_config.py                   # Config centralizada (lee sigap.cfg)
├── sigap.cfg                         # Parámetros: DB, rutas, UI, LOG_LEVEL
├── Contexto.md                       # ← Este archivo (guía de sesión IA)
├── data/
│   ├── sigap.db                      # Base de datos SQLite (fuente de verdad)
│   ├── inbox/                        # Excel bancarios a procesar
│   ├── processed/                    # Excel ya importados
│   └── rejected/                     # Excel rechazados por validación
├── scripts/
│   ├── import_santander.py           # Parser Excel Santander → Inbox UI
│   ├── factory_reset_normalized.py   # Reset + sembrado de DB
│   ├── factory_reset_preserve_learning.py
│   ├── modulos/
│   │   └── inbox_movimientos.py      # ⭐ Motor principal (UI + lógica de negocio)
│   └── utils/
│       ├── config_grafica.py         # Constantes ANSI, colores, dimensiones UI
│       └── auditar_db.py
├── tests/
│   ├── test_cerebro.py               # Motor IA (regex + matching)
│   ├── test_importacion.py           # Integridad DB + deduplicación
│   ├── test_database_init.py         # Esquema SQL
│   ├── test_avanzado.py              # Casos extremos / tortura
│   ├── test_gobernanza_similitud.py  # ⭐ Motor de Gobernanza (25 tests)
│   └── test_ui_inbox_movimientos.py  # UI mocks
├── docs/
│   ├── ADR-001-Motor-Base-Datos.md
│   ├── ADR-002-Modelo-Gobernanza.md
│   └── GUIA_GIT.md
└── logs/
    └── sigap_tecnico.log             # Log técnico rotativo
```

---

## VERSIÓN ACTUAL: v0.7.0

| Módulo | Estado |
|---|---|
| Parser Santander (XLS → Inbox) | ✅ Funcional |
| Inbox UI (viewport, navegación, edición) | ✅ Funcional |
| Motor IA (diccionario + regex) | ✅ Funcional |
| Detección de cuotas (regex financiero) | ✅ Funcional |
| Cross-platform Termux/Windows | ✅ Funcional |
| Gobernanza Alta Subcategoría (Panel + 6 criterios) | ✅ Funcional |
| Sistema de logging (consola) | ⚠️ Parcial (falta FileHandler) |
| Auditoría en DB (`auditoria_movimientos`) | ⚠️ Parcial |
| `manage.py` unificado | ❌ Pendiente |
| Parser MercadoPago | ❌ Pendiente |
| Dashboard Streamlit | 🔮 Backlog |

---

## BUGS CONOCIDOS (PENDIENTES DE FIX)

> ✅ Sin bugs críticos conocidos al cierre de Sesión #5.
> Los bugs `tx → mov` (import_santander.py) y ruta DB (sigap.py) fueron
> resueltos en sesiones anteriores y verificados en código el 2026-03-10.

---

## PRÓXIMAS TAREAS (en orden de prioridad)

1. **[FEAT]** Agregar `FileHandler` al logging en `sigap_config.py`
2. **[FEAT]** Completar flujo de auditoría (`auditoria_movimientos`) en importación
3. **[FEAT]** Crear `manage.py` como CLI unificado
4. **[FEAT]** Robots de QA: `test_robot_crear_subcategoria_nueva` y `test_robot_rechazo_por_gobernanza`
5. **[FEAT]** Parser MercadoPago

---

## DECISIONES DE ARQUITECTURA INAMOVIBLES (NO DISCUTIR)

- **SQLite es la única DB.** No hay plans de migrar a Postgres/MySQL. (Ver ADR-001)
- **Sin GUI por ahora.** Terminal pura hasta que el core esté blindado.
- **Gobernanza antes que features.** No se agrega funcionalidad sin validaciones.
- **3NF estricta.** No se desnormalizan tablas por conveniencia.
- **`sigap_config.py` es el punto de entrada de configuración.** Nunca hardcodear rutas.
- **leer_byte() es el único lector de input.** Nunca usar input() estándar en flujos UI.

---

## ÚLTIMA SESIÓN

**Fecha:** 2026-03-10
**Sesión:** #6 — Metodología: Scripts de Apertura/Cierre de Sesión
**Entorno:** Entorno A (PC Casa · Windows · VSCode)
**Branch:** `feature/metodologia-sesiones`

**Lo que hicimos:**
- Decisión de crear rama paralela `feature/metodologia-sesiones` para no
  interferir con la sesión pendiente de cierre en Entorno B.
- Diseño y generación de `scripts/utils/sesion_inicio.py`: detecta automáticamente
  entorno (Windows/Termux), rama Git activa y timestamp. Solicita solo el objetivo.
- Diseño y generación de `scripts/utils/sesion_cierre.py`: calcula duración,
  solicita observaciones opcionales, actualiza `docs/SESIONES.md` y elimina
  el archivo temporal `.sesion_activa`.
- Creación de `docs/SESIONES.md`: bitácora de sesiones con entrada inicial
  para sesiones 1-5 como registro histórico.
- Aprendizaje documentado: Entorno A requiere `Ctrl+S` explícito antes de
  `git add`. El `git status` pre-commit detectó el `.gitignore` sin guardar.
- Commit + push a `origin/feature/metodologia-sesiones`.

**Archivos modificados:**
- `scripts/utils/sesion_inicio.py` — creado
- `scripts/utils/sesion_cierre.py` — creado
- `docs/SESIONES.md` — creado
- `.gitignore` — `.sesion_activa` agregado

**Próxima sesión (Entorno B — mañana):**
1. Cerrar sesión pendiente de hoy en `feature/importar-movimiento`
2. `git fetch origin` + merge de `feature/metodologia-sesiones`
3. Estrenar `sesion_inicio.py` en Termux

---
*Actualizado por Claude Sonnet · Sesión #6 · Proyecto Fénix v0.7.0*