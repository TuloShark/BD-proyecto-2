### Importaciones
from config import config
from src import init_app

### Configuracion
configuration = config['development']

### Aplicacion
app = init_app(configuration)

### Iniciar la aplicacion
if __name__ == '__main__':
    app.run()