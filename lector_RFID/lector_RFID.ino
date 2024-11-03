#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9
#define SS_PIN 10
#define LED_RED 2
#define LED_GREEN 7
#define BUZZ 4

MFRC522 sensor(SS_PIN, RST_PIN);

void setup() {
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(BUZZ, OUTPUT);

  SPI.begin();
  sensor.PCD_Init();

  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0){
    char comm = Serial.read();
    switch(comm){
      //Acceso concedido
      case '1':
        show_access(true);
        break;
      //Acceso denegado
      case '0':
        show_access(false);
        break;
    }
  }

  if(sensor.PICC_IsNewCardPresent()){
    if(sensor.PICC_ReadCardSerial()){
      String code = "";
      for(byte i = 0; i < sensor.uid.size; i++){
        code += byte_to_hex(sensor.uid.uidByte[i]);
      }
      Serial.print(code);
      Serial.println();
      sensor.PICC_HaltA();
    }
  }
}

void show_access(bool valid){
  digitalWrite(BUZZ, HIGH);
  digitalWrite(valid ? LED_GREEN : LED_RED, HIGH);
  delay(500);
  digitalWrite(valid ? LED_GREEN : LED_RED, LOW);
  digitalWrite(BUZZ, LOW);
}

char* byte_to_hex(byte num){
  static char hex_string[3];
  sprintf(hex_string, "%02X", num);
  return hex_string;
}
