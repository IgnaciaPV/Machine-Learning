# ML-2026-02-LAB01 — Noticias delictuales, Gemini y Obsidian

Laboratorio 01 del Minor de Sistemas Inteligentes / Machine Learning de la Universidad Católica del Norte. El proyecto transforma noticias delictuales públicas en un **grafo de conocimiento Markdown navegable en Obsidian**, manteniendo trazabilidad desde la URL hasta el JSON validado y las notas finales.

## Estado final verificado

El corpus procede de **GitHub Actions, pipeline #14 (27-09-2026), SUCCESS**. Ese run capturó 12 noticias, consultó Gemini y produjo 12 JSON válidos, 38 relaciones y 19/19 pruebas aprobadas. Su evidencia original se conserva sin modificar.

La revisión de cierre del **29-09-2026 (Chile)** detectó pérdidas de texto inline, sobreafirmaciones en resúmenes, una relación geográfica inferida y una referencia de persona compartida entre casos distintos. Se corrigieron de forma acotada, **sin recapturar ni volver a consultar Gemini**. El registro de cambios y hashes está en [`docs/correcciones_cierre.json`](docs/correcciones_cierre.json).

Estado de entrega después de ese cierre:

- 12 noticias y 12 JSON válidos, sin fallos estructurales;
- 37 relaciones documentales;
- 36 etiquetas distintas de persona en 37 referencias por noticia; no es un conteo de individuos reales;
- 26 etiquetas distintas de organización, con variantes institucionales todavía presentes;
- 185 notas Markdown y 0 wikilinks rotos;
- 7 visualizaciones, cuyos recuentos siguen vigentes;
- 23/23 pruebas offline aprobadas con el RAW restaurado;
- auditoría manual previa de 12/12 documentada; cierre adicional asistido y trazable.

Los textos actuales son una revisión posterior de limpieza. Las entradas exactas enviadas a Gemini y sus respuestas originales están en **LAB01_Evidencia_Run14_Original.zip**. No se atribuyen las correcciones posteriores al run #14.

## Automatización y trazabilidad del historial

Este repositorio usa **GitHub Actions como integración continua**, por lo que algunos commits aparecen técnicamente atribuidos a `github-actions[bot]`. Esto ocurre cuando un workflow genera y publica un artefacto reproducible, por ejemplo los JSON/validaciones/vault derivados del pipeline o el PDF compilado del informe. Durante la integración inicial del proyecto también se usaron automatizaciones para materializar archivos en el repositorio, por lo que el historial contiene otros commits de esa cuenta de servicio.

`github-actions[bot]` es la identidad técnica del proceso automático de GitHub; no corresponde a un integrante adicional ni a una fuente de datos. El **run #14** del pipeline fue activado por `IgnaciaPV`, ejecutó el commit `a56119a0f1fab19fc65a792ea7058c7f499c4d60` y terminó en **SUCCESS**. El historial se mantiene sin reescritura para conservar trazabilidad entre cambios, ejecuciones y artefactos generados.

## Enfoque de ingeniería y automatización

El laboratorio se aborda como un proceso de transformación de información con etapas controlables: adquisición, limpieza, extracción, validación, generación de conocimiento y análisis. La programación implementa y estandariza ese flujo, mientras el criterio humano define el alcance, las reglas semánticas, el tratamiento de roles y la interpretación de resultados. La automatización permite repetir operaciones y concentrar la revisión en decisiones que no pueden garantizarse solo mediante código o un LLM.

## Objetivo

El pipeline implementa:

```text
Noticias públicas
  -> descubrimiento/URLs
  -> captura HTML
  -> limpieza y texto útil
  -> Gemini (extracción estructurada)
  -> validación independiente del JSON
  -> Markdown enlazado
  -> Obsidian
  -> Data Understanding + auditoría crítica
```

No se entrena clustering. Los agrupamientos emergen por entidades y relaciones explícitas compartidas. Las etiquetas de persona repetidas se mantienen separadas por noticia hasta disponer de evidencia de identidad.

## Estructura

