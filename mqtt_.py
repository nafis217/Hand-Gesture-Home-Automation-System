import paho.mqtt.client as mqtt
import time

# MQTT broker information
broker_address = "broker.hivemq.com"  # Replace with your MQTT broker address
broker_port = 1883  # Default MQTT port
topic = "chat/messages"  # Topic for publishing messages

# Define the MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, message):
    print("Test 2:", str(message.payload.decode("utf-8")))

# Attach the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Subscribe to the topic
client.subscribe(topic)

# Start the MQTT loop
client.loop_start()

try:
    while True:
        file_path = "sample.txt"  # Replace with the path to your text file

        while True:
            try:
                with open(file_path, 'r') as file:
                    # Read the entire content of the file
                    file_content = file.read()
                    # Print the content to the console
                    if len(file_content) == 0:
                        continue
                    message = file_content
                    with open(file_path, 'w') as file:
                        pass  # Clear the file after reading
                    break
            except FileNotFoundError:
                print(f"File '{file_path}' not found.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        if message.lower() == "exit":
            break

        # Publish the message to the MQTT topic
        client.publish(topic, message)

        time.sleep(1)  # Delay for a second to allow for message handling

except KeyboardInterrupt:
    print("Disconnected from the MQTT broker.")

finally:
    # Stop the MQTT loop and disconnect
    client.loop_stop()
    client.disconnect()
