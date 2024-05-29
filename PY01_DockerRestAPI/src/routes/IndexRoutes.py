### Importaciones
from flask import Blueprint, jsonify, request
import traceback
from src.utils.Logger import Logger

### Blueprint de la ruta
main = Blueprint('index_blueprint', __name__)

### Fucnion para la ruta principal 
@main.route('/')
def index():
    try:
        Logger.add_to_log("info", "{} {}".format(request.method, request.path))
        return jsonify({'message': "Start", 'success': True})
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "Internal Server Error", 'success': False})