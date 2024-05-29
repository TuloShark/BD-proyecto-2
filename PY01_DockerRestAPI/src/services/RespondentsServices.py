from src.database.db_mongodb import get_mongo_connection
from bson import ObjectId
import traceback
import pymongo
import psycopg2
# Database
#db = get_mongo_connection()
# Logger
from src.utils.Logger import Logger


class RespondentService():

    @classmethod
    def post_respondent(cls, respondent_data,survey_id):
        try:
            db = get_mongo_connection()
            conecction = db['responses']
            respondent_data['idSurvey'] = ObjectId(survey_id)
            result = conecction.insert_one(respondent_data)
            return result.inserted_id
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None
    """
    header: Content-Type   application/json
    http://localhost:5002/respondents/6623e6281188e02fda543222
    {
    "nombre":"Manuel",
    "correo":"m.aleandro00@gmail.com"
    }
    """
    @classmethod
    def get_respondents(cls,survey_id):
        try:
            db = get_mongo_connection()
            conecction = db['responses']
            respondents_cursor = conecction.find({'idSurvey': ObjectId(survey_id)})
            respondents = list(respondents_cursor)
            for respondent in respondents:
                respondent['_id'] = str(respondent['_id'])
                respondent['idSurvey'] = str(respondent['idSurvey'])
            return {'respondents':respondents}
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def get_respondent(cls, respondent_id):
        try:
            db = get_mongo_connection()
            conecction = db['responses']
            respondent = conecction.find_one({'_id': ObjectId(respondent_id)})
            if respondent:
                respondent['_id'] = str(respondent['_id'])
                respondent['idSurvey'] = str(respondent['idSurvey'])
            return {'respondent':respondent}
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def update_respondent(cls, update_data, respondent_id):
        try:
            db = get_mongo_connection()
            conecction = db['responses']
            nombre = update_data.get('nombre')
            correo = update_data.get('correo')

            update_fields = {}
            if nombre is not None:
                update_fields['nombre'] = nombre
            if correo is not None:
                update_fields['correo'] = correo

            existing_document = conecction.find_one({'_id': ObjectId(respondent_id)})
            combined_fields = {**existing_document, **update_fields}

            back = conecction.replace_one({'_id': ObjectId(respondent_id)}, combined_fields)
            return True
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def delete_respondent(cls, respondent_id):
        try:
            db = get_mongo_connection()
            conecction = db['responses']
            back = conecction.delete_one({'_id': ObjectId(respondent_id)})
            return back.deleted_count > 0
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None