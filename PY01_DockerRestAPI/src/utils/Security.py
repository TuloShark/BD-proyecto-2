### Importaciones
from decouple import config
import datetime
import jwt
import pytz
from src.utils.Logger import Logger
from src.database.db_redis import get_connection
import traceback
import os

### Clase para manejar la seguridad de los usuarios
class Security():
    secret = os.getenv("JWT_KEY")
    tz = pytz.timezone("America/Costa_Rica")

    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=10),
            'username': authenticated_user.username,
            'idTipo': authenticated_user.idTipo,
            'id': authenticated_user.id
        }
        redis = get_connection()
        token = jwt.encode(payload,cls.secret, algorithm="HS256")
        clave_token = f"token:{token}"
        redis.setex(clave_token, 600, token)
        return token
    
    @classmethod
    def verify_token(cls, headers):
        try:
            if 'token' in headers.keys():
                encoded_token = headers['token']
                try:
                    redis = get_connection()
                    clave_token = f"token:{encoded_token}"
                    if redis.exists(clave_token):
                        payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                        return payload
                    return False
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False
            return False
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False
        
    @classmethod
    def logout(cls, headers):
        try:
            if 'token' in headers.keys():
                encoded_token = headers['token']
                try:
                    redis = get_connection()
                    clave_token = f"token:{encoded_token}"
                    redis.delete(clave_token)
                    return True
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False
            return False
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False