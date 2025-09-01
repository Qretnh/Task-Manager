# Task Manager API

Асинхронный менеджер задач на FastAPI с PostgreSQL, SQLAlchemy, Alembic и Docker.

## Основные возможности

* CRUD API для задач:

  * `POST /tasks/` – создание задачи
  * `GET /tasks/` – получение списка задач
  * `GET /tasks/{task_id}` – получение задачи по ID
  * `PUT /tasks/{task_id}` – обновление задачи
  * `DELETE /tasks/{task_id}` – удаление задачи
* Асинхронная работа с базой данных (SQLAlchemy + asyncpg)
* Логгирование действий через `logging`
* Полное разделение по модулям:

  * `models` – модели базы данных
  * `schemas` – Pydantic-схемы для валидации
  * `api` – роутеры FastAPI
  * `services/db` – бизнес-логика для работы с базой
  * `core/logger.py` – централизованное логгирование
* Управление миграциями через Alembic
* Тесты через pytest (80%+ покрытия)
* Качество кода обеспечивается Flake8, Black и isort
* Конфигурация через переменные окружения
* Docker Compose для быстрого поднятия `backend + PostgreSQL`
* Makefile для базовых команд (`start`, `migrate`, `test`, `lint`)

---

## Установка и запуск

### Через Docker Compose
1. Скопировать содержимое файла .env.example в .env
```bash
2. docker-compose up --build
```

API будет доступен по адресу: `http://localhost:8000`

Документация : `http://localhost:8000/docs#/`

---

## Миграции базы данных

```bash
# Установить миграцию
make migrate
```

---

## Тестирование

```bash
make test-cov
```

---

## Makefile (пример)

```make
migrate:
	docker-compose exec backend alembic -c ./app/alembic.ini upgrade head

lint:
	flake8 ./app

format:
	black .

isort:
	isort .

test-cov:
	pytest tests/ --cov=app --cov-report=term-missing
```

---

## Переменные окружения

* `POSTGRES_USER` – пользователь базы данных
* `POSTGRES_PASSWORD` – пароль
* `POSTGRES_DB` – имя базы данных
* `DATABASE_URL` – строка подключения к базе (может быть с asyncpg)

---

## Структура проекта

```
app/
├─ api/           # Роутеры FastAPI
├─ config/        # Настройки проекта
├─ alembic/       # Миграции Alembic
├─ core/          # Логгирование, конфиги
├─ db/            # Сессии и подключение к БД
├─ models/        # SQLAlchemy модели
├─ schemas/       # Pydantic схемы
├─ services/      # Бизнес-логика работы с базой
├─ main.py        # Точка входа FastAPI
├─ requirements.txt
├─ Dockerfile
tests/            
├─ conftest.py    # Настройки окружения и тестов
├─ api_test.py    # Интеграционные тесты 
├─ db_test.py     # Тесты работы с БД
docker-compose.yml
Makefile
.env
```
