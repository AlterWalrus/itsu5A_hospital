#include <SPI.h>
#include <MFRC522.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);
unsigned long prev_millis = 0;
bool displaying = false;

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

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  delay(500);
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.display();
}

/*
CASOS DE RECHAZO
  tarjeta no registrada
  limite de visitas alcanzado
  fuera de horario
  edad no alcanzada
  edad excedida
*/

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
      //Beep
      case '2':
        beep(2);
        break;
    }
  }

  //Black magic type shit lmao
  if(displaying){
    unsigned long curr_millis = millis();
    if(curr_millis - prev_millis >= 10000){
      displaying = false;
      oled_clear();
    }
  }

  if(sensor.PICC_IsNewCardPresent()){
    if(sensor.PICC_ReadCardSerial()){
      String code = "";
      for(byte i = 0; i < sensor.uid.size; i++){
        code += byte_to_hex(sensor.uid.uidByte[i]);
      }

      show_access(true);
      delay(500);
      show_access(false);
      delay(500);
      beep(4);

      Serial.print(code);
      Serial.println();
      sensor.PICC_HaltA();
    }
  }
}

void oled_display(String s){
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(s);
  display.display();
  prev_millis = millis();
  displaying = true;
}

void oled_clear(){
  display.clearDisplay();
  display.display();
}

void show_access(bool valid){
  digitalWrite(BUZZ, HIGH);
  digitalWrite(valid ? LED_GREEN : LED_RED, HIGH);
  oled_display(valid ? "PASE USTED" : "NO PASARA");
  delay(500);
  digitalWrite(valid ? LED_GREEN : LED_RED, LOW);
  digitalWrite(BUZZ, LOW);
}

void beep(int times){
  for(int i = 0; i < times; i++){
    digitalWrite(BUZZ, HIGH);
    delay(100);
    digitalWrite(BUZZ, LOW);
    delay(100);
  }
}

char* byte_to_hex(byte num){
  static char hex_string[3];
  sprintf(hex_string, "%02X", num);
  return hex_string;
}
