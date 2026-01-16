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

Сервис запускается в составе общей системы через корневой скрипт `start-dev.sh`.
Для изолированного запуска используйте:

```bash
# Запуск сервиса и БД
docker compose -f docker-compose-dev.yml up -d --build

# Применение миграций (внутри контейнера)
docker exec user-service-local uv run alembic upgrade head
```

> **Примечание**: В режиме разработки используется порт `8010`, чтобы избежать конфликта с RAG-сервисом.

## Управление пользователями (CLI)

Регистрация пользователей осуществляется через скрипты внутри контейнера:

```bash
# Регистрация нового пользователя
docker exec user-service-local uv run python scripts/register_user.py <username> <password>

# Список пользователей
docker exec user-service-local uv run python scripts/list_users.py

# Удаление пользователя
docker exec user-service-local uv run python scripts/delete_user.py <username>
```

## Документация

Подробная информация доступна в папке `docs/`:
- [Архитектура и БД](docs/architecture.md)
- [Взаимодействие компонентов](docs/interaction.md)