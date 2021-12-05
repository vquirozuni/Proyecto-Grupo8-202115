FROM python:3.8
RUN apt update && apt install python-dev -y

WORKDIR /app
COPY requirements.txt /app
COPY src/. /app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080
CMD python app.py
