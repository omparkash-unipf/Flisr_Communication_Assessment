import random
import threading

import paho.mqtt.client as mqtt

# ==================================================
# CONFIGURATION: CHANGE THESE VALUES FOR YOUR TESTS
# ==================================================

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883

INPUT_TOPIC = "flisr/measurements/raw"
OUTPUT_TOPIC = "flisr/measurements/delivered"

LATENCY_MS = 10000
JITTER_MS = 2000
PACKET_LOSS_PERCENT = 0

# ==================================================
# STATISTICS
# ==================================================

received_count = 0
dropped_count = 0
forwarded_count = 0

stats_lock = threading.Lock()


def forward_message(client, payload, delay_ms):
    """Publish a message after its simulated communication delay."""
    global forwarded_count

    try:
        result = client.publish(
            OUTPUT_TOPIC,
            payload=payload,
            qos=0
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            with stats_lock:
                forwarded_count += 1

            print(
                f"[FORWARDED] Delay={delay_ms:.1f} ms | "
                f"Total forwarded={forwarded_count}"
            )
        else:
            print(f"[PUBLISH ERROR] MQTT result code: {result.rc}")

    except Exception as error:
        print(f"[FORWARD ERROR] {error}")


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to broker: {reason_code}")

    client.subscribe(INPUT_TOPIC, qos=0)

    print(f"Listening on: {INPUT_TOPIC}")
    print(f"Forwarding to: {OUTPUT_TOPIC}")
    print(f"Configured latency: {LATENCY_MS} ms")
    print(f"Configured jitter: +/- {JITTER_MS} ms")
    print(f"Packet loss: {PACKET_LOSS_PERCENT}%")


def on_message(client, userdata, message):
    global received_count, dropped_count

    with stats_lock:
        received_count += 1
        current_number = received_count

    payload = message.payload

    print(f"\n[RECEIVED] Message #{current_number}")

    # 1. Simulate application-level message loss
    if random.random() < PACKET_LOSS_PERCENT / 100.0:
        with stats_lock:
            dropped_count += 1
            current_dropped = dropped_count

        print(
            f"[DROPPED] Message #{current_number} "
            f"| Total dropped={current_dropped}"
        )
        return

    # 2. Add fixed latency and random jitter
    jitter = random.uniform(-JITTER_MS, JITTER_MS)
    delay_ms = max(0.0, LATENCY_MS + jitter)

    # 3. Schedule delivery without blocking MQTT reception
    timer = threading.Timer(
        delay_ms / 1000.0,
        forward_message,
        args=(client, payload, delay_ms)
    )
    timer.daemon = True
    timer.start()


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="flisr_communication_layer"
)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    print("Communication layer starting...")
    client.loop_forever()

except KeyboardInterrupt:
    print("\nCommunication layer stopped.")

finally:
    client.disconnect()
