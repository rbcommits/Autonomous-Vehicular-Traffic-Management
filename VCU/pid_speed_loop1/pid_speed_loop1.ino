/*
 * Autonomous Vehicular Traffic Management
 * PID Speed Control Loop Phase 1 Test
 * 
 * Hall Effect Sensor on pin A0
 * 
 * Display Information:
 * LiquidCrystal Library
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe
 modified 22 Nov 2010
 by Tom Igoe
 */

#include <LiquidCrystal.h>

int lcdRS = 12;
int lcdEN = 11;
int lcdD4 = 5;
int lcdD5 = 4;
int lcdD6 = 3;
int lcdD7 = 2;
int vSen = A0;
unsigned long currSenTime;
unsigned long lastSenTime;
int vSenSpeed = 0;
bool vSenLastState = false;
unsigned long vSenTimeout = 500000;

LiquidCrystal lcd(lcdRS, lcdEN, lcdD4, lcdD5, lcdD6, lcdD7);

void setup() {
  Serial.begin(115200);
  lcd.begin(16, 2);
  lcd.print("AVTM v0.0.1 Test");
  pinMode(vSen, INPUT);
  delay(1000);
  lcd.clear();
}

void loop() {
  vSenUpdate();
  displayUpdate();
}

void displayUpdate(){
  lcd.setCursor(0, 0);
  lcd.print("SP COM: ");
  lcd.setCursor(0, 1);
  lcd.print("SP ACT: ");
  lcd.print(vSenSpeed);
  lcd.print("    ");
}

void vSenUpdate(){
  if(digitalRead(vSen) != vSenLastState){
    if(vSenLastState){
      currSenTime = micros();
      vSenSpeed = 60000000/(currSenTime - lastSenTime)/2;
      lastSenTime = currSenTime;
    }
    vSenLastState = !vSenLastState;
  }
  if(micros() - lastSenTime > vSenTimeout){
    vSenSpeed = 0;
  }
}

