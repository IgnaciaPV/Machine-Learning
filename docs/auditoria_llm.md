# Auditoría manual de extracción LLM

La referencia fue construida revisando noticia original/snapshot y texto limpio antes de observar la salida del LLM. La tabla siguiente sirve como guía de revisión humana; las coincidencias automáticas no sustituyen la lectura comparativa.

## N001

- Original/snapshot disponible: **sí**
- Texto limpio disponible: **sí**
- JSON Gemini: **disponible y legible**
- Hechos que la revisión humana exige preservar:
  - detención tras persecución en La Serena
  - incautación de jarabes de codeína
  - antecedente por tráfico de drogas en pequeñas cantidades
- Riesgos de inferencia que deben comprobarse manualmente:
  - que el detenido fue formalizado o condenado por tráfico en este hecho
  - identidad del detenido
- Señales automáticas de cobertura (solo apoyo):
  - ✓ lugares_esperados: La Serena
  - ✓ lugares_esperados: Río Elqui
  - ✓ lugares_esperados: Región de Coquimbo
  - ✓ organizaciones_esperadas: Carabineros
  - ✓ organizaciones_esperadas: Primera Comisaría
  - ✓ objetos_esperados: jarabes de codeína
  - ✓ objetos_esperados: vehículo/automóvil
- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.

## N002

- Original/snapshot disponible: **sí**
- Texto limpio disponible: **sí**
- JSON Gemini: **disponible y legible**
- Hechos que la revisión humana exige preservar:
  - robo de camioneta
  - persecución policial
  - un sospechoso herido y tres menores detenidos
- Riesgos de inferencia que deben comprobarse manualmente:
  - identidad de los menores
  - condenas o culpabilidad judicial
- Señales automáticas de cobertura (solo apoyo):
  - ✓ lugares_esperados: La Serena
  - ✓ lugares_esperados: Avenida del Mar
  - ✓ lugares_esperados: Avenida Francisco de Aguirre
  - ✓ lugares_esperados: Arcos de Pinamar
  - ✓ organizaciones_esperadas: Carabineros
  - ✓ organizaciones_esperadas: Hospital de La Serena
  - ✓ objetos_esperados: camioneta/vehículo
- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.

## N003

- Original/snapshot disponible: **sí**
- Texto limpio disponible: **sí**
- JSON Gemini: **disponible y legible**
- Hechos que la revisión humana exige preservar:
  - dos homicidios investigados por separado
  - víctima masculina no identificada con impactos balísticos en Coquimbo
  - mujer de 56 años detenida en investigación por homicidio de hombre de 85 años en Salamanca
- Riesgos de inferencia que deben comprobarse manualmente:
  - que ambos casos están relacionados
  - culpabilidad de la mujer detenida
  - identidad de la víctima no identificada
- Señales automáticas de cobertura (solo apoyo):
  - ✓ lugares_esperados: Coquimbo
  - ✓ lugares_esperados: Salamanca
  - ✓ lugares_esperados: Región de Coquimbo
  - ✓ lugares_esperados: Illapel
  - △ organizaciones_esperadas: PDI
  - ✓ organizaciones_esperadas: Brigada de Homicidios
  - ✓ organizaciones_esperadas: Fiscalía ECOH
  - ✓ organizaciones_esperadas: Laboratorio de Criminalística Regional de La Serena
  - ✓ organizaciones_esperadas: Juzgado de Garantía de Illapel
- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.

## N004

- Original/snapshot disponible: **sí**
- Texto limpio disponible: **sí**
- JSON Gemini: **disponible y legible**
- Hechos que la revisión humana exige preservar:
  - Matías Letelier fue detenido
  - simuló ser carabinero para realizar controles
  - usó un vehículo con encargo por robo
- Riesgos de inferencia que deben comprobarse manualmente:
  - condena
  - que pertenecía a Carabineros
- Señales automáticas de cobertura (solo apoyo):
  - ✓ delitos_esperados: usurpación de funciones públicas
  - ✓ delitos_esperados: infracción a la Ley de Control de Armas
  - ✓ delitos_esperados: receptación de vehículo
  - ✓ lugares_esperados: La Serena
  - △ lugares_esperados: Región de Coquimbo
  - ✓ organizaciones_esperadas: Carabineros
  - ✓ organizaciones_esperadas: Ministerio Público
  - ✓ objetos_esperados: vehículo con encargo por robo
  - ✓ objetos_esperados: balizas
  - ✓ objetos_esperados: elementos que simulaban pertenecer a Carabineros
- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.

## N005

- Original/snapshot disponible: **sí**
- Texto limpio disponible: **sí**
- JSON Gemini: **disponible y legible**
- Hechos que la revisión humana exige preservar:
  - riña en Barrio Inglés
  - víctima murió por tres estocadas
  - presunto autor colombiano de 38 años fue detenido
- Riesgos de inferencia que deben comprobarse manualmente:
  - nombre del imputado
  - condena
- Señales automáticas de cobertura (solo apoyo):
  - ✓ delitos_esperados: homicidio
  - ✓ lugares_esperados: Barrio Inglés
  - ✓ lugares_esperados: Coquimbo
  - ✓ organizaciones_esperadas: seguridad municipal
  - ✓ organizaciones_esperadas: Juzgado de Garantía de Coquimbo
  - ✓ organizaciones_esperadas: Ministerio Público
  - ✓ objetos_esperados: arma cortopunzante
- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.

## N006

- Original/snapshot disponible: **sí**
- Texto limpio disponible: **sí**
- JSON Gemini: **disponible y legible**
- Hechos que la revisión humana exige preservar:
  - mujer extranjera asesinada con arma cortopunzante
  - sospechoso huyó y fue capturado por Carabineros
  - arma cortopunzante hallada en su posesión
