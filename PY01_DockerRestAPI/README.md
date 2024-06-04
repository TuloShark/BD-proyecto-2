# PY01_DockerRestAPI

Backend de encuestas con docker integrando protocolos http y sistemas como MongoDB, PostgreSQL, Redis, y Apache Spark.

## Instrucciones de Uso

* git clone <URL del repositorio> (Necesitas realizar una copia del programa de github)
* El siguiente es el url: https://github.com/EstebanPP/PY01_DockerRestAPI.git

## Construir y Desplegar la Aplicación

Después de realizar el git clone, ahora se necesitará construir la imagen:

* "cd PY01_DockerRestAPI"
* "docker-compose up --build"

## Pruebas

Para las pruebas se debe de realizar el docker compose normal primeramente

* docker-compose -f docker-compose.yml up --build (si no se ha construido la imagen anteriormente)
* Detener el contenedor de py01_docker_rest_api
* docker-compose -f docker-compose.test.yml -p py01_docker_rest_api_test up --build

Si da error de conexión inicialmente, volver a iniciar el servicio de test-1 para que se ejecuten nuevamente las pruebas. Esto pasa debido a que todavía no se han iniciado los servicios de la API y bases de datos.

## Para el uso

* Dentro del repositorio se encuentra un archivo postman con todas las rutas posibles para la aplicación
* Es necesario saber que algunas de estas rutas ocupan un token de usuario (se consigue luego de hacer login)
* El token se debe pasar dentro del JSON de la consulta

## Configuración y Ejecución de Apache Spark

### Requisitos Previos
- Docker
- Docker Compose

### Configuración

1. Añadir los servicios de Apache Spark en el archivo `docker-compose.yml`.
2. Crear un directorio `spark_jobs` y añadir el script `process_responses.py`.

### Ejecución

Para ejecutar el script de Spark:

```sh
docker-compose up --build
