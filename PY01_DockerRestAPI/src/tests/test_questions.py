import os
import requests
from unittest.mock import patch, MagicMock
from bson import ObjectId

host = os.getenv('DOCKER_HOST')
port = os.getenv('DOCKER_PORT')
#host = "localhost"
#port = "5002"
survey_id = "1" # ID de la encuesta creada

### Pruebas para los endpoints
def test_open_question():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions"
    question_data = {
        "title": "Pregunta abierta",
        "description": "¿Qué opinas sobre el cambio climático?",
        "type": "open",
        "options": []
    }
    response = requests.post(url, json=question_data)
    json = response.json()
    assert json['success'] == True

def test_single_choice_question():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions"
    question_data = {
        "title": "Pregunta de elección simple",
        "description": "¿Cuál es tu color favorito?",
        "type": "single_choice",
        "options": ["Rojo", "Azul", "Verde", "Amarillo"]
    }
    response = requests.post(url, json=question_data)
    json = response.json()
    assert json['success'] == True

def test_multiple_choice_question():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions"
    question_data = {
        "title": "Pregunta de elección múltiple",
        "description": "Selecciona todos los lenguajes de programación que conoces",
        "type": "multiple_choice",
        "options": ["Python", "Java", "C#", "JavaScript"]
    }
    response = requests.post(url, json=question_data)
    json = response.json()
    assert json['success'] == True

def test_rating_scale_question():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions"
    question_data = {
        "title": "Pregunta de escala de calificación",
        "description": "Del 1 al 5, ¿cuánto te gustó nuestro producto?",
        "type": "rating_scale",
        "scale_min": 1,
        "scale_max": 5
    }
    response = requests.post(url, json=question_data)
    json = response.json()
    assert json['success'] == True

def test_yes_no_question():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions"
    question_data = {
        "title": "Pregunta Sí/No",
        "description": "¿Recomendarías nuestro producto a un amigo?",
        "type": "yes_no",
        "options": ["Sí", "No"]
    }
    response = requests.post(url, json=question_data)
    json = response.json()
    assert json['success'] == True

def test_numeric_question():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions"
    question_data = {
        "title": "Pregunta numérica",
        "description": "¿Cuántos años tienes?",
        "type": "numeric",
        "options": []
    }
    response = requests.post(url, json=question_data)
    json = response.json()
    assert json['success'] == True

def test_get_all_question():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url_question = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions"
    question_data = {
        "title": "Pregunta numérica",
        "description": "¿Cuántos años tienes?",
        "type": "numeric",
        "options": []
    }
    response_question = requests.post(url_question, json=question_data)

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions"
    response = requests.get(url)
    json_response = response.json()
    assert json_response.get('success') is True

def test_update_question():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url_question = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions"
    question_data = {
        "title": "Pregunta numérica",
        "description": "¿Cuántos años tienes?",
        "type": "numeric",
        "options": []
    }
    response_question = requests.post(url_question, json=question_data)
    json_question = response_question.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions/{json_question['question_id']}"
    respondent_update = {
        "title": "Encuesta de Negativa",
        "description": "Una encuesta sobre la negatividad del usuario con el servicio."
    }
    response_update = requests.put(url, json = respondent_update)
    json_response = response_update.json()
    assert json_response.get('success') is True

def test_delete_question():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url_question = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions"
    question_data = {
        "title": "Pregunta numérica",
        "description": "¿Cuántos años tienes?",
        "type": "numeric",
        "options": []
    }
    response_question = requests.post(url_question, json=question_data)
    json_question = response_question.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/questions/{json_question['question_id']}"
    response_delete = requests.delete(url)
    json_response = response_delete.json()
    assert json_response.get('success') is True

### Pruebas para los metodos
def test_create_open_question():
    url = f"http://{host}:{port}/surveys/{survey_id}/questions"
    question_data = {
        "title": "Pregunta abierta",
        "description": "¿Qué opinas sobre el cambio climático?",
        "type": "open",
        "options": []
    }
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'success': True, 'question_id': '123'}
        response = requests.post(url, json=question_data)
        json = response.json()
        assert json['success'] == True and 'question_id' in json, "Debería retornar success=True y un question_id"

