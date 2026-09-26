# Auditoría manual final de la extracción con Gemini

## Alcance

Se revisaron manualmente **12 de 12 noticias** (N001-N012), superando el mínimo de 10 indicado para el laboratorio. La revisión comparó la fuente periodística, el texto limpio y el JSON generado, con foco en: fidelidad factual, roles, incertidumbre jurídica, objetos/cantidades, relaciones, contaminación editorial y trazabilidad.

La referencia técnica final es **GitHub Actions: LAB01 - Pipeline completo, run #11 (26-09-2026), estado SUCCESS**. En esa ejecución se obtuvieron **12 JSON válidos, 0 fallidos, 37 relaciones, 195 archivos Markdown, 0 enlaces rotos y 14/14 pruebas aprobadas**.

> Importante: que un JSON sea válido significa que cumple estructura, tipos y controles de trazabilidad; no implica que toda decisión semántica del LLM sea perfecta. Por eso esta auditoría se mantiene como evidencia separada.

## Revisión caso a caso

| ID | Evaluación manual | Observación principal |
|---|---|---|
| N001 | Aceptable con observaciones | Recupera correctamente detención, Río Elqui, vehículo y jarabes de codeína, y ya no confunde la valorización monetaria con cantidad física. El LLM todavía genera correferencias de la misma persona (`un hombre`, `el sujeto`, `el imputado`, `el detenido`) y llega a tratar expresiones institucionales como `los uniformados`/ `nuestros carabineros` como personas. |
| N002 | Conforme | Conserva robo de camioneta, víctima, persecución, detenidos y Hospital de La Serena sin duplicar delitos. |
| N003 | Aceptable con observaciones | Distingue los dos homicidios y conserva `PRESUNTA_AUTORA_DE` para la mujer detenida. Persisten correferencias para la primera víctima y la clasificación de `impactos de bala` no se usa como objeto en esta ejecución, evitando una falla observada antes. |
| N004 | Conforme | Matías Letelier permanece como detenido/imputado por los delitos informados. El postproceso evita convertir esa condición en una afirmación de culpabilidad. |
| N005 | Conforme | Conserva homicidio, víctima, arma cortopunzante, presunto autor y control de detención; la presunción se mantiene explícita. |
| N006 | Conforme con criterio prudente | Recupera víctima, captura, lugares y objetos incautados. El sospechoso se mantiene como detenido y no se crea una relación afirmativa de autoría. |
| N007 | Aceptable con observaciones | Recupera los cinco gendarmes detenidos, delitos investigados, comunas y objetos. La relación `PRESUNTA_VINCULACION_A` queda asociada a la cárcel de Illapel y no directamente a la red/delito; debe leerse como una limitación semántica del LLM. |
| N008 | Conforme | Mantiene que la víctima fue hallada en un pozo y que la BH/PDI indaga un homicidio; no afirma que el pozo sea necesariamente el lugar de ejecución del delito. |
| N009 | Conforme | Recupera víctima, terminal, arma cortante y tercer sujeto. La relación de ataque corresponde al relato explícito de la noticia; no se inventa identidad del autor. |
| N010 | Aceptable con observaciones | Conserva al hombre de 45 años como `imputado` y usa `PRESUNTO_AUTOR_DE`; sin embargo, la relación `USO -> arma cortante` simplifica una formulación periodística que emplea incertidumbre (`habría`). |
| N011 | Conforme | La versión final ya no incorpora la noticia recomendada del bloque `Lee también`. Conserva Los Shein, Y.A.P.L., delitos, armas, municiones, vehículos y drogas de la noticia correcta. |
| N012 | Conforme | Recupera a los dos detenidos, Tierras Blancas/Coquimbo y los antecedentes mencionados: tráfico de drogas, tenencia de armas, robo con violencia y lesiones. |

## Hallazgos detectados durante el desarrollo y correcciones aplicadas

1. **Fechas faltantes en Cooperativa.** El fallback desde URL tenía una expresión regular incorrectamente escapada. Se corrigieron los patrones para URLs normales y AMP y se añadieron pruebas unitarias.
2. **Contaminación por contenido recomendado.** BioBioChile inserta tarjetas `Lee también` dentro del contenedor editorial. Se incorporó una regla de limpieza para excluir ese bloque; esto eliminó de N011 un delito que pertenecía a otra noticia.
3. **Presunción y roles.** El prompt se reforzó para diferenciar víctima, detenido, imputado, sospechoso, fiscal e institución, y para preservar marcadores como `presunto` y `habría`.
4. **Valorización versus cantidad.** Una cifra monetaria usada para valorar drogas/medicamentos ya no se interpreta como cantidad física ni como efectivo incautado.
5. **Relaciones huérfanas.** El postproceso elimina relaciones cuyo origen o destino no coincide con una entidad del mismo JSON.
6. **Sobreafirmación de culpabilidad.** Se bloquean relaciones afirmativas de autoría/culpabilidad cuando la persona solo está descrita como detenida, imputada, sospechosa o investigada.
7. **Normalización sintáctica de relaciones.** Los tipos se convierten a mayúsculas y guiones bajos para evitar variantes como `TRASLADó` y espacios periféricos.
8. **Duplicados exactos.** Se eliminan duplicados exactos sin aplicar fusión semántica agresiva, ya que esta podría mezclar entidades distintas.

## Limitaciones residuales

La ejecución final registra **0 JSON inválidos, 0 relaciones dudosas por el validador y 0 noticias duplicadas**, pero el Data Understanding detecta **1 grupo de variantes nominales** (`Un hombre` / `un hombre`). La auditoría humana además identifica correferencias no fusionadas, alguna tipificación discutible de actores institucionales como personas y relaciones que pueden perder matices de incertidumbre.

No se corrigen silenciosamente todos esos casos porque una normalización semántica agresiva podría introducir errores de identidad. En una versión de investigación se recomendaría construir un conjunto humano anotado y medir precisión/recall por campo, además de incorporar resolución de correferencias con revisión.

## Interpretación ética

El grafo representa **afirmaciones de fuentes periodísticas**, no hechos judicialmente probados. Detención, imputación, sospecha o investigación no equivalen a condena. Los recuentos del Data Understanding describen únicamente este corpus de 12 noticias y no representan tasas oficiales de criminalidad.

## Trazabilidad

La cadena auditada es:

`NXXX -> URL/fuente -> HTML RAW -> texto procesado -> Gemini -> JSON -> validación -> Markdown Obsidian -> entidades/relaciones`.

Los HTML y textos procesados se regeneran en GitHub Actions y forman parte de la evidencia del workflow; la API key se consume desde GitHub Secrets y nunca se publica en el repositorio.
