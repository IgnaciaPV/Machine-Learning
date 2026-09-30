# Evidencia reproducible de la ejecución final

## Identidad técnica de los commits automáticos

El proyecto utiliza GitHub Actions para ejecutar el pipeline y compilar artefactos. Cuando un workflow ejecuta `git commit`, GitHub registra a `github-actions[bot]` como autor/committer técnico. El workflow `.github/workflows/lab01_pipeline.yml` publica salidas estructuradas y `.github/workflows/report_compile.yml` publica el PDF compilado. El historial también conserva automatizaciones utilizadas durante la integración inicial del repositorio.

Esta identidad de servicio no representa un tercer integrante ni una fuente del corpus. El run final del pipeline (#14, ID 36354954389) fue activado por `IgnaciaPV`, sobre el commit `a56119a0f1fab19fc65a792ea7058c7f499c4d60`, y terminó con estado `SUCCESS`. Mantener estos commits visibles permite auditar qué material fue producido automáticamente en vez de ocultarlo mediante reescritura del historial.

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

## Comprobaciones históricas del run #14

- Captura HTTP: 12/12
- Limpieza: 12/12
- JSON válidos/fallidos: 12/0
- JSON inválidos: 0
- Relaciones extraídas: 38
- Vault: 185 archivos Markdown
- Enlaces rotos: 0
- Tests: 19/19
- Auditoría manual: 12/12

## Cierre posterior sin nueva extracción

La entrega incorpora las correcciones verificadas en `docs/correcciones_cierre.json`: 12 JSON válidos, 37 relaciones, 185 notas y 0 enlaces rotos. La suite de cierre aprobó 23/23 (`outputs/test_results_cierre.txt`). El run #14 conserva sus cifras históricas 38 relaciones y 19 pruebas; no se presenta como una ejecución de los cambios posteriores.

`data/processed/` contiene la revisión de limpieza del cierre; los textos exactos enviados a Gemini permanecen dentro del ZIP original del run y se identifican por SHA-256. Los siete gráficos no se regeneraron: las correcciones no modificaron sus variables ni recuentos.

El artifact original ID 10943591125 vence el 04-10-2026 22:22 UTC. Se descargó y conservó intacto como `LAB01_Evidencia_Run14_Original.zip` (SHA-256 `457341f305b19d2cce57d379e0dc75db39510010fe523de4b02baaf86287b1c8`), para adjuntarlo con la entrega.
