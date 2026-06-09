"""
room_subscriber.py
------------------

Launch:
    python room_subscriber.py
"""

import paho.mqtt.client as mqtt
import os
from datetime import datetime

BROKER = "localhost"
PORT = 8883
# '#' = wildcard, get all topics
SUBSCRIBE_TOPIC = "building/floor1/room1/#"
CA_CERT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs", "ca.crt")


def now_str():
    return datetime.now().strftime("%H:%M:%S")


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[{now_str()}] Connected. Listening on: {SUBSCRIBE_TOPIC}\n")
        client.subscribe(SUBSCRIBE_TOPIC, qos=1)
    else:
        print(f"[{now_str()}] Connection failed (code {rc})")


def on_message(client, userdata, msg):
    value = msg.payload.decode("utf-8")
    param = msg.topic.split("/")[-1]
    print(f"[{now_str()}] -> {param:<12} = {value:<8}  ({msg.topic})")


def main():
    if not os.path.exists(CA_CERT):
        print(f"[{now_str()}] CA certificate not found: {CA_CERT}")
        return
    
    client = mqtt.Client(client_id="test-subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
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
