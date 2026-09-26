# Estado de ejecución

Este documento separa claramente **implementación** de **resultados observados**.

## Implementado y verificado localmente

- Arquitectura modular con `main.py` como orquestador.
- Adquisición HTTP responsable, limpieza HTML, contrato JSON Pydantic, validación independiente, generación de Obsidian, Data Understanding y auditoría manual.
- Corpus semilla de 12 URLs reales de Cooperativa y BioBioChile.
- Pruebas unitarias de limpieza, parsing, validación, Obsidian y análisis.
- Workflow de GitHub Actions preparado para usar el secreto `GEMINI_API_KEY`.

## Pendiente de resultados reales

Los JSON, el vault final y las visualizaciones definitivas deben generarse ejecutando el workflow con acceso a Internet y la API de Gemini. No se incluyen resultados sintéticos ni se afirma éxito de una llamada a Gemini que no haya ocurrido.

## Criterio de cierre

El laboratorio se considera cerrado cuando el workflow produce: captura trazable, al menos 10 JSON válidos, auditoría manual de 10 casos, vault sin enlaces rotos, Data Understanding y evidencia de pruebas automatizadas.
