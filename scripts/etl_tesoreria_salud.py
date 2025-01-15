from selenium.common.exceptions import NoSuchElementException,TimeoutException, ElementNotInteractableException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select

from bs4 import BeautifulSoup
from supabase import create_client, Client
from IPython.display import clear_output

import pandas as pd
import numpy as np
import time 
import timeit
from IPython.display import clear_output
import glob
import os
from itertools import product
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------------------------------------------
# connection to databases
# ------------------------------------------------------------------------------------------------------

# Función para crear el cliente
def get_supabase_client():
    """Crea y retorna un cliente Supabase"""
    url = os.environ.get('URL')
    key = os.environ.get('KEY')
    supabase: Client = create_client(url, key)

    return supabase

# Función para obtener datos de las entidades
def get_entities():
    client = get_supabase_client()
    df = pd.DataFrame(client.table('entidades').select('*').execute().data)
    return df

entidades = get_entities()

# Función para obtener datos de los periodos
def get_periods():
    client = get_supabase_client()
    periodos = client.table("periodos").select("*, trimestres(nombre)").execute()

    data = periodos.data 

    datos_trasformados = [
    {
        'id_periodo': item['id_periodo'],
        'año': item['año'],
        'nombre_trimestre': item['trimestres']['nombre']
    }
        for item in data
    ]

    def_periodos = pd.DataFrame(datos_trasformados)
    def_periodos['periodo'] = def_periodos['nombre_trimestre'].astype(str) + ' - ' + def_periodos['año'].astype(str)
    periodos = def_periodos.loc[:, ['id_periodo', 'periodo']]
    
    return periodos

periodos = get_periods()

def get_descriptions():
    client = get_supabase_client()
    df = pd.DataFrame(client.table('descripciones').select('*').execute().data)
    return df

descripciones = get_descriptions()


def insert_data_into_fact_table(df_temp):

    # Mapeo entre columnas del dtaframe y columnas de la tabla en Supabase
    column_mapping = {
        'regimen subsidiado': 'regimen_subsidiado_pesos',
        'salud publica colectiva': 'salud_publica_colectiva_pesos',
        'prestacion del servicio oferta': 'prestacion_del_servicio_oferta_pesos',
        'otros gastos en salud inversión': 'otros_gastos_salud_inversion',
        'otros gastos salud funcionamient': 'otros_gastos_salud_funcionamiento',
        'saldo otrasctas pendiente transf': 'saldo_otras_cuentas_transferencias_pendientes',
        'total de las cuentas maestras': 'total_cuentas_maestras'
    }

    # Convertir el DataFrame a una lista de diccionarios con los nombres correctos
    data_to_insert = []
    for _, row in df_temp.iterrows():
        mapped_row = {column_mapping[col]: row[col] for col in df_temp.columns if col in column_mapping}
        
        # Agregar las columnas adicionales que no necesitan mapeo
        mapped_row['id_entidad'] = row['id_entidad']
        mapped_row['id_descripcion'] = row['id_descripcion']
        mapped_row['id_periodo'] = row['id_periodo']
        
        data_to_insert.append(mapped_row)

    client = get_supabase_client()

    # Insertar los datos en la tabla de Supabase
    response = client.table("fac_tesoreria_fondo_salud").insert(data_to_insert).execute()
    
    return response

# Insertar registros
def create_record(entidad_id, periodo_id, id_estado):
    client = get_supabase_client()

    response = client.table("registros_scraping").insert({
        "id_entidad": int(entidad_id),
        "id_periodo": int(periodo_id),
        "id_estado": int(id_estado)}).execute()

    return response


def get_records():
    client = get_supabase_client()
    df = pd.DataFrame(client.table('registros_scraping').select('*').execute().data)
    return df

registros_completados = get_records()


# Sacamos todas las combinaciones posibles de entidades y periodos
combinaciones_posibles = pd.DataFrame(list(product(entidades["id_entidad"], periodos["id_periodo"])), columns=["id_entidad", "id_periodo"])


