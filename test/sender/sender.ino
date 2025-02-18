void setup() {
  // Start the serial communication at 230400 baud rate
  Serial.begin(230400);
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming byte
    char incomingByte = Serial.read();
    
    // Print the received byte to the Serial Monitor
    Serial.print(incomingByte);
  }
}