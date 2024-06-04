from pyspark.sql import SparkSession
from neo4j import GraphDatabase

# Inicializar la sesión de Spark
spark = SparkSession.builder \
    .appName("ConnectivityAnalysis") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Leer los datos de las respuestas desde una fuente (por ejemplo, un archivo JSON o una base de datos)
responses_df = spark.read.json("/app/spark_jobs/data/responses.json")

# Transformar los datos y crear un grafo
graph = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "test"))

def create_graph(tx, data):
    for row in data.collect():
        tx.run("MERGE (p:Person {id: $id})", id=row['respondent_id'])
        for response in row['responses']:
            tx.run("MATCH (p:Person {id: $id}) "
                   "MERGE (r:Response {text: $text}) "
                   "MERGE (p)-[:ANSWERED]->(r)",
                   id=row['respondent_id'], text=response['text'])

with graph.session() as session:
    session.write_transaction(create_graph, responses_df)

spark.stop()
