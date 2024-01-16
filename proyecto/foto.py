import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import serial
import cv2
from tensorflow.keras.models import load_model
import numpy as np
import time

# Carga el modelo de clasificación
modelo = load_model('proyecto/coca-pepsi-cnn2.h5')

# Inicia la comunicación serial con Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # Espera a que se establezca la conexión
print('Jetson connection with Arduino')

# Inicia la cámara
cap = cv2.VideoCapture(0)

def preprocesar_imagen(imagen, tamano_img=100):
    imagen = cv2.resize(imagen, (tamano_img, tamano_img))
    imagen = imagen / 255.0
    imagen = np.expand_dims(imagen, axis=0)
    return imagen

def clasificar_imagen(imagen):
    imagen_preprocesada = preprocesar_imagen(imagen)
    predicciones = modelo.predict(imagen_preprocesada)
    return '0' if predicciones[0] < 0.5 else '1'

def escuchar_arduino_y_tomar_foto():
    try:
        while True:
            if arduino.in_waiting:
                linea = arduino.readline().decode('utf-8').rstrip()
                if linea == 'foto':
                    # Vacía el buffer de la cámara leyendo algunos frames
                    for i in range(15):  # Lee varios frames para limpiar el buffer
                        ret, frame = cap.read()
                        time.sleep(0.1)  # Pequeña pausa para no sobrecargar el buffer

                    if ret:
                        # Preprocesar y clasificar la imagen
                        resultado = clasificar_imagen(frame)
                        arduino.write(resultado.encode()) # Enviar resultado al Arduino
                        print("Es Coca-Cola" if resultado == '0' else "Es Pepsi")
                    else:
                        print("Error al capturar la imagen")
    except KeyboardInterrupt:
        print(" Deteniendo el programa...")
    finally:
        cap.release()  # Libera la cámara
        arduino.close()  # Cierra la conexión serial
        print("Cámara y conexión serial cerradas correctamente.")

escuchar_arduino_y_tomar_foto()
