from database.db_mongodb import get_mongo_connection
from bson import ObjectId

db = get_mongo_connection()

class Survey:
    def __init__(self, title, description, questions=None):
        self.title = title
        self.description = description
        self.questions = questions or []

    def save(self):
        survey_data = {
            "title": self.title,
            "description": self.description,
            "questions": self.questions
        }
        result = db.surveys.insert_one(survey_data)
        return db.surveys.find_one({'_id': result.inserted_id}) if result.acknowledged else None

    @staticmethod
    def get_all_surveys():
        surveys = list(db.surveys.find({}, {'_id': 1, 'title': 1, 'description': 1}))
        return [{'id': str(survey['_id']), 'title': survey['title'], 'description': survey['description']} for survey in surveys]

    @staticmethod
    def find_survey(survey_id):
        return db.surveys.find_one({"_id": ObjectId(survey_id)})

    @staticmethod
    def update_survey(survey_id, update_data):
        return db.surveys.update_one({"_id": ObjectId(survey_id)}, {"$set": update_data})

    @staticmethod
    def delete_survey(survey_id):
        return db.surveys.delete_one({"_id": ObjectId(survey_id)})
