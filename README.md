# API Yatube

REST API для социальной сети Yatube на Django REST Framework.

## Возможности

- CRUD для постов, групп и комментариев
- TokenAuthentication
- Права доступа по авторству

## Технологии

- Django 5.1.1 + DRF 3.15.2
- Python 3.12+

## Установка

```bash
pip install -r requirements.txt
cp .env.example .env  # установить SECRET_KEY
python yatube_api/manage.py migrate
python yatube_api/manage.py runserver
```

## API

- `POST /api/v1/api-token-auth/` - получить токен (логин + пароль)
- `GET,POST /api/v1/posts/` - список постов / создать пост
- `GET,PUT,PATCH,DELETE /api/v1/posts/{post_id}/` - операции с постом
- `GET /api/v1/groups/` - список групп
- `GET /api/v1/groups/{group_id}/` - информация о группе
- `GET,POST /api/v1/posts/{post_id}/comments/` - комментарии поста
- `GET,PUT,PATCH,DELETE /api/v1/posts/{post_id}/comments/{comment_id}/` - операции с комментарием

## Аутентификация

```bash
Authorization: Token your_token_here
```
