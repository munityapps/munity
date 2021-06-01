#!/bin/sh

docker-compose up -d
docker-compose exec db psql -U admin -c "create database munity"
docker-compose exec api python manage.py migrate
docker-compose exec api python manage.py init_db
docker-compose exec api python manage.py createsuperuser