def test_create_single_choice_question():
    url = f"http://{host}:{port}/surveys/{survey_id}/questions"
    question_data = {
        "title": "Pregunta de elección simple",
        "description": "¿Cuál es tu color favorito?",
        "type": "single_choice",
        "options": ["Rojo", "Azul", "Verde", "Amarillo"]
    }
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'success': True, 'question_id': '123'}
        response = requests.post(url, json=question_data)
        json = response.json()
        assert json['success'] == True and 'question_id' in json, "Debería retornar success=True y un question_id"

def test_create_multiple_choice_question():
    url = f"http://{host}:{port}/surveys/{survey_id}/questions"
    question_data = {
        "title": "Pregunta de elección múltiple",
        "description": "Selecciona todos los lenguajes de programación que conoces",
        "type": "multiple_choice",
        "options": ["Python", "Java", "C#", "JavaScript"]
    }
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'success': True, 'question_id': '123'}
        response = requests.post(url, json=question_data)
        json = response.json()
        assert json['success'] == True and 'question_id' in json, "Debería retornar success=True y un question_id"

def test_create_rating_scale_question():
    url = f"http://{host}:{port}/surveys/{survey_id}/questions"
    question_data = {
        "title": "Pregunta de escala de calificación",
        "description": "Del 1 al 5, ¿cuánto te gustó nuestro producto?",
        "type": "rating_scale",
        "scale_min": 1,
        "scale_max": 5
    }
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'success': True, 'question_id': '123'}
        response = requests.post(url, json=question_data)
        json = response.json()
        assert json['success'] == True and 'question_id' in json, "Debería retornar success=True y un question_id"

def test_create_yes_no_question():
    url = f"http://{host}:{port}/surveys/{survey_id}/questions"
    question_data = {
        "title": "Pregunta Sí/No",
        "description": "¿Recomendarías nuestro producto a un amigo?",
        "type": "yes_no",
        "options": ["Sí", "No"]
    }
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'success': True, 'question_id': '123'}
        response = requests.post(url, json=question_data)
        json = response.json()
        assert json['success'] == True and 'question_id' in json, "Debería retornar success=True y un question_id"

def test_create_numeric_question():
    url = f"http://{host}:{port}/surveys/{survey_id}/questions"
    question_data = {
        "title": "Pregunta numérica",
        "description": "¿Cuántos años tienes?",
        "type": "numeric",
        "options": []
    }
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'success': True, 'question_id': '123'}
        response = requests.post(url, json=question_data)
        json = response.json()
        assert json['success'] == True and 'question_id' in json, "Debería retornar success=True y un question_id"

############################################################
import pytest
from src.services.QuestionsServices import QuestionService

