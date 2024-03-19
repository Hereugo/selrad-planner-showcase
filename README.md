# Selrad Planner

### Описание

Cпециальный веб-сайт для управления планированием

### Технологии

- Javascript
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
pip install -r requirements.txt
```

- Создайте файл .env в корневой папке проекта:

```
cp .env.example .env
```

| VAR   | Description    |
|--------------- | --------------- |
| YANDEX_API_KEY   | API key for yandex map. Follow instructions [here](https://yandex.com/dev/commercial/doc/en/concepts/jsapi-geocoder) to setup. |
| DJANGO_SECRET_KEY | Secret key every django project provides. |
| DJANGO_DEBUG | True / False. (Optional) defaults to False. Setup project in Debug Mode |  

- Установите зависимости JavaScript

```
npm i
```

- Создайте административного пользователя:

```
python3 manage.py createsuperuser
```

- Добавьте базу данных:

```
python3 manage.py loaddata data/worklist.json
python3 manage.py import_clients_csv
```

- Запустите сервер:

В папке с файлом manage.py выполните команду:

```
python3 manage.py runserver
```

### Авторы

- Амир Нурмухамбетов [github profile](https://github.com/Hereugo)  
- Мансур Нурмухамбетов [github profile](https://github.com/nomomon)

### TODO

- [ ] карта hover на точке показать всех ост клиентов на тот же день
- [ ] Включать / выключать колонки в таблице
- [ ] Хостинг
- [ ] Докеризация
