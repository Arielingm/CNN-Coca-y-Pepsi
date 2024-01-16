int ledCoca = 8; // LED conectado al pin 8
int ledPepsi = 7; // LED conectado al pin 7
int botonPin = 4; // Botón conectado al pin 4
bool botonFuePresionado = false; // Indica si el botón fue presionado previamente

void setup() {
  pinMode(ledCoca, OUTPUT);
  pinMode(ledPepsi, OUTPUT);
  pinMode(botonPin, INPUT); // Configura el pin del botón como entrada sin pull-up
  Serial.begin(9600); // Inicia la comunicación serial
}

void loop() {
  // Verifica si el botón es presionado
  bool estadoBoton = digitalRead(botonPin);
  
  if (estadoBoton == HIGH && !botonFuePresionado) {
    Serial.println("foto"); // Envía el mensaje "foto" a la Jetson Nano
    botonFuePresionado = true; // Marca el botón como presionado
    delay(200); // Pequeño retraso para evitar rebote del botón
  } if (estadoBoton == LOW) {
    botonFuePresionado = false;
    } // Marca el botón como no presionado cuando se suelta

  // Verifica si hay datos disponibles para leer desde la Jetson Nano
  if (Serial.available() > 0) {
    char resultado = Serial.read(); // Lee el resultado enviado por la Jetson Nano
  if (resultado == '0') {
    digitalWrite(ledCoca, HIGH); // Enciende el LED de Coca
    delay(5000); // Espera 5 segundos
    digitalWrite(ledCoca, LOW); // Apaga el LED de Coca
  }
  else if (resultado == '1') {
    digitalWrite(ledPepsi, HIGH); // Enciende el LED de Pepsi
    delay(5000); // Espera 5 segundos
    digitalWrite(ledPepsi, LOW); // Apaga el LED de Pepsi
    }
  }
}
