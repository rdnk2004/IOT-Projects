import random
import time
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("broker.hivemq.com", 1883)
while True:
    temp = random.randint(25, 40)
    client.publish("rajagiri/iot/temp", temp)
    print(f"Published: {temp} °C")
    time.sleep(3)
