### Запуск
```
docker-compose up --build
```

#### Запуск в режиме отладки
```
docker-compose -f docker-compose.dev.yml up --build
```

#### Для запуска необходимо в корне проекта создать файл ```.env```, со следующим содержимым
```
REDIS_HOST=redis
REDIS_PORT=6379
ALLOW_ORIGINS=http://localhost:8080,

MAIL_PORT=465
MAIL_HOST=smtp.gmail.com
SENDER_MAIL=<email>
SENDER_PASSWORD=<password>

ADMIN_USERNAME=<username>
ADMIN_PASSWORD=<password>
```

## Запросы

#### [GET]

- /generate-code - генерация кода и его отправка на email
  
#### [POST]
- /activate-email - активация email
- /load-emails - получить список email