# Excluimos las combinaciones que ya existen en registros_scraping
combinaciones_faltantes = combinaciones_posibles.merge(registros_completados[['id_entidad', 'id_periodo']], on=['id_entidad', 'id_periodo'], how='left', indicator=True)
combinaciones_faltantes = combinaciones_faltantes[combinaciones_faltantes['_merge'] == 'left_only'].drop('_merge', axis=1)


# ------------------------------------------------------------------------------------------------------
# Scraping
# ------------------------------------------------------------------------------------------------------

columns_to_convert = {
    'regimen subsidiado',
    'salud publica colectiva',
    'prestacion del servicio oferta',
    'otros gastos en salud inversión',
    'otros gastos salud funcionamient',
    'saldo otrasctas pendiente transf',
    'total de las cuentas maestras'
}

categoria = "FUT_TESORERIA_FONDO_SALUD"
formulario = "REPORTE_DE_TESORERIA"

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--force-device-scale-factor=0.95")  # Establecer el zoom al 90%
driver = Chrome( options=chrome_options)

# Inicialización del navegador Chrome y navegación a la página web
driver.maximize_window()
driver.get("https://www.chip.gov.co/schip_rt/index.jsf")

# Esperar hasta que se cargue el elemento y damo click para ir a la pág de filtros
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#j_idt105\:InformacionEnviada')))
pag_informacion_ciudadano = driver.find_element(By.CSS_SELECTOR, '#j_idt105\:InformacionEnviada')
pag_informacion_ciudadano.click()

# Esperar a que la nueva página cargue completamente (si es necesario)
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

# Hacer un pequeño scroll hacia abajo (100 píxeles en este caso)
driver.execute_script("window.scrollBy(0, 270);")


