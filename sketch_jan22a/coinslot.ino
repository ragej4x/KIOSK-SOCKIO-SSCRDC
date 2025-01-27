#include <SoftwareSerial.h>

#define BOUNCE_DURATION 50  
#define BILL 3

unsigned long bouncetime2 = 0;  
volatile int credit = 0;       

void setup() {
  Serial.begin(9600);           
  pinMode(BILL, INPUT_PULLUP);  
  attachInterrupt(digitalPinToInterrupt(BILL), ISR_count3, CHANGE); 
}

void ISR_count3() {
  if (millis() > bouncetime2) {
    if (!digitalRead(BILL)) {    // Detect LOW signal (pulse from the acceptor)
      credit += 1;               
      Serial.print("Credits: ");
      Serial.println(credit);    
    }

    bouncetime2 = millis() + BOUNCE_DURATION;
  }
}

void loop() {
}
