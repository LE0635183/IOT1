import json
import time
import paho.mqtt.client as mqtt

# Unique ID for identifying the client
id = '67e6ce38-537b-414e-875f-f0cbc009ee63'

# Define MQTT topics
client_telemetry_topic = id + '/telemetry'  # Topic where the temperature data is published
server_command_topic = id + '/commands'  # Topic to send LED control commands

# Define MQTT client name
client_name = id + '_temperature_server'

# Initialize the MQTT client
mqtt_client = mqtt.Client(client_name)

# Attempt to connect to the public MQTT broker
try:
    mqtt_client.connect('test.mosquitto.org')
    print("MQTT connected!")
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
    exit(1)

# Start MQTT loop in a separate thread to handle incoming messages
mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    """
    Callback function that handles incoming telemetry data.
    Decodes the received message, processes the temperature, and sends an LED command.
    """
    try:
        # Decode the JSON message
        payload = json.loads(message.payload.decode())
        print("Message received:", payload)

        # Check if 'temperature' exists in payload
        if 'temperature' in payload:
            # Determine LED state based on temperature
            command = {'led_on': payload['temperature'] > 25}

            # Log and publish the command
            print("Sending command:", command)
            client.publish(server_command_topic, json.dumps(command))
        else:
            print("Warning: Received telemetry data without 'temperature' field.")

    except json.JSONDecodeError:
        print("Error: Received malformed JSON payload.")
    except Exception as e:
        print(f"Error processing telemetry: {e}")

# Subscribe to the telemetry topic to receive temperature updates
mqtt_client.subscribe(client_telemetry_topic)

# Assign callback function to handle telemetry messages
mqtt_client.on_message = handle_telemetry

try:
    print("Press Ctrl+C to stop the MQTT client.")
    while True:
        time.sleep(2)  # Keep the script running and checking for new messages
except KeyboardInterrupt:
    print("\nStopping MQTT connection...")
    mqtt_client.loop_stop()  # Stop MQTT event loop
    mqtt_client.disconnect()  # Gracefully disconnect from the broker
    print("MQTT client stopped. Exiting.")
except Exception as e:
    print(f"Unexpected error: {e}")