# Iteraros sobre las combinaciones faltantes
for _, combinacion in combinaciones_faltantes.iterrows():
    entidad_id = int(combinacion["id_entidad"])
    periodo_id = int(combinacion["id_periodo"])
    entidad = entidades[entidades["id_entidad"] == entidad_id].iloc[0]
    codigo = entidad["codigo"]
    entidad_nombre = entidad["nombre"]
    periodo_valor = periodos[periodos["id_periodo"] == periodo_id].iloc[0]["periodo"]
    descripcion_id = descripciones["id_descripcion"]

    print(f"Scraping al entidad {entidad_id} - {entidad_nombre} - {periodo_id} - {periodo_valor}")

    # Encontramos y llenamos el input de entidad
    while True:
        try:
            filtro_entidad = driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxEntidadCiudadano_input')
            filtro_entidad.clear()
            filtro_entidad.send_keys(codigo)
            filtro_entidad.send_keys(Keys.ENTER)
            break
        except Exception as e:
            print(f"Error en el elemento de entidad: {e}")
        except TimeoutException:
            print("Tiempo de espera agotado al cargar el elemento o interactuar con entidad.")
            time.sleep(5)

    
    # Encontramos el input de categoria y seleccionamos con la que trabajaremos
    while True:
        try:
            #filtro_categoria = Select(driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxCategoria'))
            elemento_categoria = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#frm1\:SelBoxCategoria'))
            )
            
            filtro_categoria = Select(elemento_categoria)
            filtro_categoria.select_by_visible_text(". : : Seleccione : : .")
            filtro_categoria.select_by_visible_text(categoria)
            break
        except Exception as e:
            print(f"Error en el el elemento de categoria: {e}")
        except TimeoutException:
            print("Tiempo de espera agotado al cargar el elemento o las opciones.")
            time.sleep(2)
    
    # Para el periodo
    contar_intentos = 0
    registro_periodo_creado = False
    
    while contar_intentos < 3:
        try:
            contar_intentos += 1
            print(f"Intento de periodo: {contar_intentos}")

            elemento_periodo = WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#frm1\:SelBoxPeriodo'))
            )
            filtro_periodo = Select(elemento_periodo)                
            filtro_periodo.select_by_visible_text(". : : Seleccione : : .")

            filtro_periodo.select_by_visible_text(periodo_valor)
            trimestre = False
            break
        except Exception as e:
            print(f"Elemento de periodo no encontrado: {e}")
            time.sleep(2.5)
            trimestre = True

        if contar_intentos >= 3 and not registro_periodo_creado:
            # Se crea un nuevo registro, pero en estado 2, "no_encontrado" ya que el periodo no se encontro
            try:
                insert_record2 = create_record(entidad_id, periodo_id, 2)
                print(f"Registro creado: {insert_record2}")
                registro_periodo_creado = True

                clear_output()
            except Exception as e:
                print(f"Error al insertar el registro: {e}")

            driver.delete_all_cookies()
            driver.refresh()
            
            # Esperamos hasta que se cargue el elemento y damo click para ir a la pág de filtros
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#j_idt105\:InformacionEnviada')))
            pag_informacion_ciudadano = driver.find_element(By.CSS_SELECTOR, '#j_idt105\:InformacionEnviada')
            pag_informacion_ciudadano.click()
            time.sleep(6)
            break

    # Si no encontramos el periodo, continuamos con la siguiente combinación
    if trimestre:
        continue

    # Para el formulario
    if not trimestre:
        intentos_formulario = 0
        registro_formulario_creado = False
        
        while intentos_formulario < 3:
            try:
                intentos_formulario += 1
                print(f"Intentos formulario: {intentos_formulario}")

                elemento_formulario = WebDriverWait(driver, 6).until( 
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '#frm1\:SelBoxForma')))                    

                filtro_formulario = Select(elemento_formulario)
                filtro_formulario.select_by_visible_text(formulario)
                f_reporte = False
                break

            except (NoSuchElementException, ElementNotInteractableException) as e:
                print(f"Elemento de formulario no encontrado o no interactuable: {e}")
                print("Intentamos de nuevo")
                time.sleep(2.5)
                f_reporte = True

                if intentos_formulario >= 3 and not registro_formulario_creado:
                    try:
                        insert_record2 = create_record(entidad_id, periodo_id, 2)
                        print(f"Registro creado: {insert_record2}")
                        registro_formulario_creado = True

                        clear_output()
                    except Exception as e:
                        print(f"Error al insertar el registro: {e}")

        # Si agotamos los intentos del formulario
        if f_reporte:
            driver.delete_all_cookies()
            driver.refresh()

            # Volvemos a la página principal y damos click para ir a la pág de filtros
            WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#j_idt105\:InformacionEnviada')))
            pag_informacion_ciudadano = driver.find_element(By.CSS_SELECTOR, '#j_idt105\:InformacionEnviada')
            pag_informacion_ciudadano.click()
            time.sleep(5)
            continue

        if not f_reporte:
            # Boton generar, para obtener la tabla
            while True:
                try:
                    boton_consultar = driver.find_element(By.CSS_SELECTOR, '#frm1\:BtnConsular')
                    boton_consultar.click()
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(3.2)

            # Elegir el nivel para que me muestre toda la tabla en esa página

            try:
                nivel_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#frm1\:SelBoxNivel'))
                )
                nivel = Select(driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxNivel'))
                total_opciones = len(nivel.options)

                if total_opciones > 1:
                    print("Seleccionando el último nivel")
                    # Obtener el HTML inicial de la tabla (estado por defecto)
                    tabla_html = driver.find_element(By.CSS_SELECTOR, '#frm1\:j_idt222').get_attribute("outerHTML")
                    soup = BeautifulSoup(tabla_html, "html.parser")
                    filas_iniciales = len(soup.find_all('tr'))

                    # Seleccionar el último nivel
                    nivel.select_by_index(total_opciones - 1)

                    # Esperar a que la tabla se actualice con más filas
                    while True:
                        tabla_html = driver.find_element(By.CSS_SELECTOR, '#frm1\:j_idt222').get_attribute("outerHTML")
                        soup = BeautifulSoup(tabla_html, "html.parser")
                        filas_actuales = len(soup.find_all('tr'))

                        if filas_actuales > filas_iniciales:
                            print(f"Tabla actualizada: {filas_actuales} filas ahora disponibles.")
                            break
                        else:
                            print("Esperando que la tabla se actualice...")
                            time.sleep(4)
                else:
                    print("Solo hay un nivel disponible, no se requiere actualización.")
            except Exception as e:
                print(f"Error al seleccionar el nivel: {e}")

            # Extraer la tabla
            try:
                tabla_html = driver.find_element(By.CSS_SELECTOR, '#frm1\:j_idt222').get_attribute("outerHTML")
                soup = BeautifulSoup(tabla_html, "html.parser")
                filas = soup.find_all('tr')

                if len(filas) > 0:
                    print(f"Tabla cargada con {len(filas)} filas.")
                else:
                    print("No se encontraron filas en la tabla.")
            except Exception as e:
                print(f"Error al extraer la tabla: {e}")


            # Extraemos columnas y filas
            headers = [th.text.strip() for th in soup.find_all('th')]
            rows = []
            for tr in soup.find_all('tr'):
                cells = [td.text.strip() for td in tr.find_all('td')]
                rows.append(cells)

            df_temp = pd.DataFrame(rows, columns=headers)
            df_temp = df_temp.drop(columns=['NOMBRE'])
            df_temp = df_temp.drop(0)

            # Normalizamos los nombres de columnas para no entrar en conflicto con cambios de nombres de la pág
            def normalize_column_name(col_name):
                # Eliminamos los espacios en blanco y pasampsos a minúsculas
                col_name = col_name.strip().lower()
                # Reemplazamos "(miles)" y "(pesos)" con una cadena vacía
                col_name = col_name.replace('(miles)', '').replace('(pesos)', '').strip()
                return col_name

            df_temp.columns = [normalize_column_name(col) for col in df_temp.columns]   

            """Bloque de transformación de datos Aca estaran todas las tranformaciones a realizar"""
            # Hacemos la conversión de datos necesarias, primero a str a float para no tener conflictos
            for columns_tc in columns_to_convert:
                df_temp[columns_tc] = df_temp[columns_tc].astype(str)
                df_temp[columns_tc] = df_temp[columns_tc].str.replace(',', '').astype(float)

            # Verificamos la diferencia de códigos que no tiene o cuenta
            df_temp_codes = set(df_temp['codigo'])
            all_description_codes = set(descripciones['codigo'])
            missing_codes = all_description_codes - df_temp_codes
            print(f"La entidad {entidad_nombre}_{periodo_valor} tiene una diferencia de {len(missing_codes)} códigos")

            new_values = list(missing_codes) 

            news_rows = []

            for value in new_values:
                # Se crea un nuevo registro con el nuevo código
                nueva_fila = {'codigo': value}

                # Se llenara las filas con -1 en las otras columnas para identifica que esos códigos no pertenecen ahi
                for col in columns_to_convert:
                    nueva_fila[col] = -1

                # Se Agregaran a la nueva fila al DataFrama como una lista
                news_rows.append(nueva_fila)

            news_rows_df = pd.DataFrame(news_rows)

            # Concatenamos para agregar los otros códigos al dataframe original
            df_temp = pd.concat([df_temp, news_rows_df], ignore_index=True)
            
            df_temp['id_entidad'] = entidad_id
            df_temp['id_descripcion'] = descripcion_id
            df_temp['id_periodo'] = periodo_id
            
            print(df_temp)

            try:
                insert_to_fact = insert_data_into_fact_table(df_temp)
                print(insert_to_fact)
                print("Se insertaron los datos correctamente en la fact table")
            except Exception as e:
                print(f"Error al insertar los datos a la fact table: {e}")

            
            try:
                insert_record = create_record(entidad_id, periodo_id, 1)
                print(insert_record)
                print("Se inserto el registro correctamente")
            except Exception as e:
                print(f"Error al insertar el registro: {e}")

            # Volvemos a la página para generar otra tabla
            boton_volver = driver.find_element(By.CSS_SELECTOR, '#frm1\:j_idt148')
            boton_volver.click()

            clear_output() 

            time.sleep(5)

driver.close()
print("Se finalizo el proceso de extracción de datos")