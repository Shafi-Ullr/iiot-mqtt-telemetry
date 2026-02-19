# iiot-mqtt-telemetry
# iiot-mqtt-telemetry
# IIoT MQTT Telemetry Monitoring (HiveMQ Cloud → SQLite → Analytics + Charts)

A simple IIoT monitoring demo built in Python. A “publisher” script simulates sensor data for multiple assets and publishes it over MQTT (TLS) to HiveMQ Cloud. A “collector” subscribes to the telemetry topics and stores messages in a local SQLite database. Analytics and interactive HTML charts are generated from the stored data.

## Architecture
publisher.py -> HiveMQ Cloud (MQTT over TLS) -> collector_sqlite.py -> telemetry.db (SQLite)  
                                                     |  
                                                     +-> analytics.py (fault summary + CSV)  
                                                     +-> charts_html.py (interactive HTML charts)

## What it generates
- telemetry.db (SQLite database of telemetry)
- analytics.py output (fault counts by code + last fault per asset)
- telemetry_export.csv (open in Excel)
- Interactive HTML charts:
  - chart_temperature.html
  - chart_vibration.html
  - chart_power.html
  - chart_fault_counts.html (accurate counts from full dataset)

## MQTT topics + payload
**Topic pattern:**  
site/<site>/asset/<asset>/telemetry

**Example topic:**  
site/london_dc1/asset/ahu_01/telemetry

**Example payload (JSON):**
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
# IIoT MQTT Telemetry Monitoring (HiveMQ Cloud → SQLite → Analytics + Charts)

A simple IIoT monitoring demo built in Python. A “publisher” script simulates sensor data for multiple assets and publishes it over MQTT (TLS) to HiveMQ Cloud. A “collector” subscribes to the telemetry topics and stores messages in a local SQLite database. Analytics and interactive HTML charts are generated from the stored data.

## Architecture
publisher.py -> HiveMQ Cloud (MQTT over TLS) -> collector_sqlite.py -> telemetry.db (SQLite)  
                                                     |  
                                                     +-> analytics.py (fault summary + CSV)  
                                                     +-> charts_html.py (interactive HTML charts)

## What it generates
- telemetry.db (SQLite database of telemetry)
- analytics.py output (fault counts by code + last fault per asset)
- telemetry_export.csv (open in Excel)
- Interactive HTML charts:
  - chart_temperature.html
  - chart_vibration.html
  - chart_power.html
  - chart_fault_counts.html (accurate counts from full dataset)

## MQTT topics + payload
**Topic pattern:**  
site/<site>/asset/<asset>/telemetry

**Example topic:**  
site/london_dc1/asset/ahu_01/telemetry

**Example payload (JSON):**
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
Fault codes

0 = no fault

101 = overheat

202 = vibration spike

303 = pressure drop

Setup

Install dependencies:
python -m pip install paho-mqtt==1.6.1
python -m pip install pandas==2.0.3 plotly==5.18.0
Configure HiveMQ credentials in:

publisher.py

collector_sqlite.py

Do NOT commit real passwords to GitHub.

Run

Terminal 1 (collector):
python collector_sqlite.py
Terminal 2 (publisher):
python publisher.py
Generate analytics + charts:
python analytics.py
python charts_html.py
Open the charts by double-clicking:

chart_temperature.html

chart_vibration.html

chart_power.html

chart_fault_counts.html

Screenshots
Fault counts (per asset)
::contentReference[oaicite:0]{index=0}
