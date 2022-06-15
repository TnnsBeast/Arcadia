#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle nh;
std_msgs::String binlevel_msg;
ros::Publisher binlevel("binlevel", &binlevel_msg);

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
  nh.initNode();
  nh.advertise(binlevel);

  binlevel_msg.data = "START";
  binlevel.publish( &binlevel_msg );
  
  Serial.begin(9600);

  while (!full) {
    float volts = analogRead(adc)*0.0048828125;
    distance_cm = 13 * pow(volts, -1);

    if (distance_cm >= 30) {
      binlevel_msg.data = "Empty";
      binlevel.publish( &binlevel_msg );
      nh.spinOnce();
    } else if (distance_cm > 4) {
      binlevel_msg.data = "Some Balls";
      binlevel.publish( &binlevel_msg );
      nh.spinOnce();
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
        binlevel_msg.data = "Full";
        binlevel.publish( &binlevel_msg );
        nh.spinOnce();
        full = true;
    }
  }
}

void loop() {
  
}
