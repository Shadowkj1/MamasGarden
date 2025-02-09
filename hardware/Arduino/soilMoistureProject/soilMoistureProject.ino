#include "DHT.h"

#define DHTPIN 2      // Pin where the sensor is connected
#define DHTTYPE DHT11 // Sensor type

DHT dht(DHTPIN, DHTTYPE);

// Defined pins for the modules
int lightPin = A1;
int waterLevelPin = A2;
int moisturePin = A0; // Soil moisture sensor
int pump = 8;        // Digital pin where the relay is plugged in
int threshold = 20;   // Threshold value to trigger pump

void setup() {
  Serial.begin(9600); // Initialize the serial monitor
  dht.begin();        // Initialize the DHT sensor
  pinMode(lightPin, INPUT);
  pinMode(waterLevelPin, INPUT);
  pinMode(moisturePin, INPUT);
  pinMode(pump, OUTPUT);      // Setup for the pump as OUTPUT
  Serial.println("Reading From the Sensors...");
  delay(1000);  // 1 second delay
}

unsigned long previousMillis = 0; // Store the last time data was grabbed
const long interval = 20000; // Interval to grab data (1 minute)

void loop() {
  // Read humidity and temperature
  float humidity = dht.readHumidity();           
  float temperatureC = dht.readTemperature();   // Temperature in Celsius
  float temperatureF = dht.readTemperature(true); // Temperature in Fahrenheit
  float temperatureK = temperatureC + 273.15;   // Temperature in Kelvin

  // Read light, soil moisture, and water level sensors
  int rawLightLevel = analogRead(lightPin);
  int lightLevel = map(rawLightLevel, 0, 1023, 100, 0); // Convert to percentage (0 = dark, 100 = bright)
  int waterLevel = analogRead(waterLevelPin);
  int moistureLevel = analogRead(moisturePin);
  moistureLevel = map(moistureLevel, 550, 0, 0, 100); // Convert to percentage
  
  unsigned long currentMillis = millis();

  // Check if it's time to grab data
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    
    // Check if DHT sensor reading is valid
    if (isnan(humidity) || isnan(temperatureC)) {
      Serial.println("Error reading DHT sensor data! Fix to display data correctly");
    } else {
      printWaterStatus("NormalWaterLevel");
      printTemperatureANDHumidity(temperatureC, temperatureF, humidity);
      // Output light, soil moisture, and water level data
      printLightANDMoisture(lightLevel, waterLevel, moistureLevel);
      //Original printing format
      //Temperature: 25.00°C, 77.00°F, Humidity: 50.00%, Light: 50%, Moisture: 50%, Water Level: 50

    }


  }

  // // Check soil moisture level and control the pump
  // int moistureLevel = analogRead(moisturePin);
  // moistureLevel = map(moistureLevel, 550, 0, 0, 100); // Convert to percentage

  if (moistureLevel < threshold) { // If soil is dry, activate pump
    digitalWrite(pump, HIGH);
    Serial.println("Pump on for 1 second");
    delay(1000);  // Run pump for 1 second
    digitalWrite(pump, LOW);
    Serial.println("Pump off");
    printWaterStatus("LowWaterLevel");
    printTemperatureANDHumidity(temperatureC, temperatureF, humidity);
    printLightANDMoisture(lightLevel, waterLevel, moistureLevel);
  } else {
    static unsigned long lastPrintMillis = 0;
    if (currentMillis - lastPrintMillis >= 20000) { // 20 seconds interval
      lastPrintMillis = currentMillis;
      digitalWrite(pump, LOW);
      Serial.println("Soil moisture sufficient, Pump on standby");
    }
  }

}

//only prints the raw value to terminal, nothing else
void printTemperatureANDHumidity(float tempC, float tempF, float humidity) {
    // Output temperature and humidity data
    // Serial.print("Temperature: "); 
    Serial.print(tempC); 
    // Serial.print("°C, ");
    Serial.print(",");
    Serial.print(tempF); 
    // Serial.print("°F, ");
    Serial.print(",");
    // Serial.print(temperatureK); Serial.println("K");
    // Serial.print("Humidity: "); 
    Serial.print(humidity);
    Serial.print(","); 
    // Serial.print("%,");
}
//only prints the raw value to terminal, nothing else
void printLightANDMoisture(int lightLevel, int waterLevel, int moistLevel){
    // Output light, soil moisture, and water level data
    // Serial.print("Light: "); 
    Serial.print(lightLevel);
    Serial.print(",");
    Serial.print(moistLevel);
    // Serial.print("%, Water Level: "); 
    Serial.print(",");
    Serial.println(waterLevel); 
}

void printWaterStatus(String status){
  Serial.print(status);
  Serial.print(",");
}