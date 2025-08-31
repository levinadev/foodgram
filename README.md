# Foodgram

Веб-приложение для публикации рецептов.  
Пользователи могут создавать и редактировать рецепты, добавлять их в избранное и формировать список покупок.  

## Возможности
- Регистрация и авторизация пользователей  
- Создание, редактирование и удаление рецептов  
- Добавление рецептов в избранное
- Фильтрация рецептов по тегам
- Формирование списка покупок

## Установка и запуск

1. Клонирование репозитория:

```
git clone https://github.com/levinadev/foodgram.git
```

3. Запуск контейнеров:

```
docker-compose -f docker-compose.production.yml up -d
```

4. Остановка контейнеров:

```
docker-compose -f docker-compose.production.yml down
```

## Технологии
- Python 3, Django, DRF  
- PostgreSQL  
- Docker, Docker Compose  
- Nginx, Gunicorn

## Автор

- Имя: Анна
- Email: anna45dd@yandex.ru
- GitHub: https://github.com/levinadev