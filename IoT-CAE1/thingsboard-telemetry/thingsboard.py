import json
import os
import random
import time
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
load_dotenv()
broker = os.getenv("THINGSBOARD_BROKER", "thingsboard.cloud")
access_token = os.getenv("ACCESS_TOKEN")
if not access_token:
    print("Error: ACCESS_TOKEN not found in environment variables.")
    print("Please create a .env file with ACCESS_TOKEN=your-device-access-token")
    exit(1)
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except AttributeError:
    client = mqtt.Client()
client.username_pw_set(access_token)
print(f"Connecting to ThingsBoard Broker '{broker}'...")
client.connect(broker, 1883)
client.loop_start()
print("Connected! Streaming live telemetry to ThingsBoard Cloud...")
try:
    while True:
        temp = random.randint(25, 40)
        payload = {"temperature": temp}
        client.publish("v1/devices/me/telemetry", json.dumps(payload))
        print("Published to ThingsBoard telemetry stream:", payload)
        time.sleep(5)
except KeyboardInterrupt:
    print("\nStopping ThingsBoard telemetry streamer...")
    client.loop_stop()
    client.disconnect()
    print("Disconnected.")
