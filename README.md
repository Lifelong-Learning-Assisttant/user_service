# User Service

Сервис управления пользователями, аутентификацией и персональными настройками для системы Lifelong Learning Assistant.

## Функциональность

- **Аутентификация**: JWT-based (OAuth2 Password Flow).
- **Профили пользователей**: Хранение учетных данных в PostgreSQL.
- **Настройки LLM**: Персональный выбор моделей для Агента, RAG и Квизов.
- **История**: Хранение ссылок на сессии чатов и результатов прохождения тестов.
- **Изоляция**: Пользователи имеют доступ только к своим данным.
- **Безопасность**: Защита от brute force атак (блокировка после 5 попыток на 5 часов). Подробнее в [документации](docs/brute_force_protection.md).

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
docker exec user-service-dev uv run alembic upgrade head
```

> **Примечание**: В режиме разработки используется порт `8010`, чтобы избежать конфликта с RAG-сервисом.

## Управление пользователями (CLI)

Подробная информация об управлении пользователями, ролях и массовом создании доступна в [документации](docs/user_management.md).

```bash
# Регистрация нового пользователя (с ролью)
docker exec user-service-dev uv run python scripts/register_user.py <username> <password> [role]

# Массовое создание пользователей из JSON
docker cp users.json user-service-dev:/app/users.json
docker exec user-service-dev uv run python scripts/bulk_create_users.py users.json

# Список пользователей
docker exec user-service-dev uv run python scripts/list_users.py

# Удаление пользователя и всех его данных
docker exec user-service-dev uv run python scripts/delete_user.py <username>

# Массовое удаление пользователей
docker exec user-service-dev uv run python scripts/bulk_delete_users.py users.json
```

## Документация

Подробная информация доступна в папке `docs/`:
- [Управление пользователями](docs/user_management.md)
- [Архитектура и БД](docs/architecture.md)
- [Взаимодействие компонентов](docs/interaction.md)
- [Защита от Brute Force](docs/brute_force_protection.md)