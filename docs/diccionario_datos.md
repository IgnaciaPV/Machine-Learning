# Diccionario de datos

| Campo | Tipo | Regla |
|---|---|---|
| `id_noticia` | string | ID estable `NXXX` proveniente de `urls.csv`. |
| `titulo` | string/null | Título de la noticia; si la extracción lo omite se conserva el metadata capturado. |
| `fecha_publicacion` | string/null | Fecha publicada por la fuente, preferentemente ISO 8601. |
| `fuente` | string | Medio del `urls.csv`; no se delega al LLM. |
| `url` | string | URL original trazable; no se delega al LLM. |
| `resumen` | string/null | Síntesis extractiva sin añadir hechos. |
| `delitos` | list[string] | Solo tipos explícitamente mencionados/investigados. |
| `personas` | list[object] | `nombre`, `rol`; rol puede ser `null` si no está explícito. |
| `organizaciones` | list[string] | Instituciones, bandas, empresas, tribunales u organismos explícitos. |
| `lugares` | list[string] | Lugares explícitos. |
| `objetos` | list[object] | `tipo`, `nombre`, `cantidad`, `unidad`; cantidad/unidad pueden ser `null`. |
| `relaciones` | list[object] | `origen`, `tipo`, `destino`; debe existir respaldo textual explícito. |
