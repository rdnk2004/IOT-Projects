import json
import random
import time
# pyrefly: ignore [missing-import]
import paho.mqtt.client as mqtt
broker = "eu.thingsboard.cloud"
access_token = "BAxxM7DR25d2YBwFYD5b"
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except AttributeError:
    client = mqtt.Client()
client.username_pw_set(access_token)
client.connect(broker, 1883)
client.loop_start()
while True:
    temp = random.randint(25, 40)
    payload = {"temperature": temp}
    client.publish("v1/devices/me/telemetry", json.dumps(payload))
    print("Published to ThingsBoard:", payload)
    time.sleep(5)
