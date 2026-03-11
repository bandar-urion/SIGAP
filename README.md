# 🦅 S.I.G.A.P.
### Sistema Inteligente de Gestión y Auditoría Patrimonial
**Proyecto Fénix · Powered by Hybrid Intelligence (Human + AI)**

---

## ¿Qué es SIGAP?

SIGAP es una plataforma de **finanzas personales local, privada y sin nube**.  
Procesa extractos bancarios (Excel), los categoriza con un motor de IA propio y los almacena en SQLite.  
No depende de ningún servicio externo. El dato es tuyo, siempre.

---

## Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.12+ |
| Base de Datos | SQLite 3 (local) |
| Control de Versiones | Git |
| Interfaz | Terminal pura (Flow State UX) |

---

## Estructura del Proyecto

```
ControlGastos/
├── sigap.py                          # Orquestador CLI (status / reset)
├── sigap_config.py                   # Config centralizada (lee sigap.cfg)
├── sigap.cfg                         # Parámetros: DB, rutas, UI, LOG_LEVEL
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

## Inicio Rápido

### Requisitos
- Python 3.12+
- Git

### Instalación
```bash
# Clonar el repositorio
git clone <url-del-repo> ControlGastos
cd ControlGastos

# Inicializar la base de datos
python scripts/factory_reset_normalized.py

# Verificar estado del sistema
python sigap.py status
```

### Ejecutar los tests
```bash
python -m unittest discover tests
```

### Importar un extracto Santander
```bash
# Colocar el archivo .xlsx en data/inbox/
# Luego ejecutar:
python scripts/import_santander.py
```

---

## Filosofía del Proyecto

- **Soberanía del dato:** todo local, nada en la nube.
- **Gobernanza antes que features:** no se agrega funcionalidad sin validaciones.
- **Flow State UX:** terminal pura con viewport deslizante, sin menús, sin `input()` estándar.
- **3NF estricta:** no se desnormalizan tablas por conveniencia.
- **Sinergia Humano-IA:** el Analista aporta la lógica de negocio, la IA es el copiloto técnico.

---

## Modelo de Desarrollo: Humano-IA vs. AloneCoding

SIGAP no es desarrollado por una persona sola ni por una IA sola.
Es desarrollado por un equipo de dos con roles complementarios e irremplazables.

Este modelo no es una curiosidad metodológica. Es una ventaja de ingeniería concreta
frente al modelo tradicional de un desarrollador trabajando en solitario (AloneCoding).

| Dimensión | AloneCoding | Par Humano-IA |
|---|---|---|
| Puntos ciegos | El desarrollador no ve los suyos | El copiloto no tiene historia emocional con el código |
| Roles | Arquitecto e implementador en la misma persona | Roles separados, sin switching cost cognitivo |
| Code review | Con fricción social o inexistente | Crítica directa, sin agenda, sin jerarquía |
| Memoria de decisiones | Depende de la memoria del desarrollador | Externalizada en Contexto.md, ADRs, DECISIONES.md |
| Disponibilidad | Limitada por horarios y energía | Asimétrica: el copiloto está disponible siempre |
| Especialización | El desarrollador aprende o se detiene | On-demand: el equipo tiene el experto que el momento requiere |
| Documentación | Tarea separada, siempre postergada | Subproducto natural de la conversación técnica |
| Ego sobre el código | Presente, dificulta la crítica honesta | El copiloto no tiene inversión emocional en el código anterior |

**Lo que este modelo no es:**
No es "pedirle cosas a la IA". Es una conversación técnica entre pares
donde uno tiene el dominio del problema y el otro tiene el dominio de la implementación.
La calidad del resultado depende directamente de la calidad de esa conversación.

**Lo que garantiza la calidad del modelo:**
Los patrones de trabajo y protocolos de calidad están documentados en `VIBE_CODING_SKILLS.md`.
Ese documento es el estándar operativo que convierte la ventaja teórica del equipo
en práctica de ingeniería concreta y auditable.

---

## Estado Actual — v0.7.0

| Módulo | Estado |
|---|---|
| Parser Santander (XLS → Inbox) | ✅ Funcional |
| Inbox UI (viewport, navegación, edición) | ✅ Funcional |
| Motor IA (diccionario + regex) | ✅ Funcional |
| Detección de cuotas (regex financiero) | ✅ Funcional |
| Cross-platform Termux/Windows | ✅ Funcional |
| Gobernanza Alta Subcategoría (Panel + 6 criterios) | ✅ Funcional |
| Sistema de logging (consola + archivo) | ✅ Funcional |
| Auditoría en DB (`auditoria_movimientos`) | ⚠️ Parcial |
| `manage.py` unificado | ❌ Pendiente |
| Parser MercadoPago | ❌ Pendiente |
| Dashboard Streamlit | 🔮 Backlog |

---

## Documentación

| Documento | Descripción |
|---|---|
| `DOCUMENTACION.md` | Constitución del sistema: reglas de negocio, arquitectura, UX |
| `ROADMAP.md` | Hoja de ruta y estado de hitos |
| `VIBE_CODING_SKILLS.md` | Estándar de desarrollo Humano-IA: patrones y protocolos de calidad |
| `CHANGELOG.md` | Historial de versiones |
| `TODO.md` | Backlog táctico unificado |
| `Contexto.md` | Guía de sesión para el copiloto IA |
| `docs/ADR-001` | Decisión: SQLite como motor de DB |
| `docs/ADR-002` | Decisión: Modelo de Gobernanza |
| `docs/GUIA_GIT.md` | Estándares de commits y versionado |

---

## Entornos de Desarrollo

| Entorno | Hardware | Terminal | Rutas |
|---|---|---|---|
| A — PC Casa | Windows 11 · i9-10900KF · 80GB RAM | PowerShell / CMD | `\` |
| B — Mobile | Samsung S21 Ultra · USB Hub | Termux (Linux/Android) | `/` |

---

*S.I.G.A.P. — Proyecto Fénix · Martín · 2026*
