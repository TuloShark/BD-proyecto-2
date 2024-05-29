from flask import Blueprint, request, jsonify

import traceback

# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.UsersServices import UserService

main = Blueprint('users_blueprint', __name__)


@main.route('/', methods=['GET'])
def users():
    try:
        token = request.get_json()
        info = Security.verify_token(token)
        data = None
        if info != False:
            if info['idTipo'] == 1:
                data = UserService.get_users()
                if data == None:
                    return jsonify({'success': False, 'data':data})
                return jsonify({'success': True, 'data':data})
        return jsonify({'success': False, 'data':data})
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': 'Error','success': False})

@main.route('/<int:id>', methods=['GET'])
def user(id):
    try:
        data = UserService.get_user(id)
        if data == None:
            return jsonify({'success': False, 'data':data})
        return jsonify({'success': True, 'data':data})
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': 'Error','success': False})

@main.route('/<int:id>', methods=['PUT'])
def userPut(id):
    try:
        user_data = request.get_json()
        info = Security.verify_token(user_data)
        data = None
        if info != False:
            data = UserService.update_user(user_data, id, info)
            if data == None:
                return jsonify({'success': False, 'data':data})
            return jsonify({'success': True, 'data':data})
        return jsonify({'success': False, 'data':data})
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': 'Error','success': False})

@main.route('/<int:id>', methods=['DELETE'])
def userDelete(id):
    try:
        token = request.get_json()
        info = Security.verify_token(token)
        data = None
        if info != False:
            if info['idTipo'] == 1:
                data = UserService.delete_user(id)
                if data == None:
                    return jsonify({'success': False, 'data':data})
                return jsonify({'success': True, 'data':data})
        return jsonify({'success': False, 'data':data})
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': 'Error','success': False})