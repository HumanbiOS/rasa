FROM python:3.7-slim-buster

COPY pure_nlu/* app/
COPY requirements.txt app/requirements.txt
WORKDIR /app

RUN pip3 install -r requirements.txt

# Launch
CMD ["rasa", "run", "--enable-api", "-m", "models/latest.tar.gz"]

