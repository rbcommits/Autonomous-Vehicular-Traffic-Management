/*
   Autonomous Vehicular Traffic Management
   PID Speed Control Loop Phase 1 Test

   Hall Effect Sensor on pin A0

   Display Information:
   LiquidCrystal Library
   LCD RS pin to digital pin 12
   LCD Enable pin to digital pin 11
   LCD D4 pin to digital pin 5
   LCD D5 pin to digital pin 4
   LCD D6 pin to digital pin 3
   LCD D7 pin to digital pin 2
   LCD R/W pin to ground
   LCD VSS pin to ground
   LCD VCC pin to 5V
   10K resistor:
   ends to +5V and ground
   wiper to LCD VO pin (pin 3)

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
#include <PID_v1.h>

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
int mPinFwdA = 9;
int mPinFwdB = 10;
unsigned long scrUpdateTimer = 0;
unsigned long scrUpdateInt = 250;

LiquidCrystal lcd(lcdRS, lcdEN, lcdD4, lcdD5, lcdD6, lcdD7);

double mSpeedSet, mSpeedAct, mSpeedPwm;

//Specify the links and initial tuning parameters
PID mPID(&mSpeedAct, &mSpeedPwm, &mSpeedSet, 0.8, 3, 0.01, DIRECT);

void setup() {
  Serial.begin(115200);
  lcd.begin(16, 2);
  lcd.print("AVTM v0.0.1 Test");
  pinMode(vSen, INPUT);
  pinMode(mPinFwdA, OUTPUT);
  pinMode(mPinFwdB, OUTPUT);

  delay(1000);
  lcd.clear();
  analogWrite(mPinFwdA, 127);
  mSpeedSet = 120;
  mPID.SetMode(AUTOMATIC);
}

void loop() {
  vSenUpdate();
  if (millis() - scrUpdateTimer > scrUpdateInt) {
    displayUpdate();
    scrUpdateTimer = millis();
  }
  
}

void displayUpdate() {
  lcd.setCursor(0, 0);
  lcd.print("SCm: ");
  lcd.print((int)mSpeedSet);
  lcd.print("   ");
  lcd.setCursor(9, 0);
  lcd.print("ER: ");
  lcd.print((int)(100 * ((mSpeedAct - mSpeedSet) / (mSpeedSet / 2.0 + mSpeedAct / 2.0))));
  lcd.print("   ");
  lcd.setCursor(0, 1);
  lcd.print("SAc: ");
  lcd.print(vSenSpeed);
  lcd.print("   ");
  lcd.setCursor(9, 1);
  lcd.print("DC: ");
  lcd.print((int)(mSpeedPwm / 2.55));
  lcd.print("   ");
}

void vSenUpdate() {
  if (digitalRead(vSen) != vSenLastState) {
    if (vSenLastState) {
      currSenTime = micros();
      vSenSpeed = 60000000 / (currSenTime - lastSenTime) / 6;
      lastSenTime = currSenTime;
    }
    vSenLastState = !vSenLastState;
  }
  if (micros() - lastSenTime > vSenTimeout) {
    vSenSpeed = 0;
  }
  pidUpdate();
}

void pidUpdate() {
  mSpeedAct = vSenSpeed;
  mPID.Compute();
  analogWrite(mPinFwdA, mSpeedPwm);
  analogWrite(mPinFwdB, mSpeedPwm);
}

