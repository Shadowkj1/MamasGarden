#include "DHT.h"

#define DHTPIN 2      // Pin where the sensor is connected
#define DHTTYPE DHT11 // Sensor type

DHT dht(DHTPIN, DHTTYPE);

// Defined pins for the modules
int lightPin = A1;
int waterLevelPin = A2;
int moisturePin = A0; // Soil moisture sensor

void setup() {
  Serial.begin(9600); // Initialize the serial monitor
  dht.begin();        // Initialize the DHT sensor
  pinMode(lightPin, INPUT);
  pinMode(waterLevelPin, INPUT);
  pinMode(moisturePin, INPUT);
}

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

  // Check if DHT sensor reading is valid
  if (isnan(humidity) || isnan(temperatureC)) {
    Serial.println("Error reading DHT sensor data!");
  } else {
    // Output temperature and humidity data
    Serial.print("Temperature: ");
    Serial.print(temperatureC);
    Serial.print("°C, ");
    Serial.print(temperatureF);
    Serial.print("°F, ");
    Serial.print(temperatureK);
    Serial.println("K");

    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.print("%, ");
  }

  // Output light, soil moisture, and water level data
  Serial.print("Light: ");
  Serial.print(lightLevel);
  Serial.print("%, Moisture: ");
  Serial.print(moistureLevel);
  Serial.print(", Water Level: ");
  Serial.println(waterLevel);

  delay(5000); // Delay between readings
}
