FROM python:3.10
ENV DockerHOME=/usr/src/app
RUN mkdir -p $DockerHOME
COPY . $DockerHOME
WORKDIR $DockerHOME
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=AllenAcademy.settings
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install --upgrade pip
RUN pip install -r requirements.txt