- Riesgos de inferencia que deben comprobarse manualmente:
  - identidad o nacionalidad específica no indicada
  - condena
- Señales automáticas de cobertura (solo apoyo):
  - ✓ delitos_esperados: homicidio
  - ✓ lugares_esperados: Diaguitas
  - ✓ lugares_esperados: Vicuña
  - ✓ lugares_esperados: Andacollito
  - ✓ lugares_esperados: Provincia de Elqui
  - ✓ lugares_esperados: Región de Coquimbo
  - ✓ organizaciones_esperadas: Carabineros
  - ✓ organizaciones_esperadas: Ministerio Público
  - ✓ objetos_esperados: arma cortopunzante
  - ✓ objetos_esperados: pistola de aire comprimido
  - ✓ objetos_esperados: elementos contundentes
- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.

## N007

- Original/snapshot disponible: **sí**
- Texto limpio disponible: **sí**
- JSON Gemini: **disponible y legible**
- Hechos que la revisión humana exige preservar:
  - Operación El Dorado
  - cinco gendarmes detenidos
  - 16 personas aprehendidas
  - 21 órdenes de entrada y registro
- Riesgos de inferencia que deben comprobarse manualmente:
  - culpabilidad de los gendarmes
  - pertenencia individual a cada delito sin respaldo
- Señales automáticas de cobertura (solo apoyo):
  - ✓ delitos_esperados: asociación criminal
  - ✓ delitos_esperados: tráfico de drogas
  - ✓ delitos_esperados: cohecho
  - ✓ delitos_esperados: ingreso de elementos ilícitos a un recinto penitenciario
  - ✓ delitos_esperados: lavado de activos
  - ✓ lugares_esperados: Illapel
  - ✓ lugares_esperados: Salamanca
  - ✓ lugares_esperados: Santiago
  - ✓ lugares_esperados: Tomé
  - ✓ lugares_esperados: Región del Biobío
  - ✓ lugares_esperados: Región de Coquimbo
  - ✓ organizaciones_esperadas: Fiscalía Regional de Coquimbo
  - ✓ organizaciones_esperadas: PDI La Serena
  - ✓ organizaciones_esperadas: Fiscalía de Illapel
  - ✓ organizaciones_esperadas: Gendarmería
  - ✓ objetos_esperados: teléfonos celulares
  - ✓ objetos_esperados: marihuana
  - ✓ objetos_esperados: ketamina
  - ✓ objetos_esperados: éxtasis
  - ✓ objetos_esperados: clonazepam
  - ✓ objetos_esperados: dinero en efectivo
  - ✓ objetos_esperados: cinco vehículos motorizados
- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.

## N008

- Original/snapshot disponible: **sí**
- Texto limpio disponible: **sí**
- JSON Gemini: **disponible y legible**
- Hechos que la revisión humana exige preservar:
  - hombre de 46 años hallado muerto en un pozo
  - lesiones atribuibles a terceros
  - PDI investiga si el pozo fue sitio del homicidio u ocultamiento
- Riesgos de inferencia que deben comprobarse manualmente:
  - identidad del autor
  - que el pozo fue definitivamente el lugar del asesinato
- Señales automáticas de cobertura (solo apoyo):
  - ✓ delitos_esperados: homicidio
  - ✓ lugares_esperados: Panulcillo
  - ✓ lugares_esperados: Ovalle
  - ✓ lugares_esperados: Región de Coquimbo
  - ✓ organizaciones_esperadas: Brigada de Homicidios
  - △ organizaciones_esperadas: PDI
  - ✓ objetos_esperados: objeto contundente
  - ✓ objetos_esperados: pozo
- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.

## N009

- Original/snapshot disponible: **sí**
- Texto limpio disponible: **sí**
- JSON Gemini: **disponible y legible**
- Hechos que la revisión humana exige preservar:
  - homicidio en Terminal de Buses de Coquimbo
  - víctima chilena de 42 años atacada con arma cortante
  - presunto autor permanecía prófugo al publicarse
- Riesgos de inferencia que deben comprobarse manualmente:
  - identidad del agresor
  - que la locataria participó del ataque
- Señales automáticas de cobertura (solo apoyo):
  - ✓ delitos_esperados: homicidio
  - ✓ lugares_esperados: Terminal de Buses de Coquimbo
  - ✓ lugares_esperados: Coquimbo
  - △ organizaciones_esperadas: PDI
  - ✓ organizaciones_esperadas: Brigada de Homicidios de La Serena
  - ✓ organizaciones_esperadas: Lacrim
  - ✓ organizaciones_esperadas: Ministerio Público
  - ✓ objetos_esperados: arma cortante
- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.

## N010

- Original/snapshot disponible: **sí**
- Texto limpio disponible: **sí**
- JSON Gemini: **disponible y legible**
- Hechos que la revisión humana exige preservar:
  - actualización del homicidio del Terminal de Buses de Coquimbo
  - imputado chileno de 45 años detenido
  - víctima chilena de 42 años murió en Hospital San Pablo
- Riesgos de inferencia que deben comprobarse manualmente:
  - condena del imputado
  - motivo del ataque
- Señales automáticas de cobertura (solo apoyo):
  - ✓ delitos_esperados: homicidio
  - ✓ lugares_esperados: Terminal de Buses de Coquimbo
  - ✓ lugares_esperados: Coquimbo
  - ✓ organizaciones_esperadas: Brigada de Homicidios La Serena
  - ✓ organizaciones_esperadas: Hospital San Pablo de Coquimbo
  - ✓ organizaciones_esperadas: Juzgado de Garantía de Coquimbo
  - ✓ objetos_esperados: arma cortante
- Resultado final de esta muestra: revisar visualmente original → limpio → JSON y registrar omisiones, roles y relaciones.

