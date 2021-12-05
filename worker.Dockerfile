FROM python:3.8
RUN apt update && apt install python-dev -y
RUN apt install ffmpeg -y

WORKDIR /app

COPY requirements.txt /app
COPY src/. /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python consumer.py
