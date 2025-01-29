#include <SoftwareSerial.h>

#define BOUNCE_DURATION 100    // Adjust debounce duration (in milliseconds)
#define BILL 3                 // Pin connected to the bill acceptor
#define COUNT_WINDOW 5000      // Counting window duration (in milliseconds)
#define COIN 5

int coin_count = 0;
int coin_val = 0;
volatile unsigned long lastPulseTime = 0;  // Time of the last valid pulse
volatile int pulseCount = 0;               // Total number of pulses
volatile bool counting = false;            // Whether counting is active
unsigned long startCountingTime = 0;       // When counting started

#define motor_relay 8
#define irsensor 2
int count = 0;
int counterblock = 0;

void setup() {
  Serial.begin(9600);                  // Start serial communication
  pinMode(BILL, INPUT_PULLUP);         // Set BILL pin as input with internal pull-up
  attachInterrupt(digitalPinToInterrupt(BILL), ISR_countPulse, CHANGE);  // Interrupt on state change
  
  pinMode(COIN, INPUT_PULLUP);


  pinMode(irsensor, INPUT);  // Set the IR sensor pin as input

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


void start_change(){
  int sensorValue = digitalRead(irsensor);
  if (sensorValue == HIGH){
    count -= 5;
    counterblock = 0;
    delay(200);

  }
    if (count > 0){
      pinMode(motor_relay, HIGH);
      counterblock ++;
      }
    else if (count <  1){
      pinMode(motor_relay, LOW);
    }
  

  
  if (Serial.available() > 0){
      count = Serial.parseInt();
      
  }

  if (counterblock > 10){
    pinMode(motor_relay, LOW);
  }

}


void insert_coin(){
  if (digitalRead(COIN) == LOW){
    coin_count ++;

    if (coin_count > 4){
      coin_val += 5;
      coin_count = 0;
      Serial.println(coin_val);
      coin_val = 0;

    }
    
    delay(150);

    
    
    
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


    // Determine the inserted amount based on the pulse count
    if (count >= 9 && count <= 10) {
      Serial.println("100");
    } else if (count >= 4 && count <= 5) {
      Serial.println("50");
    } else if (count >= 1 && count <= 2) {
      Serial.println("20");
    }
  }


  start_change();
  insert_coin();

}
