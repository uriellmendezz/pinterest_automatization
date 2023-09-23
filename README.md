# 😉 Pasos para ejecutar el script 👋

## 1. Instalar Python: https://www.python.org/downloads/

## 2. Instalar el Web Driver de Google Chrome: https://chromedriver.chromium.org/downloads


## 3. Clonar el repositorio
``` bash
git clone https://github.com/uriellmendezz/pinterest_automatization.git
cd pinterest_automatization
```

## 4. Crear un entorno virtual para el proyecto
``` bash
python -m venv myenv
myenv/Scripts/activate
```

## 5. Instalar Python Package Index (`pip`)
```bash
python get-pip.py
```

## 6. Verificar si `pip` se instalo correctamente
``` bash
pip --version
```

## 7. Instalar los requirimientos necesarios
```bash
pip install -r requirements.txt
```

## 8. Abrir el archivo `main.py` y agregar el path del Web Driver como en el ejemplo
``` python
# INSERTAR EL PATH DEL CROMEDRIVER Y EL EJECUTABLE DE GOOGLE CHROME
# Ejemplo:
    #path_to_chromedriver = 'C:/Users/uriel/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
    #path_to_chrome_executable = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

path_to_chromedriver = ''
path_to_chrome_executable = ''
```

### 9. Colocar los datos de tu cuenta de Pinterest en el archivo `profile_data.json`.
```json
{
    "email":"your-email@gmail.com",
    "password":"your-password"
}
```

## 9. Ejecutar el script `main.py`
```bash
python main.py
```
