# Evidencia reproducible de la ejecución final

Esta página reúne los elementos que permiten comprobar las cifras usadas en el informe sin depender de una afirmación escrita.

## Ejecución

- Workflow: `LAB01 - Pipeline completo`
- Run: **#14**
- Run ID: **36354954389**
- Resultado: **SUCCESS**
- Commit de entrada: `a56119a0f1fab19fc65a792ea7058c7f499c4d60`
- Modelo: `gemini-3.5-flash-lite`
- Python: **3.12.14**
- SDK `google-genai`: **2.25.0**

## Evidencia dentro del repositorio

- `data/urls.csv`: IDs y URLs del corpus.
- `data/processed/N001.txt` ... `N012.txt`: texto enviado a extracción.
- `data/json/N001.json` ... `N012.json`: resultados estructurados.
- `data/validation/*.validation.json`: validación por noticia.
- `obsidian_vault/`: persistencia final Markdown.
- `outputs/test_results.txt`: resultado de 19 pruebas.
- `outputs/environment_runtime.txt`: versiones y metadatos de ejecución.
- `outputs/resumen_data_understanding.json`: métricas del corpus.
- `outputs/visualizaciones/`: siete gráficos.
- `docs/auditoria_manual_final.md`: revisión humana de N001-N012.
- `docs/trazabilidad.md`: rutas completas por ID.
- `docs/esquema_json.md`: contrato de datos y reglas de postproceso.

## Evidencia conservada como artifact de GitHub Actions

El workflow empaqueta además `data/raw/`, `data/llm_raw/`, `data/processed/`, JSON, validaciones, vault, outputs y logs. El HTML completo y la respuesta cruda del LLM no se publican como archivos normales del repositorio, pero quedan asociados a la ejecución para auditoría.

## Comprobaciones finales

- Captura HTTP: 12/12
- Limpieza: 12/12
- JSON válidos/fallidos: 12/0
- JSON inválidos: 0
- Relaciones extraídas: 38
- Vault: 185 archivos Markdown
- Enlaces rotos: 0
- Tests: 19/19
- Auditoría manual: 12/12
