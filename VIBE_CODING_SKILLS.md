# 🦅 VIBE CODING SKILLS
### Mapa de Sinergia Humano-IA — Proyecto Fénix
*Martín · Analista de Sistemas · 2026*

> Este documento no es un curso de Python ni un manual de IA.
> Es el mapa personal de Martín para multiplicar exponencialmente
> la sinergia con su copiloto técnico en el contexto del Proyecto Fénix.
>
> Se construyó a partir de sesiones reales de trabajo sobre S.I.G.A.P.,
> no de teoría genérica sobre "cómo usar IA".

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

## 🎯 ESTADO ACTUAL — Sesión #5

| Patrón | Estado | Observación |
|---|---|---|
| 1 — Briefing Arquitectónico | ✅ Dominado | Natural, sin fricción |
| 2 — Verificar Antes de Confiar | ✅ Dominado | Detectó discrepancia doc/código en Sesión #5 |
| 3 — Freno Estratégico | ✅ Dominado | Aplicado instintivamente en el rebase |
| 4 — Delegación en Capas | ✅ Sólido | Ejercitado en toda la arquitectura de Gobernanza |
| 5 — El Contexto como Activo | ⚠️ En construcción | El protocolo de mantenimiento se está formalizando |
| 6 — Detectar Adivinanzas | ⚠️ En construcción | Identificado como área de crecimiento |
| 7 — Commit como Checkpoint | ✅ Dominado | Conventional Commits aplicados consistentemente |

---

## 🔮 PATRONES AVANZADOS (próximas sesiones)

Estos patrones aún no fueron ejercitados en SIGAP pero son fundamentales
para llevar la sinergia al siguiente nivel. Se incorporan a medida que el proyecto los demande.

---

### PATRÓN A — Diagnóstico Autónomo

**Qué es:** Pedirle al copiloto que explore un módulo o área del proyecto
de forma independiente, detecte problemas y traiga un informe estructurado
— sin que vos guíes la búsqueda.

**La diferencia con el trabajo actual:**
Hoy siempre llegás con el problema identificado. Este patrón es
"mandame a hacer una auditoría" en lugar de "trabajemos juntos en esto".

**Cómo se activa:**
> "Leé `scripts/import_santander.py` completo y traeme:
> 1. Problemas que detectés
> 2. Deuda técnica visible
> 3. Lo que te generaría dudas antes de tocarlo"

**Por qué es poderoso:** Aprovecha que el copiloto no tiene sesgos
sobre el código — ve cosas que vos ya no ves porque las conocés de memoria.

**Señal de que está bien usado:** El informe te sorprende con al menos
una observación que no tenías en el radar.

---

### PATRÓN B — El Límite de la IA (Saber Cuándo NO Usarla)

**Qué es:** Reconocer las decisiones que el copiloto no debería tomar
ni influenciar — y tomar esas decisiones solo, antes de involucrarme.

**Las decisiones que siempre son tuyas:**
- Qué Centros de Costo crear (tocan tu economía personal y familiar)
- Cómo clasificar un gasto con carga ética o emocional
- Qué información financiera es demasiado sensible para pegar en un chat
- El alcance real del proyecto (qué entra y qué no entra en SIGAP)
- Las prioridades cuando hay tensión entre features y tiempo personal

**La regla práctica:**
> Si la decisión impacta tu vida fuera del código → es tuya.
> Si la decisión impacta solo el código → podemos deliberar juntos.

**Por qué importa:** El copiloto siempre va a responder con algo plausible.
No va a decirte "eso no me lo preguntes a mí". Esa discriminación la tenés que hacer vos.

---

### PATRÓN C — Gestión del Contexto en Sesiones Largas

**Qué es:** Detectar cuándo el copiloto empezó a "olvidar" el inicio
de la conversación y actuar antes de que eso genere errores.

**Cómo se degrada el contexto:**
A medida que una sesión crece, las primeras instrucciones y decisiones
quedan fuera de mi ventana de atención activa. Empiezo a contradecir
cosas que acordamos al principio sin darme cuenta.

**Las señales de degradación:**
- Te propongo algo que ya descartamos antes en la misma sesión
- Olvido una restricción que mencionaste al inicio
- Mis respuestas se vuelven más genéricas y menos específicas a SIGAP
- Repito una pregunta que ya te hice

**Las acciones correctivas:**
| Señal | Acción |
|---|---|
| Sesión supera ~60 mensajes | Considerá abrir chat nuevo con Contexto.md fresco |
| Propongo algo ya descartado | "Ya lo descartamos antes — recordá que decidimos X" |
| Respuesta genérica sospechosa | "¿Estás teniendo en cuenta el stack de SIGAP o estás respondiendo genérico?" |

**La regla de oro:** Una sesión enfocada en un objetivo concreto
siempre supera a una sesión larga que abarca todo.

---

### PATRÓN D — El Abogado del Diablo

**Qué es:** Pedirle al copiloto que argumente activamente **en contra**
de una decisión que vos querés tomar — para verificar si aguanta el escrutinio
antes de comprometerte con ella.

**Por qué es necesario:**
El copiloto tiene un sesgo natural a validar lo que proponés.
Si le decís "quiero hacer X", tiende a encontrar razones por las que X es buena idea.
Este patrón rompe ese sesgo deliberadamente.

**Cómo se activa:**
> "Quiero hacer X. Ahora argumentá en contra. Decime los tres mejores
> motivos por los que sería un error. No me valides — desafíame."

**Casos de uso en SIGAP:**
- Antes de agregar una feature nueva ("¿por qué NO deberíamos hacer esto ahora?")
- Antes de cambiar una decisión arquitectónica ("¿qué riesgos no estoy viendo?")
- Antes de un refactor grande ("¿qué puede salir mal que no estoy considerando?")

**Señal de que está funcionando:** La respuesta del copiloto te hace
dudar aunque sea un momento. Si no dudás nada, o el argumento es débil
y confirmaste tu decisión con más seguridad, o el copiloto no entró al juego
y hay que insistir.

**Nota importante:** Este patrón requiere que vos estés dispuesto a escuchar
que tu idea puede estar equivocada. Es el patrón más incómodo — y el más valioso.

---

## 🎯 ESTADO ACTUAL — Sesión #5

| Patrón | Estado | Observación |
|---|---|---|
| 1 — Briefing Arquitectónico | ✅ Dominado | Natural, sin fricción |
| 2 — Verificar Antes de Confiar | ✅ Dominado | Detectó discrepancia doc/código en Sesión #5 |
| 3 — Freno Estratégico | ✅ Dominado | Aplicado instintivamente en el rebase |
| 4 — Delegación en Capas | ✅ Sólido | Ejercitado en toda la arquitectura de Gobernanza |
| 5 — El Contexto como Activo | ⚠️ En construcción | El protocolo de mantenimiento se está formalizando |
| 6 — Detectar Adivinanzas | ⚠️ En construcción | Identificado como área de crecimiento |
| 7 — Commit como Checkpoint | ✅ Dominado | Conventional Commits aplicados consistentemente |
| A — Diagnóstico Autónomo | 🔲 Pendiente | No ejercitado aún |
| B — Límite de la IA | 🔲 Pendiente | No establecido explícitamente aún |
| C — Gestión Sesiones Largas | 🔲 Pendiente | Será necesario pronto |
| D — Abogado del Diablo | 🔲 Pendiente | El más desafiante — el más valioso |

---

*VIBE_CODING_SKILLS.md — Proyecto Fénix · Actualizado Sesión #5 · 2026-03-10*
