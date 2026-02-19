# iiot-mqtt-telemetry
# IIoT MQTT Telemetry Monitoring (HiveMQ Cloud → SQLite → Analytics + Charts)

A simple Industrial IoT (IIoT) monitoring demo. A Python “publisher” simulates sensor telemetry for multiple assets and publishes it via MQTT (TLS) to HiveMQ Cloud. A Python “collector” subscribes to the telemetry topics and stores the data into a local SQLite database. Analytics and interactive HTML charts are generated from the stored data.

## Architecture

publisher.py -> HiveMQ Cloud (MQTT over TLS) -> collector_sqlite.py -> telemetry.db (SQLite)
|
+-> analytics.py (fault summary + CSV export)
+-> charts_html.py (interactive HTML charts)

## What it generates

- `telemetry.db` (SQLite database of telemetry)
- `analytics.py` output: fault counts by code + last fault per asset
- `telemetry_export.csv` (for Excel)
- Interactive charts (HTML):
  - temperature, vibration, power (rolling average, multi-asset)
  - fault counts by code (accurate counts from full dataset)

## MQTT topics + payload

Topic pattern:

site/<site>/asset/<asset>/telemetry

Payload example:
```json
{
  "site": "london_dc1",
  "asset": "ahu_01",
  "temperature_c": 22.15,
  "pressure_bar": 3.21,
  "vibration_rms": 0.346,
  "power_kw": 12.07,
  "fault_code": 0
}
Fault codes:

0 = no fault

101 = overheat

202 = vibration spike

303 = pressure drop

## Screenshots

### Fault counts (per asset)
![Fault counts](Screenshots/01%20Fault%20Counts.PNG)

### Temperature over time
![Temperature](Screenshots/02%20Temperature.PNG)

### Vibration over time
![Vibration](Screenshots/03%20Vibration.png)

### Power over time
![Power](Screenshots/04%20Power.PNG)
