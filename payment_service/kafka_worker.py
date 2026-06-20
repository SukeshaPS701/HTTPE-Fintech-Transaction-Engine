from kafka import KafkaConsumer
import json
import time

print("Starting Kafka Worker...")

consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

for msg in consumer:

    event = msg.value

    print("\n[EVENT RECEIVED]")
    print(event)

    # Simulate async processing
    if event["event"] == "TRANSFER_COMPLETED":
        print(f"Processing transaction audit: {event}")
        time.sleep(0.5)