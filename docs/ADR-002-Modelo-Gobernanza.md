# ADR-002: Modelo de Gobernanza y Reglas de Negocio

* **Estado:** Aceptado
* **Fecha:** 2026-01-28
* **Decisores:** Martín (Lead), IA (Copilot)

## Contexto
El sistema debe validar reglas de negocio complejas (ej: "No usar nombres de marcas en subcategorías").
Inicialmente, se consideró "harcodear" (escribir en código Python) estas validaciones. Sin embargo, esto hace que cambiar una regla requiera modificar y redesplegar el código fuente.

## Opciones Evaluadas
1.  **Validación en Código (Python):** `if categoria == 'Coto': raise Error`. Rápido, pero rígido.
2.  **Validación en Base de Datos (Triggers):** Complejo de mantener y depurar en SQLite.
3.  **Modelo Híbrido Declarativo (Data-Driven):** Las reglas se almacenan como datos en tablas y el código las lee para aplicarlas.

## Decisión
Implementamos un **Modelo Relacional de Gobernanza** con dos tablas:
1.  `reglas_catalogo`: Define la regla (Constitución).
2.  `reglas_vinculos`: Asocia la regla a n-tablas (Jurisdicción).

## Justificación
* **Flexibilidad:** Permite modificar descripciones, tipos de alerta (Bloqueante/Warning) o reasignar reglas a nuevas tablas sin tocar una sola línea de código Python.
* **Reusabilidad:** Una misma regla (ej: "Generalidad") puede aplicarse a múltiples entidades (Categorías y Subcategorías) sin duplicar la lógica, solo agregando un registro en la tabla de vínculos.
* **Auditoría:** Facilita generar reportes de "Qué reglas aplican a qué tabla" mediante consultas SQL simples.

## Consecuencias
* **Positiva:** Alta mantenibilidad y escalabilidad de la lógica de negocio.
* **Negativa:** Requiere un join adicional (`JOIN`) en las consultas para recuperar las reglas aplicables.