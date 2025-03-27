import json
import time
import paho.mqtt.client as mqtt

id = '67e6ce38-537b-414e-875f-f0cbc009ee63'
client_telemetry_topic = id + '/telemetry'
client_name = id + 'temperature_server'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry
while True:
    time.sleep(2)