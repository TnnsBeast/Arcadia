int adc = A0;
int distance_cm;
int bin_max = 4;
int acceptorState;
unsigned long mark;
bool full = false;



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  while (!full) {
    float volts = analogRead(adc)*0.0048828125;
    distance_cm = 13 * pow(volts, -1);
    if (distance_cm < 40) {
      Serial.println(distance_cm);
    } else {
      Serial.println("40");
    }
    switch(acceptorState) {
      case 0:
        if (distance_cm <= bin_max) {
          acceptorState = 1;
          mark = millis();
        }
        break;
      case 1:
        if (millis() - mark > 3000) acceptorState = 2;
        if (distance_cm > bin_max) acceptorState = 0;
        break;
      case 2:
        Serial.println("Full");
        full = true;
    }
  }
}

void loop() {
  
}
