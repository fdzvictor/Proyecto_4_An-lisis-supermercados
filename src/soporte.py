# # Importamos las librerías que necesitamos
# pip install selenium 
# pip install bs4
# pip install requests
# pip install webdriver-manager
# pip install pandas
# pip install numpy
# Librerías de extracción de datos
# -----------------------------------------------------------------------

# Importaciones:
# Beautifulsoup
from bs4 import BeautifulSoup

# Requests
import requests

# Importar librerías para automatización de navegadores web con Selenium
# -----------------------------------------------------------------------
from selenium import webdriver  # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.keys import Keys  # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException # Excepciones comunes de selenium que nos podemos encontrar 


# Importar librerías para pausar la ejecución
# -----------------------------------------------------------------------
from time import sleep  # Sleep se utiliza para pausar la ejecución del programa por un número de segundos.

# Librerías para tratamiento de datos
# -----------------------------------------------------------------------
import pandas as pd
import numpy as np
#------------------------------------------------------------------------

#Accedemos al super:

def scrapeo_por_supermercado(nombre_super):

    lista_productos_gral = ["Aceite de girasol", "Aceite de oliva", "Leche"]
    lista_link_gral = []

    driver = webdriver.Chrome()
    url = f"https://super.facua.org/{nombre_super}/"
    driver.get(url)
    driver.maximize_window()
    sleep(2)

    try:
        driver.find_element("xpath",'//*[@id="rcc-confirm-button"]').click()
        print("Botón de aceptar cookies clicado con éxito.")
    except:
        print("No se pudo encontrar el botón de aceptar cookies o hacer clic en él.")


#Scrapeamos aceite de girasol
# Scroll
    driver.execute_script(f"window.scrollTo(0, {0,100});")
    sleep(2)
#Click Aceite girasol
    driver.find_element("xpath",'/html/body/section[1]/div/div[2]/div[1]/div/div[2]/div/a').click()
    sleep(1)
#Aquí hay que scrapear todos los links de aceite de girasol !
    get_url1 = driver.current_url
    print(f"La url del aceite de girasol en {nombre_super} es:"+str(get_url1))
    lista_link_gral.append(get_url1)

    driver.back()
    sleep(3)

#Click aceite de oliva
    driver.find_element("xpath","/html/body/section[1]/div/div[2]/div[2]/div/div[2]/div/a").click()
    sleep(1)
#Scrapeamos aceites de oliva
    get_url2 = driver.current_url
    print(f"La url del aceite de oliva en {nombre_super} es:"+str(get_url2))
    lista_link_gral.append(get_url2)

    driver.back()
    sleep(3)

#Click leche
    driver.find_element("xpath",'/html/body/section[1]/div/div[2]/div[3]/div/div[2]/div/a').click()
    sleep(1)
#Scrapeamos leche
    get_url3 = driver.current_url
    print(f"La url de la leche en {nombre_super} es:"+str(get_url3))
    lista_link_gral.append(get_url3)
    driver.back()
    sleep(3)

#Cerran2
    driver.close()

    diccionario_gral = dict(zip(lista_productos_gral,lista_link_gral))
    return diccionario_gral


#--------------------------------------------------------------------------------------------------------------------


#Sacamos los valores interiores
def aplicar_subproductos_a_productos(lista_enlaces_de_los_productos):
    dic_subs = {}
    for url in lista_enlaces_de_los_productos:
        url_producto = url
        res_producto = requests.get(url_producto)
        print(res_producto)

        sopa_producto = BeautifulSoup(res_producto.content,"html.parser")

        lista_subproductos = []
        enlace_historico = sopa_producto.findAll("a", class_="btn-unirme btn-verde inline-block inline-block bg-primary border-primary font-semibold rounded-full")

# Extrae el valor del atributo href
        for valores in enlace_historico:
            lista_subproductos.append(valores.get("href"))
        
       
        dic_subs[url] = lista_subproductos
    return dic_subs




#--------------------------------------------------------------------------------------------------------------------



#Sacar histórico de precios, empecemos con una url: 
def sacar_historico(url_sproducto):

#Sacar histórico de precios, empecemos con una url: 
    res_producto = requests.get(url_sproducto)
    print(res_producto)

#Creamos bs4, buscamos aquellos elementos que sean tablas y seleccionamos la que queremos en concreto
    sopa_producto = BeautifulSoup(res_producto.content,"html.parser")
    tablas = sopa_producto.find_all("table")

    tablasweb = []
    for n in tablas:
        tablasweb.append(n)
##Puesto que hay webs que tienen dos tablas, cogemos siempre la de históricos, la última.
    try:
        tabla = tablasweb[-1]
  
        lista_filas_producto = tabla.findAll("tr")
        print(f" la tabla tiene {len(lista_filas_producto)} filas")

# Creamos un diccionario llamado diccionario_producto para almacenar todos los resultados
# Iniciamos un bucle 'for' para iterar a través de la lista_filas_producto a partir de la segunda fila
        diccionario_producto = {}
        diccionario_variaciones = {}
        for fila in lista_filas_producto[1:]:
    # Para cada 'fila', extraemos el texto y los datos
            fila_texto = fila.findAll("td")
    #Creamos un diccionario con cada valor a través de la lista anteriormente generada
            diccionario_producto[fila_texto[0].getText()] = fila_texto[1].getText()
            diccionario_variaciones [fila_texto[0].getText()] = fila_texto[2].getText()

    # Imprimimos los resultados obtenidos después de iterar por la lista.
        print(f"Los resultados de iterar por la lista son:\n {diccionario_producto}")

#Creamos el df del histórico del producto
        df_producto = pd.DataFrame(diccionario_producto.values(), index = diccionario_variaciones.keys())


#Creamos columnas para la variación de precio y la variación porcentual    
        df_producto["variaciones"] = diccionario_variaciones.values()
        
#Creamos columnas para el supermercado y el producto       
        split_url = (url_sproducto.split("/"))
        df_producto["Supermercado"] = split_url[3]
        df_producto["Categoría"] = split_url[4].replace("-"," ")

#Si la columna "Variación" no tiene valores, generamos dos columnas vacías, para que cuadre todo el df final
        try:
            df_producto[["Variación","Variación_porcentual"]] = df_producto["variaciones"].str.rsplit("(", expand = True)
            df_producto["Variación_porcentual"] = df_producto["Variación_porcentual"].str.split(")")
            df_producto.drop(columns = "variaciones",inplace = True)
            ## Para estandarizar columnas dejamos los "=" como "None"
            df_producto['Variación'] = df_producto['Variación'].apply(lambda x: None if x == "=" else x)

            

        except ValueError:
            df_producto["Variación"] = "None"
            df_producto["Variación_porcentual"] = "None"
            df_producto.drop(columns = "variaciones",inplace = True)

        return df_producto 
    except:
        pass



#----------------------------------------------------------------------------
