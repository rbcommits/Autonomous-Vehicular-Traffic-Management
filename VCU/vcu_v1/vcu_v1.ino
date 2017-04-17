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
int mPinFwdA = 9;
int mPinFwdB = 10;
int sComPinL = 5;
int sComPinR = 6;
unsigned long scrUpdateTimer = 0;
unsigned long scrUpdateInt = 250;
int vCom = 0;
int sCom = 0;
int vComPwmMax = 95;
int sComPwmMax = 95;


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
  analogWrite(mPinFwdA, 127);
  mSpeedSet = 1500;
  mPID.SetMode(AUTOMATIC);
}

void loop() {
  vSenUpdate();
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
  Serial.println(vSenSpeed);
}

void pidUpdate() {
  mSpeedAct = vSenSpeed;
  mPID.Compute();
  mDriveSet();
}

void mDriveSet(){
  if(mSpeedPwm <= vComPwmMax){
    analogWrite(mPinFwdA, mSpeedPwm);
  } else {
    analogWrite(mPinFwdA, vComPwmMax);
  }
  if(mSpeedPwm <= vComPwmMax){
    analogWrite(mPinFwdB, mSpeedPwm);
  } else {
    analogWrite(mPinFwdB, vComPwmMax);
  }



}

void i2c_recv(int length){
  while(Wire.available() > 0){
    int c = Wire.read();
    if(c == 'c'){
      vCom = Wire.read();
      sCom = Wire.read();
    }
  }
}
