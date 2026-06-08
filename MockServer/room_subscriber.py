"""
room_subscriber.py
------------------

Launch:
    python room_subscriber.py
"""

import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
PORT = 1883
# '#' = wildcard, get all topics
SUBSCRIBE_TOPIC = "building/floor1/room1/#"


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
    client = mqtt.Client(client_id="test-subscriber")
    client.on_connect = on_connect
    client.on_message = on_message

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
