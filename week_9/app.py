import json
import time
import paho.mqtt.client as mqtt

id = '67e6ce38-537b-414e-875f-f0cbc009ee63'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + '_temperature_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    
    command = { 'led_on' : payload['temperature'] > 25 }
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))
        
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

    
try:
    print("Press Ctrl+C to stop the MQTT client.")
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    print("\nStopping MQTT Connection...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("MQTT client stopped. Exiting.")