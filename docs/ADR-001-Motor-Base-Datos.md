# ADR-001: Selección del Motor de Base de Datos

* **Estado:** Aceptado
* **Fecha:** 2026-01-28
* **Decisores:** Martín (Lead), IA (Copilot)

## Contexto
El proyecto S.I.G.A.P. requiere un sistema de almacenamiento para datos financieros históricos y transaccionales.
Las herramientas previas (Hojas de Cálculo) presentaban problemas de integridad de datos, rendimiento con grandes volúmenes y fragilidad en las fórmulas.
Se requiere una solución que garantice privacidad total (Soberanía de Datos) y funcione en un entorno móvil (Android/Termux).

## Opciones Evaluadas
1. **Archivos CSV/JSON planos:** Fáciles de leer, pero sin integridad referencial ni capacidad de consulta compleja (SQL).
2. **Hojas de Cálculo (Excel/Sheets):** Flexibles, pero propensas a errores humanos y corrupción de datos. Dependencia de la nube (Sheets).
3. **Base de Datos Cloud (PostgreSQL/Firebase):** Potentes, pero introducen costos, latencia y dependencia de internet.
4. **SQLite (Local):** Relacional, archivo único, serverless.

## Decisión
Elegimos **SQLite 3**.

## Justificación
1.  **Integridad (ACID):** Soporta claves foráneas (Foreign Keys) y restricciones (Constraints) que impiden físicamente la carga de datos inválidos (ej: gastos sin categoría).
2.  **Portabilidad:** La base de datos es un único archivo `.db` que vive en el dispositivo del usuario, cumpliendo el requisito de privacidad y funcionamiento offline.
3.  **Compatibilidad:** Python tiene soporte nativo para SQLite, simplificando el stack tecnológico.
4.  **Cero Configuración:** No requiere un proceso servidor corriendo en background, ideal para los recursos limitados de un entorno móvil (Termux).

## Consecuencias
* **Positiva:** Integridad de datos garantizada por el motor.
* **Negativa:** Requiere construir herramientas (scripts/UI) para interactuar con los datos, ya que no se puede "abrir y editar" tan fácilmente como un Excel.