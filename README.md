# YaMDb

## About

API backend for online database of information and reviews about movies, music, books, etc.

### Tech stack

- Django REST Framework
- Postgres DB
- JWT authorization
- Docker

## Getting started

### Set the environment variables

Set your DB data in `.env.example` file and save it as `.env`

### Install Docker

For installation guide, refer to [official documentation](https://docs.docker.com/engine/install/)

### Build the Docker container

`docker-compose build`

### Start the Docker container

`docker-compose up`

### Create Django superuser

`docker compose run web python manage.py createsuperuser`

### Import data from .json file

`docker-compose run web python manage.py loaddata path/to/your/json`

You can also load test data:

`docker-compose run web python manage.py loaddata fixtures.json`