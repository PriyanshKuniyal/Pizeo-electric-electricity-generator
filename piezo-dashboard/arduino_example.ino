/*
  Piezoelectric Energy Harvesting Monitor
  
  This Arduino sketch reads data from a piezoelectric sensor system
  and sends it to the dashboard via Serial/Bluetooth.
  
  Hardware Setup:
  - Piezo sensor connected to A0
  - LED connected to pin 13 (built-in LED)
  - Optional: HC-05/HC-06 Bluetooth module on TX/RX
  
  Author: Science Fair Project
  Date: November 2025
*/

// Configuration
const int PIEZO_PIN = A0;           // Analog pin for piezo sensor
const int LED_PIN = 13;             // LED indicator
const int BAUD_RATE = 9600;         // Serial communication speed
const int SAMPLE_RATE = 500;        // Send data every 500ms
const float V_REF = 5.0;            // Arduino reference voltage
const int ADC_MAX = 1023;           // 10-bit ADC max value

// Calibration values (adjust based on your setup)
const float VOLTAGE_MULTIPLIER = 1.0;   // Voltage calibration factor
const float RESISTANCE = 1000.0;         // Load resistance in ohms

// Variables
int stepCount = 0;
float totalEnergy = 0.0;
unsigned long lastUpdate = 0;
unsigned long lastStepTime = 0;
bool ledState = false;

// Threshold for step detection
const float STEP_THRESHOLD = 2.0;  // Voltage threshold for detecting a press
const int DEBOUNCE_TIME = 200;     // Minimum time between steps (ms)

void setup() {
  // Initialize serial communication
  Serial.begin(BAUD_RATE);
  
  // Initialize LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // Set ADC reference to default (5V or 3.3V)
  analogReference(DEFAULT);
  
  // Wait for serial connection
  delay(1000);
  
  Serial.println("=================================");
  Serial.println("Piezoelectric Energy Monitor");
  Serial.println("Starting data transmission...");
  Serial.println("=================================");
}

void loop() {
  // Read piezoelectric sensor
  int rawValue = analogRead(PIEZO_PIN);
  float voltage = (rawValue / (float)ADC_MAX) * V_REF * VOLTAGE_MULTIPLIER;
  
  // Calculate instantaneous power (P = V²/R)
  float power = (voltage * voltage) / RESISTANCE;
  
  // Calculate energy increment (E = P × Δt)
  // Energy in joules = watts × seconds
  float deltaTime = SAMPLE_RATE / 1000.0;  // Convert ms to seconds
  float energyIncrement = power * deltaTime;
  totalEnergy += energyIncrement;
  
  // Detect steps (piezo press events)
  unsigned long currentTime = millis();
  if (voltage > STEP_THRESHOLD && 
      (currentTime - lastStepTime) > DEBOUNCE_TIME) {
    stepCount++;
    lastStepTime = currentTime;
    
    // Blink LED on step detection
    ledState = true;
    digitalWrite(LED_PIN, HIGH);
  }
  
  // Turn off LED after short duration
  if (ledState && (currentTime - lastStepTime) > 100) {
    ledState = false;
    digitalWrite(LED_PIN, LOW);
  }
  
  // Send data at specified sample rate
  if (currentTime - lastUpdate >= SAMPLE_RATE) {
    sendDataToSerial(voltage, totalEnergy, stepCount, power, ledState);
    lastUpdate = currentTime;
  }
  
  // Small delay to prevent overwhelming the ADC
  delay(10);
}

void sendDataToSerial(float voltage, float energy, int steps, float power, bool led) {
  // Send data in the format expected by the dashboard
  // Format: "Key: Value" on each line
  
  Serial.print("Voltage: ");
  Serial.println(voltage, 2);  // 2 decimal places
  
  Serial.print("Energy: ");
  Serial.println(energy, 6);   // 6 decimal places for small values
  
  Serial.print("Steps: ");
  Serial.println(steps);
  
  Serial.print("Power: ");
  Serial.println(power, 5);    // 5 decimal places
  
  Serial.print("LED: ");
  Serial.println(led ? "ON" : "OFF");
  
  // Optional separator for clarity
  Serial.println("-------");
}

// Optional: Function to reset counters (call via serial command)
void resetCounters() {
  stepCount = 0;
  totalEnergy = 0.0;
  Serial.println("Counters reset!");
}

// Optional: Function to calibrate voltage reading
float calibrateVoltage(int rawValue) {
  // Add your calibration logic here
  // Example: compensate for voltage divider, amplifier gain, etc.
  float voltage = (rawValue / (float)ADC_MAX) * V_REF;
  voltage = voltage * VOLTAGE_MULTIPLIER;
  return voltage;
}
