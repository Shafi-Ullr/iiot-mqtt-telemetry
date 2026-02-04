import json, time, random
import paho.mqtt.client as mqtt

MQTT_HOST = "f6700a4b88964673ba0105d54a953219.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "Ullr1"
MQTT_PASS = "Enter_Password_Here"

SITE = "london_dc1"
ASSETS = ["ahu_01", "chiller_02", "pump_03"]

def make_payload(asset):
    # Base behaviour per asset (slightly different "normal" values)
    if asset == "ahu_01":
        temp = 22 + random.uniform(-1.0, 1.0)
        pressure = 3.2 + random.uniform(-0.10, 0.10)
        vib = 0.35 + random.uniform(-0.06, 0.06)
        power = 12 + random.uniform(-1.0, 1.0)
    elif asset == "chiller_02":
        temp = 18 + random.uniform(-1.2, 1.2)
        pressure = 2.8 + random.uniform(-0.12, 0.12)
        vib = 0.45 + random.uniform(-0.08, 0.08)
        power = 18 + random.uniform(-1.5, 1.5)
    else:  # pump_03
        temp = 24 + random.uniform(-0.8, 0.8)
        pressure = 3.8 + random.uniform(-0.15, 0.15)
        vib = 0.30 + random.uniform(-0.05, 0.05)
        power = 9 + random.uniform(-0.8, 0.8)

    # Fault injection (realistic-ish):
    # ~5% overall chance, but different fault types per asset
    fault_code = 0
    r = random.random()
    if r < 0.02:
        fault_code = 101  # overheat
        temp += 6
    elif r < 0.04:
        fault_code = 202  # vibration spike
        vib += 0.35
    elif r < 0.05:
        fault_code = 303  # pressure drop
        pressure -= 0.8

    payload = {
        "site": SITE,
        "asset": asset,
        "temperature_c": round(temp, 2),
        "pressure_bar": round(pressure, 2),
        "vibration_rms": round(vib, 3),
        "power_kw": round(power, 2),
        "fault_code": int(fault_code)
    }
    return payload

def main():
    client = mqtt.Client(client_id="publisher_win8_multi")
    client.username_pw_set(MQTT_USER, MQTT_PASS)

    client.tls_set()
    # If you ever get SSL errors on Win8, uncomment:
    # client.tls_insecure_set(True)

    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            for asset in ASSETS:
                topic = "site/{}/asset/{}/telemetry".format(SITE, asset)
                payload = make_payload(asset)
                client.publish(topic, json.dumps(payload))
                print("Sent:", payload)
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
