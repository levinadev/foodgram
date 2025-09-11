# Foodgram

![CI/CD](https://github.com/levinadev/foodgram/actions/workflows/main.yml/badge.svg)

**Foodgram** — это онлайн-сервис для публикации рецептов.

## Демо

- [Развернутый проект](https://foodgramanna.ddns.net)  
- [Административная панель](https://foodgramanna.ddns.net/admin/)  
- [Документация к API](https://foodgramanna.ddns.net/api/docs/)  


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
- [Регистрация](https://foodgramanna.ddns.net/signup)  
- [Авторизация](https://foodgramanna.ddns.net/signin)  
- [Страница с рецептами](https://foodgramanna.ddns.net/recipes)  
- [Создать рецепт](https://foodgramanna.ddns.net/recipes/create)
- [Текущий профиль](https://foodgramanna.ddns.net/user/me)  
- [Профиль администратора](https://foodgramanna.ddns.net/user/1)  
- [Смена пароля](https://foodgramanna.ddns.net/change-password)  
- [Избранные рецепты](https://foodgramanna.ddns.net/favorites)  
- [Список подписок](https://foodgramanna.ddns.net/subscriptions)  
- [Список покупок](https://foodgramanna.ddns.net/cart)  

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