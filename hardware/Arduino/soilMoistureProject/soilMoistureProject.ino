#include "DHT.h"

#define DHTPIN 2      // Pin where the sensor is connected
#define DHTTYPE DHT11 // Sensor type

DHT dht(DHTPIN, DHTTYPE);

// Defined pins for the modules
int lightPin = A1;
int waterLevelPin = A2;
int moisturePin = A0; // Soil moisture sensor
int pump = 8;        // Digital pin where the relay is plugged in
int threshold = 5;   // Threshold value to trigger pump

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
const long interval = 60000; // Interval to grab data (1 minute)

void loop() {
  unsigned long currentMillis = millis();

  // Check if it's time to grab data
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

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

    // Check if DHT sensor reading is valid
    if (isnan(humidity) || isnan(temperatureC)) {
      Serial.println("Error reading DHT sensor data!");
    } else {
      printTemperatureANDHumidity(temperatureC, temperatureF, humidity);
    }

    // Output light, soil moisture, and water level data
    printLightANDMoisture(lightLevel, waterLevel, moistureLevel);
  }

  // Check soil moisture level and control the pump
  int moistureLevel = analogRead(moisturePin);
  moistureLevel = map(moistureLevel, 550, 0, 0, 100); // Convert to percentage

  if (moistureLevel < threshold) { // If soil is dry, activate pump
    digitalWrite(pump, HIGH);
    Serial.println("Pump on for 1 second");
    delay(1000);  // Run pump for 1 second
    digitalWrite(pump, LOW);
    Serial.println("Pump off");
  } else {
    digitalWrite(pump, LOW);
    Serial.println("Soil moisture sufficient, do not turn on pump");
  }

}

void printTemperatureANDHumidity(float tempC, float tempF, float humidity) {
    // Output temperature and humidity data
    Serial.print("Temperature: "); 
    Serial.print(tempC); Serial.print("°C, ");
    Serial.print(tempF); Serial.print("°F, ");
    // Serial.print(temperatureK); Serial.println("K");
    Serial.print("Humidity: "); Serial.print(humidity); Serial.print("%, ");
}

void printLightANDMoisture(int lightLevel, int waterLevel, int moistLevel){
    // Output light, soil moisture, and water level data
    Serial.print("Light: "); Serial.print(lightLevel);
    Serial.print("%, Moisture: "); Serial.print(moistLevel);
    Serial.print("%, Water Level: "); Serial.println(waterLevel); 
}