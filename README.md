# Selrad Planner

### Описание

Cпециальный веб-сайт для управления планированием

### Технологии

- Python 3.11.7
- Django 4.3.3

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

- Запустить Docker

'''
cd infra
docker-compose -f docker-compose-dev.yml up -d --build
'''

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

### Endpoint-ы

Чтобы просмотреть endpoint-ы API, запустите сервер и пройдите по ссылке:

- Swagger UI: <http://localhost/api/schema/swagger-ui/>
- Redoc: <http://localhost/api/schema/redoc/>

### Авторы

- Амир Нурмухамбетов [github profile](https://github.com/Hereugo)  
- Мансур Нурмухамбетов [github profile](https://github.com/nomomon)
