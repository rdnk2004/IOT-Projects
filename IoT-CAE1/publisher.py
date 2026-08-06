import random
import time
# pyrefly: ignore [missing-import]
import paho.mqtt.client as mqtt
broker = "broker.hivemq.com"
topic = "rajagiri/iot/temp"
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except AttributeError:
    client = mqtt.Client()
client.connect(broker, 1883)
client.loop_start()
print(f"Connecting to {broker} and publishing to topic '{topic}'...")
try:
    while True:
        temp = random.randint(25, 40)
        client.publish(topic, str(temp))
        print("Published:", temp)
        time.sleep(3)
except KeyboardInterrupt:
    print("\nStopping publisher...")
    client.loop_stop()
    client.disconnect()
