import json
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883
TOPIC = "flisr/measurements/raw"

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="flisr_publisher"
)

client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_start()

try:
    while True:
        # Generate illustrative measurements
        voltage_kv = round(random.uniform(19.0, 21.0), 3)
        current_a = round(random.uniform(50.0, 300.0), 2)

        message = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "device_id": "RTU_DSA1",
            "voltage_kv": voltage_kv,
            "current_a": current_a
        }

        payload = json.dumps(message)

        info = client.publish(TOPIC, payload, qos=0)
        info.wait_for_publish()

        print(f"Published: {payload}")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nPublisher stopped.")

finally:
    client.loop_stop()
    client.disconnect()
