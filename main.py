# Librerias necesarias
import pandas as pd
import requests
from time import sleep
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def clean_screen(): 
    os.system('cls')

clean_screen()
# INSERTAR EL PATH DEL CROMEDRIVER Y EL EJECUTABLE DE GOOGLE CHROME
# Ejemplo:
    #path_to_chromedriver = 'C:/Users/uriel/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
    #path_to_chrome_executable = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

path_to_chromedriver = ''
path_to_chrome_executable = ''

pinterest_username = input('Nombre de usuario de Pinterest: ')
pinterest_password = input('Contraseña de Pinterest: ')

clean_screen()

# INICIARLIZAR EL WEB DRIVER (NAVEGADOR)
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.binary_location = path_to_chrome_executable
driver = webdriver.Chrome(path_to_chromedriver, options = options)
driver.get('https://ar.pinterest.com/')


# 1. INICIAR SESION EN PINTEREST
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Iniciar sesión')]"))
)
login_button.click()

# Encuentra los campos de usuario y contraseña
username_field = driver.find_element(By.NAME, 'id')
password_field = driver.find_element(By.NAME, 'password')

# Envia los valores al campo
username_field.send_keys(pinterest_username)
password_field.send_keys(pinterest_password)

sleep(3)

titulos = ['TITULO 1', 'TITULO 2', 'TITULO 3', 'TITULO 4']

for i,e in enumerate(titulos):
    # 2. PULSAR EL BOTON DE 'CREAR' PARA CREAR UN PIN

    crear_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Crear')]"))
    )
    crear_button.click()

    crear_pin_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Crear Pin')]"))
    )
    crear_pin_button.click()

    sleep(3)

    # Cargar Imagen del Pin
    file_input = driver.find_element(By.XPATH, "//input[@aria-label='Carga de archivo']")

    # Enviar la ruta del archivo al elemento de entrada de archivo
    file_input.send_keys('C:/Documents/Pinterest Project/Foto Perfil Henry 2.png')

    # Esperar un momento para que la carga de archivos se complete (puedes ajustar este tiempo según sea necesario)
    driver.implicitly_wait(10)

    titulo = driver.find_element(By.XPATH, f"//textarea[@placeholder='Agrega un título']")

    # Ingresa tu nombre de usuario y contraseña
    username = 'Este es el titulo'
    titulo.send_keys(e)

    desc = driver.find_element(By.XPATH, "//div[@aria-label='Cuéntales a todos de qué se trata tu Pin']")

    texto = 'Esta es la descripcion que elegi'
    desc.send_keys(i)

    # Guardar
    guardar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Guardar')]"))
    )
    guardar_button.click()

    sleep(5)

    driver.get('https://ar.pinterest.com/')

    sleep(5)

driver.quit()
