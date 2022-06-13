#include <ros.h>

int adc = A0;
int distance_cm;
int acceptorState;
unsigned long mark;
bool full = false;

// sensor range is 4-30cm
// 30+ cm means no balls (sees black)
// < 20 cm means bin has some balls (sees white)
// 4 cm means bin is full

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  while (!full) {
    float volts = analogRead(adc)*0.0048828125;
    distance_cm = 13 * pow(volts, -1);

    if (distance_cm >= 30) {
      //publish no balls
    } else if (distance > 4) {
      //publish has some balls
    } 
    
    switch(acceptorState) {
      case 0:
        if (distance_cm <= 4) {
          acceptorState = 1;
          mark = millis();
        }
        break;
      case 1:
        if (millis() - mark > 3000) acceptorState = 2;
        if (distance_cm > 4) acceptorState = 0;
        break;
      case 2:
        Serial.println("Full");
        full = true;
    }
  }
}

void loop() {
  
}
