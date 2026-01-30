# 🐙 GUÍA DE VERSIONADO Y GIT - PROYECTO FÉNIX

Este documento establece los estándares obligatorios para el control de versiones en el proyecto S.I.G.A.P.
Basado en [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) y [Semantic Versioning 2.0.0](https://semver.org/).

---

## 1. FORMATO DEL MENSAJE DE COMMIT
Cada commit debe tener una estructura predecible para facilitar la lectura humana y la generación automática de changelogs.

```text
<tipo>(<alcance opcional>): <descripción breve>
<LÍNEA EN BLANCO>
<cuerpo opcional>
<LÍNEA EN BLANCO>
<pie opcional>

```

### 🔹 Reglas de Oro

1. **Límite:** La primera línea no debe superar los **100 caracteres**.
2. **Imperativo:** Usa verbos como órdenes ("agrega", "corrige", "elimina") en lugar de pasado ("agregado", "corregí").
3. **Minúsculas:** La descripción empieza siempre en minúscula.
4. **Sin Punto:** No pongas punto final en la primera línea.

---

## 2. TIPOS DE CAMBIOS (TYPES)

El prefijo determina qué clase de cambio se introduce y cómo afecta al número de versión (SemVer).

| Tipo           | Significado                   | Impacto SemVer    | Ejemplo Rápido                           |
| -------------- | ----------------------------- | ----------------- | ---------------------------------------- |
| **`feat`**     | Nueva funcionalidad (Feature) | **MINOR** (0.x.0) | `feat(cli): agregar comando de reporte`  |
| **`fix`**      | Corrección de error (Bugfix)  | **PATCH** (0.0.x) | `fix(db): reparar fecha nula en sqlite`  |
| **`docs`**     | Solo documentación            | -                 | `docs: actualizar roadmap`               |
| **`style`**    | Formato (espacios, comas)     | -                 | `style: indentar codigo en main.py`      |
| **`refactor`** | Mejora interna (limpieza)     | -                 | `refactor(scripts): optimizar bucle for` |
| **`test`**     | Tests nuevos o corregidos     | -                 | `test: agregar prueba de carga`          |
| **`chore`**    | Mantenimiento/Configuración   | -                 | `chore: actualizar .gitignore`           |

> **⚠️ BREAKING CHANGE:** Si un commit rompe la compatibilidad anterior (ej: cambias el nombre de una tabla y los scripts viejos dejan de andar), se debe añadir `!` después del tipo (ej: `feat!: ...`) o poner `BREAKING CHANGE:` en el pie. Esto incrementa la versión **MAJOR** (x.0.0).

---

## 3. ALCANCE (SCOPE)

Indica el módulo o contexto afectado. Debe ir entre paréntesis.

* **`db`**: Base de datos, esquemas, SQL, Seed Data.
* **`scripts`**: Scripts de Python en `/scripts` (`factory_reset`, `input_manager`).
* **`cli`**: Interfaz de línea de comandos (`manage.py`).
* **`docs`**: Archivos Markdown (`ROADMAP`, `CHANGELOG`, `ADRs`).
* **`config`**: Archivos de configuración (`.gitignore`, `requirements.txt`).
* **`data`**: Archivos de datos crudos (CSVs).

---

## 4. EJEMPLOS PRÁCTICOS (CASOS REALES)

### A. Documentación (Lo que hacemos ahora)

Estás editando este archivo o el ROADMAP.

```text
docs(guia): mejorar formato y agregar ejemplos practicos

```

### B. Base de Datos (Cuando modificas el script de reset)

Cambiaste una categoría o agregaste una tabla nueva.

```text
feat(db): agregar categoria 'Mascotas' en seed data

```

*(Es `feat` porque agregas capacidad al sistema. Si solo corriges un error de tipeo en una categoría existente, sería `fix`).*

### C. Scripting (Cuando programas lógica)

Modificaste `input_manager.py` para que pida confirmación antes de guardar.

```text
feat(scripts): agregar confirmacion de usuario antes de guardar gasto

```

### D. Bugfix (Cuando algo explota)

El sistema fallaba al ingresar montos con decimales.

```text
fix(scripts): permitir flotantes en input de monto

Anteriormente la función int() rompía si el usuario ponía 10.50.
Se cambió por float() para soportar centavos.

```

### E. Mantenimiento (Cuando tocas Git o carpetas)

Agregaste archivos CSV al `.gitignore` para no subirlos por error.

```text
chore(config): ignorar archivos csv temporales

```

---

## 5. RELACIÓN CON SEMANTIC VERSIONING (SEMVER)

El proyecto sigue el esquema `MAJOR.MINOR.PATCH` (Ej: 1.2.5).

* **MAJOR (1.0.0):** Cambios incompatibles (Breaking Changes).
* **MINOR (0.1.0):** Nuevas funcionalidades compatibles (`feat`).
* **PATCH (0.0.1):** Corrección de errores compatibles (`fix`).

```

---