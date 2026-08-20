import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("broker.hivemq.com", 1883)
while True:
    msg = input("Enter message: ")
    client.publish("rajagiri/iot/chat", msg)
