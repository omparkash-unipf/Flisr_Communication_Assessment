
import json
import paho.mqtt.client as mqtt

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883
TOPIC = "flisr/measurements/delivered"


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT broker: {reason_code}")
    client.subscribe(TOPIC)
    print(f"Subscribed to: {TOPIC}")


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))

        print("\n--- Received Measurement ---")
        print(f"Timestamp : {data['timestamp']}")
        print(f"Device    : {data['device_id']}")
        print(f"Voltage   : {data['voltage_kv']} kV")
        print(f"Current   : {data['current_a']} A")

    except (json.JSONDecodeError, KeyError) as error:
        print(f"Invalid measurement message: {error}")


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="flisr_subscriber"
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

print("Waiting for measurements...")
client.loop_forever()
