import traceback
import psycopg2
# Database
from src.database.db_postgresql import get_connection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.UserModel import User


class UserService():

    @classmethod
    def get_users(cls):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM GeneralUser;")
                data = cursor.fetchall()
            connection.close()
            return data
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def get_user(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM GeneralUser where id = {id};")
                data = cursor.fetchall()
            connection.close()
            return data
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def update_user(self, user_data, id, info):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE GeneralUser SET username = '{user_data['username']}',\
                                password = '{user_data['password']}' WHERE id = {id} AND\
                                (id = {info['id']} OR 1 = {info['idTipo']});")
                data = cursor.rowcount
            connection.commit()
            connection.close()
            return data
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def delete_user(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM GeneralUser WHERE id = {id};")
                data = cursor.rowcount
            connection.commit()
            connection.close()
            return data
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None