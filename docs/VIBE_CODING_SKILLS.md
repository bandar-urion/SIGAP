# 🦅 VIBE CODING SKILLS
### Estándar de Desarrollo Humano-IA — Proyecto Fénix
*Martín · Analista de Sistemas · 2026*

> Este documento no es un curso de Python ni un manual de IA.
> Es el estándar operativo de desarrollo del Proyecto Fénix:
> los patrones de trabajo y los protocolos de calidad que rigen
> cada sesión, cada commit y cada decisión de arquitectura.
>
> Se construyó a partir de sesiones reales de trabajo sobre S.I.G.A.P.,
> no de teoría genérica sobre "cómo usar IA".
> Cada patrón tiene un caso real que lo justifica.
> Cada protocolo responde a una vulnerabilidad concreta identificada en el proceso.

---

## 🧭 EL MODELO MENTAL BASE

Antes de los patrones, el marco conceptual que los sostiene:

| Rol | Responsabilidad | No delegar nunca |
|---|---|---|
| **Martín (Lead Architect)** | Qué construir, por qué y cómo a nivel arquitectónico y de diseño | Lógica de negocio, decisiones de arquitectura, ética, decisión final |
| **Claude (Copiloto Técnico)** | Implementación técnica en todos los ámbitos | Criterio sobre el dominio del problema |

**Aclaración crítica sobre el Cómo:**
Martín define el Cómo a nivel arquitectónico y de diseño
(ej: base de datos en 3NF, interfaz CLI, doctrina HyperFlux, `leer_byte()` como único lector de input).
El copiloto traduce esas decisiones a implementación técnica concreta (código Python, SQL, tests).
El Cómo de bajo nivel (sintaxis, librerías, patrones de implementación) es territorio del copiloto.
El Cómo de alto nivel (arquitectura, filosofía, restricciones) es territorio de Martín.

La sinergia no es "pedirle cosas a la IA". Es una **conversación técnica entre pares**
donde uno tiene el dominio del problema y el diseño, y el otro tiene el dominio de la implementación.

---

## 🤝 POR QUÉ UN EQUIPO ES MEJOR QUE UNO SOLO

El VibeCoding no es una metodología de conveniencia. Es una respuesta directa
a las limitaciones estructurales del AloneCoding: un desarrollador único
que debe resolver todos los problemas con una sola visión, un solo conjunto
de recursos y una sola inventiva.

Un equipo tiene ventajas que no son de grado sino de naturaleza.
Estas son las que aplican concretamente al Proyecto Fénix:

**1. Dos pares de ojos sobre el mismo problema**
El desarrollador solo tiene puntos ciegos sobre su propio código, no por falta
de capacidad sino porque conocer el código demasiado bien es en sí una limitación.
El copiloto no tiene historia emocional con lo que está leyendo: ve sin nostalgia,
sin el "esto lo escribí yo y funciona" que inhibe la crítica real.

**2. Roles complementarios sin switching cost**
En un equipo humano, el arquitecto y el implementador raramente son la misma
persona por una razón: los modos de pensamiento son distintos y a veces
contradictorios. El AloneCoder tiene que cambiar de modo mental constantemente.
En el par Humano-IA, Martín opera siempre en modo arquitectónico y el copiloto
en modo implementación. El costo de ese cambio de contexto es cero.

**3. Code review sin fricción social**
En equipos humanos, señalar errores tiene consecuencias relacionales.
El copiloto señala problemas sin agenda, sin jerarquía, sin miedo a ofender.
Y Martín puede pedirle que sea brutalmente crítico sin que nadie se vaya
ofendido a su casa. El Patrón D (Abogado del Diablo) existe precisamente
porque esta ventaja hay que activarla deliberadamente — el copiloto tiene
un sesgo natural a validar. Cuando ese sesgo se rompe, el resultado es
una revisión más honesta que la mayoría de los code reviews humanos.

