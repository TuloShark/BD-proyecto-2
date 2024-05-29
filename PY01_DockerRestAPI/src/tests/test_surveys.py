import requests
import os
from bson.objectid import ObjectId
from src.services.SurveysServices import SurveyService
from unittest.mock import patch, MagicMock


host = os.getenv('DOCKER_HOST')
port = os.getenv('DOCKER_PORT')
#host = "localhost"
#port = "5002"

def test_create_survey():
    url = f"http://{host}:{port}/surveys"
    survey_data = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response = requests.post(url, json=survey_data)
    json = response.json()
    assert json['success'] == True

def test_get_all():
    url = f"http://{host}:{port}/surveys"
    response = requests.get(url)
    json = response.json()
    assert json['success'] == True

def test_get_survey_by_id():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}"
    response = requests.get(url)
    json = response.json()
    assert json['success'] == True

def test_publish_survey():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()
    
    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/publish"
    response = requests.post(url)
    json = response.json()
    assert json['success'] == True

def test_update_survey():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}"
    update_data = {
        "title": "Encuesta Actualizada"
    }
    response = requests.put(url, json=update_data)
    json = response.json()
    assert json['success'] == True

def test_delete_survey():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}"
    response = requests.delete(url)
    json = response.json()
    assert json['success'] == True

def test_get_responses_by_survey():
    url_id = f"http://{host}:{port}/surveys"
    survey_data_id = {
        "title": "Encuesta de Satisfacción",
        "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
    }
    response_id = requests.post(url_id, json=survey_data_id)
    json_id = response_id.json()

    url_post = f"http://{host}:{port}/respondents/{json_id['survey_id']}"
    respondent_post = {
        "nombre": "Manuel",
        "correo": "m.aleandro00@gmail.com"
    }
    response_post = requests.post(url_post, json = respondent_post)
    json_post = response_post.json()

    url_responses = f"http://{host}:{port}/surveys/{json_post['respondent_id']}/responses"
    responses = {
        "1": 
        {
            "Id_pregunta":"1",
            "Respuesta":"Yo considero..."
        },
        "2": 
        {
            "Id_pregunta":"2",
            "Respuesta":"3"
        }
        }
    response_responses = requests.post(url_responses, json = responses)

    url = f"http://{host}:{port}/surveys/{json_id['survey_id']}/responses"
    response = requests.get(url)
    json_response = response.json()
    assert json_response['success'] == True
        

# Prueba para la creación exitosa de una encuesta
def test_create_survey_success():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.insert_one.return_value.inserted_id = ObjectId('507f1f77bcf86cd799439011')
        survey_data = {
            "title": "Encuesta de Satisfacción",
            "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
        }
        survey_id = SurveyService.create_survey(survey_data)
        assert survey_id == (True, ObjectId('507f1f77bcf86cd799439011'))

# Prueba para obtener todas las encuestas
def test_get_all_surveys():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find.return_value = [
            {"_id": ObjectId('507f1f77bcf86cd799439011'), "title": "Survey 1"},
            {"_id": ObjectId('507f1f77bcf86cd799439012'), "title": "Survey 2"}
        ]
        surveys = SurveyService.get_all_surveys()
        mock_collection.find.assert_called_once_with({}, {'_id': 1, 'title': 1, 'description': 1})
        assert len(surveys) == 2
        assert surveys[0]['title'] == "Survey 1"

# Prueba para la eliminación exitosa de una encuesta
def test_delete_survey_success():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.delete_one.return_value.deleted_count = 1
        survey_id = '507f1f77bcf86cd799439011'
        result = SurveyService.delete_survey(survey_id)
        assert result == True

# Prueba para la creación fallida de una encuesta
def test_create_survey_failure():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.insert_one.side_effect = Exception("Error al insertar")
        survey_data = {
            "title": "Encuesta de Satisfacción",
            "description": "Una encuesta sobre la satisfacción del usuario con el servicio."
        }
        success, survey_id = SurveyService.create_survey(survey_data)
        assert not success and survey_id is None

# Prueba para obtener todas las encuestas fallida por error en la base de datos
def test_get_all_surveys_failure():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find.side_effect = Exception("Error al recuperar encuestas")
        surveys = SurveyService.get_all_surveys()
        assert surveys is None

# Prueba para la eliminación fallida de una encuesta / Simula que no se eliminó ninguna encuesta
def test_delete_survey_failure():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.delete_one.return_value.deleted_count = 0  
        survey_id = '507f1f77bcf86cd799439011'
        result = SurveyService.delete_survey(survey_id)
        assert not result


