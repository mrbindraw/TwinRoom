"""
room_subscriber.py
------------------

Launch:
    python room_subscriber.py
"""

import paho.mqtt.client as mqtt
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load secrets and settings from .env
load_dotenv()

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "8883"))
# '#' = wildcard, get all topics
SUBSCRIBE_TOPIC = "building/floor1/room1/#"

# Get the directory where the .exe was actually launched
if getattr(sys, 'frozen', False):
    # Running as a compiled .exe
    LAUNCH_DIR = os.path.dirname(sys.executable)
else:
    # Running as a normal .py script
    LAUNCH_DIR = os.path.dirname(os.path.abspath(__file__))
    
CA_CERT = os.path.join(LAUNCH_DIR, "certs", "ca.crt")

USERNAME = os.getenv("TWIN_USERNAME")
PASSWORD = os.getenv("TWIN_PASSWORD")

def now_str():
    return datetime.now().strftime("%H:%M:%S")


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[{now_str()}] Connected over TLS as '{USERNAME}'. Listening on {SUBSCRIBE_TOPIC}\n")
        client.subscribe(SUBSCRIBE_TOPIC, qos=1)
    else:
        print(f"[{now_str()}] Connection failed (code {rc})")


def on_message(client, userdata, msg):
    value = msg.payload.decode("utf-8")
    param = msg.topic.split("/")[-1]
    print(f"[{now_str()}] -> {param:<12} = {value:<8}  ({msg.topic})")


def main():
    if not USERNAME or not PASSWORD:
        print(f"[{now_str()}] Missing credentials. Copy .env.example to .env and set "
              f"TWIN_USERNAME / TWIN_PASSWORD.")
        sys.exit(1)
    
    if not os.path.exists(CA_CERT):
        print(f"[{now_str()}] CA certificate not found: {CA_CERT}")
        return
    
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="test-subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set(ca_certs=CA_CERT)
    
    try:
        client.connect(BROKER, PORT, keepalive=60)
    except Exception as e:
        print(f"[{now_str()}] Could not connect: {e}")
        print("   Please, check:  mosquitto -v")
        return

    print(f"[{now_str()}] Connecting to {BROKER}:{PORT} ...")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print(f"\n[{now_str()}] Stopping subscriber...")
        client.disconnect()


if __name__ == "__main__":
    main()
