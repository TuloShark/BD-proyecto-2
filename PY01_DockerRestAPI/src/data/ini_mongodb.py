from pymongo import MongoClient, ASCENDING
import os
from bson import ObjectId
import datetime

mongo_username = 'wandertulojimenez'  # Asegúrate de que esto es correcto
mongo_password = 'Esy9UlXjfIoBVn7v'   # Asegúrate de que esto es correcto
mongo_host = 'localhost'  # Usa 'localhost' si te conectas desde fuera de Docker
mongo_port = '27017'
mongo_db_name = 'ProyectoBases2'

mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db_name}?authSource=admin"


client = MongoClient(mongo_uri)
db = client[mongo_db_name]

def insert_test_surveys(db):
    # Lista de encuestas de prueba
    test_surveys = [
        {
            "_id": ObjectId(),  # Genera un nuevo ObjectId
            "title": "Encuesta de Satisfacción del Cliente",
            "description": "Mide la satisfacción del cliente con los servicios prestados.",
            "is_published": False,
            "created_at": datetime.datetime.utcnow()
        },
        {
            "_id": ObjectId(),  # Genera un nuevo ObjectId
            "title": "Encuesta de Evaluación de Productos",
            "description": "Recolecta opiniones sobre los productos ofrecidos.",
            "is_published": False,
            "created_at": datetime.datetime.utcnow()
        }
        # Puedes agregar más encuestas aquí...
    ]

    # Insertar datos en la colección 'surveys'
    inserted_ids = db.surveys.insert_many(test_surveys).inserted_ids
    return inserted_ids

# Llamamos a la función después de la creación de la colección
if __name__ == "__main__":
    inserted_ids = insert_test_surveys(db)
    print(f"Encuestas de prueba insertadas con éxito, IDs: {inserted_ids}")
