## Приложение: Планировщик задач.

### Установка виртуальной среды для проэкта:

1. Создать песочницу: `python -m virtualenv env`
2. Войти в виртуальную среду: `source env/bin/activate`
3. Обновить "pip" виртуальной среды: `pip install --upgrade pip`
4. Установить библиотеки проэкта: `pip install -r requirements.txt`


### Запуск Postgres и передача констант в setings.py:

1. Создать файл `.env`  и записать в него:
    - `SECRET_KEY=`
    - `DEBUG=`
    - `POSTGRES_DB=` Имя db
    - `POSTGRES_USER=` Имя Пользователя
    - `POSTGRES_PASSWORD=` Пароль Пользователя
    - `POSTGRES_HOST=` Хост постгрес, по умолчанию "localhost"
    - `POSTGRES_PORT=` Порт по умолчанию "5432"

2. Запустить Postgres через докер и передать в него секретные константы: 
```
docker run --name django_db -e POSTGRES_PASSWORD= -e POSTGRES_DB= -e POSTGRES_USER= -p 5432:5432 -d postgres
```

### Запуск проекта:

1. Записать миграции в postgres `manage.py migrate`
3. Запустить сервер `manage.py runserver`




