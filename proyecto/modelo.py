import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import serial
import time


# Carga el modelo previamente guardado
modelo = load_model('proyecto/coca-pepsi-cnn2.h5')

# Configura la conexión serial. Reemplaza '/dev/ttyUSB0' con tu puerto serial.
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # Espera a que se establezca la conexión
print('Jetson connection with Arduino')

def preprocesar_imagen(ruta_imagen, tamano_img=100):
    imagen = cv2.imread(ruta_imagen)
    imagen = cv2.resize(imagen, (tamano_img, tamano_img))
    imagen = imagen / 255.0
    imagen = np.expand_dims(imagen, axis=0)
    return imagen

def clasificar_imagen(ruta_imagen):
    imagen = preprocesar_imagen(ruta_imagen)
    predicciones = modelo.predict(imagen)
    if predicciones[0] < 0.5:
        return "Coca-Cola"
    else:
        return "Pepsi"

def enviar_dato(dato):
    arduino.write(dato.encode())

# Ruta a la imagen que quieres clasificar
ruta_imagen = 'proyecto/rtc.jpg'

# Obtener y mostrar la clasificación
clasificacion = clasificar_imagen(ruta_imagen)
print(f'La imagen es: {clasificacion}')

# Enviar dato al Arduino basado en la clasificación
if clasificacion == "Coca-Cola":
    enviar_dato('0')  # Suponiendo que '0' es para Coca-Cola
else:
    enviar_dato('1')  # Suponiendo que '1' es para Pepsi

arduino.close()  # Cierra la conexión serial
