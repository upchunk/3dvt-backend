FROM tensorflow/tensorflow:latest

# set work directory
WORKDIR /usr/src/app/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install postgresql postgresql-contrib ffmpeg libsm6 libxext6 netcat -y \
    && apt-get upgrade -y

# install requirements
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/backend/entrypoint.sh
RUN chmod +x /app/backend/entrypoint.sh

# copy project
COPY . .

# run entrypoint.prod.sh
ENTRYPOINT ["/app/backend/entrypoint.sh"]