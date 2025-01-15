# Documentación del Proyecto de Web Scraping con Python, Selenium y Supabase SQL

## Introducción
Este proyecto realiza web scraping utilizando Python y Selenium para recolectar información específica de de la página de CUIPO (más informacion en el archivo README.md inicial). Los datos recolectados se procesan y almacenan en una base de datos gestionada con Supabase SQL. El objetivo es proporcionar una solución automatizada para la extracción y almacenamiento de datos que puedan ser usados en análisis posteriores.

## Requisitos Previos
Antes de ejecutar el proyecto, asegúrate de tener lo siguiente:

### Software y Bibliotecas Necesarias
- **Python 3.8 o superior**
- **Selenium:** Para la automatización del navegador.
- **Supabase Python SDK:** Para conectarse y manejar la base de datos Supabase SQL.
- **Google Chrome y Chromedriver:** Para ejecutar las tareas de web scraping.
- **pandas:** Para manejar y estructurar los datos recolectados.
- **Tambien ver el archivo requieremts para instalar las depencias**


### Configuraciones Previas
- **Cuenta en Supabase:** Configura un proyecto y crea la base de datos necesaria.
- **Tabla en la base de datos:**
  - Define las tablas requeridas para almacenar los datos extraídos.
- **Configuración de Chromedriver:** Asegúrate de que la versión de Chromedriver sea compatible con la versión de Google Chrome instalada.

## Descripción del Proceso

### 1. Configuración Inicial
- Importación de bibliotecas necesarias.
- Inicialización de Selenium con las configuraciones del navegador.
- Configuración de las credenciales y conexión a la base de datos Supabase.

### 2. Automatización del Navegador
- Navegación a la URL objetivo mediante Selenium.
- Uso de métodos de Selenium como `find_element` y `click` para interactuar con elementos web.

### 3. Extracción de Datos
- Identificación de los elementos web que contienen la información deseada.
- Uso de bucles para recorrer y extraer múltiples datos de la página.
- Almacenamiento de los datos recolectados en estructuras pandas DataFrame.

### 4. Almacenamiento de Datos
- Formateo de los datos recolectados.
- Inserción en la base de datos Supabase mediante las credenciales configuradas.

### 5. Manejo de Errores
- Implementación de bloques `try-except` para manejar errores comunes, como problemas de conexión o cambios en la estructura de la página web.

## Estructura del Código
El código se organiza en las siguientes secciones:

1. **Configuración:**
   - Importación de librerías.
   - Configuración de Selenium y conexión a la base de datos.

2. **Funciones Principales:**
   - `init_browser()`: Inicializa el navegador.
   - `extract_data()`: Extrae los datos de la página web.
   - `save_to_supabase(data)`: Guarda los datos en la base de datos.

3. **Flujo Principal:**
   - Inicialización de configuraciones.
   - Llamado a funciones para realizar el scraping.
   - Cierre del navegador y finalización del proceso.

## Notas Adicionales
- **Actualización de Chromedriver:** Verifica regularmente la compatibilidad entre Chromedriver y tu navegador.
- **Cambios en la estructura web:** Si la página web cambia, es posible que necesites actualizar los selectores en el código.
- **Límites de scraping:** Respeta las políticas del sitio web para evitar bloqueos o fallos.

Asegúrate de que todas las dependencias estén instaladas y configuradas correctamente.

## Contacto
Si tienes dudas o comentarios, no dudes en contactarme a través de mi perfil en GitHub.
