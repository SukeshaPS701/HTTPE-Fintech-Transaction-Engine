from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    retries=5,
    acks="all"
)


def publish_transaction(event):

    try:
        producer.send("transactions", event)
        producer.flush()
    except Exception as e:
        print("Kafka publish failed:", e)
        time.sleep(1)