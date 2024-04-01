# Selrad Planner

### Описание

Cпециальный веб-сайт для управления планированием

### Технологии

- Python 3.11.7
- Django 4.3.3
- Nextjs

### Запуск проекта в dev-режиме

- Установите и активируйте виртуальное окружение

```
git clone git@github.com:Selrad-Utility-Tools/selrad-planner.git
python3 -m venv .venv
source .venv/bin/activate
```

- Установите зависимости из файла requirements.txt

```
pip install -r ./backend/requirements.txt
```

- Создайте файл .env в папке 'infra' проекта:

```
cd infra
cp .env.example .env
```

| VAR   | Description    |
|--------------- | --------------- |
| YANDEX_API_KEY   | API key for yandex map. Follow instructions [here](https://yandex.com/dev/commercial/doc/en/concepts/jsapi-geocoder) to setup. |
| DJANGO_SECRET_KEY | Secret key every django project provides. |
| DJANGO_DEBUG | True / False. (Optional) defaults to False. Setup project in Debug Mode |  
| DB_ENGINE | 'django.contrib.gis.db.backends.postgis'. PostGis, Postgres with geo extension |
| DB_NAME | 'postgres' |
| POSTGRES_USER | 'postgres' |
| POSTGRES_PASSWORD | 'postgres' |
| DB_HOST | 'db'. Same name as in docker-compose |
| DB_PORT | 5432 |

- Запустить Docker

#### Supa Fast Installation

```
cd infra
make build
```

```
cd infra
make flush
make loaddata
make superuser
```

#### Verbose Installation

```
cd infra
docker-compose -f docker-compose-dev.yml up -d --build
```

В Докере backend container-а:

- Создайте административного пользователя:

```
python3 manage.py createsuperuser
```

- Добавьте базу данных:

```
python3 manage.py loaddata ./data/worklist.json
python3 manage.py import_clients_csv
python3 manage.py import_managers_csv
```

### Запуск проекта в prod-режиме на сервере

Инструкция только при выкладавании на сервер.

- Удоствавертись что Docker-desktop версии > 4.26.0.

- Dockerfiles для backend-а и frontend-а должны быть сделаны для поддержки на linux-amd64

- Добавить новые изменения в docker image

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

- Зайти на сервер через ssh. Только у Амира есть доступ на сервер

```
ssh ubuntu@YOUR_SERVER_HOST

# Provide ssh key to gain access
```

- Обновить docker image-ы

```
cd selrad-planner
sudo docker pull hereugo/planner_backend
sudo docker pull hereugo/planner_frontend
```

- Перезапустить docker compose

```
cd selrad-planner
sudo docker compose -f docker-compose-prod.yml up -d --build
```

### Endpoint-ы

Чтобы просмотреть endpoint-ы API, запустите сервер и пройдите по ссылке:

- Swagger UI: <http://localhost/api/schema/swagger-ui/>
- Redoc: <http://localhost/api/schema/redoc/>

### Авторы

- Амир Нурмухамбетов [github profile](https://github.com/Hereugo)  
- Мансур Нурмухамбетов [github profile](https://github.com/nomomon)