```text
ML-2026-02-LAB01/
├── main.py
├── environment.yml
├── .env.example
├── data/
│   ├── urls.csv
│   ├── consultas.csv
│   ├── raw/
│   ├── processed/
│   ├── json/
│   └── validation/
├── src/
│   ├── pipeline.py
│   ├── modelos.py
│   ├── auditoria_manual.py
│   ├── adquisicion/
│   ├── limpieza/
│   ├── extraccion/
│   ├── validacion/
│   ├── conocimiento/
│   └── analisis/
├── obsidian_vault/
├── outputs/
├── docs/
├── tests/
└── report/
```

## Entorno reproducible

La pauta solicita Conda y no `requirements.txt`.

```bash
conda env create -f environment.yml
conda activate lab-noticias-obsidian
```

El entorno incluye `requests`, `beautifulsoup4`, `lxml`, `feedparser`, `pandas`, `matplotlib`, `python-dotenv`, `pydantic` y el SDK `google-genai`.

## Configuración de Gemini

1. Copiar `.env.example` como `.env`.
2. Agregar localmente la clave:

```dotenv
GEMINI_API_KEY=su_clave
```

3. Opcionalmente fijar un modelo:

```dotenv
GEMINI_MODEL=gemini-3.5-flash-lite
```

`.env` está excluido de Git. El código nunca imprime la clave.

El extractor usa el SDK actual `google-genai`, intenta la API **Interactions** con salida estructurada y conserva un fallback a `models.generate_content` para compatibilidad. Si `GEMINI_MODEL` no está definido, consulta los modelos visibles y elige un modelo actual compatible de una lista preferida.

Documentación oficial de referencia:
- https://ai.google.dev/gemini-api/docs/get-started
- https://googleapis.github.io/python-genai/

## Corpus semilla

`data/urls.csv` contiene un corpus acotado de noticias reales de la Región de Coquimbo durante 2026. El tamaño fue elegido para:

- probar todas las etapas del pipeline;
- producir un grafo no trivial;
- permitir Data Understanding básico;
- revisar manualmente al menos 10 noticias;
- mantener trazabilidad y calidad antes que volumen.

La adquisición en vivo puede repetirse, aunque el contenido de las páginas y la salida del LLM pueden cambiar. Los HTML completos de `data/raw/` se regeneran desde las URLs y se conservan como evidencia del workflow, mientras que los textos ya limpiados de `data/processed/` sí se versionan porque son parte directa del laboratorio. En una máquina o en GitHub Actions con Internet, `capturar --forzar` vuelve a obtener las fuentes originales.

## Comandos

### 1. Descubrir noticias por RSS

```bash
python main.py descubrir
```

Lee `data/consultas.csv`, consulta el RSS público de Google News para Chile, deduplica por URL y añade IDs estables `NXXX`.

### 2. Capturar y limpiar

```bash
python main.py capturar
```

Para recapturar aunque exista caché:

```bash
python main.py capturar --forzar
```

Genera `data/raw/NXXX.html`, metadata lateral y `data/processed/NXXX.txt`. Para la revisión final se reutilizó el RAW del run #14; no se recapturaron las fuentes.

### 3. Extraer con Gemini y validar

```bash
python main.py extraer
```

La salida se escribe en `data/json/NXXX.json`; cada archivo se valida de manera independiente y su reporte queda en `data/validation/`.

Para reextraer:

```bash
python main.py extraer --forzar
```

### 4. Generar Obsidian

```bash
python main.py obsidian
```

Crea:

```text
obsidian_vault/
├── 00_Indice.md
├── Noticias/
├── Delitos/
├── Personas/
├── Organizaciones/
├── Lugares/
├── Objetos/
└── Relaciones/
```

El generador audita los wikilinks internos y falla si detecta enlaces rotos con ruta.

### 5. Data Understanding

```bash
python main.py analizar
```

Genera estadísticas y visualizaciones en `outputs/`, entre ellas cobertura por fuente, delitos, lugares, entidades por noticia, faltantes y evolución temporal.

### 6. Auditoría manual

```bash
python main.py auditar
```

