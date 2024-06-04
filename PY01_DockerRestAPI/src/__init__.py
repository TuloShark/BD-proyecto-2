### Importaciones
from flask import Flask
from .routes import AuthRoutes, IndexRoutes, UserRoutes, SurveyRoutes, RespondentRoutes, QuestionsRoutes
### Aplicacion
app = Flask(__name__)

### Inicio de la aplicacio
def init_app(config):
    # Configuracion 
    app.config.from_object(config)
    # Blueprints
    app.register_blueprint(IndexRoutes.main, url_prefix='/')
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')
    app.register_blueprint(UserRoutes.main, url_prefix='/users')
    app.register_blueprint(SurveyRoutes.main)
    app.register_blueprint(SurveyRoutes.survey_routes, url_prefix='/surveys')
    app.register_blueprint(QuestionsRoutes.main)
    app.register_blueprint(RespondentRoutes.main, url_prefix='/respondents')

    # Devuelve la aplicacion
    return app

