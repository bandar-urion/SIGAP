# MAPA_TESTS.md — Suite de Tests de S.I.G.A.P.

> Generado: 2026-04-12  
> Suite: `python -m unittest discover tests`  
> Archivos analizados: 10  
> Total de tests: 71

---

## test_aislamiento_cuotas.py

**Módulo cubierto:** `scripts/modulos/inbox_movimientos.py` — lógica de asignación de cuotas en RAM

### `TestAislamientoFinanciero`

| Método | Descripción |
|--------|-------------|
| `test_aislamiento_de_cuotas_manuales` | Verifica que asignar cuotas a un movimiento no contamine (no escriba) la columna `amortizacion_default` de la subcategoría en la DB. |

---

## test_gobernanza_similitud.py

**Módulo cubierto:** `scripts/modulos/inbox_movimientos.py` — motor de detección de similitud (función `detectar_similares`) y lógica de frecuencia/justificación

### `TestGobernanzaSimilitud`

| Método | Descripción |
|--------|-------------|
| `test_contencion_nuevo_dentro_existente` | 'Super' está contenido en 'Supermercado' → debe alertar (criterio A). |
| `test_contencion_existente_dentro_nuevo` | 'Gas Y Combustible' contiene a 'Combustible' → debe alertar (criterio A). |
| `test_contencion_exacta_no_duplica_con_paso3` | Nombre exacto igual a uno existente también detecta similitud. |
| `test_prefijo_comun_farmacia` | 'Farma' comparte prefijo 'farm' (4+ chars) con 'Farmacia' → debe alertar (criterio B). |
| `test_prefijo_comun_seguro` | 'Seguro Vida' comparte prefijo 'seguro' con 'Seguro Auto' → debe alertar (criterio B). |
| `test_prefijo_corto_no_alerta` | Prefijo de solo 2 chars ('se') no debe generar alerta por prefijo. |
| `test_palabras_clave_transporte` | 'Uber Transporte' comparte la palabra 'transporte' con 'Transporte Público' → debe alertar (criterio C). |
| `test_palabras_clave_servicios` | 'Servicios Digitales' comparte 'servicios' con 'Servicios Básicos' → debe alertar (criterio C). |
| `test_palabras_cortas_ignoradas` | Palabras de ≤2 chars ('de', 'la') no deben generar match. |
| `test_sin_similitud_totalmente_nuevo` | 'Netflix' no tiene similitud con nada del catálogo → lista vacía. |
| `test_sin_similitud_gimnasio` | 'Gimnasio' no matchea nada del catálogo → sin alerta. |
| `test_sin_similitud_colegio` | 'Colegio Cuota' no matchea nada → sin alerta. |
| `test_caso_real_desayuno_almuerzo` | 'Cafe Desayuno' comparte 'desayuno' con 'Desayuno' → debe alertar. |
| `test_caso_real_restaurant_vs_restaurante` | 'Restaurant' está contenido en 'Restaurante' → debe alertar. |
| `test_caso_real_tv_sin_similitud` | 'Smart Tv' es completamente nuevo → sin alerta. |
| `test_caso_real_nafta_combustible` | 'Nafta' no tiene similitud directa con 'Combustible' → sin alerta. |

### `TestGobernanzaFrecuencia`

| Método | Descripción |
|--------|-------------|
| `test_freq_lote_multiple` | 'Electricidad' aparece 3 veces en el lote → `freq_lote = 3`. |
| `test_freq_lote_unica` | 'Smart Tv' aparece solo 1 vez en el lote → `freq_lote = 1`. |
| `test_freq_lote_ninguna` | 'Gimnasio' no aparece en el lote → `freq_lote = 0`. |
| `test_requiere_justificacion_primera_vez` | Sin historial y solo 1 ocurrencia en lote → `requiere_justificacion = True`. |
| `test_no_requiere_por_historial` | Con historial existente → no requiere justificación aunque sea nuevo en lote. |
| `test_no_requiere_por_lote_multiple` | Aparece 3 veces en el lote → no requiere justificación. |
| `test_no_requiere_ambas_fuentes` | Con historial y múltiples en lote → verde total, sin fricción. |
| `test_caso_real_electricidad_nueva` | Electricidad: primera vez (freq_lote=1, freq_hist=0) → pide justificación. |
| `test_caso_real_tv_unica` | Smart TV: gasto único, sin historial → pide justificación. |

---

## test_config.py

**Módulo cubierto:** `sigap_config.py` — configuración de rutas y compatibilidad cross-platform

### `TestConfiguracionMultiplataforma`

| Método | Descripción |
|--------|-------------|
| `test_get_db_path_es_absoluta` | La ruta retornada por `get_db_path()` debe ser absoluta y terminar en `sigap.db`. |
| `test_get_path_normaliza_barras` | Las rutas respetan el separador del OS (`os.sep`), compatibles con Windows y Termux. |

---

## test_motor_clasificacion.py

**Módulo cubierto:** `scripts/modulos/inbox_movimientos.py` — limpieza de texto (`limpiar_texto_visual`), detección de cuotas (`detectar_cuotas_regex`), motor de clasificación (`reanalizar_inteligencia`)

