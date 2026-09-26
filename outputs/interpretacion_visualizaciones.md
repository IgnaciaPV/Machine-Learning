# Data Understanding — interpretación de visualizaciones

Se analizaron **12** JSON legibles. Se detectaron **0** archivos JSON inválidos.

## 01. Noticias por fuente
El gráfico muestra la cobertura por medio. La fuente con más registros es **Cooperativa** (8 noticias). Esto permite identificar concentración de cobertura; no debe interpretarse como mayor incidencia delictual real, porque el corpus depende de la selección de noticias y de la agenda de cada medio.

## 02. Delitos frecuentes
El tipo más repetido en la extracción es **homicidio** (6 menciones a nivel de noticia). El patrón describe el corpus periodístico seleccionado, no una tasa delictual poblacional ni estadística policial oficial.

## 03. Lugares frecuentes
El lugar con más menciones es **Región de Coquimbo** (6). La concentración puede reflejar el alcance geográfico definido, la mayor producción noticiosa en comunas urbanas o la selección de fuentes; no demuestra por sí sola mayor riesgo delictual.

## 04. Delitos por lugar
La visualización apila **co-menciones dentro de una misma noticia**. Sirve para explorar conexiones documentales, pero no implica una relación causal ni reemplaza estadísticas oficiales por comuna.

## 05. Personas y organizaciones por noticia
El gráfico permite detectar notas densas en entidades y otras con poca información explícita. Valores altos suelen corresponder a operativos u organizaciones; valores bajos pueden reflejar hechos sin identidades publicadas o restricciones editoriales.

## 06. Campos faltantes
El mayor porcentaje de ausencia corresponde a **relaciones** (8.3%). En campos de personas, objetos o relaciones, una lista vacía puede ser correcta: la regla del laboratorio es no inventar información ausente.

## 07. Evolución temporal
La serie temporal describe cuándo se publicaron las noticias del corpus. Con una muestra pequeña, no debe interpretarse como tendencia criminal: está afectada por la ventana de recolección y la disponibilidad de artículos.

## Calidad del corpus
Duplicados detectados: **0** grupos. Variantes potencialmente inconsistentes de entidades: **1**. Advertencias de relaciones: **0**.

Las advertencias requieren revisión humana porque las equivalencias nominales y el respaldo semántico de una relación no pueden resolverse de forma segura mediante similitud textual agresiva.
