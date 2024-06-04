### Importaciones
from config import config
from src import init_app
from kafka_consumer import start_consumer
import threading

### Configuracion
configuration = config['development']

### Aplicacion
app = init_app(configuration)

### Iniciar la aplicacion
if __name__ == '__main__':
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.start()
    app.run()
