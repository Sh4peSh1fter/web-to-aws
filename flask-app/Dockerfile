# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
RUN mkdir -p /usr/src/flask-app
WORKDIR /usr/src/flask-app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP_PORT 5000

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/flask-app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY entrypoint.sh /usr/src/flask-app/
RUN chmod u+x /usr/src/flask-app/entrypoint.sh

COPY . /usr/src/flask-app/

# run entrypoint.sh
CMD ["/bin/bash", "/usr/src/flask-app/entrypoint.sh"]