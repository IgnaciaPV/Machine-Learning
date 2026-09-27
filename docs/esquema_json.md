# Esquema JSON y reglas de modelado

Este documento resume el contrato que se usa entre la extracción con Gemini, la validación y la generación de Obsidian. La idea es que el JSON sea una etapa intermedia controlada, no una respuesta libre del modelo.

## Campos de una noticia

| Campo | Tipo | Regla |
|---|---|---|
| `id_noticia` | string | Identificador estable `NXXX`; debe coincidir con `data/urls.csv`. |
| `titulo` | string o null | Título recuperado de la fuente. |
| `fecha_publicacion` | string o null | Fecha explícita de la noticia o recuperada desde la URL cuando el medio lo permite. |
| `fuente` | string | Medio de origen. No se delega al LLM. |
| `url` | string | URL original. No se delega al LLM. |
| `resumen` | string o null | Síntesis del hecho sin agregar culpabilidad ni datos externos. |
| `delitos` | lista de string | Solo delitos mencionados de forma explícita. |
| `personas` | lista de objetos | Cada elemento usa `nombre` y `rol`. |
| `organizaciones` | lista de string | Bandas, instituciones, empresas, tribunales, fiscalías y organismos policiales. |
| `lugares` | lista de string | Comunas, ciudades, regiones, países o puntos geográficos. |
| `objetos` | lista de objetos | `tipo`, `nombre`, `cantidad`, `unidad`. |
| `relaciones` | lista de objetos | `origen`, `tipo`, `destino`. |

## Reglas que se aplican después del LLM

- Un tribunal o juzgado se clasifica como **organización**, no como lugar.
- Expresiones colectivas como `los uniformados`, `detectives` o `personal policial` no se mantienen como personas individuales.
- Los tipos de relación se normalizan a mayúsculas y guiones bajos.
- Una relación se descarta si su origen o destino no existe en las entidades del mismo JSON.
- Una persona descrita como detenida, imputada, sospechosa o investigada no puede quedar asociada a una relación afirmativa de culpabilidad sin conservar la incertidumbre de la fuente.
- Una relación de “vinculación” no se conserva si termina en un lugar físico; es preferible omitirla a reinterpretar el texto.
- Una valorización monetaria de droga, medicamento u otro objeto no se transforma en cantidad física ni en dinero incautado.
- Se eliminan duplicados exactos. No se usa similitud difusa para fusionar nombres de personas u organizaciones.

## Ejemplo reducido

```json
{
  "id_noticia": "N005",
  "delitos": ["homicidio"],
  "personas": [
    {"nombre": "Un hombre", "rol": "víctima"},
    {"nombre": "el presunto autor del homicidio", "rol": "detenido"}
  ],
  "organizaciones": [
    "seguridad municipal",
    "Ministerio Público",
    "Juzgado de Garantía de Coquimbo"
  ],
  "lugares": ["Barrio Inglés", "Coquimbo", "hospital local"],
  "objetos": [
    {"tipo": "arma", "nombre": "arma cortopunzante", "cantidad": null, "unidad": null}
  ],
  "relaciones": [
    {"origen": "Un hombre", "tipo": "VICTIMA_DE_DELITO", "destino": "homicidio"},
    {"origen": "el presunto autor del homicidio", "tipo": "PRESUNTO_AUTOR_DE", "destino": "homicidio"}
  ]
}
```

El ejemplo se usa únicamente para mostrar la estructura. La fuente completa, el texto limpio y el JSON final se conservan por ID dentro del pipeline.
