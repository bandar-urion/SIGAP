# 📋 Protocolo de Certificación UI - S.I.G.A.P.

Este checklist define los vectores de prueba manuales y automatizados para garantizar la resiliencia del Motor UI operando bajo el KVM/Termux y la integridad de la base de datos SQLite.

## Fase 1: Estrés de Hardware (Resiliencia I/O KVM)
- [ ] **Prueba de Inundación (Flood Test):** Mantener presionada la flecha `⬇️` por 3s. Validar scroll sin crash y sin filtrado de secuencias ANSI (`\x1b[B`).
- [ ] **Prueba de Límites (Boundary Test):** Intentar subir más allá del registro [1] y bajar más allá del último. El cursor debe detenerse sin `IndexError`.

## Fase 2: Máquina de Estados (Navegación y Edición)
- [ ] **Descarte Rápido:** Presionar `⮕`. Validar estado [DESCARTADO], color gris y auto-avance.
- [ ] **Recuperación:** Presionar `⬅` sobre un descartado. Validar retorno a estado [PEND] o [AUTO].
- [ ] **Freno de Inercia:** Editar con `Enter`, tipear basura y presionar flecha. Validar aborto instantáneo sin guardar basura en buffer.

## Fase 3: Flujos de Negocio y UX
- [ ] **Motor Híbrido (Fast-Pick):** Ingresar índice numérico en edición y presionar `Enter`. Validar selección instantánea.
- [ ] **Motor Híbrido (Texto):** Tipear string parcial (ej: "Sup") y presionar `Enter`. Validar autocompletado.
- [ ] **Apilamiento Visual:** Validar que los pasos CC > CAT > SUBCAT queden impresos en pantalla sin parpadeo ciego.
- [ ] **Leyendas Dinámicas:** Validar que el menú inferior cambie contextualmente entre Modo Navegación y Modo Edición.

## Fase 4: Excepciones (Manejo de Cuotas)
- [ ] **Vía Rápida (Silent Apply):** Seleccionar subcategoría con amortización predefinida. Validar asignación silenciosa.
- [ ] **Intervención Manual (Tecla `C`):** Presionar `C`, ingresar cuotas. Validar prefijo `💳 [1/X]`. Ingresar `1` o `0` para anular.

## Fase 5: Persistencia Atómica (Botón `G`)
- [ ] **Commit Visual:** Presionar `G`. Validar que consola reporte la misma cantidad de guardados que los registros [OK]/[AUTO].
- [ ] **Idempotencia (INSERT OR IGNORE):** Re-importar el mismo Excel. Validar rechazo silencioso de duplicados (por `num_referencia`).

## Fase 6: Paginación y Renderizado Dinámico
- [ ] **Límites de Viewport:** Interfaz con movimientos límite (ej: 10 y 11). Validar transición de página sin líneas fantasma.
- [ ] **Trunco Visual:** Movimiento con descripción de >100 caracteres. Validar trunco con `..` sin romper la tabla ASCII.
- [ ] **Persistencia en Scroll:** Editar registro 1 a [OK], bajar fuera de pantalla, volver a subir. Validar retención de estado visual.

## Fase 7: Motor de Aprendizaje (Diccionario IA)
- [ ] **Prompt de Memorización:** Validar sugerencia de patrón al finalizar clasificación manual.
- [ ] **Cancelación de IA:** Presionar `N` o `ESC`. Validar imputación de un solo uso sin guardar sinónimo.
- [ ] **Edición de Clave:** Borrar sugerencia y tipear frase propia. Validar existencia en descripción original (anti-alucinación).

## Fase 8: Resiliencia de Inputs (Edge Cases)
- [ ] **Enter en Vacío:** Presionar `Enter` sin texto en búsqueda. Validar `beep_error()` sin avance aleatorio.
- [ ] **Creación No Autorizada:** Intentar crear (+) un CC si `permitir_nuevo=False`. Validar bloqueo de INSERT.
- [ ] **Caracteres Hostiles:** Tipear `%` o `*`. Validar limpieza de buffer para prevenir SQL Injection accidental.

## Fase 9: Estrés de Ingesta (Fábrica de Veneno / Mock .xlsx)
- [ ] **Excel Mutante:** Cambios de formato o headers corridos. Validar captura de `KeyError` sin tocar DB.
- [ ] **Type Juggling / Nulls:** Montos como texto (`$ 1.500`) o filas `NaN`. Validar casteo o descarte limpio.
- [ ] **Inversión de Signos:** Compra y devolución exacta consecutiva. Validar renderizado visual sin romper columnas.
- [ ] **Colisiones Internas:** Excel con filas de igual referencia. Validar rechazo de duplicados en la misma transacción.
- [ ] **Mix de Estados:** Sumario inicial debe calcular con exactitud la matemática de Omitidos + Autos + Nuevos = Total.
