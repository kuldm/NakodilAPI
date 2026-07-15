# NakodilAPI

Небольшой сервис на FastAPI, который формирует отчёт по пользователю в фоне.

Запросили отчёт → получили `job_id` → периодически проверяете статус → забираете результат, когда готово.

---

## Требования

- Python **3.13**
- [uv](https://docs.astral.sh/uv/) — менеджер зависимостей и виртуальных окружений

---

## Быстрый старт

**1. Склонируйте репозиторий:**

```bash
git clone https://github.com/kuldm/NakodilAPI.git
cd NakodilAPI
```

**2. Создайте venv**

```bash
uv venv
```
И активируйте его

```bash
.venv\Scripts\activate
```
**3. Установите зависимости:**

```bash
uv sync
```

**4. Создайте `.env` из примера:**

```bash
cp .env_example .env
```

**5. Запустите сервер:**

```bash
uv run python src/main.py
```

Сервис поднимется на `http://localhost:8000`  
Документация: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Тесты

```bash
uv run pytest
```

---

## API


| Метод | Путь | Что делает |
|-------|------|------------|
| `POST` | `/reports/{user_id}` | Запускает формирование отчёта, возвращает `job_id` |
| `GET` | `/reports/jobs/{job_id}` | Статус задачи: `running` → `done` или `error` |
| `GET` | `/ping` | Проверка, что сервис жив |

### Как пользоваться

1. `POST /reports/1` → `{"job_id": 1, "status": "running"}`
2. `GET /reports/jobs/1` → ждёте, пока `"status": "done"`
3. В ответе будет `result` с данными пользователя и его todos

---

## Стек

Python 3.13 · uv · FastAPI · httpx · Pydantic · uvicorn · pytest
