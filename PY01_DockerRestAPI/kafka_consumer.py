from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'survey_edit_topic',
    bootstrap_servers=['kafka-broker-1:9092'],
    auto_offset_reset='earliest',
    api_version=(0, 10, 2),
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    print(f"Received message: {message.value}")

