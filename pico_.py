import network
import time
from umqtt.simple import MQTTClient
from machine import Pin

# Replace with your Wi-Fi credentials
ssid = "Sambit's S23 Ultra"
password = "22082002"

# MQTT broker information
broker_address = "broker.hivemq.com"  # Public broker
broker_port = 1883  # Default MQTT port
client_id = "pico_mqtt_client"  # Unique ID for the Pico client
topic = b"chat/messages"  # Topic to subscribe to (must be bytes)

# Define GPIO pins for lights
led = Pin(15, Pin.OUT)  # LED light on pin 15
rgb_red = Pin(16, Pin.OUT)  # Red on pin 16
rgb_green = Pin(17, Pin.OUT)  # Green on pin 17
rgb_blue = Pin(18, Pin.OUT)  # Blue on pin 18

# Function to connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        print('Waiting for connection...')
        time.sleep(1)
    
    print('Connected to Wi-Fi', wlan.ifconfig())

# Function to control RGB light
def control_rgb(state):
    if state == "on":
        rgb_red.value(1)  # Turn on Red
        rgb_green.value(1)  # Turn on Green
        rgb_blue.value(1)  # Turn on Blue
    elif state == "off":
        rgb_red.value(0)  # Turn off Red
        rgb_green.value(0)  # Turn off Green
        rgb_blue.value(0)  # Turn off Blue

# Function to control LED light
def control_led(state):
    if state == "on":
        led.value(1)  # Turn on LED
    elif state == "off":
        led.value(0)  # Turn off LED

# Callback function to handle received messages
def on_message(topic, msg):
    message = msg.decode('utf-8')
    print(f"Received message: {message}")
    
    r = message.split(",")
    p1 = r[0]
    p2 = r[1]
    
    if p1 == "1":
        if p2 == "Disco on":
            control_rgb("on")  # Turn on RGB light
            print("Disco On")
        elif p2 == "Disco off":
            control_rgb("off")  # Turn off RGB light
            print("Disco off")
        # elif message == "Bulb on":
        #     control_led("on")  # Turn on LED light
        #     print("Bulb On")
        # elif message == "Bulb off":
        #     control_led("off")  # Turn off LED light
        #     print("Bulb off")
    elif p1 == "2":
        # if message == "Disco on":
        #     control_rgb("on")  # Turn on RGB light
        #     print("Disco On")
        # elif message == "Disco off":
        #     control_rgb("off")  # Turn off RGB light
        #     print("Disco off")
        if p2 == "Bulb on":
            control_led("on")  # Turn on LED light
            print("Bulb On")
        elif p2 == "Bulb off":
            control_led("off")  # Turn off LED light
            print("Bulb off")

# Connect to Wi-Fi
connect_to_wifi()

# Create an MQTT client
client = MQTTClient(client_id, broker_address, port=broker_port)

# Set the callback function to handle incoming messages
client.set_callback(on_message)

# Connect to the MQTT broker
client.connect()
print(f"Connected to MQTT broker at {broker_address}")

# Subscribe to the topic
client.subscribe(topic)
print(f"Subscribed to topic {topic.decode()}")

try:
    while True:
        # Wait for a message and process it when it arrives
        client.wait_msg()  # Blocking call that waits for new messages

except KeyboardInterrupt:
    print("Disconnected from MQTT broker.")

finally:
    client.disconnect()
