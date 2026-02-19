# iiot-mqtt-telemetry
# IIoT MQTT Telemetry Monitoring (HiveMQ Cloud → SQLite → Analytics + Charts)

A simple Industrial IoT (IIoT) monitoring demo. A Python “publisher” simulates sensor telemetry for multiple assets and publishes it via MQTT (TLS) to HiveMQ Cloud. A Python “collector” subscribes to the telemetry topics and stores the data into a local SQLite database. Analytics and interactive HTML charts are generated from the stored data.

## Architecture

## Screenshots

### Fault counts (per asset)
![Fault counts](Screenshots/01%20Fault%20Counts.PNG)

### Temperature over time
![Temperature](Screenshots/02%20Temperature.PNG)

### Vibration over time
![Vibration](Screenshots/03%20Vibration.png)

### Power over time
![Power](Screenshots/04%20Power.PNG)
