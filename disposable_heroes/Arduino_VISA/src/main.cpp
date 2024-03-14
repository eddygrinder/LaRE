#include <Arduino.h>

const byte bufferSize = 6;
char inputBuffer[bufferSize + 1] ={0,0,0,0} ;
int i = 0;

const int rele_um = 2;
const int rele_dois = 3;
const int rele_tres = 4;
const int rele_quatro = 5;

void setup() {
  pinMode(rele_um, OUTPUT);
  pinMode(rele_dois, OUTPUT);
  pinMode(rele_tres, OUTPUT);
  pinMode(rele_quatro, OUTPUT);

  digitalWrite(rele_um, HIGH);
  digitalWrite(rele_tres, HIGH);
  digitalWrite(rele_dois, HIGH);
  digitalWrite(rele_quatro, HIGH);


  // initialize both serial ports:

  Serial.begin(9600);

  Serial1.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial1.available() > 0) {
    for (i = 0; i < 6; i++) {
      int inByte = Serial1.read();
      inputBuffer[i] = inByte;
      Serial.println(inByte);
      Serial.write(inputBuffer[i]);
    }
    switch (inputBuffer[2]) {
      case '1':  // your hand is on the sensor
        Serial.println("relé um");
        break;
      case '2':  // your hand is close to the sensor
        Serial.println("relé dois");
        digitalWrite(rele_um, LOW);
        digitalWrite(rele_dois, LOW);
        break;
      case '3':  // your hand is a few inches from the sensor
        Serial.println("relé três");
        break;
      case '4':  // your hand is nowhere near the sensor
        Serial.println("relé tres");
        digitalWrite(rele_tres, LOW);
        Serial.println("relé quatro");
        digitalWrite(rele_quatro, LOW);
        break;
    }
    delay(1000);
  }
}