
FROM python:3.10-slim


WORKDIR /app


RUN apt-get update && apt-get install -y python3-venv && apt-get clean


RUN python3 -m venv /app/venv


RUN /app/venv/bin/pip install --upgrade pip


COPY . .


RUN /app/venv/bin/pip install django pillow django-widget-tweaks


EXPOSE 8000


CMD ["/app/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
