import requests
import json
import os
from bson import ObjectId

host = os.getenv('DOCKER_HOST')
port = os.getenv('DOCKER_PORT')
#host = "localhost"
#port = "5002"

def test_respondents():
    url = f"http://{host}:{port}/respondents/6623e6281188e02fda543222"
    respondent = {
        "nombre": "Manuel",
        "correo": "m.aleandro00@gmail.com"
    }
    response = requests.post(url, json = respondent)
    json_id = response.json()
    assert json_id.get('success') is True

def test_get_all_respondent():
    url = f"http://{host}:{port}/respondents/all/6623e6281188e02fda543222"
    url_in = f"http://{host}:{port}/auth/login"
    user_in = {
        "username": "Esteban",
        "password": "1234",
    }
    response = requests.post(url_in, json = user_in)
    json_r = response.json()
    response = requests.get(url, json=json_r)
    json_response = response.json()
    assert json_response.get('success') is True

def test_get_by_id_respondent():
    url_post = f"http://{host}:{port}/respondents/6623e6281188e02fda543222"
    respondent_post = {
        "nombre": "Manuel",
        "correo": "m.aleandro00@gmail.com",
        "token": ""
    }

    url_in = f"http://{host}:{port}/auth/login"
    user_in = {
        "username": "Esteban",
        "password": "1234",
    }
    response = requests.post(url_in, json = user_in)
    json_r = response.json()
    respondent_post['token'] = json_r['token']

    response_post = requests.post(url_post, json = respondent_post)
    json_id = response_post.json()
    url = f"http://{host}:{port}/respondents/{json_id['respondent_id']}"
    response = requests.get(url, json=json_r)
    json_response = response.json()
    assert json_response.get('success') is True

def test_respondent_put():
    url_post = f"http://{host}:{port}/respondents/6623e6281188e02fda543222"
    respondent = {
        "nombre": "Manuel",
        "correo": "m.aleandro00@gmail.com",
        "token": ""
    }

    url_in = f"http://{host}:{port}/auth/login"
    user_in = {
        "username": "Esteban",
        "password": "1234",
    }
    response = requests.post(url_in, json = user_in)
    json_r = response.json()
    respondent['token'] = json_r['token']

    response = requests.post(url_post, json = respondent)
    json_id = response.json()

    url = f"http://{host}:{port}/respondents/{json_id['respondent_id']}"
    respondent_update = {
        "nombre": "Esteban",
        "correo": "m.alejandro00@hotmail.com",
        "token": ""
    }
    respondent_update['token'] = json_r['token']
    response_update = requests.put(url, json = respondent_update)
    json_response = response_update.json()
    assert json_response.get('success') is True

def test_respondent_delete():
    url_post = f"http://{host}:{port}/respondents/6623e6281188e02fda543222"
    respondent = {
        "nombre": "Manuel",
        "correo": "m.aleandro00@gmail.com",
        "token": ""
    }

    url_in = f"http://{host}:{port}/auth/login"
    user_in = {
        "username": "Esteban",
        "password": "1234",
    }
    response = requests.post(url_in, json = user_in)
    json_r = response.json()
    respondent['token'] = json_r['token']

    response = requests.post(url_post, json = respondent)
    json_id = response.json()

    url = f"http://{host}:{port}/respondents/{json_id['respondent_id']}"
    response_delete = requests.delete(url, json= json_r)
    json_response = response_delete.json()
    assert json_response.get('success') is True

### Pruebas para los metodos
import pytest
from unittest.mock import patch, MagicMock
from src.services.RespondentsServices import RespondentService

