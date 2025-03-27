from gpiozero import LED
import time
import paho.mqtt.client as mqtt
import json
import temperature

red = LED(17)
id = '67e6ce38-537b-414e-875f-f0cbc009ee63'
client_telemetry_topic = id + '/telemetry'
client_name = id + '_temperature_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")

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
    print("Press Ctrl+C to quit")
    try:
        loop()
    except KeyboardInterrupt:
        print("\n Exiting program.")
