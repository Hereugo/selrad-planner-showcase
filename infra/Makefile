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
	docker-compose -f docker-compose-dev.yml logs --follow

migrate:
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py migrate

superuser:
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py createsuperuser	
loaddata:
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py loaddata ./data/08-05-2024.json; 

flush:
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py flush

static_down:
	docker volume rm selrad-planner-dev_static_value -f

volume_down:
	docker volume rm selrad-planner-dev_db_value

volume:
	docker volume inspect selrad-planner-dev_db_value

bash:
	docker-compose -f docker-compose-dev.yml exec backend bash
shell:
	docker-compose -f docker-compose-dev.yml exec backend python3 manage.py shell

