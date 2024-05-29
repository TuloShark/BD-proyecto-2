import os
import redis
import traceback
from src.utils.Logger import Logger

def get_connection() -> None:
    try:
        redis_connection = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            decode_responses=True  # Para decodificar automáticamente las respuestas a cadenas
        )
        return redis_connection
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return None