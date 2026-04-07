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

> [!NOTE]
> Ниже приведены инструкции по получению скриншотов после деплоя.

### 4.1 Сборка образов

```bash
docker build -t corp-news-backend:v1 ./src/backend
docker build -t corp-news-frontend:v1 ./src/frontend
```

**Скриншот успешной сборки:**
*(Место для скриншота)*

### 4.2 Статус подов в K8s

```bash
kubectl apply -f k8s/postgres-db.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl get pods
```

**Скриншот вывода kubectl get pods:**
*(Место для скриншота, все поды должны быть в статусе Running)*

### 4.3 Работа приложения

Приложение доступно по адресу: `http://localhost:30082`

1. **Лента новостей:**
*(Скриншот главной страницы с новостями)*

2. **Добавление новости:**
*(Скриншот заполненной формы добавления)*

3. **Аналитика:**
*(Скриншот графиков из вкладки Аналитика)*
