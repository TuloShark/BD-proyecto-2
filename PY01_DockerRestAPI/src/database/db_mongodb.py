from pymongo import MongoClient
from decouple import config
from src.utils.Logger import Logger
import traceback
import os

def get_mongo_connection():
    try:
        client = MongoClient(os.getenv('MONGO_DATABASE_HOST'), int(os.getenv('MONGO_DATABASE_PORT', 27017)),
                            username= os.getenv('MONGO_INITDB_ROOT_USERNAME'), password = os.getenv('MONGO_INITDB_ROOT_PASSWORD'))
        db = client[os.getenv('MONGO_DATABASE_NAME')]
        return db
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return None
