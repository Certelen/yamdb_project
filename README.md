# API для YaMDb в контейнере Docker.

[![Django-app workflow](https://github.com/Certelen/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Certelen/yamdb_final/actions/workflows/yamdb_workflow.yml)

## Описание
Проект YaMDb функционирует через API и собирает отзывы (Review) пользователей на произведения (Titles). 
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории (Category). 
Произведению может быть присвоен жанр (Genre). 
Новые жанры и категории может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок высчитывается средняя оценка произведения.
На отзывы можно оставлять комментарии (Comment).


## Технологии
- Python 3.7
- Django 3.2
- Docker
- nginx
- DRF
- JWT

# Установка
## Копирование репозитория
Клонируем репозиторий и переходим в директорию infra:
```
~ git clone git@github.com:Studio-Yandex-Practicum-Hackathons/cafe_azu_bot_2.git
~ cd ./cafe_azu_bot_2/infra/
```
Требуется изменить server_name и listen в ./infra/nginx/default.conf, ports в docker-compose.yml

## Подготовка боевого сервера:
1. Перейдите на боевой сервер:
```
ssh username@server_address
```
2. Обновите индекс пакетов APT:
```
sudo apt update
```
и обновите установленные в системе пакеты и установите обновления безопасности:
```
sudo apt upgrade -y
```
Создайте папку `nginx`:
```
mkdir nginx
``` 
Скопируйте файлы docker-compose.yaml, nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml, home/<ваш_username>/nginx/default.conf соответственно:
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
Установите Docker и Docker-compose:
```
sudo apt install docker.io
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
Проверьте правильность установки Docker-compose:
```
sudo docker-compose --version
```
На боевом сервере создайте файл .env:
```
touch .env
```
и заполните переменные окружения
```
nano .env
- DB_ENGINE=django.db.backends.postgresql #Указываем, что работаем с postgresql
- DB_NAME=postgres # имя базы данных
- POSTGRES_USER=postgres # логин для подключения к базе данных
- POSTGRES_PASSWORD=xxxyyyzzz # пароль для подключения к БД
- DB_HOST=db # название сервиса (контейнера)
- DB_PORT=5432 # порт для подключения к БД
- TOKEN=p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs # проверочный токен
```

## Развертывание проекта с помощью Docker:
Разворачиваем контейнеры в фоновом режиме из папки infra:
```
sudo docker compose up -d
```
При первом запуске выполняем миграции:
```
sudo docker compose exec backend python manage.py migrate
```
И собираем статику:
```
sudo docker compose exec backend python manage.py collectstatic --no-input
```
Создаем суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```

## Функционал:
###### USERS
- Получить список всех пользователей (ADMIN)
- Создание пользователя (ADMIN)
- Получить пользователя по username (ADMIN)
- Изменить данные пользователя по username (ADMIN)
- Удалить пользователя по username (ADMIN)
- Получить данные своей учетной записи (OWNER, ADMIN)
- Изменить данные своей учетной записи (OWNER, ADMIN)
###### AUTH
- Отправление confirmation_code на переданный email (ANY)
- Получение JWT-токена в обмен на email и confirmation_code (ANY)
###### CATEGORIES
- Получить список всех категорий (ANY)
- Создать категорию (ADMIN)
- Удалить категорию (ADMIN)
###### GENRES
- Получить список всех жанров (ANY)
- Создать жанр (ADMIN)
- Удалить жанр (ADMIN)
###### TITLES
- Получить список всех объектов (ANY)
- Создать произведение для отзывов (ADMIN)
- Информация об объекте (ANY)
- Обновить информацию об объекте (ADMIN)
- Удалить произведение (ADMIN)
###### REVIEWS
- Получить список всех отзывов (ANY)
- Создать новый отзыв (AUTH)
- Получить отзыв по id (ANY)
- Частично обновить отзыв по id (OWNER, MODERATOR, ADMIN)
- Удалить отзыв по id (OWNER, MODERATOR, ADMIN)
###### COMMENTS
- Получить список всех комментариев к отзыву по id (ANY)
- Создать новый комментарий для отзыва (AUTH)
- Получить комментарий для отзыва по id (ANY)
- Частично обновить комментарий к отзыву по id (OWNER, MODERATOR, ADMIN)
- Удалить комментарий к отзыву по id (OWNER, MODERATOR, ADMIN)

## REDOC
Документация к API доступна по адресу 'http://127.0.0.1:8000/redoc/'

### Пример запроса
Получение списка всех произведений - GET 'http://127.0.0.1:8000/api/v1/titles/'

Добавление нового отзыва - POST 'http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/'

С телом запроса:

{
  "text": "string",
  "score": 1
}

Изменение данных своей учетной записи - PATCH 'http://127.0.0.1:8000/api/v1/users/me/'

С телом запроса:

{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}


### Самостоятельная регистрация новых пользователей

##### Получаем confirmation_code

Отправляем POST-запрос на адрес 'http://127.0.0.1:8000/api/v1/auth/signup/'

- Обязательные поля: `email`, `username`

Код подтверждения будет доступен в папке проекта `api_yamdb\sent_emails\file.log`

##### Получаем token
Отправляем POST-запрос для получения JWT-токена на адрес 'http://127.0.0.1:8000/api/v1/auth/token/'.
- Обязательные поля: `username`, `confirmation_code`


## Developer

Команда разработки:
- :white_check_mark: [Коломейцев Дмитрий(в роли Python-разработчика Тимлид - разработчик 1)](https://github.com/Certelen)
- :white_check_mark: [Борель Николай(в роли Python-разработчика - разработчик 2)](https://github.com/nikolaiborel)
- :white_check_mark: [Минин Георгий(в роли Python-разработчика - разработчик 3)](https://github.com/georgy-min)


Проект сделан в рамках учебного процесса по специализации Python-разработчик (back-end) Яндекс.Практикум.
