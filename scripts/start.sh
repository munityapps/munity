#!/bin/bash

set -e
set -x

### Start Munity services
docker-compose up -d

### Create your database and migrate
docker-compose exec db psql -U munityapps -c "create database munity"
docker-compose exec api python manage.py migrate
docker-compose restart api

### Create your first user
docker-compose exec api python manage.py createsuperuser

### Start frontend
cd app ; yarn install ; yarn start

### Have fun :)
