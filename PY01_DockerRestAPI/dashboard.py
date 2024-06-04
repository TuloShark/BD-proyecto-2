import streamlit as st
import pandas as pd

# Leer los datos procesados
data = pd.read_json("/app/spark_jobs/data/processed_responses.json")

# Crear un dashboard sencillo
st.title("Dashboard de Encuestas")
st.write("Promedio de tiempo de respuesta por encuesta")
st.bar_chart(data.groupby('survey_id')['response_time'].mean())
