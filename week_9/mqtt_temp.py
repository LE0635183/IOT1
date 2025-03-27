from gpiozero import LED
import time
import random
import paho.mqtt.client as mqtt
import json
from temperature import read_temperature, setup

red = LED(17)
id = '67e6ce38-537b-414e-875f-f0cbc009ee63'
client_telemetry_topic = id + '/telemetry'
client_name = id + '_temperature_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")

while True:
    
    
    temperature = read_temperature(setup) #replace with actual readings from your sensor
    
    
    telemetry = json.dumps({'temperature' : temperature})
    print("Sending telemetry ", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    time.sleep(5)