### `TestLimpiezaTexto`

| Método | Descripción |
|--------|-------------|
| `test_elimina_prefijos_bancarios` | `limpiar_texto_visual()` elimina prefijos bancarios genéricos como "Compra con tarjeta de debito", "DEBITO DIRECTO", "Pago DEBIN". |
| `test_normaliza_espacios` | Trim y colapso de espacios múltiples en la descripción. |

### `TestMotorCuotasValidos`

| Método | Descripción |
|--------|-------------|
| `test_formato_barra_estandar` | `03/12` en descripción → cuota 3 de 12. |
| `test_formato_barra_ultimo` | `12/12` → última cuota correctamente reconocida. |
| `test_formato_barra_primero` | `01/12` → primera cuota de 12. |
| `test_formato_barra_corto` | `01/03` → plan de 3 cuotas. |
| `test_formato_cta_solo_actual` | `CTA 2` → cuota actual=2, total=0 (comportamiento documentado del regex). |
| `test_formato_cta_numerico` | `CTA 3` → solo cuota actual=3 sin total. |

### `TestMotorCuotasTrampasFechas`

| Método | Descripción |
|--------|-------------|
| `test_fecha_completa_con_anio` | `DD/MM/AAAA` no debe confundirse con cuotas → (0, 0). |
| `test_fecha_completa_vto` | `VTO DD/MM/AAAA` no debe confundirse con cuotas → (0, 0). |
| `test_rango_de_fechas_del_al` | `PERIODO DEL 01/12 AL 31/12` es un rango de fechas, no cuotas → (0, 0). |
| `test_vencimiento_vto` | `VTO 10/05 CIERRE` es un vencimiento, no cuotas → (0, 0). |

### `TestMotorCuotasLogicaImposible`

| Método | Descripción |
|--------|-------------|
| `test_cuota_actual_mayor_al_total` | `13/12` es imposible (actual > total) → rechazado como (0, 0). |
| `test_total_exagerado` | `01/99` supera el límite de 60 cuotas del sistema → rechazado como (0, 0). |

### `TestMotorClasificacion`

| Método | Descripción |
|--------|-------------|
| `test_match_termino_simple` | 'COTO' en descripción matchea la regla del diccionario → subcategoría 'Supermercado'. |
| `test_match_termino_compuesto` | Término compuesto 'TRANSFERENCIA A JOSE' matchea texto más largo correctamente. |
| `test_no_match_descripcion_desconocida` | Descripción sin términos del diccionario → `ia_match = False`. |

### `TestInferenciaContexto`

| Método | Descripción |
|--------|-------------|
| `test_relleno_automatico_cc` | El motor infiere el Centro de Costo histórico preferido de una subcategoría y lo asigna automáticamente (`estado = 'AUTO'`). |

---

## test_contrato_santander.py

**Módulo cubierto:** `scripts/import_santander.py` — contract test del formato Excel de Santander Río  
**Nota:** Los tests `test_02` a `test_07` se saltean automáticamente si no hay `.xlsx` en `data/inbox/`.

### `TestContratoSantander`

| Método | Descripción |
|--------|-------------|
| `test_01_archivo_presente_en_inbox` | Verifica que exista al menos un `.xlsx` válido (no lock-file) en `data/inbox/`. |
| `test_02_lectura_sin_errores` | El archivo se puede abrir con `openpyxl` y `skiprows=13` sin excepciones. |
| `test_03_columnas_requeridas_presentes` | Todas las columnas que el parser necesita están presentes en el Excel. |
| `test_04_sin_columnas_desconocidas_nuevas` | Detecta (sin bloquear) si Santander agregó columnas nuevas no documentadas. |
| `test_05_columna_fecha_parseable` | La columna `Fecha` contiene valores convertibles a datetime con `dayfirst=True`. |
| `test_06_hay_movimientos_con_monto` | La fusión de columnas CA+CC produce al menos un movimiento con `Monto_Real != 0`. |
| `test_07_skiprows_produce_cabecera_valida` | Después de saltar `SKIPROWS=13` filas, los nombres de columna son strings (no fechas/números). |

### `TestContratoSantanderInforme`

| Método | Descripción |
|--------|-------------|
| `test_00_diagnostico_general` | Imprime un diagnóstico completo del archivo en inbox; siempre pasa (test informativo). |

---

## test_database_init.py

**Módulo cubierto:** `scripts/factory_reset_normalized.py` — validez del esquema SQL

### `TestInfraestructuraDB`

| Método | Descripción |
|--------|-------------|
| `test_tablas_esenciales` | Verifica que el esquema SQL básico sea válido creando las tablas `movimientos` y `centros_costo` en una DB en memoria. |

---

## test_gui_logic.py

**Módulo cubierto:** `scripts/modulos/inbox_movimientos.py` — lógica de filtrado del selector UI

### `TestNavegacion`

