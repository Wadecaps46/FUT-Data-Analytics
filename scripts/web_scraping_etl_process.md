# **Web Scraping de Datos Presupuestales con Python y Selenium**

## Introducción
Este proyecto utiliza Python y Selenium para automatizar la extracción de datos presupuestales desde la página CUIPO. Los datos recolectados son procesados y almacenados en una base de datos Supabase SQL, con el objetivo de proporcionar una solución automatizada y eficiente para análisis posteriores.

---

## **Requisitos Previos**

### **Software Requerido**
- **Python 3.8 o superior**
- **Selenium:** Para la automatización del navegador.
- **Supabase Python SDK:** Para interactuar con la base de datos.
- **Google Chrome y Chromedriver:** Asegúrate de que ambas versiones sean compatibles.
- **pandas:** Para estructurar y limpiar los datos recolectados.
- **Instalación de dependencias:** Usa el archivo `requirements.txt` para instalar todas las bibliotecas necesarias:
  ```bash
  pip install -r requirements.txt

---

### Configuraciones Previas
- **Cuenta en Supabase:** Configura un proyecto y crea la base de datos necesaria.
- **Tabla en la base de datos:**
  - Define las tablas requeridas para almacenar los datos extraídos.
- **Configuración de Chromedriver:** Asegúrate de que la versión de Chromedriver sea compatible con la versión de Google Chrome instalada.

---

## **Descripción del Proceso**

### **1. Configuración Inicial**
- Importación de librerías necesarias.
- Configuración de Selenium con opciones del navegador.
- Conexión a la base de datos Supabase utilizando credenciales seguras.

---

### **2. Automatización del Navegador**
- Navegación a la página CUIPO mediante Selenium.
- Interacción con elementos web como menús desplegables y botones utilizando métodos como `find_element` y `click`.

---

### **3. Extracción de Datos**
- Identificación de elementos web relevantes para la extracción.
- Uso de bucles para recorrer los datos disponibles en diferentes períodos y entidades.
- Organización de los datos extraídos en estructuras pandas DataFrame para su posterior procesamiento.

---

### **4. Almacenamiento de Datos**
- Validación y limpieza de datos extraídos.
- Inserción de los datos en la base de datos Supabase mediante consultas SQL o el SDK de Supabase.

---

### **5. Manejo de Errores**
- Implementación de bloques `try-except` para manejar:
  - Problemas de conexión.
  - Cambios inesperados en la estructura web.
  - Errores en la conexión con Supabase.

---

## Estructura del Código
El código se organiza en las siguientes secciones:

1. **Configuración:**
   - Importación de librerías.
   - Configuración de Selenium y conexión a la base de datos.

---

2. **Funciones Principales:**
   - `init_browser()`: Inicializa el navegador.
   - `extract_data()`: Extrae los datos de la página web.
   - `save_to_supabase(data)`: Guarda los datos en la base de datos.

---

3. **Flujo Principal:**
   - Inicialización de configuraciones.
   - Llamado a funciones para realizar el scraping.
   - Cierre del navegador y finalización del proceso.

---

## **Notas Adicionales**
- **Actualización de Chromedriver:** Verifica regularmente que la versión de Chromedriver sea compatible con tu versión de Google Chrome.
- **Cambios en la estructura web:** Si la página CUIPO cambia su estructura, deberás actualizar los selectores en el código (`XPATH`, `CSS selectors`).
- **Respeto por el sitio web:** Asegúrate de cumplir con las políticas del sitio para evitar bloqueos.
- **Reintentos automáticos:** Considera implementar una lógica de reintento en caso de fallos temporales en la conexión.
Asegúrate de que todas las dependencias estén instaladas y configuradas correctamente.

---

## Contacto
Si tienes dudas o comentarios, no dudes en contactarme a través de mi perfil en GitHub.
