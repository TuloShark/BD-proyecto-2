import requests
import os

host = os.getenv('DOCKER_HOST')
port = os.getenv('DOCKER_PORT')
#host = "localhost"
#port = "5002"

def test_users():
    url = f"http://{host}:{port}/users"
    url_in = f"http://{host}:{port}/auth/login"
    user = {
        "username": "Esteban",
        "password": "1234",
    }
    response = requests.post(url_in, json = user)
    json_r = response.json()
    response = requests.get(url, json= json_r)
    json = response.json()
    assert 'data' in json

def test_user():
    id = 1
    url = f"http://{host}:{port}/users/{id}"
    response = requests.get(url)
    json = response.json()
    assert 'data' in json

def test_user_put():
    id = 2
    url = f"http://{host}:{port}/users/{id}"
    user = {
        "username": "Manuel",
        "password": "3333",
        "token": ""
    }
    url_in = f"http://{host}:{port}/auth/login"
    user_in = {
        "username": "Esteban",
        "password": "1234",
    }
    response = requests.post(url_in, json = user_in)
    json_r = response.json()
    user['token'] = json_r['token']
    response = requests.put(url, json = user)
    json = response.json()
    assert json['data'] != None

def test_user_delete():
    id = 2
    url = f"http://{host}:{port}/users/{id}"
    url_in = f"http://{host}:{port}/auth/login"
    user_in = {
        "username": "Esteban",
        "password": "1234",
    }
    response = requests.post(url_in, json = user_in)
    json_r = response.json()
    response = requests.delete(url, json= json_r)
    json = response.json()
    assert 'data' in json

### Pruebas para los metodos
import pytest
from unittest.mock import patch, MagicMock
from src.services.UsersServices import UserService

def test_get_users_success():
    data = [(1, 'usuario1', 'contraseña1', 1), (2, 'usuario2', 'contraseña2', 2)]
    with patch('src.services.UsersServices.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = data
        result = UserService.get_users()
        mock_get_connection.return_value.close.assert_called_once()
        assert result == data

def test_get_users_failure():
    with patch('src.services.UsersServices.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = Exception("Error al ejecutar la consulta")
        result = UserService.get_users()
        assert result is None

def test_get_user_success():
    user_id = 1
    data = [(1, 'usuario1', 'contraseña1', 1)]
    with patch('src.services.UsersServices.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = data
        result = UserService.get_user(user_id)
        mock_get_connection.return_value.close.assert_called_once()
        assert result == data

def test_get_user_failure():
    user_id = 1
    with patch('src.services.UsersServices.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = Exception("Error al ejecutar la consulta")
        result = UserService.get_user(user_id)
        assert result is None

def test_update_user_success():
    user_data = {'username': 'usuario1', 'password': 'nueva_contraseña'}
    id = 1
    info = {'id': 1, 'idTipo': 1}
    with patch('src.services.UsersServices.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.rowcount = 1
        result = UserService.update_user(user_data, id, info)
        mock_get_connection.return_value.close.assert_called_once()
        assert result == 1

def test_update_user_failure():
    user_data = {'username': 'usuario1', 'password': 'nueva_contraseña'}
    id = 1
    info = {'id': 2, 'idTipo': 2}
    with patch('src.services.UsersServices.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.rowcount = 0
        result = UserService.update_user(user_data, id, info)
        mock_get_connection.return_value.close.assert_called_once()
        assert result == 0

def test_delete_user_success():
    user_id = 1
    with patch('src.services.UsersServices.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.rowcount = 1
        result = UserService.delete_user(user_id)
        mock_get_connection.return_value.close.assert_called_once()
        assert result == 1

def test_delete_user_failure():
    user_id = 1
    with patch('src.services.UsersServices.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.rowcount = 0  # Simulamos que no se eliminó ningún usuario
        result = UserService.delete_user(user_id)
        mock_get_connection.return_value.close.assert_called_once()
        assert result == 0