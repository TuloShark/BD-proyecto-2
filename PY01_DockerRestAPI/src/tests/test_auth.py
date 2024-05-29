import requests
import os

host = os.getenv('DOCKER_HOST')
port = os.getenv('DOCKER_PORT')
#host = "localhost"
#port = "5002"

### Pruebas para los endpoints
def test_auth():
    url = f"http://{host}:{port}/auth/login"
    user = {
        "username": "Esteban",
        "password": "1234"
    }
    response = requests.post(url, json = user)
    json = response.json()
    assert 'token' in json

def test_auth_register():
    url = f"http://{host}:{port}/auth/register"
    user = {
        "username": "Dilan",
        "password": "2000",
        "idTipo": 1
    }
    response = requests.post(url, json = user)
    json = response.json()
    assert 'Registered' == json['message']

def test_auth_logout():
    url = f"http://{host}:{port}/auth/logout"
    url_in = f"http://{host}:{port}/auth/login"
    user = {
        "username": "Esteban",
        "password": "1234",
    }
    response = requests.post(url_in, json = user)
    json_r = response.json()
    response = requests.get(url, json = json_r)
    json = response.json()
    assert 'Logout' == json['message']

### Pruebas para los metodos
import pytest
from unittest.mock import patch, MagicMock
from src.services.AuthService import AuthService

@pytest.fixture
def user():
    return {
        'username': 'usuario',
        'password': 'contraseña'
    }

def test_login_user_authenticated(user):
    data = (1, 'usuario', 'contraseña', 1)
    # Mock de la función get_connection
    with patch('src.services.AuthService.get_connection') as mock_get_connection:
        # Creamos un mock del cursor
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        # Configuramos el comportamiento del cursor al ejecutar la consulta SQL
        mock_cursor.fetchone.return_value = data
        # Ejecutamos la función que queremos probar
        authenticated_user = AuthService.login_user(user)
        # Verificamos que la conexión se haya cerrado
        mock_get_connection.return_value.close.assert_called_once()
        assert authenticated_user is not None

def test_login_user_not_authenticated(user):
    with patch('src.services.AuthService.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        authenticated_user = AuthService.login_user(user)
        mock_get_connection.return_value.close.assert_called_once()
        assert authenticated_user is None

@pytest.fixture
def user_r():
    return {
        'username': 'usuario',
        'password': 'contraseña',
        'idTipo': 1
    }

def test_register_user_success(user_r):
    with patch('src.services.AuthService.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        mock_cursor.rowcount = 1
        result = AuthService.register_user(user_r)
        mock_get_connection.return_value.close.assert_called_once()
        assert result == 1

def test_register_user_failure(user_r):
    with patch('src.services.AuthService.get_connection') as mock_get_connection:
        mock_cursor = MagicMock()
        mock_get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1]]  # Simulamos que el usuario ya existe en la base de datos
        result = AuthService.register_user(user_r)
        mock_get_connection.return_value.close.assert_called_once()
        assert result == 0