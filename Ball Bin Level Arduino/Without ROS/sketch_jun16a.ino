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
  while (!full) {
    float volts = analogRead(adc)*0.0048828125;
    distance_cm = 13 * pow(volts, -1);

    if (distance_cm >= 30) {
      // Empty
    } else if (distance_cm > 4) {
      // Some balls
    } 
    
    switch(acceptorState) {
      case 0:
        if (distance_cm <= 4) {
          acceptorState = 1;
          mark = millis();
        }
        break;
      case 1:
        // Change 3000 if necessary - bin is full when distance is 4cm for 3 seconds
        if (millis() - mark > 3000) acceptorState = 2;
        if (distance_cm > 4) acceptorState = 0;
        break;
      case 2:
        // Full
  }
}

void loop() {
  
}
