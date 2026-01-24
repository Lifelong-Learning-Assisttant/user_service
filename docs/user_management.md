# Управление пользователями (CLI)

Для управления доступом к системе предусмотрен набор Python-скриптов, расположенных в директории `scripts/`. Эти скрипты позволяют выполнять административные задачи напрямую через контейнер `user-service`.

## Доступные скрипты

### 1. Регистрация пользователя (`register_user.py`)
Создает нового пользователя в системе.

**Синтаксис:**
```bash
docker exec user-service-dev uv run python scripts/register_user.py <username> <password> [role]
```
*   `<username>`: Имя пользователя (уникальное).
*   `<password>`: Пароль.
*   `[role]`: (Опционально) Роль пользователя: `user` (по умолчанию) или `developer`.

**Пример:**
```bash
docker exec user-service-dev uv run python scripts/register_user.py admin secret123 developer
```

---

### 2. Массовое создание пользователей (`bulk_create_users.py`)
Позволяет создать сразу несколько пользователей из JSON-файла.

**Синтаксис:**
```bash
# 1. Скопируйте файл в контейнер
docker cp users.json user-service-dev:/app/users.json

# 2. Запустите скрипт
docker exec user-service-dev uv run python scripts/bulk_create_users.py users.json
```

**Формат JSON-файла:**
```json
[
  {
    "username": "dev_user",
    "password": "password123",
    "role": "developer"
  },
  {
    "username": "student_01",
    "password": "password456",
    "role": "user"
  }
]
```

---

### 3. Просмотр списка пользователей (`list_users.py`)
Выводит список всех зарегистрированных пользователей, их ID, роли и дату создания.

**Синтаксис:**
```bash
docker exec user-service-dev uv run python scripts/list_users.py
```

---

### 4. Удаление пользователя (`delete_user.py`)
Удаляет пользователя и **все связанные с ним данные** (настройки, сессии чата, результаты тестов).

**Синтаксис:**
```bash
docker exec user-service-dev uv run python scripts/delete_user.py <username>
```

---

### 5. Массовое удаление пользователей (`bulk_delete_users.py`)
Позволяет массово удалить пользователей, указанных в JSON-файле.

**Синтаксис:**
```bash
# 1. Скопируйте файл в контейнер
docker cp users_to_delete.json user-service-dev:/app/users_to_delete.json

# 2. Запустите скрипт
docker exec user-service-dev uv run python scripts/bulk_delete_users.py users_to_delete.json
```

---

## Роли пользователей

В системе поддерживаются две основные роли:
1.  **`user`**: Обычный пользователь. Имеет доступ к чату и тестам. Видит только свои сессии.
2.  **`developer`**: Разработчик/Администратор. Имеет расширенный доступ, может видеть системные и тестовые сессии в Web UI.

## Интеграция с инициализацией сервера
Скрипт `./init-new-server.sh` автоматически ищет файл `users_to_create.json` в корне проекта и, если он найден, выполняет массовое создание пользователей при развертывании системы.