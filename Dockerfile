FROM tensorflow/tensorflow:latest

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install postgresql postgresql-contrib -y \
    && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .