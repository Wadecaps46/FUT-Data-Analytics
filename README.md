# **Análisis de Fondos de Salud del FUT (2014-2023)**

## **Resumen**
Este proyecto analiza la distribución y evolución de los fondos de salud en los 23 municipios del departamento del Atlántico, Colombia, durante el período 2014-2023. Se enfoca en la categoría "FUT Tesorería Fondo de Salud", automatizando la extracción de datos del portal CHIP para crear una base de datos histórica completa.

El objetivo principal es observar y determinar qué municipios administran de manera más eficiente sus recursos, identificar áreas de mejora en la inversión en salud, diferencias presupuestales y evaluar tendencias en cada categoría presupuestal.

---

## **Contexto del Problema**
El sector salud en Colombia enfrenta desafíos relacionados con la distribución y el uso eficiente de los recursos públicos. Esto incluye el manejo de fondos en los municipios y departamentos, especialmente en el contexto del FUT (Formulario Único Territorial). En este proyecto, se busca analizar la información histórica de la categoría "FUT Tesorería Fondo de Salud" para identificar patrones, diferencias y oportunidades de mejora en la distribución y uso de los recursos entre los municipios del Atlántico desde 2014 hasta 2023. Eso hace abordar problemas mediante la obtención de datos historicos para el análisis, enfrentando las siguientes dificultades:
 - Necesidad de análisis histórico de la gestión de fondos de salud municipales
 - Dificultad en la recopilación manual de datos (920+ reportes individuales)
 - Inconsistencia en la disponibilidad de datos (2-6 reportes faltantes por período)
 - Variabilidad en los tiempos de carga del portal que impiden obtener los elementos para generar los 
   reportes

---

### **Objetivos del Proyecto**
1. Crear una base de datos histórica centralizada de fondos de salud municipales.
2. Automatizar la extracción de datos desde el portal CHIP.
3. Facilitar análisis comparativos entre municipios.
4. Identificar patrones de gasto e inversión en salud.

---

## **Arquitectura de Datos**

### **Modelo de Datos**
El modelo de datos fue diseñado utilizando Supabase y SQL. Adopta un enfoque de **modelo estrella** para optimizar consultas analíticas y mejorar la trazabilidad de los datos.

#### **Tablas Dimensionales**
- **Entidades**: Información básica de los municipios (código, nombre).
- **Trimestres**: Períodos trimestrales que maneja el portal.
- **Periodos**: Relación entre trimestres y años para sacar dicha combinación para el reporte.
- **Descripciones**: Catálogo de códigos y descripciones de los reportes.
- **Estados**: Estado de extracción (completado, no encontrado, etc.).

#### **Tabla de Hechos**
- **Fac_Tesoreria_Fondo_Salud**: Contiene las métricas financieras principales por entidad, período y tipo de gasto.
- **Registros_Scraping**: Registro de las combinaciones (entidad-período) que han sido extraídas correctamente o reportadas como faltantes.

---

## **Proceso ETL**

### **1. Extracción (Web Scraping)**
El scraping de datos trimestrales se realiza desde el portal oficial de la Contaduría General de la Nación.  
- **Tecnologías utilizadas:** Python, Selenium.
- **Automatización:** Selección dinámica de entidad, período y categoría.
- **Manejo de errores:** Registro de estados de extracción (completado o faltante).
- **Reto técnico:** Manejo de tiempos de carga variables.

### **2. Transformación**
Limpieza y procesamiento de los datos utilizando pandas en Python:
- Conversión de valores monetarios a números flotantes.
- Normalización de columnas (nombres estandarizados).
- Validación de integridad y consistencia.
- Mapeo de códigos y descripciones.

### **3. Carga**
Los datos transformados se cargan en una base de datos alojada en Supabase:
- **Inserción SQL y Python:** Uso de comandos SQL con ayuda de Python para insertar registros.
- **Registro de estado:** Se documenta cada carga realizada.

---

## **Analítica**
Próximanete, esta en desarrollo.

---

## **Estructura del Repositorio**

```plaintext
├── README.md               # Información general del proyecto
├── scripts/                # Código de scraping y ETL
│   ├── web_scraping.py     # Extracción de datos del portal CHIP, etls.
│   └── web_scraping_etl_process.md           # Explicación de los scripts
├── sql/                    # Scripts SQL
│   ├── ddl.sql             # Creación de tablas y modelo de datos
│   └── README.md           # Descripción del modelo de datos
├── analysis/               # Análisis y dashboards (en desarrollo)
│   └── README.md           # Explicación futura de los análisis
├── requirements.txt        # Dependencias del proyecto
```

---

## **Tecnologías Utilizadas**
 - **Lenguajes:** Python, SQL.
 - **Librerías:** Selenium, pandas, bs4, supabase, etc ... (ver archivo requirements.txt)
 - **Bases de datos:** Supabase (Postgres).
 - **Otros:** Git, GitHub, Power BI (para visualizaciones futuras).

---

## **Próximos Pasos**
 - Análisis comparativos avanzados entre municipios.
 - Creación de dashboards interactivos en Power BI.
 - Ampliación del scraping para incluir otros departamentos y categorías del FUT (Posiblemente).

 ---

 ## **Autores / Contactos**
 - Wilson De Caro: [LinkedIn](https://www.linkedin.com/in/wilson-andres-de-caro-puertas-618704201)

 - Anderson Arenas: [LinkedIn](https://www.linkedin.com/in/anderson-arenas-suarez-43898a1b2/)