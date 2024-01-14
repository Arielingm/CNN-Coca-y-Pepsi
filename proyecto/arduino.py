import serial
import time

# Configura la conexión serial. Reemplaza '/dev/ttyUSB0' con tu puerto serial.
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # Espera a que se establezca la conexión
print('Jetson connection with Arduino')

def enviar_dato(dato):
    arduino.write(dato.encode())  # Envía el dato al Arduino

try:
    while True:
        dato = input("Ingresa '0' para Botellas de Coca Cola, '1' para para Botellas de Fanta: ")
        if dato in ['0', '1']:
            enviar_dato(dato)
        else:
            print("Entrada inválida. Por favor, ingresa '0' o '1'.")
except KeyboardInterrupt:
    print("Programa terminado por el usuario")

arduino.close()  # Cierra la conexión serial
