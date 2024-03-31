#!/bin/bash

reset_db() {
rm -rf user/migrations
rm -rf user/__pycache__
rm -rf property/__pycache__
rm -rf property/migrations
rm -rf product/__pycache__
rm -rf product/migrations
mysql \
  --user="airbnb" \
  --password="Thaianh171193" \
  --execute="DROP DATABASE django_airbnb_db; CREATE DATABASE django_airbnb_db;"
}

migrate() {
ENV_TYPE=dev python manage.py makemigrations user property product
ENV_TYPE=dev python manage.py migrate
}

runserver() {
ENV_TYPE=dev python manage.py runserver
}

createsuperuser() {
ENV_TYPE=dev python manage.py createsuperuser
}

shell() {
ENV_TYPE=dev python manage.py shell
}

$@