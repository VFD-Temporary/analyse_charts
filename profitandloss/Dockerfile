FROM python:3.7-slim-stretch
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE profitandloss.settings

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000