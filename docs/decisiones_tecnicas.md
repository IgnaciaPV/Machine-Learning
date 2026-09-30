# Decisiones técnicas y trazabilidad de fuentes

## Material inicial realmente disponible

La presentación oficial describe un repositorio donde adquisición y limpieza aparecen implementadas y el alumno completa extracción, validación, conocimiento y análisis. En los archivos efectivamente proporcionados para esta ejecución no venía ese repositorio: el ZIP de clase contiene la presentación y el notebook `01_obtener_y_limpiar_noticia.ipynb`; el ZIP de plantilla contiene el `main.tex` IEEE y una imagen de ejemplo. Por ello se reconstruyó la arquitectura indicada por la presentación sin cambiar sus responsabilidades, nombres conceptuales ni comandos.

## Gemini

Se usa el SDK vigente `google-genai`. El extractor intenta primero la API Interactions con `response_format` y esquema JSON; mantiene fallback a `models.generate_content` para instalaciones del SDK que aún utilicen esa vía. El modelo se puede fijar con `GEMINI_MODEL`; si se omite, se consulta la lista visible y se selecciona el primer modelo actual compatible de una lista preferida. Esto evita codificar de manera ciega un nombre antiguo.

## Normalización

La normalización de entidades es deliberadamente conservadora: Unicode, espacios, mayúsculas y acentos pueden compartir una clave técnica, pero no se usa fuzzy matching ni distancia de edición para fusionar personas u organizaciones.

## Captura en el entorno de desarrollo

El runtime utilizado para construir esta entrega no disponía de resolución DNS desde la terminal. Para no inventar datos, el corpus semilla se recuperó desde las páginas públicas mediante un navegador/lector web disponible y se conservaron snapshots semánticos del **contenido principal real** con URL, título y fecha. Los sidecars iniciales declaraban `modo=browser_semantic_snapshot`. El run #14 los reemplazó por capturas HTTP reales: sus 12 sidecars conservados declaran `modo=http_live`. En una máquina con Internet, `python main.py capturar --forzar` usa `requests` y reemplaza esos snapshots por captura HTTP real. Esta diferencia queda explícita para no hacer pasar un snapshot semántico por una copia byte-a-byte del HTML original.

## Cierre final

Se preservó el run #14 y se corrigió la limpieza inline sin nuevas dependencias. Las referencias de persona repetidas se separan por noticia: coincidencia textual no equivale a identidad. `36` y `26` son etiquetas normalizadas de persona y organización, no conteos certificados de individuos e instituciones. Las correcciones de JSON se registran como revisión asistida posterior al LLM, no como respuesta nueva de Gemini.
