from src.database.db_mongodb import get_mongo_connection
from bson import ObjectId
import traceback
import pymongo
import psycopg2
# Database
db = get_mongo_connection()
# Logger
from src.utils.Logger import Logger


class SurveyService():

    @classmethod
    def create_survey(cls, survey_data):
        try:
            db = get_mongo_connection()
            conecction = db['surveys']
            result = conecction.insert_one(survey_data)
            return True, result.inserted_id
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return False, None
    
    def get_responses_by_survey(cls, survey_id):
        try:
            db = get_mongo_connection()
            connection = db['responses']
            responses = list(connection.find({"idSurvey": ObjectId(survey_id)}))
            for response in responses:
                response['_id'] = str(response['_id'])
                response['idSurvey'] = str(response['idSurvey'])
            return responses
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def get_all_surveys(cls):
        try:
            db = get_mongo_connection()
            conecction = db['surveys']
            surveys = list(conecction.find({}, {'_id': 1, 'title': 1, 'description': 1}))
            for survey in surveys:
                survey['_id'] = str(survey['_id'])
            return surveys
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def get_survey_by_id(cls, survey_id):
        try:
            db = get_mongo_connection()
            conecction = db['surveys']
            survey = conecction.find_one({"_id": ObjectId(survey_id)})
            if survey:
                survey['_id'] = str(survey['_id'])
            return survey
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def post_responses_user(cls, responses_data, responses_id):
        try:
            db = get_mongo_connection()
            connection = db['responses']
            result = connection.update_one(
                {"_id": ObjectId(responses_id)},
                {"$set": {"responses": responses_data}}
            )
            return result.modified_count
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def post_responses(cls, responses_data, id):
        try:
            data = {
                "surveyId": ObjectId(id),
                "responses": responses_data,
                "userId": None
            }
            conecction = db['responses']
            result = conecction.insert_one(data).inserted_id
            return result
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def update_survey(cls, survey_id, update_data):
        try:
            db = get_mongo_connection()
            conecction = db['surveys']
            result = conecction.update_one(
                {"_id": ObjectId(survey_id)},
                {"$set": update_data}
            )
            return result.matched_count > 0
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return False

    @classmethod
    def delete_survey(cls, survey_id):
        try:
            db = get_mongo_connection()
            conection = db['surveys']
            result = conection.delete_one({"_id": ObjectId(survey_id)})
            return result.deleted_count > 0
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return False

    @classmethod
    def publish_survey(cls, survey_id):
        try:
            db = get_mongo_connection()
            conection = db['surveys']
            result = conection.update_one(
                {"_id": ObjectId(survey_id)},
                {"$set": {"is_published": True}}
            )
            return result.modified_count > 0
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return False
    
    @classmethod
    def get_responses_by_survey(cls, survey_id):
        try:
            db = get_mongo_connection()
            connection = db['responses']
            responses = list(connection.find({"idSurvey": ObjectId(survey_id)}))
            for response in responses:
                response['_id'] = str(response['_id'])
                response['idSurvey'] = str(response['idSurvey'])
            return responses
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def get_analysis(cls,survey_id):
        try:
            db = get_mongo_connection()
            conecction = db['responses']
            query = {'idSurvey': ObjectId(survey_id)}
            results = conecction.find(query)
            conteo_respuestas_por_pregunta = {}
            for result in results:
                for response in result["responses"].values():
                    id_pregunta = response["Id_pregunta"]
                    if id_pregunta in conteo_respuestas_por_pregunta:
                        conteo_respuestas_por_pregunta[id_pregunta] += 1
                    else:
                        conteo_respuestas_por_pregunta[id_pregunta] = 1

            return conteo_respuestas_por_pregunta
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None
    