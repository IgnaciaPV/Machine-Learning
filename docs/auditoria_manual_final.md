# Auditoría manual final - N001 a N012

## Criterio de revisión

La auditoría final compara el hecho descrito en la fuente con el texto preparado para el LLM y con el JSON generado. Se revisan especialmente: entidades inventadas, omisiones relevantes, confusión de roles, relaciones demasiado fuertes, clasificación organización/lugar y contaminación por contenido editorial.

La referencia técnica es **GitHub Actions run #14 (ID 36354954389), estado SUCCESS**. La ejecución produjo 12 JSON válidos, 0 fallidos, 38 relaciones, 185 archivos Markdown sin enlaces rotos y 19/19 pruebas aprobadas.

Que un JSON sea válido significa que cumple el contrato estructural y los controles automáticos. La auditoría humana sigue siendo necesaria para revisar matices que no se resuelven con `json.loads` o Pydantic.

## Revisión de cierre posterior

La tabla siguiente conserva la auditoría manual declarada del run #14. La revisión asistida posterior detectó problemas adicionales, registrados en `docs/correcciones_cierre.json`: pérdida de fragmentos inline, sobreafirmaciones en resúmenes N001/N003/N006/N009/N010, geografía inferida en N004, verbo incorrecto y falta de contexto de antecedentes en N012, y fusión de la etiqueta `un hombre` entre N001 y N005. No se presenta esa revisión asistida como una nueva auditoría humana firmada.

El cierre deja 37 relaciones, 185 notas y 23/23 pruebas. N010 conserva `HABRIA_COMETIDO` y `HABRIA_AGREDIDO_A`, también en su resumen. N012 usa `DETUVO_A` y `TIENE_ANTECEDENTES_POR`. Los nombres y roles omitidos que no se completaron siguen siendo limitaciones del extractor; no se afirma extracción exhaustiva.

## Revisión caso a caso

| ID | Estado final | Observación |
|---|---|---|
| N001 | Conforme con observación menor | Se mantienen el detenido, La Serena, Río Elqui y los jarabes de codeína. Se eliminaron referencias policiales genéricas tratadas como personas y la valorización dejó de interpretarse como cantidad física. Puede persistir alguna correferencia nominal del mismo actor. |
| N002 | Conforme | Se conserva el robo, la víctima, la persecución y las personas detenidas sin agregar hechos no presentes en la fuente. |
| N003 | Conforme con observación menor | Se distinguen los dos homicidios y se conserva la condición de presunta autora. Algunas referencias descriptivas de personas pueden aparecer separadas, por lo que no se aplica fusión automática. |
| N004 | Conforme | Matías Letelier permanece como detenido y los delitos corresponden a lo informado. El postproceso impide convertir detención o imputación en culpabilidad afirmada. |
| N005 | Conforme | Homicidio, víctima, arma y presunto autor permanecen respaldados. El Juzgado de Garantía de Coquimbo se clasifica como organización y ya no contamina el análisis de lugares. |
| N006 | Conforme | Se mantienen víctima, captura, lugares y objetos incautados sin generar una relación afirmativa de autoría cuando el texto conserva condición de sospecha. |
| N007 | Corregido | Se mantienen los cinco gendarmes, delitos investigados y objetos. La relación `PRESUNTA_VINCULACION_A -> cárcel de Illapel` fue descartada porque el destino era un lugar y no la red u organización mencionada. No se reemplazó por una relación inventada. |
| N008 | Conforme | El JSON indica que la víctima fue hallada en un pozo y que el caso se investiga como homicidio; no se afirma que el pozo sea necesariamente el lugar donde ocurrió la agresión. |
| N009 | Conforme | Se mantienen víctima, terminal, arma cortante y tercer sujeto sin inventar identidad para el autor. |
| N010 | Corregido | El hombre de 45 años permanece como presunto autor. Las relaciones finales conservan incertidumbre (`HABRIA_COMETIDO`, `HABRIA_AGREDIDO_A`) y se eliminan relaciones afirmativas que podían borrar ese matiz. |
| N011 | Conforme | La limpieza elimina la tarjeta `Lee también`; el JSON ya no incorpora el delito perteneciente a una noticia recomendada ajena al caso. |
| N012 | Conforme | Se mantienen los dos detenidos y los antecedentes delictuales explícitos. El Tribunal de Garantía de Coquimbo se clasifica como organización y no como lugar. |

## Problemas encontrados y cómo se cerraron

1. **Fechas de Cooperativa:** se corrigió el fallback basado en URL y se agregaron dos tests.
2. **Contenido “Lee también”:** se agregó una regla de limpieza y un test específico.
3. **Tribunales como lugares:** el postproceso los mueve a organizaciones antes del análisis.
4. **Actores policiales genéricos:** expresiones institucionales no se mantienen como personas individuales.
5. **Relaciones huérfanas:** se descartan si origen o destino no existe en el mismo JSON.
6. **Presunción de inocencia:** se filtran tipos afirmativos cuando el rol es detenido, imputado, sospechoso o investigado y la relación no conserva incertidumbre.
7. **N007:** se elimina la vinculación cuyo destino era una cárcel.
8. **N010:** se conserva `HABRIA_` y se descartan relaciones afirmativas de agresión/uso.
9. **Valorizaciones:** una cifra en pesos no se convierte en cantidad física ni en dinero incautado.
10. **Reproducibilidad:** el workflow registra versiones del entorno y deja 19 tests automatizados.

## Limitaciones que se mantienen de forma consciente

Los JSON conservan las etiquetas (`Un hombre` / `un hombre`), pero sus notas de persona se separan por noticia: N001 es un detenido y N005 una víctima de otro caso. La similitud textual no identifica a una misma persona. La salida y pueden existir correferencias como `un hombre` / `el sujeto` que una persona reconocerá como el mismo actor. No se aplica fuzzy matching a nombres de personas porque una fusión agresiva puede mezclar individuos distintos.

Los recuentos y gráficos describen únicamente las 12 noticias seleccionadas. No son tasas oficiales de delincuencia ni permiten inferir riesgo por comuna.
