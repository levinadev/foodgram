# Foodgram

![CI/CD](https://github.com/levinadev/foodgram/actions/workflows/main.yml/badge.svg)

**Foodgram** — это онлайн-сервис для публикации рецептов.

## Демо
- [Развернутый проект](https://foodgram.levinadev.ru/)  
- [Административная панель](https://foodgram.levinadev.ru/admin/)  
- [Документация к API](https://foodgram.levinadev.ru/api/docs/)

## Возможности
- Регистрация и авторизация пользователей  
- Смена пароля и загрузка аватара пользователя
- Создание, редактирование и удаление рецептов  
- Добавление рецептов в избранное
- Подписка на других пользователей
- Фильтрация рецептов по тегам
- Формирование списка покупок 
- Подсчет ингредиентов

## Установка и запуск локально

1. Клонировать репозиторий:
```
git clone https://github.com/levinadev/foodgram.git
cd foodgram
```

2. Создать файл `.env` в корне проекта на основе шаблона:
```
cp .env.example .env
```
При необходимости измените значения переменных в `.env` (например, `DJANGO_SECRET_KEY` и `DJANGO_ALLOWED_HOSTS`) под ваше окружение.

3. Запуск:
```
docker-compose -f docker-compose.production.yml up -d
```

4. После этого проект будет доступен по адресу: http://127.0.0.1:8000/

5. Остановка контейнеров:

```
docker-compose -f docker-compose.production.yml down
```

## Технологии
- **Backend:** Python 3, Django, Django REST Framework, Djoser  
- **Database:** PostgreSQL  
- **Frontend:** React (сборка)  
- **Web-server:** Nginx, Gunicorn  
- **Инфраструктура:** Docker, Docker Compose  

## Автор

- Имя: Анна
- Email: anna45dd@yandex.ru
- GitHub: https://github.com/levinadev