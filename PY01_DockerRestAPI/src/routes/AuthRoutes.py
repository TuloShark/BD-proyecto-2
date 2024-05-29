### Importaciones
from flask import Blueprint, request, jsonify
import traceback
from src.utils.Logger import Logger
from src.models.UserModel import User
from src.utils.Security import Security
from src.services.AuthService import AuthService

### Blueprint de la ruta
main = Blueprint('auth_blueprint', __name__)

### Funcion para la ruta del login
@main.route('/login', methods=['POST'])
def login():
    try:
        user = request.get_json()
        authenticated_user = AuthService.login_user(user)
        if (authenticated_user != None):
            encoded_token = Security.generate_token(authenticated_user)
            return jsonify({'message': 'Authorized','success': True, 'token': encoded_token})
        else:
            return jsonify({'message': 'Unauthorized', 'success': False})
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error", 'success': False})
    
@main.route('/register', methods=['POST'])
def register():
    try:
        user = request.get_json()
        data = AuthService.register_user(user)
        if data == 1:
            return jsonify({'message': 'Registered','success': True})
        else:
            return jsonify({'message': 'Not registered','success': False})
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error", 'success': False})
    
@main.route('/logout', methods=['GET'])
def logout():
    try:
        info = request.get_json()
        data = Security.logout(info)
        if data:
            return jsonify({'message': 'Logout','success': True})
        return jsonify({'message': 'Unauthorized', 'success': False})
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Error", 'success': False})
