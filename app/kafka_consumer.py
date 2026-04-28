import json
import os
from uuid import uuid4
from confluent_kafka import Consumer

DEFAULT_GROUP_ID = f"flask-events-consumer-{uuid4().hex}"

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": os.getenv("KAFKA_GROUP_ID", DEFAULT_GROUP_ID),
    "auto.offset.reset": "latest"
})

consumer.subscribe(["detections"])


def get_recent_events(max_messages=10):
    events = []

    for _ in range(max_messages):
        msg = consumer.poll(0.1)

        if msg is None:
            break

        if msg.error():
            continue

        event = json.loads(msg.value().decode("utf-8"))
        events.append(event)

    return events