| Método | Descripción |
|--------|-------------|
| `test_filtrado_letras_seguidas` | Al escribir 'FA', el filtro retorna exactamente las opciones que contienen 'FA' en el nombre. |
| `test_filtrado_sin_coincidencias` | Buffer con texto sin coincidencias retorna lista vacía sin crashear. |

---

## test_importacion.py

**Módulo cubierto:** `scripts/import_santander.py` — deduplicación por `num_referencia`

### `TestIntegridadBancaria`

| Método | Descripción |
|--------|-------------|
| `test_evitar_duplicados_crash` | `INSERT OR IGNORE` rechaza un movimiento duplicado silenciosamente: no lanza `IntegrityError` y la tabla queda con exactamente 1 registro. |

---

## test_ui_inbox_movimientos.py

**Módulo cubierto:** `scripts/modulos/inbox_movimientos.py` — loop principal de UI (`iniciar_inbox_movimientos`) con mocks de I/O

### `TestUiInboxMovimientos`

| Método | Descripción |
|--------|-------------|
| `test_01_1_inundacion` | Flood Test: 20 comandos DOWN seguidos no rompen el loop ni causan excepción. |
| `test_01_2_limites` | Boundary Test: UP/DOWN en los extremos del viewport no crashean el sistema. |
| `test_02_1_descarte_rapido` | Flecha derecha marca el movimiento con estado `DESCARTADO`. |
| `test_02_2_recuperacion` | Flecha izquierda sobre un movimiento descartado restaura el estado `PENDIENTE`. |
| `test_02_3_freno_inercia` | ESC dentro del modo edición aborta limpiamente sin modificar el estado del movimiento. |
| `test_03_1_motor_hibrido_numerico` | Fast-pick numérico completa el embudo CC → CAT → SUBCAT y el movimiento queda en estado `LISTO`. |
| `test_03_2_motor_hibrido_texto` | Búsqueda por texto en motor híbrido completa el embudo y asigna Centro de Costo correctamente. |
| `test_04_2_intervencion_manual` | Tecla `C` permite asignar cuotas manualmente (`cuotas_totales = 3`). |

---

## test_robots_gobernanza.py

**Módulo cubierto:** `scripts/modulos/inbox_movimientos.py` — funciones `evaluar_gobernanza` y `render_panel_gobernanza`

### `TestRobotsGobernanza`

| Método | Descripción |
|--------|-------------|
| `test_robot_crear_subcategoria_nueva` | Nombre nuevo sin duplicados ni similares; ENTER confirma directamente → decisión `CONFIRMAR`. |
| `test_robot_rechazo_duplicado_exacto` | Nombre exactamente igual a uno existente; el panel devuelve `CANCELAR` sin importar la tecla. |
| `test_robot_alerta_similitud` | 'Super' activa alerta por 'Supermercado'; presionar [1] adopta el similar → decisión `ADOPTAR:<id>`. |
| `test_robot_justificacion_requerida` | Sin subcategorías ni historial; tecla [M] confirma con justificación 'Pago mensual recurrente'. |
| `test_robot_cancelacion_por_usuario` | ESC cancela en cualquier estado → decisión `CANCELAR` y justificación `None`. |

---

## Tabla Resumen

| Archivo | Módulo cubierto | Cantidad de tests |
|---------|----------------|:-----------------:|
| [test_aislamiento_cuotas.py](../tests/test_aislamiento_cuotas.py) | `scripts/modulos/inbox_movimientos.py` — aislamiento de cuotas en RAM | 1 |
| [test_gobernanza_similitud.py](../tests/test_gobernanza_similitud.py) | `scripts/modulos/inbox_movimientos.py` — motor de similitud y lógica de frecuencia/justificación | 25 |
| [test_config.py](../tests/test_config.py) | `sigap_config.py` — rutas absolutas y compatibilidad cross-platform | 2 |
| [test_motor_clasificacion.py](../tests/test_motor_clasificacion.py) | `scripts/modulos/inbox_movimientos.py` — limpieza de texto, motor de cuotas, motor de clasificación IA | 18 |
| [test_contrato_santander.py](../tests/test_contrato_santander.py) | `scripts/import_santander.py` — contract test del formato Excel (se saltea si no hay .xlsx en inbox) | 8 |
| [test_database_init.py](../tests/test_database_init.py) | `scripts/factory_reset_normalized.py` — validez del esquema SQL | 1 |
| [test_gui_logic.py](../tests/test_gui_logic.py) | `scripts/modulos/inbox_movimientos.py` — lógica de filtrado del selector UI | 2 |
| [test_importacion.py](../tests/test_importacion.py) | `scripts/import_santander.py` — deduplicación por `num_referencia` | 1 |
| [test_ui_inbox_movimientos.py](../tests/test_ui_inbox_movimientos.py) | `scripts/modulos/inbox_movimientos.py` — loop principal de UI con mocks de I/O | 8 |
| [test_robots_gobernanza.py](../tests/test_robots_gobernanza.py) | `scripts/modulos/inbox_movimientos.py` — `evaluar_gobernanza` y `render_panel_gobernanza` | 5 |
| **TOTAL** | | **71** |
