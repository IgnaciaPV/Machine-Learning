# Business Understanding

## Usuario y problema

El usuario conceptual es un **analista de información delictual** que necesita transformar noticias públicas, no estructuradas y heterogéneas en conocimiento consultable. El problema no es almacenar artículos, sino conservar trazabilidad y convertir hechos, entidades y relaciones explícitas en una red navegable.

## Objetivo

Construir un pipeline reproducible que capture noticias delictuales públicas, limpie el contenido, extraiga información estructurada con Gemini, valide el JSON y genere automáticamente una bóveda Obsidian que permita explorar conexiones documentales entre delitos, personas, organizaciones, lugares y objetos.

## Alcance del corpus

- **Área geográfica:** Región de Coquimbo, Chile.
- **Ventana:** noticias publicadas durante 2026 disponibles públicamente.
- **Corpus semilla congelado:** 12 noticias verificadas, suficientes para probar el pipeline completo, realizar estadística descriptiva básica, generar un grafo no trivial y auditar manualmente al menos 10 casos sin convertir la adquisición masiva en el objetivo del laboratorio.
- **Fuentes del corpus semilla:** Cooperativa y BioBioChile. El módulo de adquisición soporta además La Tercera y un fallback genérico.
- **Tipos delictuales:** homicidio y hechos investigados como homicidio, tráfico de drogas, robo de vehículo, receptación, usurpación de funciones, infracciones de armas y delitos asociados cuando la fuente los menciona expresamente.

## Entidades

1. Noticia: título, fecha, fuente, URL y resumen.
2. Delito: tipo delictual principal o secundario explícitamente mencionado.
3. Persona: nombre/referencia y rol explícito.
4. Organización: banda, institución, tribunal, fiscalía, organismo policial u otra organización nombrada.
5. Lugar: comuna, ciudad, región, país o punto geográfico.
6. Objeto: arma, sustancia, vehículo, dinero u otro elemento relevante/incautado.
7. Relación: enlace explícito entre entidades, expresado con un tipo semántico estable.

## Criterio de relación entre noticias

Dos noticias pueden observarse como relacionadas cuando comparten **exactamente** un delito, una persona con identidad verificada, una organización, un lugar u otra entidad normalizada de forma conservadora. No se entrena clustering y no se infieren similitudes latentes.

## Información incompleta y ausente

- Los nombres incompletos, iniciales o descripciones se conservan como aparecen; no se intenta identificar a la persona por similitud.
- Cuando un escalar no aparece, se usa `null`.
- Cuando una colección no tiene elementos respaldados, se usa `[]`.
- No se transforma “detenido”, “imputado”, “acusado”, “condenado”, “víctima” o “testigo” en roles equivalentes.

## Restricciones éticas

- Una investigación, detención o imputación no implica culpabilidad.
- Solo se extrae información explícita de la fuente.
- Se conserva URL y medio para volver al contexto original.
- No se intenta perfilar personas ni inferir características sensibles.
- El resultado es académico y exploratorio, no una base de inteligencia operativa ni una estadística oficial de criminalidad.

## Criterios de éxito

El laboratorio se considera técnicamente exitoso si mantiene trazabilidad NXXX de extremo a extremo; genera JSON válidos conforme al esquema; produce una bóveda con enlaces internos sin roturas; permite responder preguntas descriptivas sobre fuentes, delitos, lugares, entidades y relaciones; y documenta mediante auditoría manual las limitaciones y errores de extracción.

Una misma descripción de persona en documentos distintos no prueba identidad. Las referencias repetidas se mantienen separadas por ID de noticia; las conexiones entre los casos pueden analizarse a través de delitos, organizaciones y lugares explícitos.