**4. Memoria técnica externa e ilimitada**
El AloneCoder depende de su memoria para recordar por qué tomó una decisión
hace tres meses. El par externaliza esa memoria en Contexto.md, ADRs y
DECISIONES.md. El copiloto puede reconstituir el estado completo del proyecto
en segundos. Un desarrollador solo que vuelve de dos semanas de vacaciones
no tiene ese lujo.

**5. Disponibilidad asimétrica**
Un equipo humano tiene horarios, vacaciones, urgencias personales, días malos.
El copiloto está disponible a las 2 AM en Termux desde un Samsung S21.
La productividad no depende de la agenda de nadie más que de Martín.

**6. Especialización on-demand**
Cuando el proyecto necesita un experto en regex financieros, el copiloto
es ese experto. Cuando necesita un especialista en SQLite, también.
Cuando necesita a alguien que conozca las particularidades de raw mode
en Termux Android, ídem. El AloneCoder aprende todo desde cero o se detiene.
El par tiene acceso instantáneo al conocimiento especializado en el momento
exacto en que se necesita.

**7. El rubber duck que responde**
El rubber duck debugging funciona porque articular el problema en voz alta
fuerza la claridad que a veces sola resuelve el problema. El copiloto es
un rubber duck que responde. La combinación de articular más recibir
una perspectiva externa es cualitativamente superior a cada parte por separado.

**8. Documentación como subproducto natural**
En equipos humanos, documentar es una tarea separada que siempre se posterga.
En el par Humano-IA, la conversación técnica ya es documentación en estado bruto.
El copiloto transforma una discusión en un ADR, un bloque de Contexto.md
o una entrada de DECISIONES.md sin interrumpir el flujo de trabajo.

**9. Escalada sin fricción ni burocracia**
Cuando un problema supera la capacidad del equipo, contratar o consultar
a alguien externo tiene costo, tiempo y burocracia. En el par, la "escalada"
es cambiar el enfoque de la conversación. El copiloto puede operar como junior
implementando código repetitivo, como senior revisando arquitectura, o como
consultor externo cuestionando decisiones estratégicas, según lo que el momento requiera.

**10. El equipo no tiene ego colectivo**
Los equipos humanos desarrollan inercias y resistencia al cambio por razones
sociales. Nadie quiere ser quien diga "lo que construimos el año pasado está mal".
El copiloto no tiene inversión emocional en el código anterior. Puede señalar
que una decisión de la Sesión #2 fue un error sin que eso amenace la cohesión
de nadie ni la reputación de nadie.

### La condición para que estas ventajas sean reales

Ninguna de estas ventajas es automática. Todas dependen de que la colaboración
esté estructurada. Un equipo humano sin metodología produce caos más rápido
que un desarrollador solo. Lo mismo aplica aquí.

Los Patrones de Trabajo y los Protocolos de Calidad de este documento son
exactamente eso: la estructura que convierte las ventajas teóricas del equipo
en práctica de ingeniería concreta y auditable.

**Sin los patrones y protocolos, el VibeCoding es solo velocidad sin dirección.
Con ellos, es un equipo que produce con la agilidad de uno y la solidez de dos.**

---

# PARTE 1 — PATRONES DE TRABAJO

*Los patrones describen cómo se conduce la colaboración Humano-IA.
Son hábitos operativos, no reglas abstractas.*

---

## 📐 PATRÓN 1 — El Briefing Arquitectónico

**Qué es:** La forma de iniciar una tarea para obtener arquitectura sólida en lugar de código suelto.

**La diferencia:**

| Briefing débil | Briefing arquitectónico |
|---|---|
| "Haceme una función que importe el Excel" | "Necesito desacoplar el parser de Pandas de la UI. El objetivo es que `parsear_excel_santander()` sea testeable sin levantar la interfaz. ¿Cómo lo encaramos?" |
| Resultado: código que funciona | Resultado: decisión de diseño + código que encaja |

