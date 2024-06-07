from kafka import KafkaConsumer
import json
import threading
from src.database.db_mongodb import get_mongo_connection

def consume_messages():
    consumer = KafkaConsumer(
        'survey_edit_topic',
        bootstrap_servers=['kafka-broker-1:9092'],
        auto_offset_reset='earliest',
        api_version=(0, 10, 2),
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    db = get_mongo_connection()
    survey_edit_collection = db.survey_edit_messages  # Definimos la colección donde se almacenarán los mensajes de edición de encuestas
    chat_messages_collection = db.chat_messages  # Definimos la colección donde se almacenarán los mensajes de chat

    for message in consumer:
        print(f"Received message: {message.value}")
        if message.topic == 'survey_edit_topic':
            survey_edit_collection.insert_one(message.value)  # Guardamos el mensaje en la base de datos MongoDB
        elif message.topic == 'chat_messages':
            chat_messages_collection.insert_one(message.value)  # Guardamos el mensaje en la base de datos MongoDB

def start_consumer():
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()

if __name__ == "__main__":
    start_consumer()
