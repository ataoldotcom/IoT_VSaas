
import json
from datetime import datetime
from confluent_kafka import Producer

producer = Producer({
    "bootstrap.servers": "localhost:9092"
})

TOPIC = "detections"


def send_event(confidence):
    event = {
        "event_type": "dog_detected",
        "confidence": confidence,
        "timestamp": datetime.utcnow().isoformat(),
        "source": "webcam_1"
    }

    producer.produce(
        TOPIC,
        value=json.dumps(event).encode("utf-8")
    )
    producer.flush()