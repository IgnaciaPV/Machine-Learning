# Estado final de ejecución - Laboratorio 01

**Fecha de verificación:** 26-09-2026  
**Repositorio:** `IgnaciaPV/Machine-Learning`  
**Workflow final:** `LAB01 - Pipeline completo`, run **#11**  
**Run ID:** `36276952811`  
**Resultado:** **SUCCESS**

## Ejecución validada

El workflow final completó correctamente:

1. verificación de `GEMINI_API_KEY`;
2. creación del entorno Conda desde `environment.yml`;
3. captura HTTP real;
4. pruebas automatizadas;
5. extracción real con Gemini y validación;
6. generación de la bóveda Obsidian;
7. Data Understanding y visualizaciones;
8. auditoría;
9. revisión de secretos;
10. publicación de salidas estructuradas;
11. empaquetado de evidencia.

## Indicadores finales

- Noticias procesadas: **12**
- Fuentes: **8 Cooperativa / 4 BioBioChile**
- JSON Gemini válidos / fallidos: **12 / 0**
- JSON estructuralmente inválidos: **0**
- Relaciones extraídas: **37**
- Relaciones dudosas detectadas por validador: **0**
- Noticias duplicadas: **0**
- Variantes nominales potenciales: **1 grupo**
- Personas únicas: **39**
- Organizaciones únicas: **24**
- Archivos Markdown en Obsidian: **195**
- Enlaces rotos en Obsidian: **0**
- Visualizaciones de Data Understanding: **7**
- Auditoría manual: **12/12 noticias**
- Pruebas automatizadas: **14/14 aprobadas**

## Data Understanding

El delito más frecuente del corpus es **homicidio (6 noticias)**, seguido por **tráfico de drogas (3)**. El lugar con mayor mención es **Región de Coquimbo (7)**; La Serena aparece en 5 y Coquimbo en 4. El único campo con ausencia a nivel de noticia es **objetos (8,33%)**; los demás campos auditados registran 0% de ausencia.

Estos valores caracterizan el corpus periodístico seleccionado y no constituyen estadísticas oficiales de criminalidad.

## Seguridad y reproducibilidad

- La API key no está versionada.
- `.env` se excluye mediante `.gitignore`.
- GitHub Actions consume `secrets.GEMINI_API_KEY`.
- El entorno oficial se reproduce mediante `environment.yml`; no se usa `requirements.txt`.
- `main.py` actúa como orquestador.
- La lógica se distribuye en clases/módulos dentro de `src/`.
- El workflow recaptura fuentes, reextrae con Gemini, valida, reconstruye Obsidian y reproduce los análisis.
- La auditoría de secretos del workflow final terminó correctamente.

## Limitaciones

No quedan bloqueos técnicos para reproducir el laboratorio. Permanecen limitaciones metodológicas documentadas: tamaño pequeño del corpus, sesgo por selección de medios, variabilidad del LLM, correferencias y necesidad de validación humana para decisiones semánticas finas.
