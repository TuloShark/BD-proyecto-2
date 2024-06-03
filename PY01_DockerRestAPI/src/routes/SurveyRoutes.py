from flask import Blueprint, request, jsonify
from src.services.SurveysServices import SurveyService
from src.services.RespondentsServices import RespondentService
import traceback
from src.utils.Logger import Logger
from src.utils.Security import Security
from src.utils.kafka_producer import send_message  # Importa el productor de Kafka

main = Blueprint('surveys_blueprint', __name__)

# Crea una nueva encuesta
@main.route("/surveys", methods=["POST"])
def surveyPost():
    survey_data = request.get_json()
    result, survey_id = SurveyService.create_survey(survey_data)
    if result:
        return jsonify({"success": True, "survey_id": str(survey_id)}), 201
    else:
        return jsonify({"success": False, "error": "Error creating survey"}), 400

@main.route('/surveys/<string:survey_id>/responses', methods=['GET'])
def get_responses(survey_id):
    responses = SurveyService.get_responses_by_survey(survey_id)
    if responses is not None:
        return jsonify({"success": True, "responses": responses}), 200
    else:
        return jsonify({"success": False, "error": "Responses not found"}), 404

# Lista todas las encuestas
@main.route("/surveys", methods=["GET"])
def surveysGet():
    surveys = SurveyService.get_all_surveys()
    return jsonify({"success": True, "surveys": surveys}), 200

# Muestra los detalles de encuesta
@main.route("/surveys/<string:survey_id>", methods=["GET"])
def surveyGet(survey_id):
    survey = SurveyService.get_survey_by_id(survey_id)
    if survey:
        return jsonify({"success": True, "survey": survey}), 200
    else:
        return jsonify({"success": False, "error": "Survey not found"}), 404

# Actualiza una encuesta 
@main.route("/surveys/<string:survey_id>", methods=["PUT"])
def surveyPut(survey_id):
    update_data = request.get_json()
    result = SurveyService.update_survey(survey_id, update_data)
    if result:
        return jsonify({"success": True, "updated": True}), 200
    else:
        return jsonify({"success": False, "error": "Error updating survey"}), 400

# Elimina una encuesta
@main.route("/surveys/<string:survey_id>", methods=["DELETE"])
def surveyDelete(survey_id):
    result = SurveyService.delete_survey(survey_id)
    if result:
        return jsonify({"success": True, "deleted": True}), 200
    else:
        return jsonify({"success": False, "error": "Error deleting survey"}), 400

# Publica una encuesta
@main.route("/surveys/<string:survey_id>/publish", methods=["POST"])
def surveyPublish(survey_id):
    result = SurveyService.publish_survey(survey_id)
    if result:
        return jsonify({"success": True, "published": True}), 200
    else:
        return jsonify({"success": False, "error": "Error publishing survey"}), 400

@main.route('/surveys/<string:responses_id>/responses', methods=['POST'])
def responsesPost(responses_id):
    try:
        responses_data = request.get_json()
        data = SurveyService.post_responses_user(responses_data, responses_id)
        return jsonify({'success': True, 'Data':data})
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())

@main.route("/surveys/analysis/<string:survey_id>", methods=["GET"])
def analysisGet(survey_id):
    token = request.get_json()
    info = Security.verify_token(token)
    analysis = False
    if info != False:
        analysis = SurveyService.get_analysis(survey_id)
    if analysis:
        return jsonify({"success": True, "Analysis": analysis}), 200
    else:
        return jsonify({"success": False, "error": "Question not found"}), 404

# Nuevas rutas para la edición colaborativa
@main.route('/surveys/<string:id>/edit/start', methods=['POST'])
def start_edit_session(id):
    message = {'survey_id': id, 'action': 'start_edit'}
    send_message('edit_topic', message)
    return jsonify({'status': 'edit session started'}), 200

@main.route('/surveys/<string:id>/edit/submit', methods=['POST'])
def submit_edit(id):
    changes = request.json
    message = {'survey_id': id, 'action': 'submit_edit', 'changes': changes}
    send_message('edit_topic', message)
    return jsonify({'status': 'changes submitted'}), 200

@main.route('/surveys/<string:id>/edit/status', methods=['GET'])
def edit_status(id):
    return jsonify({'status': 'edit in progress'}), 200
