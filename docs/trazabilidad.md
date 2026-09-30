# Trazabilidad del corpus

Cada noticia mantiene el mismo identificador desde la selección de la URL hasta la nota de Obsidian. Esto permite revisar una extracción sin depender de nombres de archivo ambiguos.

| ID | Fuente | URL de origen | RAW | Texto limpio | JSON | Validación | Nota Obsidian |
|---|---|---|---|---|---|---|---|
| N001 | Cooperativa | registrada en `data/urls.csv` | `data/raw/N001.html` | `data/processed/N001.txt` | `data/json/N001.json` | `data/validation/N001.validation.json` | `obsidian_vault/Noticias/N001.md` |
| N002 | Cooperativa | registrada en `data/urls.csv` | `data/raw/N002.html` | `data/processed/N002.txt` | `data/json/N002.json` | `data/validation/N002.validation.json` | `obsidian_vault/Noticias/N002.md` |
| N003 | Cooperativa | registrada en `data/urls.csv` | `data/raw/N003.html` | `data/processed/N003.txt` | `data/json/N003.json` | `data/validation/N003.validation.json` | `obsidian_vault/Noticias/N003.md` |
| N004 | Cooperativa | registrada en `data/urls.csv` | `data/raw/N004.html` | `data/processed/N004.txt` | `data/json/N004.json` | `data/validation/N004.validation.json` | `obsidian_vault/Noticias/N004.md` |
| N005 | Cooperativa | registrada en `data/urls.csv` | `data/raw/N005.html` | `data/processed/N005.txt` | `data/json/N005.json` | `data/validation/N005.validation.json` | `obsidian_vault/Noticias/N005.md` |
| N006 | Cooperativa | registrada en `data/urls.csv` | `data/raw/N006.html` | `data/processed/N006.txt` | `data/json/N006.json` | `data/validation/N006.validation.json` | `obsidian_vault/Noticias/N006.md` |
| N007 | Cooperativa | registrada en `data/urls.csv` | `data/raw/N007.html` | `data/processed/N007.txt` | `data/json/N007.json` | `data/validation/N007.validation.json` | `obsidian_vault/Noticias/N007.md` |
| N008 | Cooperativa | registrada en `data/urls.csv` | `data/raw/N008.html` | `data/processed/N008.txt` | `data/json/N008.json` | `data/validation/N008.validation.json` | `obsidian_vault/Noticias/N008.md` |
| N009 | BioBioChile | registrada en `data/urls.csv` | `data/raw/N009.html` | `data/processed/N009.txt` | `data/json/N009.json` | `data/validation/N009.validation.json` | `obsidian_vault/Noticias/N009.md` |
| N010 | BioBioChile | registrada en `data/urls.csv` | `data/raw/N010.html` | `data/processed/N010.txt` | `data/json/N010.json` | `data/validation/N010.validation.json` | `obsidian_vault/Noticias/N010.md` |
| N011 | BioBioChile | registrada en `data/urls.csv` | `data/raw/N011.html` | `data/processed/N011.txt` | `data/json/N011.json` | `data/validation/N011.validation.json` | `obsidian_vault/Noticias/N011.md` |
| N012 | BioBioChile | registrada en `data/urls.csv` | `data/raw/N012.html` | `data/processed/N012.txt` | `data/json/N012.json` | `data/validation/N012.validation.json` | `obsidian_vault/Noticias/N012.md` |

## Ejemplo de revisión: N005

Para auditar N005 se puede seguir el recorrido completo sin buscar manualmente archivos:

1. abrir la URL guardada en `data/urls.csv`;
2. contrastar el HTML de `data/raw/N005.html`;
3. revisar qué quedó en `data/processed/N005.txt`;
4. comparar con `data/json/N005.json`;
5. comprobar estructura y advertencias en `data/validation/N005.validation.json`;
6. abrir `obsidian_vault/Noticias/N005.md` y seguir sus wikilinks.

La misma secuencia funciona para N001-N012. En GitHub Actions, `data/raw/` y `data/processed/` también quedan empaquetados en el artifact de evidencia de la ejecución.

## Distinción de versiones

Los RAW y las respuestas LLM del run #14 se conservan en `LAB01_Evidencia_Run14_Original.zip`. El artifact temporal vence el 04-10-2026. `data/processed/` y algunos JSON incorporan revisiones posteriores; los hashes de las entradas originales y los valores antes/después constan en `docs/correcciones_cierre.json`. La secuencia histórica Gemini se reconstruye desde el ZIP, y la persistencia actual desde los JSON corregidos.
