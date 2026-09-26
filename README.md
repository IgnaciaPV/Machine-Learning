# ML-2026-02-LAB01 — Noticias delictuales, Gemini y Obsidian

Laboratorio 01 del Minor de Sistemas Inteligentes / Machine Learning de la Universidad Católica del Norte. El proyecto transforma noticias delictuales públicas en un **grafo de conocimiento Markdown navegable en Obsidian**, manteniendo trazabilidad desde la URL hasta el JSON validado y las notas finales.

## Estado final verificado

La versión final fue ejecutada de extremo a extremo en **GitHub Actions (run #11, 26-09-2026)** con estado **SUCCESS**:

- 12 noticias procesadas;
- 12 JSON válidos y 0 fallidos;
- 37 relaciones extraídas;
- 195 archivos Markdown en la bóveda;
- 0 enlaces rotos;
- 7 visualizaciones de Data Understanding;
- 14/14 pruebas automatizadas aprobadas;
- auditoría manual de 12/12 noticias;
- 0 relaciones dudosas detectadas por el validador final.

El detalle de ejecución está en [`docs/estado_ejecucion.md`](docs/estado_ejecucion.md) y la revisión humana caso a caso en [`docs/auditoria_manual_final.md`](docs/auditoria_manual_final.md).

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

No se entrena clustering. Los agrupamientos emergen por entidades y relaciones explícitas compartidas.

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
GEMINI_MODEL=gemini-3.8-flash
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

La adquisición en vivo es reproducible. Los archivos `data/raw/` y `data/processed/` se generan al ejecutar `capturar`; no se publican copias completas de las noticias en Git para evitar redistribuir contenido periodístico. En una máquina o GitHub Actions con Internet, `capturar --forzar` recaptura desde la URL original.

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

Genera `data/raw/NXXX.html`, metadata lateral y `data/processed/NXXX.txt`.

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

Construye `docs/auditoria_llm.md` a partir de una referencia humana preparada para 10 noticias. La herramienta ayuda a detectar omisiones, roles mal asignados y relaciones dudosas, pero no reemplaza la lectura manual de original -> texto limpio -> JSON.

### 7. Pipeline completo

```bash
python main.py pipeline
```

Para reproducir exactamente el corpus semilla sin añadir URLs nuevas:

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

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas cubren limpieza, prompt/parsing estructurado, validación, generación de Obsidian, enlaces internos, Data Understanding y trazabilidad del corpus.

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
- `docs/estado_ejecucion.md` (evidencia y métricas del run final)
- `report/LAB01_Informe_Final.pdf` (informe académico final, cuando se compila/publica)

## Seguridad

Antes de publicar se revisa que no existan `.env`, API keys, contraseñas, caches o secretos. Nunca agregue la clave Gemini al código, al informe ni al repositorio.
