from flask import Blueprint, request, jsonify
from src.services.QuestionsServices import QuestionService
from src.services.RespondentsServices import RespondentService
from src.utils.Logger import Logger

main = Blueprint('main', __name__)

@main.route("/surveys/<string:survey_id>/questions", methods=["POST"])
def post_question(survey_id):
    question_data = request.get_json()
    result = QuestionService.create_question(survey_id, question_data)
    if result.get('success'):
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@main.route("/surveys/<string:survey_id>/questions", methods=["GET"])
def get_questions(survey_id):
    result = QuestionService.get_all_questions(survey_id)
    return jsonify(result), 200 if result.get('success') else 400

@main.route("/surveys/<string:survey_id>/questions/<string:question_id>", methods=["PUT"])
def update_question(survey_id, question_id):
    update_data = request.get_json()
    result = QuestionService.update_question(question_id, update_data)
    return jsonify(result), 200 if result.get('success') else 400

@main.route("/surveys/<string:survey_id>/questions/<string:question_id>", methods=["DELETE"])
def delete_question(survey_id, question_id):
    result = QuestionService.delete_question(question_id)
    return jsonify(result), 200 if result.get('success') else 400
