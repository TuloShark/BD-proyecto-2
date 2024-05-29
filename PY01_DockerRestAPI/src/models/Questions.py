from src.database.db_mongodb import get_mongo_connection
from bson import ObjectId

db = get_mongo_connection()

class Question:
    def __init__(self, survey_id, question_data):
        self.survey_id = ObjectId(survey_id)
        self.text = question_data['text']
        self.question_type = question_data['type']
        
        if self.question_type == 'open':
            self.response_format = 'text'
        elif self.question_type in ['single_choice', 'multiple_choice']:
            self.options = question_data.get('options', [])  # Debe ser una lista de opciones
        elif self.question_type == 'rating_scale':
            self.scale_min = question_data.get('scale_min', 1)
            self.scale_max = question_data.get('scale_max', 5)
        elif self.question_type == 'yes_no':
            self.response_format = 'boolean'
        elif self.question_type == 'numeric':
            self.response_format = 'number'
        else:
            raise ValueError('Unsupported question type')


    def save(self):
        # Crear un documento con la estructura correspondiente al tipo de pregunta
        question_document = {
            "surveyId": self.survey_id,
            "text": self.text,
            "type": self.question_type,
        }
        
        # Agregar al documento los campos específicos del tipo de pregunta
        if hasattr(self, 'options'):
            question_document['options'] = self.options
        if hasattr(self, 'scale_min') and hasattr(self, 'scale_max'):
            question_document['scale'] = {
                'min': self.scale_min,
                'max': self.scale_max
            }
        if hasattr(self, 'response_format'):
            question_document['response_format'] = self.response_format
        
        result = db.questions.insert_one(question_document)
        return str(result.inserted_id) if result.acknowledged else None

    @staticmethod
    def get_questions_for_survey(survey_id):
        questions = list(db.questions.find({"surveyId": ObjectId(survey_id)}, {'_id': 1, 'text': 1, 'type': 1, 'options': 1}))
        return [{'id': str(question['_id']), 'text': question['text'], 'type': question['type'], 'options': question['options']} for question in questions]

    @staticmethod
    def find_question(question_id):
        return db.questions.find_one({"_id": ObjectId(question_id)})

    @staticmethod
    def update_question(question_id, update_data):
        return db.questions.update_one({"_id": ObjectId(question_id)}, {"$set": update_data})

    @staticmethod
    def delete_question(question_id):
        return db.questions.delete_one({"_id": ObjectId(question_id)})
