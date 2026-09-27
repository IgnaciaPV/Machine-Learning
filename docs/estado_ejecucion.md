# Estado final de ejecución - Laboratorio 01

**Fecha de verificación:** 27-09-2026  
**Repositorio:** `IgnaciaPV/Machine-Learning`  
**Workflow final:** `LAB01 - Pipeline completo`, run **#14**  
**Run ID:** `36354954389`  
**Commit de entrada:** `a56119a0f1fab19fc65a792ea7058c7f499c4d60`  
**Resultado:** **SUCCESS**

## Resultado de la ejecución

La versión final completó sin errores:

1. verificación de `GEMINI_API_KEY`;
2. creación del entorno Conda desde `environment.yml`;
3. registro de versiones del entorno;
4. captura HTTP real y limpieza;
5. pruebas automatizadas;
6. extracción con Gemini y validación;
7. generación de la bóveda Obsidian;
8. Data Understanding y siete visualizaciones;
9. auditoría de la muestra;
10. revisión de secretos;
11. publicación de resultados reproducibles;
12. empaquetado del artifact de evidencia.

## Indicadores finales

- Noticias del corpus: **12**
- Capturadas / limpiadas: **12 / 12**
- Fuentes: **8 Cooperativa / 4 BioBioChile**
- JSON válidos / fallidos: **12 / 0**
- JSON estructuralmente inválidos: **0**
- Relaciones extraídas: **38**
- Personas únicas: **36**
- Organizaciones únicas: **26**
- Noticias duplicadas: **0**
- Variantes nominales potenciales: **1 grupo**
- Archivos Markdown del vault: **185**
- Enlaces rotos: **0**
- Visualizaciones: **7**
- Pruebas automatizadas: **19/19**
- Auditoría manual: **12/12 noticias**
- Advertencias estructurales de relaciones en la salida final: **0**

## Correcciones incorporadas después de la auditoría

- Los juzgados y tribunales se reclasifican como **organizaciones**, de acuerdo con el modelo de conocimiento del laboratorio.
- Las referencias genéricas `los uniformados`, `detectives`, `personal policial` y equivalentes no se modelan como personas.
- N007 ya no conserva una relación de “vinculación” cuyo destino era un lugar físico.
- N010 conserva la incertidumbre mediante relaciones como `HABRIA_COMETIDO` y `HABRIA_AGREDIDO_A`; se filtran relaciones afirmativas incompatibles con el rol de imputado.
- Las valorizaciones monetarias no se interpretan como cantidades físicas.
- El bloque `Lee también` de BioBioChile se elimina antes de enviar el texto a Gemini.
- Los textos procesados `data/processed/N001.txt` a `N012.txt` se versionan como parte del entregable.

## Entorno registrado

El archivo `outputs/environment_runtime.txt` conserva:

- Python 3.12.14
- google-genai 2.25.0
- pydantic 2.13.5
- pandas 3.0.6
- matplotlib 3.11.2
- requests 2.34.2
- beautifulsoup4 4.15.0
- modelo Gemini: `gemini-3.5-flash-lite`

La API key no se registra ni se imprime.
