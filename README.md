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
cd backend
pip install -r requirements.txt
```

- В папке с файлом manage.py выполните команду:

```
python3 manage.py runserver
```

### Авторы

- Амир Нурмухамбетов [github profile](https://github.com/Hereugo)  

### TODO

- [ ] карта hover на точке показать всех ост клиентов на тот же день
- [ ] Включать / выключать колонки в таблице
- [ ] Кнопка "отчет"
- [ ] Хостинг
- [ ] Докеризация
- [ ] Yandex карта имплеминтация
- [ ] Тесты (optional)
