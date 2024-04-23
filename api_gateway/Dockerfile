FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE=api_gateway.settings

ENV DockerHOME=/usr/src/app
RUN mkdir -p $DockerHOME
COPY . $DockerHOME
WORKDIR $DockerHOME

RUN apt-get update \
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000