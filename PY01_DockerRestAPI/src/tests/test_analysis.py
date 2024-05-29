import requests
import json
import os
from bson import ObjectId

host = os.getenv('DOCKER_HOST')
port = os.getenv('DOCKER_PORT')
#host = "localhost"
#port = "5002"

def test_get_analysis():
    url_s = f"http://{host}:{port}/surveys"
    survey_data = {
        "title": "Encuesta de analiticas",
        "description": "Una encuesta",
        "idUser": 1
    }
    response_s = requests.post(url_s, json=survey_data)
    json_s = response_s.json()

    url_post = f"http://{host}:{port}/respondents/{json_s['survey_id']}"
    respondent_post = {
        "nombre": "Manuel",
        "correo": "m.aleandro00@gmail.com"
    }
    response_post = requests.post(url_post, json = respondent_post)
    json_id = response_post.json()

    url_responses = f"http://{host}:{port}/surveys/{json_id['respondent_id']}/responses"
    responses_responses = {
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
    response_responses = requests.post(url_responses, json = responses_responses)

    url_in = f"http://{host}:{port}/auth/login"
    user_in = {
        "username": "Esteban",
        "password": "1234",
    }
    response = requests.post(url_in, json = user_in)
    json_r = response.json()

    url = f"http://{host}:{port}/surveys/analysis/{json_s['survey_id']}"
    response = requests.get(url, json=json_r)
    json_response = response.json()
    assert json_response.get('success') is True

### Pruebas para los metodos
import pytest
from unittest.mock import patch, MagicMock
from src.services.SurveysServices import SurveyService

def test_get_analysis_success():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_cursor = MagicMock()
        mock_collection.find.return_value = mock_cursor
        mock_cursor.__iter__.return_value = iter([
            {
                'responses': {
                    "1": 
                    {
                        "Id_pregunta":"1",
                        "Respuesta":"Yo considero..."
                    },
                    "2": 
                    {
                        "Id_pregunta":"2",
                        "Respuesta":"3"
                    },
                    "3":
                    {
                        "Id_pregunta":"3",
                        "Respuesta":"1"
                    }
                }
            },
            {
                'responses': {
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
            }
        ])
        survey_id = '6623e6281188e02fda543222'
        result = SurveyService.get_analysis(survey_id)
        mock_db.assert_called_once()
        mock_collection.find.assert_called_once_with({'idSurvey': ObjectId('6623e6281188e02fda543222')})
        assert result == {'1': 2, '2': 2, '3': 1}

def test_get_analysis_failure():
    with patch('src.services.SurveysServices.get_mongo_connection') as mock_db:
        mock_collection = MagicMock()
        mock_db.return_value.__getitem__.return_value = mock_collection
        mock_collection.find.side_effect = Exception("Error executing query")
        survey_id = '6623e6281188e02fda543222'
        result = SurveyService.get_analysis(survey_id)
        mock_db.assert_called_once()
        mock_collection.find.assert_called_once_with({'idSurvey': ObjectId('6623e6281188e02fda543222')})
        assert result is None