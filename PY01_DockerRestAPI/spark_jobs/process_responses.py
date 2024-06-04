from pyspark.sql import SparkSession

# Inicializar la sesión de Spark
spark = SparkSession.builder \
    .appName("SurveyResponsesProcessor") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Leer los datos de las respuestas desde una fuente (por ejemplo, un archivo JSON o una base de datos)
# Aquí, se asume que hay un archivo JSON con respuestas de encuestas
responses_df = spark.read.json("/app/spark_jobs/data/responses.json")

# Realizar algunas transformaciones o análisis
# Ejemplo: Calcular el tiempo promedio de respuesta
avg_response_time = responses_df.groupBy("survey_id").avg("response_time")

# Mostrar el resultado
avg_response_time.show()

# Guardar el resultado de vuelta a un almacenamiento o base de datos
avg_response_time.write.mode("overwrite").json("/app/spark_jobs/data/processed_responses.json")

# Detener la sesión de Spark
spark.stop()
