# Foodgram

![CI/CD](https://github.com/levinadev/foodgram/actions/workflows/foodgram_workflow.yml/badge.svg)


**Foodgram** — это онлайн-сервис для публикации рецептов.

## Демо

- [Развернутый проект](http://89.169.188.80:8000)  
- [Административная панель](http://89.169.188.80:8000/admin/)  
- [Документация к API](http://89.169.188.80:8000/api/docs/)  

Данные для входа в админку:
```
superuser@mail.com
wBkyisAt
```

## Возможности
- Регистрация и авторизация пользователей  
- Смена пароля и загрузка аватара пользователя
- Создание, редактирование и удаление рецептов  
- Добавление рецептов в избранное
- Подписка на других пользователей
- Фильтрация рецептов по тегам
- Формирование списка покупок 
- Подсчет ингредиентов

## Примеры использования API:
- [Регистрация](http://89.169.188.80:8000/signup)  
- [Авторизация](http://89.169.188.80:8000/signin)  
- [Страница с рецептами](http://89.169.188.80:8000/recipes)  
- [Создать рецепт](http://89.169.188.80:8000/recipes/create)  
- [Текущий профиль](http://89.169.188.80:8000/user/me)  
- [Профиль администратора](http://89.169.188.80:8000/user/1)  
- [Смена пароля](http://89.169.188.80:8000/change-password)  
- [Избранные рецепты](http://89.169.188.80:8000/favorites)  
- [Список подписок](http://89.169.188.80:8000/subscriptions)  
- [Список покупок](http://89.169.188.80:8000/cart)  

## Установка и запуск локально

1. Клонировать репозитория:

```
git clone https://github.com/levinadev/foodgram.git
cd foodgram
```

2. Создать файл `.env` в корне проекта с таким содержимым:
```
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY='django-insecure-hlqrll@a+2wr-va9)0fw*r)+$)&i6*!u4na&z4z5b#2kx86=jo'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=89.169.188.80,foodgramanna.ddns.net,91.200.151.93,localhost,127.0.0.1
```

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