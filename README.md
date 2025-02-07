# Selrad Planner

## TODO:

- [ ] add pytest
- [ ] memory optimization 

### Описание

Cпециальный веб-сайт для управления планированием

### Технологии

-   Python 3.11.7
-   Django 4.3.3
-   Nextjs

### Запуск проекта в dev-режиме

-   Установите и активируйте виртуальное окружение

```
git clone git@github.com:Selrad-Utility-Tools/selrad-planner.git
python3 -m venv .venv
source .venv/bin/activate
```

-   Установите зависимости из файла requirements.txt

```
pip install -r ./backend/requirements.txt
```

-   Создайте файл .env в папке 'infra' проекта:

```
cd infra
cp .env.example .env
```
-   Запустить Docker

#### Supa Fast Installation

```
cd infra
make build
```

```
cd infra
make flush
make migrate
make loaddata
make superuser
```

#### Verbose Installation

```
cd infra
docker-compose -f docker-compose-dev.yml up -d --build
```

В Докере backend container-а:

-   Добавьте базу данных:

```
python3 manage.py flush
python3 manage.py loaddata ./data/worklist.json
python3 manage.py loaddata ./data/clients_w_address.json
python3 manage.py import_managers_csv
```

-   Создайте административного пользователя:

```
python3 manage.py createsuperuser
```

### Запуск проекта в prod-режиме на сервере

Инструкция только при выкладавании на сервер.

-   Удоствавертись что Docker-desktop версии > 4.26.0.

-   Dockerfiles для backend-а и frontend-а должны быть сделаны для поддержки на linux-amd64

-   Добавить новые изменения в docker image

```
cd backend
docker build -t hereugo/planner_backend .
docker push hereugo/planner_backend
```

```
cd frontend
docker build -t hereugo/planner_frontend .
docker push hereugo/planner_frontend
```

-   Зайти на сервер через ssh. Только у Амира есть доступ на сервер

```
ssh ubuntu@YOUR_SERVER_HOST

# Provide ssh key to gain access
```

-   Обновить docker image-ы

```
cd selrad-planner
sudo docker pull hereugo/planner_backend
sudo docker pull hereugo/planner_frontend
```

-   Перезапустить docker compose

```
cd selrad-planner
sudo docker compose -f docker-compose-prod.yml up -d --build
```

### Выгрузка данных с prod на local

Enter remote server:

```
ssh ubuntu@YOUR_SERVER_HOST
# provide ssh key to gain access
```

Goto backend's container terminal:

```
cd selrad-planner
sudo docker compose -f docker-compose-prod.yml exec backend bash
```

Dump data to a local file:

```
python3 manage.py dumpdata -e contenttypes -e auth > <current-date>.json
```

Copy file from backend's container to remote server:

```
sudo docker compose -f docker-compose-prod.yml cp backend:/app/<current-date>.json ./data/
```

Copy file from remote server to local computer:

```
scp ubuntu@YOUR_SERVER_HOST:./selrad-planner/data/<current-date>.json ./
```

Change Makefile loaddata command to point at a new file:

```
loaddata:
 docker-compose -f docker-compose-dev.yml exec backend python3 manage.py loaddata ./data/<current-date>.json
```

Rebuild local containers with brand new data:

```
cd infra
make build
make down
make volume_down
make build
make migrate
make superuser
make loaddata
```

### Endpoint-ы

Чтобы просмотреть endpoint-ы API, запустите сервер и пройдите по ссылке:

-   Swagger UI: <http://localhost/api/schema/swagger-ui/>
-   Redoc: <http://localhost/api/schema/redoc/>

### Авторы

-   Амир Нурмухамбетов [github profile](https://github.com/Hereugo)
-   Мансур Нурмухамбетов [github profile](https://github.com/nomomon)
