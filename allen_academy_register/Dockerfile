FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE=allen_academy_register.settings

ENV DockerHOME=/usr/src/app
RUN mkdir -p $DockerHOME
COPY . $DockerHOME
WORKDIR $DockerHOME

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2-binary
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000 > $LOGFILE 2>&1
CMD python manage.py makemigrations
CMD python manage.py migrate