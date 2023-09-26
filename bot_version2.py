# Librerias necesarias
import pandas as pd
import time
from time import sleep
import os
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

path_driver = 'C:/Users/uriel/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
path_chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
df_accounts = pd.read_excel('accounts_excel.xlsx')

df_accounts['PATH TO IMAGES'] = df_accounts['PATH TO IMAGES'].str.strip('"').replace("\\",'/')

# INICIARLIZAR EL WEB DRIVER (NAVEGADOR)
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.binary_location = path_chrome
driver = webdriver.Chrome(path_driver, options = options)

def Random_Duration_Action(start, end):
    # Crear la lista de números
    lista_numeros = []
    current_num = start

    while current_num <= end:
        lista_numeros.append(round(current_num, 2))
        current_num += 0.01

    random_number = random.choice(lista_numeros)
    return sleep(random_number)

def Open_Pinterest():
    driver.get('https://ar.pinterest.com/')

def Log_In(email, password):
    # 1. INICIAR SESION EN PINTEREST
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Iniciar sesión')]"))
    )
    login_button.click()

    # Encuentra los campos de usuario y contraseña
    username_field = driver.find_element(By.NAME, 'id')
    password_field = driver.find_element(By.NAME, 'password')

    Random_Duration_Action(1,3)

    # Envia los valores al campo
    username_field.send_keys(email)

    Random_Duration_Action(0.5,2)

    password_field.send_keys(password)

    Random_Duration_Action(1,2.3)

    password_field.send_keys(Keys.ENTER)

    Random_Duration_Action(5,7)

def Create_Pin():
    crear_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Crear')]"))
    )
    crear_button.click()

    Random_Duration_Action(1.4,2.13)

    crear_pin_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Crear Pin')]"))
    )
    crear_pin_button.click()

    Random_Duration_Action(2,5)

def Load_Images(path_to_imgs):
    fotos = os.listdir(path_to_imgs)[:20]
    last_one = fotos[-1]
    for i in range(len(fotos) - 1):
        try:
            file_input = driver.find_element(By.XPATH, "//input[@aria-label='Carga de archivo']")
            file_input.send_keys(path_to_imgs  + '/' + fotos[i])
            os.remove(path_to_imgs  + '/' + fotos[i])
            Random_Duration_Action(2,4.5)
            boton = driver.find_element(By.XPATH, '//button[@style="background-color: rgb(255, 255, 255); border: 0px; border-radius: 8px; box-sizing: border-box; cursor: pointer; height: 60px; outline: none; padding: 0px; width: 40px;"]')
            boton.click()
            Random_Duration_Action(2.63,3.2)
        except Exception:
            pass

    file_input = driver.find_element(By.XPATH, "//input[@aria-label='Carga de archivo']")
    file_input.send_keys(path_to_imgs + '/' + last_one)

    Random_Duration_Action(2,4)

def Edit_Pins(title_, description_, link_):

    tick_button = driver.find_element(By.XPATH, '//button[@aria-label="Seleccionar Pin"]')
    tick_button.click()

    Random_Duration_Action(2,3)

    select_all = driver.find_element(By.XPATH, '//div[contains(text(), "Seleccionar todo")]')
    select_all.click()

    Random_Duration_Action(1.5,2.8)

    select_all = driver.find_element(By.XPATH, '//button[@aria-label="Editar"]')
    select_all.click()

    Random_Duration_Action(1.2,2.1)

    title = driver.find_element(By.XPATH, '//input[@id="pin-builder-edit-modal-title"]')
    title.send_keys(title_)

    Random_Duration_Action(1.5,2.3)

    desc = driver.find_element(By.XPATH, '//textarea[@id="pin-builder-edit-modal-description"]')
    desc.send_keys(description_)

    Random_Duration_Action(2.2,4.9)

    link = driver.find_element(By.XPATH, '//input[@id="pin-builder-edit-modal-link"]')
    link.send_keys(link_)

    Random_Duration_Action(2,2.3)

    update_info_button = driver.find_element(By.XPATH, '//div[contains(text(), "Actualizar información")]')
    update_info_button.click()

    Random_Duration_Action(1.5,2.6)

def Publish_Pins():
    publish_button = driver.find_element(By.XPATH, '//div[contains(text(), "Publicar")]')
    publish_button.click()

def Log_Out():
    driver.get('https://ar.pinterest.com/')

    Random_Duration_Action(1.4,2.7)

    options_button = driver.find_element(By.XPATH, '//button[@aria-label="Cuentas y más opciones"]')
    options_button.click()

    Random_Duration_Action(1,1.7)

    log_out = driver.find_element(By.XPATH, '//span[contains(text(), "Salir")]')
    log_out.click()

def Turn_Off_WebDriver():
    driver.quit()

if __name__ == '__main__':
    for number_account in range(len(df_accounts)):
        #1
        Open_Pinterest()
        #2
        Log_In(email = df_accounts.iloc[number_account]['EMAIL'],
               password = df_accounts.iloc[number_account]['PASSWORD'])
        #3
        Create_Pin()
        #4
        Load_Images(path_to_imgs = df_accounts.iloc[number_account]['PATH TO IMAGES'])
        #5
        Edit_Pins(title_ = df_accounts.iloc[number_account]['PINS TITLE'],
                  description_ = df_accounts.iloc[number_account]['PINS DESCRIPTION'],
                  link_ = df_accounts.iloc[number_account]['LINK'])
        #6
        Publish_Pins()
        #7
        Log_Out()
        sleep(random.choice(range(67,126)))

    Turn_Off_WebDriver()


        