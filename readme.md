# TeamFinder

Платформа для поиска команды на проект. Разработчики могут публиковать свои проекты, набирать участников и находить интересные проекты других авторов.

## Возможности

- Регистрация и авторизация по email
- Создание и редактирование проектов с GitHub-ссылкой
- Участие в чужих проектах и выход из них
- Добавление проектов в избранное
- Автоматическая генерация аватара при регистрации
- Список участников с фильтрацией
- Панель администратора

## Стек технологий

- **Python 3.12**
- **Django 5.x**
- **PostgreSQL** — основная база данных
- **Docker / Docker Compose** — запуск базы данных
- **Pillow** — генерация аватаров
- **django-crispy-forms** — стилизация форм
- **python-decouple** — управление переменными окружения

## Развёртывание

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd team-finder-ad
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv venv
```

- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Windows (cmd):** `venv\Scripts\activate`
- **Linux/Mac:** `source venv/bin/activate`

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить переменные окружения

Скопировать пример и заполнить значения:

```bash
cp .env_example .env
```

| Переменная          | Описание                                                                                         |
|---------------------|--------------------------------------------------------------------------------------------------|
| `DJANGO_SECRET_KEY` | Секретный ключ Django. Сгенерировать: `from django.core.management.utils import get_random_secret_key` |
| `DJANGO_DEBUG`      | Режим отладки. `True` для разработки, `False` для продакшена.                                   |
| `ALLOWED_HOSTS`     | Список хостов через запятую, например `localhost,127.0.0.1`                                     |
| `POSTGRES_DB`       | Имя базы данных PostgreSQL.                                                                      |
| `POSTGRES_USER`     | Имя пользователя PostgreSQL.                                                                     |
| `POSTGRES_PASSWORD` | Пароль пользователя PostgreSQL.                                                                  |
| `POSTGRES_HOST`     | Адрес сервера БД. По умолчанию `localhost`.                                                      |
| `POSTGRES_PORT`     | Порт подключения к БД. По умолчанию `5432`.                                                     |

### 5. Запустить базу данных

```bash
docker compose up -d
```

Остановить:

```bash
docker compose down
```

### 6. Применить миграции и запустить сервер

```bash
python manage.py migrate
python manage.py runserver
```

Проект доступен по адресу [http://localhost:8000](http://localhost:8000).

## Автор

[flavvvour](https://github.com/flavvvour)
