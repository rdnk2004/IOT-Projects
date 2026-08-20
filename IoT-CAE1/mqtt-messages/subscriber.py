import paho.mqtt.client as mqtt
def on_message(client, userdata, msg):
    print(f"Received: {msg.payload.decode()}")
client = mqtt.Client()
client.on_message = on_message
client.connect("broker.hivemq.com", 1883)
client.subscribe("rajagiri/iot/chat")
print("Waiting for messages...")
client.loop_forever()
