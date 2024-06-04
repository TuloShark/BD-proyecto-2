FROM python:3.11.6

WORKDIR /opt/app

ENV FLASK_APP index.py

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]