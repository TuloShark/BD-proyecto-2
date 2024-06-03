### Importaciones
from flask import Flask
from config import config
from src import init_app

### Configuracion
configuration = config['development']

### Aplicacion
app = Flask(__name__)
app.config.from_object(configuration)
app.register_blueprint(survey_bp, url_prefix='/api')

### Iniciar la aplicacion
if __name__ == '__main__':
    app.run()
