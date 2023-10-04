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


class PinterestClient:
    def __init__(self, webdriver_path:str, chrome_exe_path:str):
        self.path_to_webdriver_driver = webdriver_path
        self.path_to_chrome_exe = chrome_exe_path
        self.driver = None
        self.upload_images = []
        self.small_images = []

    def Initialize_WebDriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        options.binary_location = self.path_to_chrome_exe
        self.driver = webdriver.Chrome(self.path_to_webdriver_driver, options = options)

    def Send_Email(self, receiver_email, subject, body):
        sender_email = 'mybestfriendbot@gmail.com'  # Reemplaza con tu dirección de correo electrónico
        password = 'zzwy mdgs dtbh kjkh'
        em = EmailMessage()
        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as smtp:
            smtp.login(sender_email, password)
            smtp.sendmail(sender_email, receiver_email, em.as_string())

    def Random_Duration_Action(self, start, end):
        # Crear la lista de números
        lista_numeros = []
        current_num = start

        while current_num <= end:
            lista_numeros.append(round(current_num, 2))
            current_num += 0.01

        random_number = random.choice(lista_numeros)
        print(random_number)
        return sleep(random_number)

    def is_small_image(self, image_path):
        with Image.open(image_path) as img:
            width, height = img.size
            if width < 100 or height < 100:
                return True
            else:
                return False
            
    def duration(self, start, end):
        general_time_total = end - start
        h, rem = divmod(general_time_total, 3600)
        m, s = divmod(rem, 60)
        general_formatted_time = '{:0>2}:{:0>2}:{:0>2}'.format(int(h), int(m), int(s))
        return general_formatted_time

    def Open_Pinterest(self):
        self.driver.get('https://ar.pinterest.com/')
        self.Random_Duration_Action(3,4)

    def Log_In(self, email, password):
        # 1. INICIAR SESION EN PINTEREST
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log in')]"))
            )
            login_button.click()
        except TimeoutException:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Iniciar sesión')]"))
            )
            login_button.click()

        # Encuentra los campos de usuario y contraseña
        username_field = self.driver.find_element(By.NAME, 'id')
        password_field = self.driver.find_element(By.NAME, 'password')

        self.Random_Duration_Action(1,3)

        # Envia los valores al campo
        username_field.send_keys(email)

        self.Random_Duration_Action(0.5,2)

        password_field.send_keys(password)

        self.Random_Duration_Action(1,2.3)

        password_field.send_keys(Keys.ENTER)

        self.Random_Duration_Action(5,7)

def Create_Pin(self):
    try:
        crear_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Create')]"))
        )
        crear_button.click()

        self.Random_Duration_Action(1.4, 2.13)

        crear_pin_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Create Pin')]"))
        )
        crear_pin_button.click()

        self.Random_Duration_Action(2, 5)
    except Exception:
        crear_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//h4[contains(text(), 'Business hub')]"))
        )
        crear_button.click()

        self.Random_Duration_Action(1.4, 2.13)

        crear_pin_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Create Pin')]"))
        )
        crear_pin_button.click()

        self.Random_Duration_Action(2, 5)



    def Load_Images(self, path_to_imgs):
        fotos = os.listdir(path_to_imgs)[:20]
        last_one = fotos[-1]
        
        path_to_imgs = path_to_imgs.replace('\\','/').strip()
        small_images_folder = os.path.join(path_to_imgs + '/' + 'small_images')
        os.makedirs(small_images_folder, exist_ok=True)

        for i in range(len(fotos) - 1):
            try:
                image_path = path_to_imgs  + '/' + fotos[i]
                if os.path.isdir(image_path):
                    continue
                else:
                    if self.is_small_image(image_path) == True:
                        os.rename(image_path, small_images_folder + '/' + fotos[i])
                    else:
                        # Subir la imagen
                        file_input = self.driver.find_element(By.XPATH, "//input[@aria-label='File upload']")
                        file_input.send_keys(image_path)
                        self.upload_images.append(image_path)
                        self.Random_Duration_Action(0.5, 2.5)
                        boton = self.driver.find_element(By.XPATH, '//button[@style="background-color: rgb(255, 255, 255); border: 0px; border-radius: 8px; box-sizing: border-box; cursor: pointer; height: 60px; outline: none; padding: 0px; width: 40px;"]')
                        boton.click()
                        self.Random_Duration_Action(1.33, 4.2)
            except Exception:
                pass

        last_image_path = path_to_imgs  + '/' + last_one
        if os.path.isdir(last_image_path):
            pass
        else:
            if self.is_small_image(last_image_path) == True:
                os.rename(last_image_path, small_images_folder + '/' + fotos[i])
            else:
                # Subir la imagen
                file_input = self.driver.find_element(By.XPATH, "//input[@aria-label='File upload']")
                file_input.send_keys(last_image_path)
                self.upload_images.append(last_image_path)
                self.Random_Duration_Action(2, 4)

    def Edit_Pins(self,title_, description_, link_):

        tick_button = self.driver.find_element(By.XPATH, '//button[@aria-label="Select Pin"]')
        tick_button.click()

        self.Random_Duration_Action(2,3)

        select_all = self.driver.find_element(By.XPATH, '//div[contains(text(), "Select all")]')
        select_all.click()

        self.Random_Duration_Action(1.5,2.8)

        select_all = self.driver.find_element(By.XPATH, '//button[@aria-label="Edit"]')
        select_all.click()

        self.Random_Duration_Action(1.2,2.1)

        title = self.driver.find_element(By.XPATH, '//input[@id="pin-builder-edit-modal-title"]')
        title.send_keys(title_)

        self.Random_Duration_Action(1.5,2.3)

        desc = self.driver.find_element(By.XPATH, '//textarea[@id="pin-builder-edit-modal-description"]')
        desc.send_keys(description_)

        self.Random_Duration_Action(2.2,4.9)

        link = self.driver.find_element(By.XPATH, '//input[@id="pin-builder-edit-modal-link"]')
        link.send_keys(link_)

        self.Random_Duration_Action(2,2.3)

        update_info_button = self.driver.find_element(By.XPATH, '//div[contains(text(), "Update info")]')
        update_info_button.click()

        self.Random_Duration_Action(1.5,2.6)

    def Count_Pins(self):
        number_of_pins = self.driver.find_element(By.XPATH, '//div[@class="tBJ dyH iFc sAJ O2T zDA IZT swG"]')
        total = number_of_pins.text
        number = int(total.split()[0])
        return number

    def Publish_Pins(self):
        publish_button = self.driver.find_element(By.XPATH, '//div[contains(text(), "Publish")]')
        publish_button.click()

    def Delete_Images(self):
        for img in self.upload_images:
            os.remove(img)

    def Log_Out(self):
        self.driver.get('https://ar.pinterest.com/')

        self.Random_Duration_Action(1.4,2.7)

        options_button = self.driver.find_element(By.XPATH, '//button[@aria-label="Accounts and more options"]')
        options_button.click()

        self.Random_Duration_Action(1,1.7)

        log_out = self.driver.find_element(By.XPATH, '//span[contains(text(), "Log out")]')
        log_out.click()

    def Turn_Off_WebDriver(self):
        self.driver.quit()