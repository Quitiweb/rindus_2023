SHELL := /bin/bash

build:
	docker-compose -f docker-compose.yml up -d --build

up:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down

migrate:
	docker-compose -f docker-compose.yml run --rm web python manage.py migrate

shell:
	docker-compose -f docker-compose.yml run --rm web python manage.py shell

createsuperuser:
	docker-compose -f docker-compose.yml run --rm web python manage.py createsuperuser

import_data:
	docker-compose -f docker-compose.yml run --rm web python manage.py import_data

import_data_force_reset:
	docker-compose -f docker-compose.yml run --rm web python manage.py import_data --force_reset

bash:
	docker exec -it rindus_2023-web-1 bash

test:
	docker-compose -f docker-compose.yml run --rm web python manage.py test

coverage:
	docker exec -it rindus_2023-web-1 coverage run --source='.' manage.py test blog

report:
	docker exec -it rindus_2023-web-1 coverage report

initial: ## Initialise the project
	@make build
	@make migrate
