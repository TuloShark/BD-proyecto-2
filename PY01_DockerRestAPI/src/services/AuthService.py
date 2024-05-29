### Importaciones
import traceback
from src.database.db_postgresql import get_connection
from src.utils.Logger import Logger
from src.models.UserModel import User

### Clase para los servicios de la ruta auth
class AuthService():

    @classmethod
    def login_user(cls, user):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM GeneralUser AS U\
                                    WHERE U.username = '{user['username']}'\
                                    AND U.password = '{user['password']}';")
                data = cursor.fetchone()
                if data != None:
                    authenticated_user = User(int(data[0]), data[1], data[2], int(data[3]))
                else:
                    authenticated_user = None
            connection.close()
            return authenticated_user
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def register_user(cls, user):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT 1 FROM GeneralUser\
                                    WHERE username = '{user['username']}'\
                                    AND password = '{user['password']}';")
                existing_user = cursor.fetchall()
                if existing_user == []:
                    cursor.execute(f"INSERT INTO GeneralUser (username, password, idTipo)\
                                        VALUES ('{user['username']}',\
                                                '{user['password']}',\
                                                {user['idTipo']});")
                    data = cursor.rowcount
                else:
                    data = 0
            connection.commit()
            connection.close()
            return data
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return 0