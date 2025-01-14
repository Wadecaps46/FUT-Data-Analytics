# FUT-Data-Analytics
Proyecto de análisis de datos del FUT tesorería fondo de salud (2014-2023 o más): modelado de datos, scraping, ETL, análisis y visualización

## Descripción
Análisis de la distribución de fondos de salud en 23 municipios del Atlántico, Colombia (2014-2023)

## Problema
El sector salud en Colombia enfrenta desafíos relacionados con la distribución y el uso eficiente de los recursos públicos. Esto incluye el manejo de fondos en los municipios y departamentos, especialmente en el contexto del FUT (Formulario Único Territorial). En este proyecto, se busca analizar la información histórica de la categoría "FUT Tesorería Fondo de Salud" para identificar patrones, diferencias y oportunidades de mejora en la distribución y uso de los recursos entre los municipios del Atlántico desde 2014 hasta 2023. Y otros más como: 
 - Necesidad de análisis histórico de la gestión de fondos de salud municipales
 - Dificultad en la recopilación manual de datos (920+ reportes individuales)
 - Inconsistencia en la disponibilidad de datos (2-6 reportes faltantes por período)
 - Variabilidad en los tiempos de carga del portal que impiden obtener los elementos para generar los 
   reportes


## Arquitectura
[Diagrama de la arquitectura]

## Modelo de Datos
Diseñada en Supabase, SQL.
### Tablas Dimensionales:
 - Entidades: Contiene los municipios y su información básica
 - Trimestres: Catálogo de períodos trimestrales que maneja la página para los reportes de las categorías 
   FUT 
 - Periodos: Relaciona trimestres con años
 - Descripciones: Catálogo de códigos y descripciones que contiene los reportes de fondo de salud 
 - Estados: Catálogo de estados de extracción, como completado y no_encontrado para scrapear.
### Tabla de Hechos:
 - Fac_Tesoreria_Fondo_Salud: Es la tabla central, donde se almacenan las cifras financieras por entidad, 
 - periodo y tipo de gasto. Es decir, las métricas principales
 - Registros_Scraping: Registro de extracciones realizadas. Es decir, qué combinaciones (entidad - 
   periodo) se han realizado correctamente y cuales no se encuentran

## Proceso ETL
- Web Scraping (Python + Selenium)
- Transformación de datos
- Carga en Supabase

## Tecnologías
- Python, pandas
- Selenium
- Beautifulsoup4
- SQL (Supabase)

## Estructura del Repositorio
En repositorio cuenta con las siguientes carpetas: 
 - /docs: Documentación un poco más detallada sobre el proyecto
 - /sql: Scripts DDL y queries
 - /scripts: Código Python del web scraping + ETLS
 - /diagrams: Diagramas ERD y flujos de trabajo
 - /dashboards: Código y configuración


