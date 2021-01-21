### Данный сервис предоставляет возможность активировать email при помощи четырёхзначного кода

### Запуск
```
docker-compose up --build
```

#### Для запуска необходимо в корне проекта создать файл ```.env```, со следующим содержимым
```
REDIS_HOST=redis
REDIS_PORT=6379

MAIL_PORT=465
MAIL_HOST=smtp.gmail.com
SENDER_MAIL=<email>
SENDER_PASSWORD=<password>
```

## Запросы

#### [POST]

- /generate-code - генерация кода и его отправка на email
- /activate-email - активация email


