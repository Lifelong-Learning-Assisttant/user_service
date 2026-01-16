# User Service

Сервис управления пользователями, аутентификацией и персональными настройками для системы Lifelong Learning Assistant.

## Функциональность

- **Аутентификация**: JWT-based (OAuth2 Password Flow).
- **Профили пользователей**: Хранение учетных данных в PostgreSQL.
- **Настройки LLM**: Персональный выбор моделей для Агента, RAG и Квизов.
- **История**: Хранение ссылок на сессии чатов и результатов прохождения тестов.
- **Изоляция**: Пользователи имеют доступ только к своим данным.

## Технологический стек

- **FastAPI** — веб-фреймворк.
- **PostgreSQL** — база данных.
- **SQLAlchemy (Async)** — ORM.
- **Alembic** — миграции.
- **Passlib (bcrypt)** — безопасность.

## Быстрый запуск (Разработка)

```bash
# Запуск сервиса и БД
docker compose -f docker-compose-dev.yml up -d

# Применение миграций (внутри контейнера)
docker exec user_service alembic upgrade head
```

## Управление пользователями (CLI)

Регистрация пользователей в прототипе осуществляется через скрипты:

```bash
# Регистрация нового пользователя
docker exec -it user_service python scripts/register_user.py <username> <password>

# Список пользователей
docker exec -it user_service python scripts/list_users.py

# Удаление пользователя
docker exec -it user_service python scripts/delete_user.py <username>
```

## Документация

Подробная информация доступна в папке `docs/`:
- [Архитектура и БД](docs/architecture.md)
- [Взаимодействие компонентов](docs/interaction.md)