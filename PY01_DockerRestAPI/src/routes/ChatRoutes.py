# ChatRoutes.py
from flask import Blueprint, request, jsonify
from kafka_producer import KafkaProducerSingleton
from src.database.db_mongodb import get_mongo_connection
import traceback
import datetime

chat_routes = Blueprint('chat_routes', __name__)

kafka_producer = KafkaProducerSingleton.get_instance()

@chat_routes.route('/send', methods=['POST'])
def send_message():
    try:
        message_content = request.json.get('message')
        author = request.json.get('author')
        timestamp = datetime.datetime.utcnow().isoformat()
        message = {
            "timestamp": timestamp,
            "author": author,
            "message": message_content
        }
        kafka_producer.send_message('chat_messages', message)
        return jsonify({'message': 'Message sent', 'success': True})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': 'Error sending message', 'success': False, 'error': str(e)})

@chat_routes.route('/history', methods=['GET'])
def get_chat_history():
    try:
        db = get_mongo_connection()
        if db is not None:
            collection = db.chat_messages
            messages = list(collection.find({}, {'_id': False}))
            return jsonify({'message': 'Chat history retrieved', 'success': True, 'history': messages})
        else:
            return jsonify({'message': 'Error connecting to MongoDB', 'success': False})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': 'Error retrieving chat history', 'success': False, 'error': str(e)})

@chat_routes.route('/users', methods=['POST'])
def add_user():
    try:
        user_name = request.json.get('user_name')
        role = request.json.get('role')
        db = get_mongo_connection()
        if db is not None:
            collection = db.chat_users
            collection.insert_one({"user_name": user_name, "role": role})
            return jsonify({'message': 'User added', 'success': True})
        else:
            return jsonify({'message': 'Error connecting to MongoDB', 'success': False})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': 'Error adding user', 'success': False, 'error': str(e)})

@chat_routes.route('/users', methods=['DELETE'])
def remove_user():
    try:
        user_name = request.json.get('user_name')
        db = get_mongo_connection()
        if db is not None:
            collection = db.chat_users
            user = collection.find_one({"user_name": user_name})
            if user:
                collection.delete_one({"user_name": user_name})
                return jsonify({'message': 'User removed', 'success': True})
            else:
                return jsonify({'message': 'User not found', 'success': False})
        else:
            return jsonify({'message': 'Error connecting to MongoDB', 'success': False})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': 'Error removing user', 'success': False, 'error': str(e)})
    
@chat_routes.route('/all', methods=['GET'])
def get_all_users():
    try:
        db = get_mongo_connection()
        if db is not None:
            collection = db.chat_users
            users = list(collection.find({}, {'_id': False}))
            return jsonify({'message': 'Users retrieved', 'success': True, 'users': users})
        else:
            return jsonify({'message': 'Error connecting to MongoDB', 'success': False})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': 'Error retrieving users', 'success': False, 'error': str(e)})

