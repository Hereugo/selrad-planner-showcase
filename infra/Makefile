ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env
endif


ifeq ($(strip $(d)),)
	d := $(shell date +"%d-%m-%Y")
endif

DEV_FILE := docker-compose-dev.yml
BACKEND := backend
DB_VOLUME := selrad-planner-dev_db_value

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
	docker-compose -f $(DEV_FILE) exec $(BACKEND) python3 manage.py migrate

superuser:
	docker-compose -f $(DEV_FILE) exec $(BACKEND) python3 manage.py createsuperuser	

#=============================

# Executes django loaddata on backend docker container, loadding values to db from a file on the container
loaddata:
	docker-compose -f $(DEV_FILE) exec $(BACKEND) python3 manage.py loaddata ./data/$(d).json 

# Executes django dumpdata on backend docker container, output is treated as input to a local file
# Use DATA variable to change file name, by default current date is used. 
dumpdata:
	docker-compose -f $(DEV_FILE) exec $(BACKEND) python3 manage.py dumpdata -e contenttypes -e auth > ../backend/data/$(d).json

#=============================

flush:
	docker-compose -f $(DEV_FILE) exec $(BACKEND) python3 manage.py flush

volume_down:
	docker volume rm $(DB_VOLUME)
volume:
	docker volume inspect $(DB_VOLUME)

#=============================

bash:
	docker-compose -f $(DEV_FILE) exec $(BACKEND) bash

shell:
	docker-compose -f $(DEV_FILE) exec $(BACKEND) python3 manage.py shell