Construye una guía de comparación en `docs/auditoria_llm.md` a partir de una referencia humana preparada para 10 noticias. La herramienta ayuda a detectar omisiones, roles mal asignados y relaciones dudosas, pero no reemplaza la lectura manual de original -> texto limpio -> JSON.

### 7. Pipeline completo

```bash
python main.py pipeline
```

Para repetir el flujo sobre las mismas URLs semilla sin añadir URLs nuevas (la respuesta del LLM puede variar):

```bash
python main.py pipeline --sin-descubrir
```

## Contrato JSON

Campos obligatorios:

- `id_noticia`
- `titulo`
- `fecha_publicacion`
- `fuente`
- `url`
- `resumen`
- `delitos`
- `personas` (`nombre`, `rol`)
- `organizaciones`
- `lugares`
- `objetos` (`tipo`, `nombre`, `cantidad`, `unidad`)
- `relaciones` (`origen`, `tipo`, `destino`)

Los metadatos de trazabilidad (`id_noticia`, `fuente`, `url`) no se confían al LLM: se restablecen desde el origen antes de la validación.

## Principios de extracción

- Solo información explícita de la noticia.
- Ausencia de escalar -> `null`; ausencia de colección -> `[]`.
- No inferir culpabilidad.
- No equiparar detenido, imputado, acusado, condenado, víctima o testigo.
- No fusionar personas/organizaciones por similitud difusa.
- Toda relación debe tener respaldo textual explícito.

## Correcciones de cierre y evidencia histórica

`docs/auditoria_cierre.md` contrasta la pauta y el estado de entrega. `docs/correcciones_cierre.json` registra las modificaciones semánticas y los hashes de las entradas originales. El artifact `LAB01-evidencia` del run #14 conserva HTML, respuestas LLM, textos originales y logs, pero **vence el 04-10-2026 a las 22:22 UTC**. Se conserva además una copia íntegra descargada, `LAB01_Evidencia_Run14_Original.zip`, para adjuntar con la entrega. El ZIP conserva los datos originales; no contiene las correcciones posteriores.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas cubren adquisición, fechas, limpieza, eliminación de bloques editoriales ajenos, prompt y parsing estructurado, controles de presunción, reclasificación de tribunales, validación, Obsidian, enlaces internos, Data Understanding y trazabilidad. El run #14 aprobó 19/19. La suite ampliada de cierre aprobó 23/23 con los RAW restaurados; en una clonación nueva omite explícitamente solo la comprobación de RAW no versionado y ejecuta las otras 22 pruebas.

## Abrir la bóveda

En Obsidian:

1. **Open folder as vault / Abrir carpeta como bóveda**.
2. Seleccionar `obsidian_vault/`.
3. Abrir `00_Indice.md`.
4. Revisar backlinks y **Graph view** para explorar conexiones.

## Ética y limitaciones

Este proyecto es académico y exploratorio. Una investigación, detención o imputación no equivale a condena. La frecuencia de delitos o lugares en el corpus refleja una selección periodística pequeña, no una estadística oficial de criminalidad. Consulte `docs/etica_limitaciones.md` y la URL original antes de interpretar un caso.

## Documentación

- `docs/business_understanding.md`
- `docs/arquitectura.md`
- `docs/diccionario_datos.md`
- `docs/decisiones_tecnicas.md`
- `docs/etica_limitaciones.md`
- `docs/referencia_auditoria_manual.json`
- `docs/auditoria_llm.md` (guía generada al ejecutar la auditoría)
- `docs/auditoria_manual_final.md` (revisión humana final N001-N012)
- `docs/esquema_json.md` (estructura y reglas de modelado)
- `docs/trazabilidad.md` (rutas N001-N012 desde fuente hasta Obsidian)
- `docs/evidencia_ejecucion.md` (archivos que permiten comprobar las cifras del informe)
- `docs/estado_ejecucion.md` (métricas y entorno del run final)
- `outputs/environment_runtime.txt` (modelo, Python y versiones de dependencias)
- `report/LAB01_Informe_Final.pdf` (informe académico final)

## Seguridad

Antes de publicar se revisa que no existan `.env`, API keys, contraseñas, caches o secretos. Nunca agregue la clave Gemini al código, al informe ni al repositorio.
