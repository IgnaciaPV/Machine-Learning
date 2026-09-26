# Auditoría manual final de la extracción con Gemini

## Alcance

Se revisaron manualmente **12 de 12 noticias** (N001-N012), superando el mínimo de 10 indicado en el laboratorio. La revisión comparó la noticia original, el texto limpio y el JSON generado. El objetivo fue detectar alucinaciones, confusión de roles, duplicidades, contaminación por contenido relacionado, relaciones sin respaldo y problemas de trazabilidad.

La ejecución final corresponde al workflow **LAB01 - Pipeline completo, run #7** del 26-09-2026. En esa ejecución se obtuvieron 12 JSON válidos, 0 JSON fallidos, 0 relaciones con endpoints no trazables y 10 pruebas automatizadas aprobadas.

## Resultado por noticia

| ID | Evaluación manual | Observaciones finales |
|---|---|---|
| N001 | Aceptable con observaciones | El hecho principal, detenido, lugar y jarabes de codeína están correctamente recuperados. Persisten variantes nominales de la misma organización (`Primera Comisaría`, `1ª Comisaría`, `Carabineros Región de Coquimbo`) y la valorización monetaria se conserva como `cantidad` textual del medicamento, por lo que no debe interpretarse como cantidad física. |
| N002 | Aceptable con observaciones | Conserva robo de camioneta, persecución, víctima y detenidos. Gemini genera dos etiquetas semánticamente equivalentes para el delito (`robo de auto` y `robo de su vehículo`) y duplica conceptualmente `camioneta` / `vehículo`. |
| N003 | Aceptable con observaciones | Distingue los dos homicidios y conserva la condición de `presunta autora`. Persisten correferencias duplicadas para la misma víctima y la misma imputada; además, `impactos de bala/balísticos` aparecen tipificados como objetos de tipo arma, lo que es una clasificación semántica imperfecta. |
| N004 | Conforme | Identifica a Matías Letelier como detenido, los tres delitos explícitos y el contexto de La Serena. No se infiere pertenencia a Carabineros. La descripción del vehículo es algo más genérica que la fuente, pero no altera el hecho. |
| N005 | Conforme | Conserva homicidio, víctima, arma cortopunzante, presunto autor y detención por seguridad municipal. Las relaciones mantienen la condición de presunción. |
| N006 | Conforme | Recupera víctima, captura, lugares y objetos incautados. No se inventa identidad ni nacionalidad específica. |
| N007 | Conforme con criterio conservador | Recupera como actor central a los cinco gendarmes detenidos, los delitos investigados, lugares y objetos incautados. La relación de presunta vinculación no se conserva porque su destino no era una entidad exacta del JSON; el postproceso la descarta para evitar un enlace huérfano. |
| N008 | Conforme | Mantiene que la víctima fue hallada en un pozo y que se investiga un homicidio; no afirma que el pozo haya sido definitivamente el lugar del asesinato. |
| N009 | Conforme | Recupera víctima, terminal, arma cortante y que el autor era buscado. No atribuye participación delictiva a la locataria. |
| N010 | Conforme | Corrige una falla observada en una ejecución anterior: ya no clasifica a detectives como detenidos y conserva la incertidumbre mediante `HABRIA_COMETIDO` y `HABRIA_AGREDIDO_A`. |
| N011 | Conforme | La versión final ya no incorpora la noticia recomendada del bloque `Lee también`. Conserva Los Shein, Y.A.P.L., delitos, armas, municiones, vehículos y drogas sin introducir el homicidio de otra noticia. |
| N012 | Aceptable con observaciones | Recupera a los dos detenidos, Tierras Blancas, Coquimbo, tráfico de drogas, robo con violencia y lesiones. Omite `tenencia de armas` en la lista final de delitos, aunque aparece en la fuente como parte del prontuario mencionado. |

## Problemas detectados durante la auditoría y correcciones aplicadas

1. **Fechas faltantes en Cooperativa.** El fallback de fecha contenía una expresión regular incorrectamente escapada. Se corrigieron los patrones para URLs normales y AMP y se añadieron pruebas unitarias específicas.
2. **Contaminación por noticias relacionadas en BioBioChile.** El cuerpo podía incluir tarjetas `Lee también`. Se añadió una regla de limpieza que elimina el marcador y el titular/fecha de la tarjeta asociada. Esto corrigió N011, que en una ejecución previa incorporó erróneamente un delito de otra noticia.
3. **Roles y presunción.** El prompt fue reforzado para distinguir detenido, imputado, víctima, autor presunto y colectivos institucionales. También se exigió conservar marcadores de incertidumbre como `presunto` y `habría`.
4. **Cantidades y valorizaciones.** Se indicó explícitamente que una valorización monetaria no equivale a dinero incautado y que el número de heridas no debe convertirse en cantidad del arma.
5. **Relaciones huérfanas.** Se añadió postproceso determinista: una relación solo se conserva si origen y destino coinciden con entidades ya presentes en el mismo JSON. La ejecución final registra **0 advertencias de relaciones dudosas**.
6. **Duplicados exactos.** El postproceso elimina duplicados exactos en delitos, organizaciones, lugares, personas, objetos y relaciones. No se aplica una fusión semántica agresiva para evitar combinar entidades distintas por error.

## Errores residuales y limitaciones

La auditoría final no detectó JSON inválidos ni relaciones huérfanas, pero sí conserva errores semánticos menores propios de la extracción con LLM: variantes nominales, correferencias no fusionadas, etiquetas conceptualmente redundantes y alguna omisión puntual. Estos casos se documentan en lugar de corregirse silenciosamente, porque una normalización automática agresiva podría introducir errores de identidad o modificar hechos de la fuente.

Por esta razón, los resultados del grafo y del Data Understanding deben interpretarse como **estructura documental del corpus periodístico**, no como estadísticas oficiales de criminalidad ni como determinación de culpabilidad.

## Trazabilidad auditada

Para cada ID se preserva la cadena:

`NXXX -> URL/fuente -> HTML RAW -> texto procesado -> JSON Gemini -> validación -> Markdown Obsidian -> entidades/relaciones`.

Los archivos RAW y textos procesados se regeneran durante GitHub Actions y se incluyen en el artifact de evidencia; el repositorio conserva los elementos reproducibles y las salidas estructuradas sin publicar la API key.
