// Define the PWM pin
const int pwmPin = 9;

void setup() {
  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);
  
  // Set the PWM pin as an output
  pinMode(pwmPin, OUTPUT);
}

void loop() {
  // Check if data is available to read from Serial port
  if (Serial.available() > 0) {
    // Read the incoming byte
    int dutyCycle = Serial.read();

    analogWrite(pwmPin, dutyCycle);
  }
}
