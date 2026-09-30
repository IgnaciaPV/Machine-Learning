# Auditoría de cierre del Laboratorio 01

Fecha local: 29 de septiembre de 2026 (Chile). Revisión del repositorio público `IgnaciaPV/Machine-Learning`, sin reconstrucción, nuevas llamadas Gemini ni reescritura Git.

## Pauta y evidencia

| Criterio de la presentación LAB01 | Peso propuesto | Estado verificado | Evidencia |
|---|---:|---|---|
| Business Understanding y alcance | 10% | Documentado | `docs/business_understanding.md`, informe I y III-A |
| Modelo de conocimiento y JSON | 15% | Verificado, con limitaciones explícitas de identidad | `src/modelos.py`, esquema, 12 JSON, referencias separadas por noticia |
| Adquisición y limpieza | 15% | Verificado sobre RAW histórico; corregida pérdida de texto inline | 12 capturas `http_live` en ZIP, 12 textos revisados, tests de limpieza |
| Gemini y validación | 20% | Extracción histórica confirmada y revisión posterior trazable | Run #14, 12 respuestas originales, Pydantic, 12 validaciones, registro de correcciones |
| Vault Obsidian | 20% | 185 notas, 0 enlaces rotos; 37 referencias de persona separadas | Jerarquía, índice, wikilinks, notas de relaciones y pruebas |
| Data Understanding | 10% | 7 gráficos y sus interpretaciones; frecuencias documentales | JSON, CSV, gráficos, `outputs/interpretacion_visualizaciones.md` |
| Crítica, ética y reproducibilidad | 10% | Documentado y verificado en el alcance disponible | Auditoría manual previa, registro de cierre, tests, entorno, historial y ZIP |

Esta matriz usa los siete pesos de la presentación, titulados allí «Pauta de evaluación propuesta». No asigna nota ni porcentajes de logro. La clase Preliminares también indica evaluación global de LAB01: revisión de código 30%, trazabilidad 20% e informe 50%; ambas estructuras no se convierten ni se suman entre sí.

## Resultados y alcance de la verificación

- Origen: pipeline #14, ID 36354954389, commit `a56119a0f1fab19fc65a792ea7058c7f499c4d60`, actor `IgnaciaPV`, SUCCESS. Logs: 12 extracciones con `gemini-3.5-flash-lite`, 0 entradas ERROR.
- El artifact original coincide byte a byte con los resultados de entrada al cierre: 12 textos, 12 JSON, 12 validaciones, 185 Markdown y 15 archivos de outputs.
- Cierre: 12 JSON válidos, 37 relaciones, 185 Markdown y 0 enlaces rotos. Pruebas: 23/23 con RAW restaurado; 22 ejecutadas y 1 omitida expresamente en una clonación sin RAW.
- Las 36 etiquetas distintas de persona no equivalen a individuos únicos. Hay 37 referencias por noticia, incluyendo descripciones colectivas y correferencias. Las 26 etiquetas de organización también conservan variantes no fusionadas.
- La auditoría manual previa 12/12 consta en la documentación. La revisión adicional es asistida; no inventa una nueva firma humana ni atribuciones individuales.
- El vault se verificó por estructura, generación determinista y enlaces. No se afirma haber abierto una aplicación nativa Obsidian en este entorno.
- Los siete gráficos siguen válidos porque no cambiaron fuente, fecha, listas de delitos/lugares/objetos ni cantidad de entidades por noticia. Las menciones de delitos incluyen antecedentes; no representan incidencia criminal.

## Correcciones justificadas

`docs/correcciones_cierre.json` registra los valores antes/después y hashes. Se corrigió el filtrado de texto inline, rechazo de raíces JSON no objeto, identidad de personas repetidas, incertidumbre en cinco resúmenes, rol explícito de Eugenio Olea, una relación geográfica inferida y los verbos/contexto de N012. Se aseguró además `pipefail` en el paso de tests de CI, para que `tee` no oculte una falla de pruebas. Se mantuvieron arquitectura, dependencias, autoría declarada e historial.

Los textos del repositorio son la revisión de limpieza del cierre. Para reconstruir la entrada exacta del LLM se usan los textos del ZIP original, cuyos hashes están registrados; no se atribuyen los textos revisados al run #14.

## Seguridad y conservación

Se revisaron 1112 blobs históricos únicos antes del cierre y los archivos modificados: sin coincidencias de patrones de claves Google, tokens GitHub, claves AWS ni claves privadas. Solo `.env.example` está versionado, sin valores secretos. La comprobación basada en patrones no constituye una prueba absoluta de ausencia de cualquier secreto posible.

El artifact GitHub ID 10943591125 vence el 04-10-2026 a las 22:22 UTC. Se conserva una copia íntegra descargada como `LAB01_Evidencia_Run14_Original.zip`, SHA-256 `457341f305b19d2cce57d379e0dc75db39510010fe523de4b02baaf86287b1c8`, para adjuntar y preservar la evidencia.

## Limitaciones que no se ocultan

Persisten omisiones de entidades y roles, descripciones colectivas, variantes de organizaciones y correferencias. No se dispone de un conjunto etiquetado para medir precisión/recall. La muestra es intencional, pequeña y no representativa. Ningún JSON válido ni test aprobado demuestra exhaustividad o corrección semántica total.

Antes de enviar, adjuntar el PDF y el enlace del repositorio; incluir el ZIP original como evidencia de captura y extracción para que su acceso no dependa del artifact temporal.
