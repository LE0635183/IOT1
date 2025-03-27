from gpiozero import LED
import time
import random
import paho.mqtt.client as mqtt

red = LED(17)
id = '67e6ce38-537b-414e-875f-f0cbc009ee63'
client_name = id + 'temperature_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")

while True:
    temperature = random.randrange(23,27)
    print('Light level:', temperature)

    if temperature > 24:
        red.on()
    else:
        red.off()
    
    time.sleep(3)