def test_create_question_failure():
    with patch('src.services.QuestionsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.insert_one.side_effect = Exception("Error inserting document")
        survey_id = '6623e6281188e02fda543222'
        question_data = {
        "title": "Pregunta numérica",
        "description": "¿Cuántos años tienes?",
        "type": "numeric",
        "options": []
        }
        result = QuestionService.create_question(survey_id, question_data)
        mock_db.assert_called_once()
        mock_collection.insert_one.assert_called_once_with({
        "title": "Pregunta numérica",
        "description": "¿Cuántos años tienes?",
        "type": "numeric",
        "options": [], 
        'surveyId': ObjectId('6623e6281188e02fda543222')})
        assert result == {'success': False, 'error': 'Error inserting document'}

def test_get_all_questions_success():
    with patch('src.services.QuestionsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_cursor = MagicMock()
        mock_collection.find.return_value = mock_cursor
        question_data = [
            {'_id': ObjectId('6623e6281188e02fda543222'), 'Question 1': 'text', 'surveyId': ObjectId('7723e6281188e02fda543244')},
            {'_id': ObjectId('6623e6281188e02fda543223'), 'Question 2': 'text', 'surveyId': ObjectId('7723e6281188e02fda543244')}
        ]
        mock_cursor.__iter__.return_value = iter(question_data)
        survey_id = '7723e6281188e02fda543244'
        result = QuestionService.get_all_questions(survey_id)
        mock_db.assert_called_once()
        mock_collection.find.assert_called_once_with({"surveyId": ObjectId('7723e6281188e02fda543244')})
        assert result == {
            'success': True,
            'questions': [
                {'_id': '6623e6281188e02fda543222', 'Question 1': 'text', 'surveyId':'7723e6281188e02fda543244'},
                {'_id': '6623e6281188e02fda543223', 'Question 2': 'text', 'surveyId':'7723e6281188e02fda543244'}
            ]
        }

def test_get_all_questions_failure():
    with patch('src.services.QuestionsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find.side_effect = Exception("Error executing query")
        survey_id = '6623e6281188e02fda543222'
        result = QuestionService.get_all_questions(survey_id)
        mock_db.assert_called_once()
        mock_collection.find.assert_called_once_with({"surveyId": ObjectId('6623e6281188e02fda543222')})
        assert result == {'success': False, 'error': 'Error executing query'}

def test_get_question_by_id_success():
    with patch('src.services.QuestionsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find_one.return_value = {'_id': ObjectId('6623e6281188e02fda543222'), 'Question 1': 'text', 'surveyId': ObjectId('7723e6281188e02fda543233')}
        question_id = '6623e6281188e02fda543222'
        result = QuestionService.get_question_by_id(question_id)
        mock_db.assert_called_once()
        mock_collection.find_one.assert_called_once_with({"_id": ObjectId('6623e6281188e02fda543222')})
        assert result == {
            'success': True,
            'question': {'_id': '6623e6281188e02fda543222', 'Question 1': 'text', 'surveyId': '7723e6281188e02fda543233'}
        }

def test_get_question_by_id_not_found():
    with patch('src.services.QuestionsServices.get_mongo_connection')as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find_one.return_value = None
        question_id = '6623e6281188e02fda543222'
        result = QuestionService.get_question_by_id(question_id)
        mock_db.assert_called_once()
        mock_collection.find_one.assert_called_once_with({"_id": ObjectId('6623e6281188e02fda543222')})
        assert result == {'success': False, 'error': 'Question not found'}

def test_get_question_by_id_failure():
    with patch('src.services.QuestionsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find_one.side_effect = Exception("Error executing query")
        question_id = '6623e6281188e02fda543222'
        result = QuestionService.get_question_by_id(question_id)
        mock_db.assert_called_once()
        mock_collection.find_one.assert_called_once_with({"_id": ObjectId('6623e6281188e02fda543222')})
        assert result == {'success': False, 'error': 'Error executing query'}

def test_update_question_success():
    with patch('src.services.QuestionsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.update_one.return_value.matched_count = 1
        question_id = '6623e6281188e02fda543222'
        update_data = {'Question': 'Updated text'}
        result = QuestionService.update_question(question_id, update_data)
        mock_db.assert_called_once()
        mock_collection.update_one.assert_called_once_with(
            {"_id": ObjectId('6623e6281188e02fda543222')},
            {"$set": {'Question': 'Updated text'}}
        )
        assert result == {'success': True}

def test_update_question_failure():
    with patch('src.services.QuestionsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.update_one.side_effect = Exception("Error updating document")
        question_id = '6623e6281188e02fda543222'
        update_data = {'text': 'Updated Question'}
        result = QuestionService.update_question(question_id, update_data)
        mock_db.assert_called_once()
        mock_collection.update_one.assert_called_once_with(
            {"_id": ObjectId('6623e6281188e02fda543222')},
            {"$set": {'text': 'Updated Question'}}
        )
        assert result == {'success': False, 'error': 'Error updating document'}

def test_delete_question_success():
    with patch('src.services.QuestionsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.delete_one.return_value.deleted_count = 1
        question_id = '6623e6281188e02fda543222'
        result = QuestionService.delete_question(question_id)
        mock_db.assert_called_once()
        mock_collection.delete_one.assert_called_once_with({"_id": ObjectId('6623e6281188e02fda543222')})
        assert result == {'success': True}

def test_delete_question_failure():
    with patch('src.services.QuestionsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.delete_one.side_effect = Exception("Error deleting document")
        question_id = '6623e6281188e02fda543222'
        result = QuestionService.delete_question(question_id)
        mock_db.assert_called_once()
        mock_collection.delete_one.assert_called_once_with({"_id": ObjectId('6623e6281188e02fda543222')})
        assert result == {'success': False, 'error': 'Error deleting document'}