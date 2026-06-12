"""
room_publisher.py
-----------------
Publishes the full room state as a single JSON message:

    building/floor1/room1/state -> {"temperature": 23.4, "occupancy": true, "lamp": true, "timestamp": "..."}

Launch:
    1) mosquitto -c mosquitto.conf -v
    2) python room_publisher.py
"""

import paho.mqtt.client as mqtt
import json
import random
import time
import math
import os
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load secrets and settings from .env into environment variables
load_dotenv()

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "8883"))
STATE_TOPIC = "building/floor1/room1/state"
PUBLISH_INTERVAL = 2.0 # sec
CA_CERT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs", "ca.crt")

USERNAME = os.getenv("SENSOR_USERNAME")
PASSWORD = os.getenv("SENSOR_PASSWORD")

last = {"temperature": None, "occupancy": None, "lamp": None}

# lamp logic: stays on while the room is occupied, and then LAMP_TIMEOUT seconds after
LAMP_TIMEOUT = 20.0
last_occupied_time = 0.0


def now_str():
    return datetime.now().strftime("%H:%M:%S")


def log_change(param, old, new):
    ts = now_str()
    if param == "temperature":
        print(f"[{ts}] Temperature: {old}°C → {new}°C")
    elif param == "occupancy":
        status = "OCCUPIED" if new else "EMPTY"
        print(f"[{ts}] Occupancy:   {status}")
    elif param == "lamp":
        extra = "" if new else "  (timeout after empty)"
        print(f"[{ts}] Lamp:        {('OFF' if old else 'ON')} → {('ON' if new else 'OFF')}{extra}")


# ---- Callbacks ----
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[{now_str()}] Connected over TLS as '{USERNAME}' to {BROKER}:{PORT}")
        print(f"[{now_str()}] Publishing JSON to: {STATE_TOPIC} every {PUBLISH_INTERVAL}s\n")
    else:
        print(f"[{now_str()}] Connection failed (code {rc})")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties=None):
    print(f"[{now_str()}] Disconnected from broker (code {reason_code})")


def main():
    # Fail early with a clear message if secrets or certs are missing
    if not USERNAME or not PASSWORD:
        print(f"[{now_str()}] Missing credentials. Copy .env.example to .env and set "
              f"SENSOR_USERNAME / SENSOR_PASSWORD.")
        sys.exit(1)

    if not os.path.exists(CA_CERT):
        print(f"[{now_str()}] CA certificate not found: {CA_CERT}")
        return

    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="room1-sensor-sim")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set(ca_certs=CA_CERT)

    try:
        client.connect(BROKER, PORT, keepalive=60)
    except Exception as e:
        print(f"[{now_str()}] Could not connect to broker: {e}")
        print("Please, check:  mosquitto -c mosquitto.conf -v")
        return

    client.loop_start()
    start = time.time()
    global last_occupied_time

    try:
        while True:
            t = time.time() - start

            temperature = round(22 + 2 * math.sin(t / 30) + random.uniform(-0.2, 0.2), 1)
            occupancy = (int(t / 10) % 2 == 0) # switches every 10 sec

            if occupancy:
                last_occupied_time = t
                lamp = True
            else:
                # the lamp is still on for LAMP_TIMEOUT seconds after release
                lamp = (t - last_occupied_time) < LAMP_TIMEOUT

            state = {
                "temperature": temperature,
                "occupancy": occupancy,
                "lamp": lamp,
                "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
            client.publish(STATE_TOPIC, json.dumps(state), qos=1, retain=True)

            # --- print logs ---
            if last["temperature"] is not None and abs(temperature - last["temperature"]) > 0.2:
                log_change("temperature", last["temperature"], temperature)
            if last["occupancy"] is not None and occupancy != last["occupancy"]:
                log_change("occupancy", last["occupancy"], occupancy)
            if last["lamp"] is not None and lamp != last["lamp"]:
                log_change("lamp", last["lamp"], lamp)

            last["temperature"] = temperature
            last["occupancy"] = occupancy
            last["lamp"] = lamp

            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print(f"\n[{now_str()}] Stopping publisher...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
