import requests
import os

host = os.getenv('DOCKER_HOST')
port = os.getenv('DOCKER_PORT')
#host = "localhost"
#port = "5002"  

def test_index():
    url = f"http://{host}:{port}"
    response = requests.get(url)
    assert response.json() == {'message': "Start", 'success': True}