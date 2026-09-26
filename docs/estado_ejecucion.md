# Estado final de ejecución - Laboratorio 01

**Fecha de verificación:** 26-09-2026  
**Repositorio:** `IgnaciaPV/Machine-Learning`  
**Workflow final:** `LAB01 - Pipeline completo`, run **#7**  
**Resultado:** **SUCCESS**

## Ejecución validada

La ejecución final completó correctamente, en este orden:

1. verificación del secreto `GEMINI_API_KEY`;
2. instalación de Miniforge y creación del entorno desde `environment.yml`;
3. captura HTTP real de las fuentes;
4. ejecución de pruebas automatizadas;
5. extracción real con Gemini y validación;
6. generación del vault Obsidian;
7. Data Understanding y visualizaciones;
8. auditoría de muestra;
9. auditoría de secretos;
10. publicación de salidas estructuradas;
11. empaquetado de evidencia como artifact.

## Resultados finales

- Noticias del corpus: **12**
- Captura/limpieza procesada: **12/12**
- JSON Gemini válidos: **12/12**
- JSON fallidos: **0**
- JSON sintácticamente inválidos: **0**
- Fuentes: **8 Cooperativa, 4 BioBioChile**
- Relaciones extraídas: **31**
- Advertencias de relaciones no trazables: **0**
- Noticias duplicadas: **0**
- Pruebas automatizadas: **10/10 aprobadas**
- Auditoría manual: **12/12 noticias**
- Archivos Markdown del vault: **generados automáticamente para las 12 noticias y sus entidades**
- Enlaces rotos del vault: **0**
- Visualizaciones de Data Understanding: **7**

## Hallazgos de Data Understanding

El delito más frecuente en el corpus estructurado es **homicidio (6 noticias)** y la fuente con mayor presencia es **Cooperativa (8 de 12)**. La **Región de Coquimbo** aparece en 6 noticias; La Serena y Coquimbo registran 5 menciones cada una. El 8,33% de las noticias queda sin relaciones explícitas, mientras que el resto de los campos estructurales presenta 0% de ausencia en la ejecución final.

Estos recuentos describen únicamente el corpus periodístico seleccionado y no representan tasas oficiales de delincuencia.

## Seguridad y reproducibilidad

- La API key no está versionada.
- `.env` está ignorado por Git.
- GitHub Actions consume `secrets.GEMINI_API_KEY`.
- No existe `requirements.txt`; el entorno oficial se reproduce con `environment.yml`.
- `main.py` actúa como orquestador.
- La lógica se organiza en módulos OOP dentro de `src/`.
- Los HTML completos y textos procesados se generan durante la ejecución y se preservan como evidencia temporal del workflow, evitando publicar masivamente contenido periodístico completo en el repositorio.

## Limitaciones pendientes

No quedan bloqueos técnicos para ejecutar el laboratorio. Las limitaciones restantes son metodológicas: tamaño pequeño del corpus, sesgo de selección por medio y fecha, variabilidad semántica del LLM y necesidad de revisión humana para correferencias y normalización de entidades.
