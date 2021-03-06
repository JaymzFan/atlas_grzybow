FROM python:3.8

WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD flask run --host=0.0.0.0 --port=$PORT
EXPOSE $PORT