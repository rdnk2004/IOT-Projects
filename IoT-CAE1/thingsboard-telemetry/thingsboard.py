import json, os, random, time
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

load_dotenv()
client = mqtt.Client()
client.username_pw_set(os.getenv("ACCESS_TOKEN"))
client.connect(os.getenv("THINGSBOARD_BROKER", "thingsboard.cloud"), 1883)

while True:
    data = {"temperature": random.randint(25, 40)}
    client.publish("v1/devices/me/telemetry", json.dumps(data))
    print("Published to ThingsBoard:", data)
    time.sleep(5)
