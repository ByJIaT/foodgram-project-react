### Описание
https://foodgram.dynnamn.ru/

- login: superuser 
- password: superuser

Foodgram - здесь собираются любители еды и кулинарные энтузиасты, чтобы 
создавать, делиться и исследовать разнообразные кулинарные рецепты.
- Создавайте рецепты
- Добавляйте в избранное
- Подписывайтесь на авторов
- Скачивайте список покупок

---
### Технологии
- Python 3
- Django 4
- PostgreSQL 15
### Запуск на удаленном сервере
Создайте .env файл и заполните по образцу .env.example:
``` bash
touch .env
```
Скопируйте папку infra на сервер.
```bash
scp -r infra/ <server user>@<server IP>:/home/<server user>/foodgram/
```
```bash
cd infra
```
Запустите докер
```bash
sudo docker compose -f docker-compose.production.yml up -d
```

