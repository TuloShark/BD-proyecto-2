from kafka import KafkaProducer
import json
import traceback
from src.database.db_mongodb import get_mongo_connection

class KafkaProducerSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if KafkaProducerSingleton._instance is None:
            KafkaProducerSingleton()
        return KafkaProducerSingleton._instance

    def __init__(self):
        if KafkaProducerSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.producer = KafkaProducer(
                bootstrap_servers=['kafka-broker-1:9092'],
                api_version=(0, 10, 2),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            KafkaProducerSingleton._instance = self

    def send_message(self, topic, message):
        try:
            db = get_mongo_connection()
            if db is not None:
                collection = db.chat_messages if topic == 'chat_messages' else db.survey_edit_messages
                result = collection.insert_one(message)
                message['_id'] = str(result.inserted_id)
            self.producer.send(topic, value=message)
            self.producer.flush()
        except Exception as e:
            print(f"Failed to send message: {e}")
            traceback.print_exc()