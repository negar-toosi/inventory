include .env

ifeq ($(DOCKER_COMPOSE_ENV), dev)
	DOCKER_COMPOSE_FILE := docker-compose.dev.yaml
else ifeq ($(DOCKER_COMPOSE_ENV), stage)
	DOCKER_COMPOSE_FILE := docker-compose.stage.yaml
else ifeq ($(DOCKER_COMPOSE_ENV), prod)
	DOCKER_COMPOSE_FILE := docker-compose.prod.yaml
endif


.PHONY: lint runserver check makemigrations migrate \
	syncdb ps build up up-build down clean backend-logs \
	backend-bash createsuperuser test

lint:
	@ echo "-> running ruff check --fix..."
	@ ruff check --fix

	@ echo "-> running ruff format..."
	@ ruff format

runserver:
	uv run manage.py runserver

check:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec -it backend python manage.py check

makemigrations:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec -it backend python manage.py makemigrations

migrate:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec -it backend python manage.py migrate

syncdb: makemigrations migrate

ps:
	docker compose -f $(DOCKER_COMPOSE_FILE) ps -a

build:
	docker compose -f $(DOCKER_COMPOSE_FILE) build

up:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

up-build:
	docker compose -f $(DOCKER_COMPOSE_FILE) up --build -d

down:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

restart:
	docker compose -f $(DOCKER_COMPOSE_FILE) restart

clean: down
	docker compose -f $(DOCKER_COMPOSE_FILE) down --remove-orphans
	docker compose -f $(DOCKER_COMPOSE_FILE) rm -v -s
	docker compose -f $(DOCKER_COMPOSE_FILE) down -v

backend-bash:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec -it backend bash

backend-shell:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec -it backend python manage.py shell

backend-logs:
	docker compose -f $(DOCKER_COMPOSE_FILE) logs backend -f

createsuperuser:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec -it backend \
		env DJANGO_SUPERUSER_PASSWORD=$(DJANGO_SUPERUSER_PASSWORD) \
		python manage.py createsuperuser \
		--noinput \
		--username root\
		--email root@gmail.com
	@ echo "-> superuser created with username: root & password: $(DJANGO_SUPERUSER_PASSWORD)"


collectstatic:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec -it backend python manage.py collectstatic --noinput

