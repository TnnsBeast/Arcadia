#include <Wire.h>
#include <TFMPI2C.h>
TFMPI2C tfmp;

void setup() {
  Serial.begin(115200);
  tfmp.recoverI2CBus();
}

int16_t distance = 0; // cm
int16_t flux = 0; // strength of returned signal
int16_t temp = 0; // celsius

void loop() {
  tfmp.getData(distance, flux, temp);
  if (tfmp.status == TFMP_READY) {
    Serial.print("Distance: ");
    Serial.println(distance);
    Serial.print("Flux: ");
    Serial.println(flux);
    Serial.print("Temperature: ");
    Serial.println(temp);
    Serial.println();
  }
  else {
    tfmp.printFrame(); // Should show errors
    if (tfmp.status == TFMP_I2CWRITE) {
      tfmp.recoverI2CBus();
    }
  }
  delay(50);

}
