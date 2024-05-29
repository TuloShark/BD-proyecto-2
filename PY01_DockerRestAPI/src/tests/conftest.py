### Importaciones
import pytest
from config import config
from src import init_app

### Configuracion
configuration = config['development']

@pytest.fixture()
def app():
    app = init_app(configuration)

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()    
