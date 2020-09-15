#include <DRV8833.h>
#include <Wire.h>
#include <VL53L0X.h>

DRV8833 driver = DRV8833();
VL53L0X sensor1;
VL53L0X sensor2;

const int inputA1 = 4, inputA2 = 5;
const int shd1 = 7, shd2 = 8;
const int ls1 = 2, ls2 = 3;

const int motorSpeed = 255; // Half speed (255 / 2)

int state = 0;
int* statePtr = &state;

void moveMotors(int* statePtr);

void setup() {
  // Start the serial port:
  pinMode(shd1, OUTPUT);
  pinMode(shd2, OUTPUT);
  pinMode(ls1, INPUT);
  pinMode(ls2, INPUT);
  
  driver.attachMotorA(inputA1, inputA2);
  
  Serial.begin(115200);
  while (!Serial);
  Wire.begin();

  Serial.println("Yo momma");
  
  // activating sensor1 and reseting sensor2
  digitalWrite(shd1, HIGH);
  digitalWrite(shd2, LOW);
  delay(10);

  Serial.println("initing both sensors");

  if (!sensor1.init(true)){
    Serial.println("Failed to init sensor 1");
    while(1){};
  }
  sensor1.setTimeout(100);
  sensor1.setAddress(0x29);

  Serial.println("inited sensor 1");

  // unreset sensor2
  digitalWrite(shd2, HIGH);
  delay(10);
  if (!sensor2.init(true)){
    Serial.println("Failed to init sensor 2");
    while(1){};
  }
  sensor2.setTimeout(100);

  sensor1.startContinuous();
  sensor2.startContinuous();
  
  Serial.println("inited sensor2, ready!");

}

void loop() {
  moveMotors(statePtr);
  int dist1 = sensor1.readRangeContinuousMillimeters();
  int dist2 = sensor2.readRangeContinuousMillimeters();
  bool light1 = digitalRead(ls1);
  bool light2 = digitalRead(ls2);
  Serial.print("Sensor1: ");
  Serial.print(dist1);
  Serial.print(", Sensor2: ");
  Serial.print(dist2);
  Serial.print(" LS1: ");
  Serial.print(light1);
  Serial.print(" LS2: ");
  Serial.println(light2);
  
  delay(500);

}

void moveMotors(int* statePtr){

  Serial.print(*statePtr);
  Serial.print(" ");
  
  if (*statePtr == 0){
    Serial.println("Forward");
    driver.motorAForward(motorSpeed);
    *statePtr = 1;
  } else if (*statePtr == 1){
    Serial.println("Stop");
    driver.motorAStop();
    *statePtr = 2;
  } else if (*statePtr == 2){
    Serial.println("Reverse");
    driver.motorAReverse(motorSpeed);
    *statePtr = 3;
  } else {
    Serial.println("Stop");
    driver.motorAStop();
    *statePtr = 0;
  }
}
