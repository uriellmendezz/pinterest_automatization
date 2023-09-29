# Librerias necesarias
import pandas as pd
import time
from time import sleep
import os
import random
import smtplib
import ssl
from email.message import EmailMessage
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

path_driver = 'C:/Users/uriel/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
path_chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

# INSERTAR EL PATH DEL CROMEDRIVER Y EL EJECUTABLE DE GOOGLE CHROME
# Ejemplo:
    #path_to_chromedriver = 'C:/Users/user1/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
    #path_to_chrome_executable = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

#path_to_chromedriver = ''
#path_to_chrome_executable = ''

df_accounts = pd.read_excel('../accounts_excel.xlsx')
df_accounts['PATH TO IMAGES'] = df_accounts['PATH TO IMAGES'].str.strip('"').replace("\\",'/')

# INICIARLIZAR EL WEB DRIVER (NAVEGADOR)
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.binary_location = path_chrome
driver = webdriver.Chrome(path_driver, options = options)

def Send_Email(receiver_email, subject, body):
    sender_email = 'mybestfriendbot@gmail.com'  # Reemplaza con tu dirección de correo electrónico
    with open('../password.txt', 'r') as f:
        password = f.read().strip()

    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, receiver_email, em.as_string())

def Random_Duration_Action(start, end):
    # Crear la lista de números
    lista_numeros = []
    current_num = start

    while current_num <= end:
        lista_numeros.append(round(current_num, 2))
        current_num += 0.01

    random_number = random.choice(lista_numeros)
    print(random_number)
    return sleep(random_number)

def is_small_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        if width < 100 or height < 100:
            return True
        else:
            return False
        
def duration(start, end):
    general_time_total = end - start
    h, rem = divmod(general_time_total, 3600)
    m, s = divmod(rem, 60)
    general_formatted_time = '{:0>2}:{:0>2}:{:0>2}'.format(int(h), int(m), int(s))
    return general_formatted_time
        
# ----------------------------------------- MAIN FUNCTIONS -----------------------------------------

def Open_Pinterest():
    driver.get('https://ar.pinterest.com/')
    Random_Duration_Action(3,4)

def Log_In(email, password):
    # 1. INICIAR SESION EN PINTEREST
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log in')]"))
        )
        login_button.click()
    except TimeoutException:
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
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create')]"))
    )
    crear_button.click()

    Random_Duration_Action(1.4,2.13)

    crear_pin_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create Pin')]"))
    )
    crear_pin_button.click()

    Random_Duration_Action(2,5)

upload_images = []

def Load_Images(path_to_imgs):
    fotos = os.listdir(path_to_imgs)[:5]
    last_one = fotos[-1]
    
    # Carpeta para imágenes pequeñas
    small_images_folder = os.path.join(path_to_imgs + '/' + 'small_images')
    os.makedirs(small_images_folder, exist_ok=True)

    for i in range(len(fotos) - 1):
        try:
            image_path = path_to_imgs  + '/' + fotos[i]
            if is_small_image(image_path) == True:
                # Mover a la carpeta de imágenes pequeñas
                os.rename(image_path, small_images_folder + '/' + fotos[i])
            else:
                # Subir la imagen
                file_input = driver.find_element(By.XPATH, "//input[@aria-label='File upload']")
                file_input.send_keys(image_path)
                upload_images.append(image_path)
                Random_Duration_Action(0.5, 2.5)
                boton = driver.find_element(By.XPATH, '//button[@style="background-color: rgb(255, 255, 255); border: 0px; border-radius: 8px; box-sizing: border-box; cursor: pointer; height: 60px; outline: none; padding: 0px; width: 40px;"]')
                boton.click()
                Random_Duration_Action(1.33, 4.2)
        except Exception:
            pass

    # Subir la última imagen
    last_image_path = path_to_imgs  + '/' + last_one
    if is_small_image(last_image_path) == True:
        # Mover a la carpeta de imágenes pequeñas
        os.rename(last_image_path, small_images_folder + '/' + last_one)
    else:
        # Subir la imagen
        file_input = driver.find_element(By.XPATH, "//input[@aria-label='File upload']")
        file_input.send_keys(last_image_path)
        upload_images.append(last_image_path)
        Random_Duration_Action(2, 4)

def Edit_Pins(title_, description_, link_):

    tick_button = driver.find_element(By.XPATH, '//button[@aria-label="Select Pin"]')
    tick_button.click()

    Random_Duration_Action(2,3)

    select_all = driver.find_element(By.XPATH, '//div[contains(text(), "Select all")]')
    select_all.click()

    Random_Duration_Action(1.5,2.8)

    select_all = driver.find_element(By.XPATH, '//button[@aria-label="Edit"]')
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

    update_info_button = driver.find_element(By.XPATH, '//div[contains(text(), "Update info")]')
    update_info_button.click()

    Random_Duration_Action(1.5,2.6)

def Count_Pins():
    number_of_pins = driver.find_element(By.XPATH, '//div[@class="tBJ dyH iFc sAJ O2T zDA IZT swG"]')
    total = number_of_pins.text
    number = int(total.split()[0])
    return number

def Publish_Pins():
    publish_button = driver.find_element(By.XPATH, '//div[contains(text(), "Publish")]')
    publish_button.click()

def Log_Out():
    driver.get('https://ar.pinterest.com/')

    Random_Duration_Action(1.4,2.7)

    options_button = driver.find_element(By.XPATH, '//button[@aria-label="Accounts and more options"]')
    options_button.click()

    Random_Duration_Action(1,1.7)

    log_out = driver.find_element(By.XPATH, '//span[contains(text(), "Log out")]')
    log_out.click()

def Turn_Off_WebDriver():
    driver.quit()

if __name__ == '__main__':
    general_time_start = time.time()

    accounts = []
    total_pins = []
    time_executed = []

    for number_account in range(len(df_accounts)):
        start_time = time.time()
        #1
        Open_Pinterest()
        #2
        Log_In(email = df_accounts.iloc[number_account]['PINTEREST EMAIL'],
               password = df_accounts.iloc[number_account]['PINTEREST PASSWORD'])
        #3
        Create_Pin()
        #4
        Load_Images(path_to_imgs = df_accounts.iloc[number_account]['PATH TO IMAGES'])
        #5
        Edit_Pins(title_ = df_accounts.iloc[number_account]['PINS TITLE'],
                  description_ = df_accounts.iloc[number_account]['PINS DESCRIPTION'],
                  link_ = df_accounts.iloc[number_account]['PINS LINK'])
        
        number_of_pins = Count_Pins()
        #6
        Publish_Pins()

        #7
        Log_Out()

        finish_time = time.time()

        total_time = duration(start_time,finish_time)

        accounts.append(df_accounts.iloc[number_account]['ACCOUNT NAME'])
        total_pins.append(number_of_pins)
        time_executed.append(total_time)

        if number_account == len(df_accounts):
            break
        else:
            Random_Duration_Action(63,138)

    general_time_finish = time.time()
    total_general_time = duration(general_time_start, general_time_finish)

    body = ''
    for i,e in enumerate(accounts):
        message = f'''Account: {e}\n - Total Pins uploaded: {total_pins[i]}\n - Process duration: {time_executed[i]}\n\n'''
        body += message

    body += f'\nProcess total duration: {total_general_time}'

    Send_Email(
        receiver_email = df_accounts.iloc[number_account]['YOUR GMAIL'],
        subject='Uploading Pins to Pinterest',
        body=body
    )

    Turn_Off_WebDriver()