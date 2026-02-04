import json
import sqlite3
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

MQTT_HOST = "f6700a4b88964673ba0105d54a953219.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "Ullr1"
MQTT_PASS = "Enter_Password_Here"

TOPIC = "site/+/asset/+/telemetry"
DB_NAME = "telemetry.db"

def init_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            received_utc TEXT,
            topic TEXT,
            site TEXT,
            asset TEXT,
            temperature_c REAL,
            pressure_bar REAL,
            vibration_rms REAL,
            power_kw REAL,
            fault_code INTEGER,
            raw_json TEXT
        )
    """)
    con.commit()
    con.close()

def insert_row(topic, payload_text):
    # Parse JSON
    data = json.loads(payload_text)

    received_utc = datetime.now(timezone.utc).isoformat()

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO telemetry (
            received_utc, topic, site, asset,
            temperature_c, pressure_bar, vibration_rms, power_kw, fault_code,
            raw_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        received_utc,
        topic,
        data.get("site"),
        data.get("asset"),
        data.get("temperature_c"),
        data.get("pressure_bar"),
        data.get("vibration_rms"),
        data.get("power_kw"),
        data.get("fault_code"),
        payload_text
    ))
    con.commit()
    con.close()

def on_connect(client, userdata, flags, rc):
    print("Connected (0 is good):", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    text = msg.payload.decode("utf-8")
    print("Received:", msg.topic, text)

    try:
        insert_row(msg.topic, text)
    except Exception as e:
        print("Could not save to DB:", e)

def main():
    init_db()

    client = mqtt.Client(client_id="collector_sqlite_win8")
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.tls_set()
    # If Windows 8 gives SSL errors, uncomment:
    # client.tls_insecure_set(True)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_forever()

if __name__ == "__main__":
    main()
