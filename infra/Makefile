ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env
endif


ifeq ($(strip $(d)),)
	d := $(shell date +"%d-%m-%Y")
endif

DEV_FILE := docker-compose-dev.yml
DOCKER_COMPOSE_NAME := selrad-planner-dev

BACKEND_CON := backend
DATABASE_CON := db

DATABASE_VOLUME := $(DOCKER_COMPOSE_NAME)_db_value
STATIC_VOLUME := $(DOCKER_COMPOSE_NAME)_static_value

#============================

build:
	docker-compose -f $(DEV_FILE) up $(c) --build -d --remove-orphans
up:
	docker-compose -f $(DEV_FILE) up $(c) -d
down:
	docker-compose -f $(DEV_FILE) down $(c)
stop:
	docker-compose -f $(DEV_FILE) stop $(c)

restart:
	docker-compose -f $(DEV_FILE) stop $(c)
	docker-compose -f $(DEV_FILE) up -d $(c)

ps:
	docker-compose -f $(DEV_FILE) ps

logs:
	docker-compose -f $(DEV_FILE) logs $(c) --follow --tail=100

#=============================

migrate:
	docker-compose -f $(DEV_FILE) exec $(BACKEND_CON) python3 manage.py migrate

migrate_fake:
	docker-compose -f $(DEV_FILE) exec $(BACKEND_CON) python3 manage.py migrate --fake-initial

superuser:
	docker-compose -f $(DEV_FILE) exec $(BACKEND_CON) python3 manage.py createsuperuser	

#=============================

collectstatic:
	docker-compose -f $(DEV_FILE) exec $(BACKEND_CON) python3 manage.py collectstatic 

loaddata:
	docker-compose -f $(DEV_FILE) exec $(BACKEND_CON) python3 manage.py loaddata ./data/$(d).json 

dumpdata:
	docker-compose -f $(DEV_FILE) exec $(BACKEND_CON) python3 manage.py dumpdata -e contenttypes -e auth > ../backend/data/$(d).json

pg_dumpdata:
	docker-compose -f $(DEV_FILE) exec $(DATABASE_CON) pg_dump --username=$(POSTGRES_USER) --password --dbname=$(DB_NAME) > ../backend/backup/$(d)-local.sql

pg_loaddata:
	docker-compose -f $(DEV_FILE) exec -T $(DATABASE_CON) psql --username=$(POSTGRES_USER) --password --dbname=$(DB_NAME) < ../backend/backups/$(d).sql

#=============================

flush:
	docker-compose -f $(DEV_FILE) exec $(BACKEND_CON) python3 manage.py flush

volume_down:
	docker volume rm $(DATABASE_VOLUME)

static_down:
	docker volume rm $(STATIC_VOLUME)

volume:
	docker volume inspect $(DATABASE_VOLUME)

#=============================

bash:
	docker-compose -f $(DEV_FILE) exec $(BACKEND_CON) bash

shell:
	docker-compose -f $(DEV_FILE) exec $(BACKEND_CON) python3 manage.py shell