**La estructura del briefing arquitectónico:**
1. **Contexto:** qué módulo/archivo estamos tocando
2. **Objetivo:** qué problema resuelve (no qué código querés)
3. **Restricciones:** qué no puede romperse (filosofía, ADRs, tests existentes)
4. **Pregunta:** ¿cómo lo encaramos? (invitás al copiloto a pensar, no solo a ejecutar)

**Señal de que lo estás haciendo bien:** El copiloto te responde con un plan antes de escribir código.

**Ejercitado en SIGAP — caso real:**
Martín solicitó: *"Necesito desacoplar el parser de Pandas de la UI. El objetivo es que
`parsear_excel_santander()` sea testeable sin levantar la interfaz. ¿Cómo lo encaramos?"*
→ Resultado: decisión de diseño documentada en TODO FASE 2, no código suelto.

También ejercitado en Sesión #5: al describir el problema de divergencia Git
en lugar de pedir "arreglame el push", lo que permitió diagnóstico preciso y
resolución quirúrgica (format-patch / reset / git am).

---

## 📐 PATRÓN 2 — Verificar Antes de Confiar

**Qué es:** El hábito de pedir evidencia en el código real antes de aceptar
cualquier afirmación del copiloto — incluso cuando suena correcta.

**Por qué importa:** El copiloto trabaja con el contexto que tiene.
Si la documentación está desactualizada, sus afirmaciones lo estarán también.

**La regla práctica:**
> Ante cualquier afirmación sobre el estado del código → pedí verificación en el archivo real.

**Ejemplos concretos:**
- "El bug `tx→mov` está resuelto" → `grep -n "tx\." scripts/import_santander.py`
- "La ruta DB está corregida" → `grep -n "DB_FILE\|sigap_config" sigap.py`
- "El test pasa" → `python -m unittest tests/test_X.py`

**Señal de que lo estás haciendo bien:** Encontrás al menos una discrepancia
entre documentación y código real cada 3 sesiones. Si nunca encontrás nada,
no estás verificando — estás confiando a ciegas.

**Ejercitado en SIGAP:** Sesión #5 — detectaste que los bugs listados como
pendientes en Contexto.md ya estaban resueltos en el código.

---

## 📐 PATRÓN 3 — El Freno Estratégico

**Qué es:** Saber cuándo detener al copiloto antes de que genere trabajo que
va en la dirección equivocada.

**La señal de alarma:** Cuando el copiloto propone algo y vos sentís
"esto puede complicarse" — aunque no sepas exactamente por qué.
Esa intuición de Analista de Sistemas es más valiosa que cualquier output de código.

**La frase que lo activa:**
> "Esperá. Antes de continuar, confirmame que entendiste el problema."

**Por qué funciona:** Fuerza al copiloto a reformular el problema con sus palabras.
Si la reformulación no coincide con tu visión → encontraste la desviación antes
de que se convierta en código que hay que deshacer.

**Caso real en SIGAP:** Sesión #5 — cuando el rebase explotó con conflictos,
el freno inmediato (`git rebase --abort`) evitó un estado corrupto del repositorio.
No sabías exactamente qué pasó, pero sabías que había que parar.

---

## 📐 PATRÓN 4 — Delegación en Capas

**Qué es:** Dividir una tarea compleja en capas de responsabilidad clara,
manteniendo el control arquitectónico en cada transición.

**El anti-patrón:** "Haceme todo el módulo de auditoría."
→ Resultado: código que técnicamente funciona pero no respeta
las decisiones de diseño que solo vos conocés.

**La delegación en capas:**
```
Capa 1 (Martín): Definís QUÉ debe hacer, sus restricciones
                 y el CÓMO arquitectónico (diseño, filosofía, ADRs)
     ↓
Capa 2 (copiloto): Propone el CÓMO de implementación (Blueprint técnico)
     ↓
Capa 3 (Martín): Aprobás, corregís o rechazás el Blueprint
     ↓
Capa 4 (copiloto): Ejecuta el código
     ↓
Capa 5 (Martín): Validás contra el comportamiento esperado (no contra el código)
```

