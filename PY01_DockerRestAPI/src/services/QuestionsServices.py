from src.database.db_mongodb import get_mongo_connection
from bson import ObjectId
import traceback

db = get_mongo_connection()

from src.utils.Logger import Logger

class QuestionService:

    @classmethod
    def create_question(cls, survey_id, question_data):
        try:
            db = get_mongo_connection()
            conecction = db['questions']
            question_data['surveyId'] = ObjectId(survey_id)
            result = conecction.insert_one(question_data)
            return {'success': True, 'question_id': str(result.inserted_id)} if result.acknowledged else None
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return {'success': False, 'error': str(e)}

    @classmethod
    def get_all_questions(cls, survey_id):
        try:
            db = get_mongo_connection()
            conecction = db['questions']
            questions_cursor = conecction.find({"surveyId": ObjectId(survey_id)})
            questions = list(questions_cursor)
            for question in questions:
                question['_id'] = str(question['_id'])
                question['surveyId'] = str(question['surveyId'])
            return {'success': True, 'questions': questions}
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return {'success': False, 'error': str(e)}

    @classmethod
    def get_question_by_id(cls, question_id):
        try:
            db = get_mongo_connection()
            conecction = db['questions']
            question = conecction.find_one({"_id": ObjectId(question_id)})
            if question:
                question['_id'] = str(question['_id'])
                question['surveyId'] = str(question['surveyId'])
                return {'success': True, 'question': question}
            return {'success': False, 'error': 'Question not found'}
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return {'success': False, 'error': str(e)}

    @classmethod
    def update_question(cls, question_id, update_data):
        try:
            db = get_mongo_connection()
            conecction = db['questions']
            result = conecction.update_one({"_id": ObjectId(question_id)}, {"$set": update_data})
            return {'success': result.matched_count > 0}
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return {'success': False, 'error': str(e)}

    @classmethod
    def delete_question(cls, question_id):
        try:
            db = get_mongo_connection()
            conecction = db['questions']
            result = conecction.delete_one({"_id": ObjectId(question_id)})
            return {'success': result.deleted_count > 0}
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return {'success': False, 'error': str(e)}
