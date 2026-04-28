
import json
import os
from datetime import datetime, timezone
from confluent_kafka import Producer

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
# Checking which host
print("Kafka bootstrap:", bootstrap_servers)
if not os.path.exists("/.dockerenv") and bootstrap_servers.startswith("host.docker.internal"):
    bootstrap_servers = bootstrap_servers.replace("host.docker.internal", "localhost", 1)

producer = Producer({
    "bootstrap.servers": bootstrap_servers
})

TOPIC = os.getenv("KAFKA_TOPIC", "detections")
SOURCE = os.getenv("KAFKA_SOURCE", "webcam_1")


def send_event(confidence):
    event = {
        "event_type": "dog_detected",
        "confidence": confidence,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": SOURCE
    }

    producer.produce(
        TOPIC,
        value=json.dumps(event).encode("utf-8")
    )
    producer.poll(0)