**La clave de la Capa 5:** Validar comportamiento, no código.
No necesitás entender cada línea de Python. Necesitás saber si
el sistema hace lo que dijiste que tenía que hacer.

**Ejercitado en SIGAP:** Toda la arquitectura de Gobernanza — Martín
definió los 6 criterios, los 3 flujos de interacción, la doctrina HyperFlux
y las restricciones filosóficas (sin input() estándar, leer_byte() único).
El copiloto implementó. Martín validó con los 25 tests.

---

## 📐 PATRÓN 5 — El Contexto como Activo

**Qué es:** Tratar el `Contexto.md` no como documentación sino como
**herramienta de trabajo activa** que maximiza la productividad de cada sesión.

**El costo de un Contexto desactualizado:**
- El copiloto arranca con información incorrecta
- Los primeros 10-15 minutos de sesión se gastan en correcciones
- Se generan sugerencias basadas en bugs ya resueltos (pasó en Sesión #5)

**El protocolo de mantenimiento:**
| Momento | Acción |
|---|---|
| Al cerrar sesión | Copiloto genera bloque ÚLTIMA SESIÓN |
| Antes del commit | Verificar que bugs resueltos se eliminan de pendientes |
| Al iniciar sesión nueva | Pegar Contexto.md completo al copiloto |

**El multiplicador:** Cada minuto invertido en mantener el Contexto.md
ahorra entre 5 y 10 minutos de "reconstrucción de estado" al inicio de la próxima sesión.

---

## 📐 PATRÓN 6 — Detectar Cuándo el Copiloto Está Adivinando

**Qué es:** Distinguir cuándo el copiloto opera con certeza técnica
vs cuándo está generando output plausible sin base sólida.

**Las señales de que el copiloto está adivinando:**
- Usa frases como "probablemente", "debería estar en", "típicamente"
- Hace afirmaciones sobre el estado del código sin haberlo leído
- Propone soluciones genéricas sin referenciar tu stack específico
- No hace preguntas antes de responder algo complejo

**Las señales de que opera con certeza:**
- Cita líneas o funciones específicas del código
- Dice "verificá con este comando antes de continuar"
- Propone un plan antes de ejecutar
- Señala explícitamente qué no sabe y cómo averiguarlo

**La respuesta correcta ante una adivinanza:**
> "¿Eso lo sabés o lo estás infiriendo? ¿Lo verificamos primero?"

---

## 📐 PATRÓN 7 — El Commit como Checkpoint Mental

**Qué es:** Usar el ciclo Git (commit + push) no solo como control de versiones
sino como **ritual de cierre cognitivo** de cada unidad de trabajo.

**Por qué importa para la sinergia:**
Un commit bien redactado es un contrato entre vos, el copiloto y el futuro.
Cuando la próxima sesión arranca y leemos el log, en 30 segundos
reconstruimos el estado exacto del proyecto.

**La anatomía de un buen commit en SIGAP:**
```
tipo(alcance): descripción imperativa en minúsculas

- Detalle 1 de qué cambió y por qué
- Detalle 2

Sesión #N · Entorno A o B · branch: nombre-branch
```

**El test del buen commit:**
> ¿Podría alguien (o yo mismo en 6 meses) entender exactamente
> qué pasó y por qué, solo leyendo este mensaje?

---

## 🔮 PATRONES AVANZADOS

Estos patrones son fundamentales para llevar la sinergia al siguiente nivel.
Se incorporan a medida que el proyecto los demande.

---

### PATRÓN A — Diagnóstico Autónomo

**Qué es:** Pedirle al copiloto que explore un módulo o área del proyecto
de forma independiente, detecte problemas y traiga un informe estructurado
— sin que vos guíes la búsqueda.

**La diferencia con el trabajo habitual:**
Normalmente llegás con el problema identificado. Este patrón es
"hacé una auditoría" en lugar de "trabajemos juntos en esto".

**Cómo se activa:**
> "Leé `scripts/import_santander.py` completo y traeme:
> 1. Problemas que detectés
> 2. Deuda técnica visible
> 3. Lo que te generaría dudas antes de tocarlo"

**Por qué es poderoso:** El copiloto no tiene sesgos sobre el código —
ve cosas que vos ya no ves porque las conocés de memoria.

**Señal de que está bien usado:** El informe te sorprende con al menos
una observación que no tenías en el radar.

---

### PATRÓN B — El Límite de la IA (Saber Cuándo NO Usarla)

**Qué es:** Reconocer las decisiones que el copiloto no debería tomar
ni influenciar — y tomarlas solo, antes de involucrar al copiloto.

**Las decisiones que siempre son de Martín:**
- Qué Centros de Costo crear (tocan la economía personal y familiar)
- Cómo clasificar un gasto con carga ética o emocional
- Qué información financiera es demasiado sensible para pegar en un chat
- El alcance real del proyecto (qué entra y qué no entra en SIGAP)
- Las prioridades cuando hay tensión entre features y tiempo personal

**La regla práctica:**
> Si la decisión impacta tu vida fuera del código → es tuya.
> Si la decisión impacta solo el código → podemos deliberar juntos.

**Por qué importa:** El copiloto siempre va a responder con algo plausible.
No va a decir "eso no me lo preguntes a mí". Esa discriminación la tiene que hacer Martín.

---

### PATRÓN C — Gestión del Contexto en Sesiones Largas

**Qué es:** Detectar cuándo el copiloto empezó a "olvidar" el inicio
de la conversación y actuar antes de que eso genere errores.

**Las señales de degradación:**
- El copiloto propone algo que ya fue descartado en la misma sesión
- Olvida una restricción mencionada al inicio
- Las respuestas se vuelven más genéricas y menos específicas a SIGAP
- Repite una pregunta que ya hizo

**Las acciones correctivas:**
| Señal | Acción |
|---|---|
| Sesión supera ~60 mensajes | Abrir chat nuevo con Contexto.md fresco |
| Propone algo ya descartado | "Ya lo descartamos — decidimos X porque Y" |
| Respuesta genérica sospechosa | "¿Estás considerando el stack de SIGAP o estás respondiendo genérico?" |

**La regla de oro:** Una sesión enfocada en un objetivo concreto
siempre supera a una sesión larga que abarca todo.

---

### PATRÓN D — El Abogado del Diablo

**Qué es:** Pedirle al copiloto que argumente activamente **en contra**
de una decisión que se quiere tomar — para verificar si aguanta el escrutinio
antes de comprometerse con ella.

**Por qué es necesario:**
El copiloto tiene un sesgo natural a validar lo que se propone.
Este patrón rompe ese sesgo deliberadamente.

**Cómo se activa:**
> "Quiero hacer X. Ahora argumentá en contra. Decime los tres mejores
> motivos por los que sería un error. No me valides — desafíame."

**Casos de uso en SIGAP:**
- Antes de agregar una feature nueva ("¿por qué NO deberíamos hacer esto ahora?")
- Antes de cambiar una decisión arquitectónica ("¿qué riesgos no estoy viendo?")
- Antes de un refactor grande ("¿qué puede salir mal?")

**Señal de que está funcionando:** La respuesta genera al menos un momento de duda genuina.
Si no hay duda, o el argumento fue débil y confirmó la decisión con más seguridad,
o el copiloto no entró al juego y hay que insistir.

**Nota:** Este patrón requiere disposición real a escuchar que la idea puede estar equivocada.
Es el patrón más incómodo y el más valioso.

---

# PARTE 2 — PROTOCOLOS DE CALIDAD

*Los protocolos responden a vulnerabilidades concretas del modelo de trabajo Humano-IA.
No son sugerencias: son estándares operativos. Su ausencia tiene consecuencias conocidas.*

---

## 🛡️ PROTOCOLO 1 — Comentario de Intención

**Vulnerabilidad que resuelve:** Código generado por el copiloto que Martín no puede
explicar con sus propias palabras. Deuda técnica diferida que se vuelve visible
recién cuando el sistema falla.

**La regla:**
Toda función no trivial generada por el copiloto lleva un comentario escrito
**por Martín**, en su propio lenguaje, antes del merge. No un docstring técnico:
una declaración de intención de negocio.

```python
# MARTÍN: Esta función existe porque el banco mezcla fechas con formato
# de cuota en la misma descripción. El regex limpia primero las fechas
# conocidas para que no contaminen la detección de cuotas reales.
def detectar_cuotas_regex(self):
    ...
```

**El criterio de cumplimiento:**
> Si Martín no puede escribir ese comentario, el código no se mergea.

---

## 🛡️ PROTOCOLO 2 — Paridad de Sesión

**Vulnerabilidad que resuelve:** Sesiones que cierran con documentación nueva
pero sin código ni tests nuevos. La documentación es fácil de generar con IA
y puede convertirse en un sustituto cómodo del trabajo real.

**La regla:**
Cada sesión cierra con al menos un entregable en la columna de código:

| Columna Código | Columna Documentación |
|---|---|
| Función nueva, bug fix, refactor, o test nuevo | Actualización de estado existente (no documentos nuevos) |

**La excepción controlada:**
Una sesión puede ser exclusivamente de planificación, pero se registra
explícitamente como tal en el commit y se limita a **una cada cuatro sesiones**.

**El criterio de cumplimiento:**
> Antes del commit: ¿hay al menos un archivo `.py` o de test modificado?
> Si no → la sesión no cierra hasta que lo haya, o se declara Sesión de Planificación.

---

## 🛡️ PROTOCOLO 3 — Definition of Done Financiero

**Vulnerabilidad que resuelve:** Features marcadas como completadas que funcionan
técnicamente pero no resuelven el problema financiero real que las motivó.

**La regla:**
Antes de marcar cualquier feature como ✅ en el ROADMAP, debe cumplir
las tres condiciones sin excepción:

1. **Funciona en producción real:** probado en el entorno donde va a usarse.
2. **Tiene test de regresión:** existe al menos un test que falla si la lógica se rompe.
3. **Tiene justificación financiera:** Martín puede explicar en una oración
   qué problema financiero resuelve — no técnico, **financiero**.

**El criterio de cumplimiento:**
> "¿Qué problema financiero concreto resuelve esto?"
> Si la respuesta es técnica en lugar de financiera, la feature no está done.

---

## 🛡️ PROTOCOLO 4 — Diario de Decisiones

**Vulnerabilidad que resuelve:** Dependencia operativa en el copiloto como
única fuente de memoria del razonamiento detrás de las decisiones arquitectónicas.

**La regla:**
Martín mantiene `DECISIONES.md` escrito exclusivamente por él, sin asistencia
del copiloto. Una entrada por decisión arquitectónica relevante.

**Formato mínimo:**
```
[Fecha] Decidí X porque Y.
Consideré Z y lo descarté porque W.
```

**El test de independencia:**
> ¿Podría Martín continuar el proyecto sin el copiloto durante una semana,
> basándose solo en `DECISIONES.md` y los ADRs?
> Si la respuesta es no, el archivo está desactualizado.

---

## 🛡️ PROTOCOLO 5 — Justificación de Complejidad

**Vulnerabilidad que resuelve:** Capas de abstracción que se acumulan porque
"parecía necesario en el momento" pero cuya eliminación no rompería nada real.

**La regla:**
Toda capa de abstracción no trivial debe tener un test que demuestre
que la complejidad es necesaria — un test que falle si se elimina esa capa.

**Aplicación directa en SIGAP:**
La capa cross-platform (`leer_byte()`, `leer_input_navegacion()`) existe
porque el Entorno B es Termux. Si esa justificación desaparece,
los tests de esa capa deben revisarse antes que el código.

**El criterio de cumplimiento:**
> "¿Podemos escribir el test que falla si esto no existe?"
> Si no se puede → la abstracción probablemente no debería existir todavía.

---

## 🛡️ PROTOCOLO 6 — Sesión de Arqueología Trimestral

**Vulnerabilidad que resuelve:** Acumulación silenciosa de código que funciona
pero que su autor ya no comprende completamente. Deuda de comprensión
que los tests no detectan porque validan comportamiento, no entendimiento.

**La regla:**
Una vez por trimestre, una sesión dedicada a leer código de sesiones anteriores
**sin el copiloto presente**. El objetivo no es refactorizar: es auditar la comprensión.

**Las tres preguntas:**
1. ¿Entiendo por qué está escrito así?
2. ¿Lo escribiría igual hoy?
3. ¿Qué asumiría alguien que lee esto por primera vez?

**Herramienta obligatoria — Auditoría de cobertura:**
Cada sesión trimestral incluye medición de cobertura de tests con `coverage.py`:

```powershell
pip install coverage
coverage run -m unittest discover tests
coverage report -m --include="scripts/modulos/inbox_movimientos.py,scripts/import_santander.py,sigap_config.py,scripts/utils/auditar_db.py"
coverage erase
```

El reporte identifica código activo sin cobertura de test. Los gaps se documentan
en `TODO.md` como ítems `[QA]` — no se corrigen en la misma sesión salvo que
sean críticos. El objetivo es visibilidad, no corrección inmediata.

**Incorporado en:** Sesión #17 (2026-04-09). Primera ejecución encontró
68% de cobertura en `inbox_movimientos.py` y 0% en `import_santander.py`
y `auditar_db.py`. Gaps documentados en `TODO.md`.

**El criterio de cumplimiento:**
> Si después de la sesión no hay ninguna entrada nueva en `DECISIONES.md`,
> la arqueología no fue honesta.
> Si no se corrió `coverage.py`, la arqueología fue incompleta.

---

# 🎯 ESTADO ACTUAL — Sesión #6

## Patrones de Trabajo

| Patrón | Estado | Observación |
|---|---|---|
| 1 — Briefing Arquitectónico | ✅ Dominado | Natural, sin fricción |
| 2 — Verificar Antes de Confiar | ✅ Dominado | Detectó discrepancia doc/código en Sesión #5 |
| 3 — Freno Estratégico | ✅ Dominado | Aplicado instintivamente en el rebase |
| 4 — Delegación en Capas | ✅ Sólido | Ejercitado en toda la arquitectura de Gobernanza |
| 5 — El Contexto como Activo | ⚠️ En construcción | Protocolo de mantenimiento en formalización |
| 6 — Detectar Adivinanzas | ⚠️ En construcción | Identificado como área de crecimiento |
| 7 — Commit como Checkpoint | ✅ Dominado | Conventional Commits aplicados consistentemente |
| A — Diagnóstico Autónomo | 🔲 Pendiente | No ejercitado aún |
| B — Límite de la IA | 🔲 Pendiente | No establecido explícitamente aún |
| C — Gestión Sesiones Largas | 🔲 Pendiente | Será necesario pronto |
| D — Abogado del Diablo | ✅ Ejercitado | Aplicado en Sesión #6 sobre las bases del VibeCoding |

## Protocolos de Calidad

| Protocolo | Estado | Observación |
|---|---|---|
| 1 — Comentario de Intención | 🔲 A implementar | Retroactivo en funciones críticas existentes |
| 2 — Paridad de Sesión | 🔲 A implementar | Desde Sesión #7 en adelante |
| 3 — Definition of Done Financiero | 🔲 A implementar | Aplicar al backlog del ROADMAP |
| 4 — Diario de Decisiones | 🔲 A implementar | Crear `DECISIONES.md` como primer paso |
| 5 — Justificación de Complejidad | 🔲 A implementar | Auditar capa cross-platform como caso piloto |
| 6 — Arqueología Trimestral | ✅ Activo | Primera ejecución: Sesión #17 (2026-04-09). Próxima: Julio 2026 |

---

*VIBE_CODING_SKILLS.md — Proyecto Fénix · Actualizado Sesión #6 · 2026-03-11*
