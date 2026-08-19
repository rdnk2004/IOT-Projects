import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
topic = "rajagiri/iot/temp"

def on_message(client, userdata, msg):
    print(f"Received from [{msg.topic}]: {msg.payload.decode()} °C")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to broker successfully! Subscribed to topic: '{topic}'")
        client.subscribe(topic)
    else:
        print(f"Failed to connect, return code {rc}")

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except AttributeError:
    client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to broker {broker}...")
client.connect(broker, 1883)
print("Listening for incoming messages (Press Ctrl+C to stop)...")
client.loop_forever()
