import asyncio
from amqtt.broker import Broker


async def main():
    config = {
        "listeners": {
            "default": {
                "type": "tcp",
                "bind": "127.0.0.1:1883",
            }
        },
        "sys_interval": 10,
        "auth": {
            "allow-anonymous": True,
        },
    }

    broker = Broker(config)
    await broker.start()

    print("MQTT broker is running on 127.0.0.1:1883")
    print("Press Ctrl+C to stop the broker.")

    try:
        await asyncio.Event().wait()
    finally:
        await broker.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMQTT broker stopped.")
