#include <SoftwareSerial.h>
#include <ArduinoJson.h>

#define BOUNCE_DURATION 100    // Adjust debounce duration (in milliseconds)
#define BILL 3                 // Pin connected to the bill acceptor
#define COUNT_WINDOW 5000      // Counting window duration (in milliseconds)

volatile unsigned long lastPulseTime = 0;  // Time of the last valid pulse
volatile int pulseCount = 0;               // Total number of pulses
volatile bool counting = false;            // Whether counting is active
unsigned long startCountingTime = 0;       // When counting started


const int sensorPin = 2;
const int motorPin = 9;
int coinCount = 0;
int targetCount = 0; // Example target


void setup() {
  Serial.begin(9600);                  // Start serial communication
  pinMode(BILL, INPUT_PULLUP);         // Set BILL pin as input with internal pull-up
  attachInterrupt(digitalPinToInterrupt(BILL), ISR_countPulse, CHANGE);  // Interrupt on state change

  pinMode(sensorPin, INPUT_PULLUP);
  pinMode(motorPin, OUTPUT);
  digitalWrite(motorPin, HIGH); // Start motor
}

void ISR_countPulse() {
  static unsigned long pulseStartTime = 0;  // Keeps track of pulse duration
  unsigned long currentTime = millis();     // Get the current time

  if (digitalRead(BILL) == LOW) {  // Detect only LOW pulses
    if (currentTime - lastPulseTime > BOUNCE_DURATION) {  // Debounce logic
      lastPulseTime = currentTime;  // Update last valid pulse time
      pulseCount++;                 // Increment the pulse count

      // Start counting if not already active
      if (!counting) {
        counting = true;
        startCountingTime = currentTime;
      }
    }
  }
}


void changer(){


  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    StaticJsonDocument<200> doc;
    deserializeJson(doc, data);

    targetCount = doc["change"];

    // Modify the received value
    
      
      if (digitalRead(sensorPin) == LOW) {
      coinCount++;
      delay(100); // Debounce
      }
      if (coinCount >= targetCount) {
          digitalWrite(motorPin, LOW); // Stop motor

          StaticJsonDocument<200> updatedDoc;
          updatedDoc["get_change"] = false;
          updatedDoc["change"] = 0;
          String updatedData;
          serializeJson(updatedDoc, updatedData);

      }

    // Create JSON with updated value

    // Send updated JSON back
  }

}

void loop() {
  // Check if the counting window has elapsed
  if (counting && (millis() - startCountingTime > COUNT_WINDOW)) {
    noInterrupts();               // Temporarily disable interrupts
    int count = pulseCount;       // Copy pulse count
    pulseCount = 0;               // Reset pulse count
    counting = false;             // Reset counting flag
    interrupts();                 // Re-enable interrupts

    // Display the pulse count

    // Determine the inserted amount based on the pulse count
    if (count >= 9 && count <= 10) {
      Serial.println(100);
    } else if (count >= 4 && count <= 5) {
      Serial.println(50);
    } else if (count >= 1 && count <= 2) {
      Serial.println(20);
    }
  }

  changer();
}
