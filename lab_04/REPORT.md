# Отчет по лабораторной работе 4.1-4.2

## Тема: Создание и развертывание полнофункционального приложения в Kubernetes

### Вариант 2: Corp News Feed (Корпоративная лента новостей)

---

## 1. Описание архитектуры

Приложение представляет собой трехуровневую (three-tier) архитектуру, развернутую в кластере Kubernetes:

1. **Database (PostgreSQL)**: Хранилище новостей. Содержит таблицу `news` с полями: `id`, `title` (заголовок), `content` (текст), `date` (дата публикации), `category` (категория).
2. **Backend (FastAPI)**: RESTful API, написанное на Python. Выполняет CRUD-операции с базой данных через SQLAlchemy ORM.
    - `GET /news` — получение списка всех новостей.
    - `POST /news` — создание новой новости.
    - `DELETE /news/{id}` — удаление новости.
3. **Frontend (Streamlit)**: Интерактивный веб-интерфейс. Позволяет просматривать ленту, фильтровать новости по категориям, добавлять новые записи и просматривать аналитическую статистику.

**Схема взаимодействия:**
`User` <-> `news-frontend` <-> `news-backend` <-> `news-postgres`

---

## 2. Листинги кода

### 2.1 Backend (FastAPI)

**Файл: `src/backend/main.py`**

```python
# (Здесь приводится основная логика работы с БД и эндпоинты)
# Модель таблицы:
class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String)
```

**Файл: `src/backend/Dockerfile`**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.2 Frontend (Streamlit)

**Файл: `src/frontend/app.py`**

```python
# (Здесь приводится логика UI и обращения к API)
BACKEND_URL = os.getenv("BACKEND_URL", "http://news-backend-service:8000")
st.title("📰 Corp News Feed")
# ...
tabs = st.tabs(["📋 Лента новостей", "➕ Добавить новость", "📊 Аналитика"])
```

**Файл: `src/frontend/Dockerfile`**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 3. Kubernetes манифесты

Для каждого сервиса предусмотрен отдельный манифест:

1. **`k8s/postgres-db.yaml`**: Deployment и Service для базы данных PostgreSQL (`news-postgres-service`, порт 5432).
2. **`k8s/backend.yaml`**: Deployment и ClusterIP Service для API (`news-backend-service`, порт 8000).
3. **`k8s/frontend.yaml`**: Deployment и NodePort Service для фронтенда (`news-frontend-service`, доступ на порту 30082).

---

## 4. Результаты работы (Скриншоты)

### 4.1 Сборка образов

```bash
docker build -t corp-news-backend:v1 ./src/backend
docker build -t corp-news-frontend:v1 ./src/frontend
```
<img width="1152" height="495" alt="Снимок экрана 2026-04-07 150751" src="https://github.com/user-attachments/assets/8c7cbeb7-e587-49f4-a757-3aa7760db7c5" />
<img width="1103" height="523" alt="Снимок экрана 2026-04-07 150700" src="https://github.com/user-attachments/assets/892ba45d-4064-4984-a9f6-0cc91b2c47a4" />

### 4.2 Статус подов в K8s

```bash
kubectl apply -f k8s/postgres-db.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl get pods
```
<img width="1036" height="168" alt="image" src="https://github.com/user-attachments/assets/42f0e52d-e685-43f0-8b76-cab0c469e843" />
<img width="1125" height="169" alt="image" src="https://github.com/user-attachments/assets/258d14bd-0dd8-4a74-af67-570b39bfc91c" />
<img width="1148" height="100" alt="image" src="https://github.com/user-attachments/assets/1b9328df-d277-4ab0-aecf-a2f78c5a183d" />

### 4.3 Работа приложения

Приложение доступно по адресу: `http://localhost:30082`

1. **Лента новостей:**
*(Скриншот главной страницы с новостями)*

2. **Добавление новости:**
*(Скриншот заполненной формы добавления)*

3. **Аналитика:**
*(Скриншот графиков из вкладки Аналитика)*
