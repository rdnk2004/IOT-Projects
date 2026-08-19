import random
import time
import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
topic = "rajagiri/iot/temp"

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except AttributeError:
    client = mqtt.Client()

print(f"Connecting to MQTT broker '{broker}'...")
client.connect(broker, 1883)
client.loop_start()
print(f"Connected! Publishing temperature telemetry to topic '{topic}'...")

try:
    while True:
        temp = random.randint(25, 40)
        client.publish(topic, str(temp))
        print(f"Published telemetry to [{topic}]: {temp} °C")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nStopping publisher gracefully...")
    client.loop_stop()
    client.disconnect()
    print("Disconnected.")