def test_post_respondent_success():
    with patch('src.services.RespondentsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.insert_one.return_value.inserted_id = ObjectId('6623e6281188e02fda543222')
        respondent_data = {'nombre': 'Manuel', 'correo': 'm.aleandro@gmail.com'} 
        survey_id = '7723e6281188e02fda543233'
        result = RespondentService.post_respondent(respondent_data, survey_id)
        mock_db.assert_called_once()
        mock_collection.insert_one.assert_called_once_with({'nombre': 'Manuel', 'correo': 'm.aleandro@gmail.com', 'idSurvey': ObjectId('7723e6281188e02fda543233')})
        assert result == ObjectId('6623e6281188e02fda543222')


def test_post_respondent_failure():
    with patch('src.services.RespondentsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.insert_one.side_effect = Exception("Error inserting document")
        respondent_data = {'nombre': 'Manuel', 'correo': 'm.aleandro@gmail.com'} 
        survey_id = '7723e6281188e02fda543233'
        result = RespondentService.post_respondent(respondent_data, survey_id)
        mock_db.assert_called_once()
        mock_collection.insert_one.assert_called_once_with({'nombre': 'Manuel', 'correo': 'm.aleandro@gmail.com', 'idSurvey': ObjectId('7723e6281188e02fda543233')})
        assert result is None

def test_get_respondents_success():
    with patch('src.services.RespondentsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_cursor = MagicMock()
        mock_collection.find.return_value = mock_cursor
        survey_id = '7723e6281188e02fda543233'
        respondent_data = [
            {'_id': ObjectId('6623e6281188e02fda543222'), 'nombre': 'Manuel', 'correo': 'm.aleandro@gmail.com', 'idSurvey': ObjectId('7723e6281188e02fda543233')},
            {'_id': ObjectId('8823e6281188e02fda543244'), 'nombre': 'Esteban', 'correo': 'estaban@gmail.com', 'idSurvey': ObjectId('7723e6281188e02fda543233')}
        ]
        mock_cursor.__iter__.return_value = iter(respondent_data)
        result = RespondentService.get_respondents(survey_id)
        mock_db.assert_called_once()
        mock_collection.find.assert_called_once_with({'idSurvey': ObjectId('7723e6281188e02fda543233')})
        assert result == {
            'respondents': [
                {'_id': '6623e6281188e02fda543222', 'nombre': 'Manuel', 'correo': 'm.aleandro@gmail.com', 'idSurvey': '7723e6281188e02fda543233'},
                {'_id': '8823e6281188e02fda543244', 'nombre': 'Esteban', 'correo': 'estaban@gmail.com', 'idSurvey': '7723e6281188e02fda543233'}
            ]
        }

def test_get_respondents_failure():
    with patch('src.services.RespondentsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find.side_effect = Exception("Error executing query")
        survey_id = '7723e6281188e02fda543233'
        result = RespondentService.get_respondents(survey_id)
        mock_db.assert_called_once()
        mock_collection.find.assert_called_once_with({'idSurvey': ObjectId('7723e6281188e02fda543233')})
        assert result is None

def test_get_respondent_success():
    with patch('src.services.RespondentsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find_one.return_value = {
            '_id': ObjectId('6623e6281188e02fda543222'),
            'nombre': 'Manuel', 
            'correo': 'm.aleandro@gmail.com',
            'idSurvey': ObjectId('7723e6281188e02fda543233')
        }
        respondent_id = '6623e6281188e02fda543222'
        result = RespondentService.get_respondent(respondent_id)
        mock_db.assert_called_once()
        mock_collection.find_one.assert_called_once_with({'_id': ObjectId('6623e6281188e02fda543222')})
        assert result == {
            'respondent': {
                '_id': '6623e6281188e02fda543222',
                'nombre': 'Manuel', 
                'correo': 'm.aleandro@gmail.com',
                'idSurvey': '7723e6281188e02fda543233'
            }
        }

def test_get_respondent_failure():
    with patch('src.services.RespondentsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find_one.side_effect = Exception("Error executing query")
        respondent_id = '6623e6281188e02fda543222'
        result = RespondentService.get_respondent(respondent_id)
        mock_db.assert_called_once()
        mock_collection.find_one.assert_called_once_with({'_id': ObjectId('6623e6281188e02fda543222')})
        assert result is None

def test_update_respondent_success():
    with patch('src.services.RespondentsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find_one.return_value = {
            '_id': ObjectId('6623e6281188e02fda543222'),
            'nombre': 'Manuel', 
            'correo': 'm.aleandro@gmail.com'
        }
        update_data = {'nombre': 'Dilan', 'correo': 'Dilan@gmail.com'}
        respondent_id = '6623e6281188e02fda543222'
        result = RespondentService.update_respondent(update_data, respondent_id)
        mock_db.assert_called_once()
        mock_collection.find_one.assert_called_once_with({'_id': ObjectId('6623e6281188e02fda543222')})
        mock_collection.replace_one.assert_called_once_with(
            {'_id': ObjectId('6623e6281188e02fda543222')},
            {'_id': ObjectId('6623e6281188e02fda543222'), 'nombre': 'Dilan', 'correo': 'Dilan@gmail.com'}
        )
        assert result is True

def test_update_respondent_failure():
    with patch('src.services.RespondentsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find_one.side_effect = Exception("Error executing query")
        update_data = {'nombre': 'Dilan', 'correo': 'Dilan@gmail.com'}
        respondent_id = '6623e6281188e02fda543222'
        result = RespondentService.update_respondent(update_data, respondent_id)
        mock_db.assert_called_once()
        mock_collection.find_one.assert_called_once_with({'_id': ObjectId('6623e6281188e02fda543222')})
        assert result is None

def test_delete_respondent_success():
    with patch('src.services.RespondentsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.delete_one.return_value.deleted_count = 1
        respondent_id = '6623e6281188e02fda543222'
        result = RespondentService.delete_respondent(respondent_id)
        mock_db.assert_called_once()
        mock_collection.delete_one.assert_called_once_with({'_id': ObjectId('6623e6281188e02fda543222')})
        assert result is True

def test_delete_respondent_failure():
    with patch('src.services.RespondentsServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.delete_one.side_effect = Exception("Error deleting document")
        respondent_id = '6623e6281188e02fda543222'
        result = RespondentService.delete_respondent(respondent_id)
        mock_db.assert_called_once()
        mock_collection.delete_one.assert_called_once_with({'_id': ObjectId('6623e6281188e02fda543222')})
        assert result is None