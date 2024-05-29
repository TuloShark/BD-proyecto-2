import requests
import os
from bson import ObjectId
import json

host = os.getenv('DOCKER_HOST')
port = os.getenv('DOCKER_PORT')
#host = "localhost"
#port = "5002"

def test_respondents():
    url_post = f"http://{host}:{port}/respondents/6623e6281188e02fda543222"
    respondent_post = {
        "nombre": "Manuel",
        "correo": "m.aleandro00@gmail.com"
    }
    response_post = requests.post(url_post, json = respondent_post)
    json_id = response_post.json()


    url = f"http://{host}:{port}/surveys/{json_id['respondent_id']}/responses"
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
    response = requests.post(url, json = responses)
    json_response = response.json()
    assert json_response.get('success') is True


### Pruebas para los metodos
import pytest
from unittest.mock import patch, MagicMock
from src.services.SurveysServices import SurveyService

def test_post_responses_user_success():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.update_one.return_value.modified_count = 1
        responses_data = {'Pregunta1': {'Id_pregunta':'7723e6281188e02fda543233','Respuesta':'Yo opino...'}, 'Pregunta2': {'Id_pregunta':'8823e6281188e02fda543244','Respuesta':'1'}}
        responses_id = '6623e6281188e02fda543222'
        result = SurveyService.post_responses_user(responses_data, responses_id)
        mock_db.assert_called_once()
        mock_collection.update_one.assert_called_once_with(
            {"_id": ObjectId('6623e6281188e02fda543222')},
            {"$set": {"responses": {'Pregunta1': {'Id_pregunta':'7723e6281188e02fda543233','Respuesta':'Yo opino...'}, 'Pregunta2': {'Id_pregunta':'8823e6281188e02fda543244','Respuesta':'1'}}}}
        )
        assert result == 1


def test_post_responses_user_failure():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.update_one.side_effect = Exception("Error updating document")
        responses_data = {'Pregunta1': {'Id_pregunta':'7723e6281188e02fda543233','Respuesta':'Yo opino...'}, 'Pregunta2': {'Id_pregunta':'8823e6281188e02fda543244','Respuesta':'1'}}
        responses_id = '6623e6281188e02fda543222'
        result = SurveyService.post_responses_user(responses_data, responses_id)
        mock_db.assert_called_once()
        mock_collection.update_one.assert_called_once_with(
            {"_id": ObjectId('6623e6281188e02fda543222')},
            {"$set": {"responses": {'Pregunta1': {'Id_pregunta':'7723e6281188e02fda543233','Respuesta':'Yo opino...'}, 'Pregunta2': {'Id_pregunta':'8823e6281188e02fda543244','Respuesta':'1'}}}}
        )
        assert result is None