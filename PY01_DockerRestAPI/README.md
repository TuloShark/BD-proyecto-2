# PY01_DockerRestAPI

Backend de encuestas con docker integrando protocolos http y sistemas como MongoDB, PostgreSQL y Redis.

## Instrucciones de Uso

* git clone <URL del repositorio> (Necesitas realizar una copia del programa de github)
* El siguiente es el url: https://github.com/EstebanPP/PY01_DockerRestAPI.git

## Construir y Desplegar la Aplicación

Despues de realizar el git clone, ahora se necesitara construir la imagen:

* "cd PY01_DockerRestAPI"
* "docker-compose up --build"

## Pruebas

Para las pruebas se debe de realizar el docker compose normal primeramente

* docker-compose -f docker-compose.yml up --build (si no se ha construido la imagen anteriormente)
* Detener el contendor de py01_dockerrestapi
* docker-compose -f docker-compose.test.yml -p py01_docker_rest_api_test up --build

Si da error de conexcion inicialmente volver a iniciar el servicio de test-1 para que se ejecuten nuevamente las pruebas, esto pasa debido a que todavia no se han iniciado los servicios de la api y bases de datos.

## Para el uso

* Dentro del repositorio se encuentra un archivo postman con todas las rutas posibles para la alpicacion
* Es necesario saber que algunas de estas rutas ocupan un token de usuario (se consigue luego de hacer login)
* el token se debe de pasar dentro del json de la consulta
