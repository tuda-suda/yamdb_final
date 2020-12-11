FROM python:3.8-alpine

WORKDIR /code
COPY /. .

# Install build tools and dependencies
RUN apk update && apk add postgresql postgresql-contrib python3-dev musl-dev \          
    && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

RUN python manage.py collectstatic --noinput
RUN pip install -r requirements.txt

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
