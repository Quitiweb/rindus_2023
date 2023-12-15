SHELL := /bin/bash

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

migrate:
	docker-compose run web python manage.py migrate

shell:
	docker-compose run web python manage.py shell

createsuperuser:
	docker-compose run web python manage.py createsuperuser

bash:
	docker-compose run web bash
