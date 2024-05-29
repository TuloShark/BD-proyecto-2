### Importaciones
from decouple import config
import os

### Clase para la configuracion 
class Config():

    #SECRET_KEY = config('SECRET_KEY')
    SECRET_KEY = os.getenv("SECRET_KEY")

### Activa el modo debug de la aplicaion
class DevelopmentConfig(Config):
    DEBUG = True
    
### Configuraciones extra
config = {
    'development': DevelopmentConfig
}