# MamasGarden

## Story
### Inspiration
There's nothing quite like the feeling of watching your plants flourish – the vibrant green leaves, the new growth, the sense of accomplishment. Plants bring life and beauty to our homes, and caring for them can be incredibly rewarding. But sometimes it can be difficult to keep track of the specificities of all the kinds of plants there are and the different things they require. This is especially daunting when you become a super plant lover and have a large collection. Mama's Garden aims to keep the joy of plant care alive while reducing the amount of work by helping you keep track of exactly how your plant is feeling when and how often.

### What it does
Mama's Garden tracks the amount of humidity, temperature, sunlight, water level, and moisure your little plant actively has. When the plant reaches self set undesirable levels of moisture, the device automatically resaturates the plant with a water reserve.

### How we built it
Hardware Devices Used:
- Arduino
- Raspberry Pi
- DHT11 Humidity Detector
- Water Level Sensor
- Photo Resistor
Software Technologies:
- MongoDB
- Arduino IDE
- Python Scripts
- Flask
- Spline

We have an arduino that is connected to our Raspberry pi that runs the script to activate the arduino. Once the arduino is running and activating the external tools connected to it through a bread board, we export the data to a python script which then writes all of our plant data in json format to a file. This file is then exported to MongoDB and then used for front end purposes such as graphing and plant data checking actively.

### Challenges we ran into
- A problem early on was the water pump would continue to pump water even when not needed
- Getting the data from arduino to a proper json for parsing
- Integrating MongoDB with UI was a challenge
- *fighting sleep*

### Accomplishments
- EVERYTHING!!
- GRAPHS!
- BEAUTIFUL UI
- HARDWARE HASNT FAILED SPONTANEOUSLY

### Whats Next For Mama's Garden
Incorporating more machines for this project and having a case for this device. Since time and resources were limited, we could not incorporate multiple machines for the project that connect to various plants so that we would improve that. Also, add a case to make the project more neater, more cohesive, and fewer accidents on the hardware side.

## How to run (hardware so far)
1. Connect all of your Arduino and Raspberry Pi components
2. Open Arduino IDE with the io file
3. Compile, and run the file
4. Verify it is sent to the Arduino Successfully
5. Run plantTesting.py and let it log plant status
