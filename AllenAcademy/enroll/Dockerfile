FROM allenacademy_web:latest
COPY . $DockerHOME
WORKDIR $DockerHOME
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]