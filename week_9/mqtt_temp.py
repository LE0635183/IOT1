from gpiozero import LED
import time
import paho.mqtt.client as mqtt
import json
import temperature

red = LED(17)
id = '67e6ce38-537b-414e-875f-f0cbc009ee63'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + '_temperature_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

mqtt_client.subscribe(server_command_topic)

print("MQTT connected!")

def handle_command(client, userdata, message):
    """Handles incoming MQTT commands."""
    payload = json.loads(message.payload.decode())
    print("Received command:", payload)

    if "led_on" in payload:
        if payload["led_on"]:
            red.on()
            print("LED turned ON")
        else:
            red.off()
            print("LED turned OFF")

mqtt_client.on_message = handle_command 

def loop():
    while True:
        device_file = temperature.setup()  
        read_temperature = temperature.read_temperature(device_file) #replace with actual readings from your sensor
        temp_C= read_temperature[0]
        
        telemetry = json.dumps({'temperature' : temp_C})
        print("Sending telemetry ", telemetry)
        mqtt_client.publish(client_telemetry_topic, telemetry) 
        time.sleep(3)

if __name__ == '__main__':
    try:
        print("Press Ctrl+C to stop the MQTT client.")
        loop()
    except KeyboardInterrupt:
        print("\nStopping MQTT connection...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("MQTT client stopped. Exiting.")