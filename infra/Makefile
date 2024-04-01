ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env
endif

build:
	docker-compose -f docker-compose-dev.yml up --build -d --remove-orphans
up:
	docker-compose -f docker-compose-dev.yml up -d
down:
	docker-compose -f docker-compose-dev.yml down
logs:
	docker-compose -f docker-compose-dev.yml logs
migrate:
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py migrate

superuser:
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py createsuperuser	
loaddata:
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py loaddata ./data/worklist.json; \
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py import_clients_csv; \
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py import_managers_csv

flush:
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py flush

volume:
	docker volume inspect selrad-planner-dev_db

shell:
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py shell

