from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
import time

# ──────────────────────────────────────────────
# Подключение к PostgreSQL через переменные окружения
# ──────────────────────────────────────────────
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "news_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ──────────────────────────────────────────────
# Модель таблицы «Новости» (Variant 2)
# ──────────────────────────────────────────────
class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)          # Заголовок
    content = Column(Text)                      # Текст новости
    date = Column(DateTime, default=datetime.datetime.utcnow) # Дата
    category = Column(String)                   # Категория

# ──────────────────────────────────────────────
# Ожидание готовности БД (с повторными попытками)
# ──────────────────────────────────────────────
MAX_RETRIES = 30
for attempt in range(MAX_RETRIES):
    try:
        Base.metadata.create_all(bind=engine)
        print(f"✅ БД подключена (попытка {attempt + 1})")
        # Добавим тестовую новость если таблица пуста
        db = SessionLocal()
        if db.query(News).count() == 0:
            initial_news = News(
                title="Добро пожаловать в Corp News Feed!",
                content="Это первая корпоративная новость. Проверьте функционал добавления новостей на главной странице.",
                category="Общее"
            )
            db.add(initial_news)
            db.commit()
        db.close()
        break
    except Exception as e:
        print(f"⏳ Ожидание БД... попытка {attempt + 1}/{MAX_RETRIES}: {e}")
        time.sleep(2)
else:
    raise RuntimeError("❌ Не удалось подключиться к БД после 30 попыток")

# ──────────────────────────────────────────────
# FastAPI приложение
# ──────────────────────────────────────────────
app = FastAPI(title="Corp News API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
# Pydantic-схема для валидации входных данных
# ──────────────────────────────────────────────
class NewsModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)

# ──────────────────────────────────────────────
# CRUD-эндпоинты
# ──────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Corp News API is running"}

@app.get("/news")
def get_news():
    """Получить список всех новостей."""
    db = SessionLocal()
    news_list = db.query(News).order_by(News.date.desc()).all()
    db.close()
    return [
        {
            "id": n.id, 
            "title": n.title, 
            "content": n.content, 
            "date": n.date.isoformat(), 
            "category": n.category
        }
        for n in news_list
    ]

@app.post("/news")
def add_news(news: NewsModel):
    """Добавить новую новость."""
    db = SessionLocal()
    new_news = News(
        title=news.title,
        content=news.content,
        category=news.category
    )
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    db.close()
    return {
        "id": new_news.id, 
        "title": new_news.title, 
        "content": new_news.content, 
        "date": new_news.date.isoformat(), 
        "category": new_news.category
    }

@app.delete("/news/{news_id}")
def delete_news(news_id: int):
    """Удалить новость по ID."""
    db = SessionLocal()
    news_item = db.query(News).filter(News.id == news_id).first()
    if not news_item:
        db.close()
        raise HTTPException(status_code=404, detail="Новость не найдена")
    db.delete(news_item)
    db.commit()
    db.close()
    return {"detail": f"Новость {news_id} удалена"}
