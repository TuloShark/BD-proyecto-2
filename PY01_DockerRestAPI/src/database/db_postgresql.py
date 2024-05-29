### Importaciones
import psycopg2
import os
from src.utils.Logger import Logger
import traceback

### Funcion para realizar la conexion
def get_connection() -> None:
    try:
        return psycopg2.connect(database=os.getenv('DATABASE_NAME'),
                                host=os.getenv('DATABASE_HOST'),
                                user=os.getenv('DATABASE_USER'),
                                password=os.getenv('DATABASE_PASSWORD'),
                                port=os.getenv('DATABASE_PORT'))
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return None