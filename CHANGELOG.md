# Changelog - S.I.G.A.P.

Todas las modificaciones notables a este proyecto serán documentadas en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

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

## [v0.1.1] - 2026-01-30 (Mejora de Modelo de Datos)
### 💎 Base de Datos
- **Refactorización de Categorías:** Separación de `Terreno` (Inversión) y `Casa` (Gasto).
- **Inteligencia de Datos:** Implementación de tabla `diccionario_terminos` para mapeo de sinónimos.
- **Normalización:** Ajuste de Subcategorías basado en análisis de CSVs históricos (Regla de Abstracción).
- **Medios de Pago:** Inclusión de Billeteras Virtuales (Lemon) y Cuentas de Terceros (Santander Mamá).