################################################
def test_get_responses_by_survey_success():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_cursor = MagicMock()
        mock_collection.find.return_value = mock_cursor
        mock_cursor.__iter__.return_value = iter([
            {'_id': ObjectId('6623e6281188e02fda543222'), 'response_data': 'data1', 'idSurvey': ObjectId('8823e6281188e02fda543255')},
            {'_id': ObjectId('7723e6281188e02fda543233'), 'response_data': 'data2', 'idSurvey': ObjectId('8823e6281188e02fda543255')}
        ])
        survey_id = '8823e6281188e02fda543255'
        result = SurveyService.get_responses_by_survey(survey_id)
        mock_db.assert_called_once()
        mock_collection.find.assert_called_once_with({"idSurvey": ObjectId('8823e6281188e02fda543255')})
        assert result == [
            {'_id': '6623e6281188e02fda543222', 'response_data': 'data1', 'idSurvey': '8823e6281188e02fda543255'},
            {'_id': '7723e6281188e02fda543233', 'response_data': 'data2', 'idSurvey': '8823e6281188e02fda543255'}
        ]

def test_get_responses_by_survey_failure():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find.side_effect = Exception("Error executing query")
        survey_id = '8823e6281188e02fda543255'
        result = SurveyService.get_responses_by_survey(survey_id)
        mock_db.assert_called_once()
        mock_collection.find.assert_called_once_with({"idSurvey": ObjectId('8823e6281188e02fda543255')})
        assert result is None

def test_get_survey_by_id_success():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find_one.return_value = {'_id': ObjectId('8823e6281188e02fda543255'), 'name': 'Survey 1', 'description': 'Survey Description'}
        survey_id = '8823e6281188e02fda543255'
        result = SurveyService.get_survey_by_id(survey_id)
        mock_db.assert_called_once()
        mock_collection.find_one.assert_called_once_with({"_id": ObjectId('8823e6281188e02fda543255')})
        assert result == {'_id': '8823e6281188e02fda543255', 'name': 'Survey 1', 'description': 'Survey Description'}

def test_get_survey_by_id_failure():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find_one.side_effect = Exception("Error executing query")
        survey_id = '8823e6281188e02fda543255'
        result = SurveyService.get_survey_by_id(survey_id)
        mock_db.assert_called_once()
        mock_collection.find_one.assert_called_once_with({"_id": ObjectId('8823e6281188e02fda543255')})
        assert result is None

def test_update_survey_success():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.update_one.return_value.matched_count = 1
        survey_id = '6088c024186c144a41840b6f'
        update_data = {'name': 'Updated Survey Name', 'description': 'Updated Survey Description'}
        result = SurveyService.update_survey(survey_id, update_data)
        mock_db.assert_called_once()
        mock_collection.update_one.assert_called_once_with(
            {"_id": ObjectId('6088c024186c144a41840b6f')},
            {"$set": {'name': 'Updated Survey Name', 'description': 'Updated Survey Description'}}
        )
        assert result is True

def test_update_survey_failure():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.update_one.side_effect = Exception("Error updating document")
        survey_id = '6088c024186c144a41840b6f'
        update_data = {'name': 'Updated Survey Name', 'description': 'Updated Survey Description'}
        result = SurveyService.update_survey(survey_id, update_data)
        mock_db.assert_called_once()
        mock_collection.update_one.assert_called_once_with(
            {"_id": ObjectId('6088c024186c144a41840b6f')},
            {"$set": {'name': 'Updated Survey Name', 'description': 'Updated Survey Description'}}
        )
        assert result is False

def test_publish_survey_success():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_get_mongo_connection:
        mock_db = MagicMock()
        mock_get_mongo_connection.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_result = MagicMock()
        mock_result.modified_count = 1
        mock_collection.update_one.return_value = mock_result
        survey_id = '8823e6281188e02fda543255'
        result = SurveyService.publish_survey(survey_id)
        mock_get_mongo_connection.assert_called_once()
        mock_collection.update_one.assert_called_once_with(
            {"_id": ObjectId('8823e6281188e02fda543255')},
            {"$set": {"is_published": True}}
        )
        assert result is True

def test_publish_survey_failure():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.update_one.side_effect = Exception("Error updating document")
        survey_id = '8823e6281188e02fda543255'
        result = SurveyService.publish_survey(survey_id)
        mock_db.assert_called_once()
        mock_collection.update_one.assert_called_once_with(
            {"_id": ObjectId('8823e6281188e02fda543255')},
            {"$set": {"is_published": True}}
        )
        assert result is False