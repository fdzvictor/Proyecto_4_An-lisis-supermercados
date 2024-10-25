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