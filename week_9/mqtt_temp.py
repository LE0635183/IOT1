from gpiozero import LED
import time
import paho.mqtt.client as mqtt
import json
import temperature  # Custom module for reading temperature

# Initialize LED on GPIO pin 17
red = LED(17)

# Unique client ID for MQTT communication
id = '67e6ce38-537b-414e-875f-f0cbc009ee63'
client_telemetry_topic = id + '/telemetry'  # Topic for sending temperature data
server_command_topic = id + '/commands'  # Topic for receiving commands
client_name = id + '_temperature_client'  # MQTT client name

# Initialize MQTT client
mqtt_client = mqtt.Client(client_name)

# Connect to public MQTT broker (replace with your own broker if needed)
try:
    mqtt_client.connect('test.mosquitto.org')
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
    exit(1)

# Start MQTT loop in a separate thread
mqtt_client.loop_start()

# Subscribe to command topic for LED control
mqtt_client.subscribe(server_command_topic)

print("MQTT connected and subscribed to topic!")

def handle_command(client, userdata, message):
    """Handles incoming MQTT commands and controls LED accordingly."""
    try:
        payload = json.loads(message.payload.decode())  # Decode received JSON message
        print("Received command:", payload)

        if "led_on" in payload:
            if payload["led_on"]:
                red.on()
                print("LED turned ON")
            else:
                red.off()
                print("LED turned OFF")
    except json.JSONDecodeError:
        print("Error: Received malformed JSON payload.")
    except Exception as e:
        print(f"Error handling command: {e}")

# Assign callback function to handle incoming messages
mqtt_client.on_message = handle_command 

def loop():
    """Continuously reads temperature and sends telemetry data via MQTT."""
    try:
        device_file = temperature.setup()  # Initialize temperature sensor
    except Exception as e:
        print(f"Error setting up temperature sensor: {e}")
        exit(1)

    while True:
        try:
            # Read temperature (returns a tuple: (temp_C, temp_F))
            read_temperature = temperature.read_temperature(device_file)
            temp_C = read_temperature[0]

            # Create JSON telemetry payload
            telemetry = json.dumps({'temperature': temp_C})
            print("Sending telemetry:", telemetry)

            # Publish temperature data
            mqtt_client.publish(client_telemetry_topic, telemetry)

            time.sleep(3)  # Wait before next reading
        except Exception as e:
            print(f"Error in telemetry loop: {e}")
            time.sleep(5)  # Wait before retrying to avoid excessive errors

if __name__ == '__main__':
    try:
        print("Press Ctrl+C to stop the MQTT client.")
        loop()
    except KeyboardInterrupt:
        print("\nStopping MQTT connection...")
        mqtt_client.loop_stop()  # Stop the MQTT loop
        mqtt_client.disconnect()  # Disconnect from the MQTT broker
        print("MQTT client stopped. Exiting.")
    except Exception as e:
        print(f"Unexpected error: {e}")
