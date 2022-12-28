## Приложение: Планировщик задач.

стек (python3.9, Django, Postgres)

## Запуск проекта через docker-compose:
1. В директории создать файл `.env`:
    - `SECRET_KEY=`
    - `DEBUG=`
    - `POSTGRES_DB=` Имя db
    - `POSTGRES_USER=` Имя Пользователя
    - `POSTGRES_PASSWORD=` Пароль Пользователя
    - `VK_OAUTH2_KEY=`  id приложения vk
    - `VK_OAUTH2_SECRET=` ключ приложения vk
    - `BOT_TOKEN=` токен бота Телеграм

2.  Запустить командой `docker-compose up --build`

### Установка виртуальной среды для проекта:

1. Создать песочницу: `python -m virtualenv env`
2. Войти в виртуальную среду: `source env/bin/activate`
3. Обновить "pip" виртуальной среды: `pip install --upgrade pip`
4. Установить библиотеки проекта: `pip install -r requirements.txt`

### Запуск Postgres и передача констант в setings.py:

1. Создать файл `.env` в директории и записать в него:
    - `SECRET_KEY=`
    - `DEBUG=`
    - `POSTGRES_DB=` Имя db
    - `POSTGRES_USER=` Имя Пользователя
    - `POSTGRES_PASSWORD=` Пароль Пользователя
    - `POSTGRES_HOST=` Хост, по умолчанию "localhost"
    - `POSTGRES_PORT=` Порт по умолчанию "5432"
    - `VK_OAUTH2_KEY=`  id приложения vk
    - `VK_OAUTH2_SECRET=` ключ приложения vk
    - `BOT_TOKEN=` токен бота Телеграм
    
2. Запустить Postgres через докер и передать в него секретные константы: 
```
docker run --name django_db -e POSTGRES_PASSWORD= -e POSTGRES_DB= -e POSTGRES_USER= -p 5432:5432 -d postgres
```
    - Выполнить миграции  `manage.py migrate`.
    - Запустить Бэкэнд `manage.py runserver`.
    - Запустить бота `/manage.py runbot`
