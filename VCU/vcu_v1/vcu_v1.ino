/*
   Autonomous Vehicular Traffic Management
   PID Motor Control System V1

   Hall Effect Sensor on pin A0
*/

#include <Wire.h>
#include <PID_v1.h>

int vSen = A0;
unsigned long currSenTime;
unsigned long lastSenTime;
int vSenSpeed = 0;
bool vSenLastState = false;
unsigned long vSenTimeout = 500000;
int mPinFwdA = 5;
int mPinFwdB = 6;
int sPinL = 11;
int sPinR = 10;
unsigned long scrUpdateTimer = 0;
unsigned long scrUpdateInt = 250;
int vCom = 0;
int sCom = 127;
int vComPwmMax = 95;
int sComPwmMax = 95;
int i2cIndex = 0;
int mSpeedMult = 20;
unsigned long lastRecvTime = 0;
int cmdTimeout = 1000;


double mSpeedSet, mSpeedAct, mSpeedPwm;

//Specify the links and initial tuning parameters
PID mPID(&mSpeedAct, &mSpeedPwm, &mSpeedSet, 0.07, 0.25, 0.005, DIRECT);

void setup() {
  Wire.begin(0x0a);
  Wire.onReceive(i2c_recv);
  Serial.begin(115200);
  pinMode(vSen, INPUT);
  pinMode(mPinFwdA, OUTPUT);
  pinMode(mPinFwdB, OUTPUT);
  mSpeedSet = 0;
  mPID.SetMode(AUTOMATIC);
}

void loop() {
  vSenUpdate();
  watchDog();
}

void vSenUpdate() {
  if (digitalRead(vSen) != vSenLastState) {
    if (vSenLastState) {
      currSenTime = micros();
      vSenSpeed = 60000000 / (currSenTime - lastSenTime);
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
  mDriveSet();
  mDriveCmd();
  sDriveCmd();
  mPID.Compute();
}

void mDriveSet() {
  mSpeedSet = vCom * mSpeedMult;
}

void mDriveCmd() {
  if (mSpeedPwm <= vComPwmMax && vCom != 0) {
    analogWrite(mPinFwdB, mSpeedPwm);
  } else if(mSpeedPwm != 0 && vCom != 0) {
    analogWrite(mPinFwdB, vComPwmMax);
  } else {
    analogWrite(mPinFwdB, 0);
  }
}

void sDriveCmd() {
  // left steer, invert
  if (sCom == 127) {
    analogWrite(sPinL, 0);
    analogWrite(sPinR, 0);
  }
  if (sCom < 127) {
    analogWrite(sPinR, 0);
    analogWrite(sPinL, map(sCom, 127, 0, 0, sComPwmMax));
  }
  if (sCom > 127) {
    analogWrite(sPinL, 0);
    analogWrite(sPinR, map(sCom, 128, 255, 0, sComPwmMax));
  }

}

void i2c_recv(int length) {
  while (Wire.available() > 0) {
    int c = Wire.read();
    lastRecvTime = millis();
    Serial.print("Command execution read: ");
    Serial.println(c);
    if (i2cIndex == 2) {
      i2cIndex = 0;
      sCom = c;
      Serial.print("sCom receive: ");
      Serial.println(sCom);
    }

    if (i2cIndex == 1) {
      i2cIndex = 2;
      vCom = c;
      Serial.print("vCom receive: ");
      Serial.println(vCom);
    }

    if (c == 'c' || i2cIndex == 0) {
      i2cIndex = 1;
    }
  }
}

void watchDog() {
  if (millis() > lastRecvTime + cmdTimeout) {
    vCom = 0;
    sCom = 127;
    analogWrite(sPinL, 0);
    analogWrite(sPinR, 0);
  }
}

