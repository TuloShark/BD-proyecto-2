from flask import Blueprint, request, jsonify

import traceback

# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.RespondentsServices import RespondentService

main = Blueprint('respondents_blueprint', __name__)

@main.route('/<string:survey_id>', methods=['POST'])
def respondentsPost(survey_id):
    try:
        respondent_data = request.get_json()
        data = RespondentService.post_respondent(respondent_data,survey_id)
        print(data)
        if data:
            return jsonify({"success": True, "respondent_id": str(data)}), 201
        else:
            return jsonify({"success": False, "error": "Error creating respondent"}), 400
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())

@main.route('/all/<string:survey_id>', methods=['GET'])
def respondents(survey_id):
    try:
        token = request.get_json()
        info = Security.verify_token(token)
        data = False
        if info != False:
            if info['idTipo'] == 1:
                data = RespondentService.get_respondents(survey_id)
        if data:
            return jsonify({"success": True, "respondents": data}), 200
        else:
            return jsonify({"success": False, "error": "respondents not found"}), 404
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())


@main.route('/<string:respondent_id>', methods=['GET'])
def respondent(respondent_id):
    try:
        token = request.get_json()
        info = Security.verify_token(token)
        data = False
        if info != False:
            if info['idTipo'] == 1:
                data = RespondentService.get_respondent(respondent_id)
        if data:
            return jsonify({"success": True, "respondents": data}), 200
        else:
            return jsonify({"success": False, "error": "respondent not found"}), 404
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())

@main.route('/<string:respondent_id>', methods=['PUT'])
def respondentsPut(respondent_id):
    try:
        token = request.get_json()
        info = Security.verify_token(token)
        data = False
        if info != False:
            if info['idTipo'] == 1:
                update_data = {'nombre':'', 'correo': ''}
                update_data['nombre'] = token['nombre']
                update_data['correo'] = token['correo']
                data = RespondentService.update_respondent(update_data, respondent_id)
        if data:
            return jsonify({"success": True, "updated": True}), 200
        else:
            return jsonify({"success": False, "error": "Error updating survey"}), 400
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())

@main.route('/<string:respondent_id>', methods=['DELETE'])
def respondentsDelete(respondent_id):
    try:
        token = request.get_json()
        info = Security.verify_token(token)
        data = False
        if info != False:
            if info['idTipo'] == 1:
                data = RespondentService.delete_respondent(respondent_id)
        if data:
            return jsonify({"success": True, "deleted": True}), 200
        else:
            return jsonify({"success": False, "error": "Error deleting survey"}), 400
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
