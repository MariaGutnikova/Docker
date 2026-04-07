import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
import time
from datetime import datetime

# ──────────────────────────────────────────────
# Конфигурация
# ──────────────────────────────────────────────
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:8000")

st.set_page_config(
    page_title="Corp News Feed",
    page_icon="📰",
    layout="wide",
)

# Инициализация темы
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ──────────────────────────────────────────────
# CSS-стили
# ──────────────────────────────────────────────
def get_css(theme: str) -> str:
    if theme == "dark":
        return """
        <style>
            :root {
                --bg-primary: #0f172a;
                --bg-card: #1e293b;
                --accent: #38bdf8;
                --text-primary: #f8fafc;
                --text-secondary: #94a3b8;
            }
            .stApp { background-color: var(--bg-primary); color: var(--text-primary); }
            .news-card {
                background: var(--bg-card);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                border-left: 5px solid var(--accent);
                box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            }
            .news-title { font-size: 1.5rem; font-weight: 700; color: var(--accent); margin-bottom: 8px; }
            .news-meta { font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 12px; }
            .news-content { line-height: 1.6; }
            .category-badge {
                display: inline-block;
                padding: 2px 10px;
                background: rgba(56, 189, 248, 0.2);
                color: var(--accent);
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 600;
                margin-right: 10px;
            }
        </style>
        """
    else:
        return """
        <style>
            :root {
                --bg-primary: #f8fafc;
                --bg-card: #ffffff;
                --accent: #0284c7;
                --text-primary: #0f172a;
                --text-secondary: #475569;
            }
            .stApp { background-color: var(--bg-primary); color: var(--text-primary); }
            .news-card {
                background: var(--bg-card);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                border-left: 5px solid var(--accent);
                box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
            }
            .news-title { font-size: 1.5rem; font-weight: 700; color: var(--accent); margin-bottom: 8px; }
            .news-meta { font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 12px; }
            .news-content { line-height: 1.6; }
            .category-badge {
                display: inline-block;
                padding: 2px 10px;
                background: rgba(2, 132, 199, 0.1);
                color: var(--accent);
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 600;
                margin-right: 10px;
            }
        </style>
        """

st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Заголовок
# ──────────────────────────────────────────────
st.title("📰 Corp News Feed")
st.markdown("---")

# ──────────────────────────────────────────────
# Сайдбар
# ──────────────────────────────────────────────
with st.sidebar:
    st.header("Настройки")
    if st.button("Сменить тему"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()
    
    st.markdown("---")
    st.subheader("Статус Backend")
    try:
        r = requests.get(f"{BACKEND_URL}/", timeout=2)
        if r.status_code == 200:
            st.success("Онлайн ✅")
        else:
            st.warning(f"Ошибка {r.status_code}")
    except:
        st.error("Оффлайн ❌")

# ──────────────────────────────────────────────
# Основной интерфейс
# ──────────────────────────────────────────────
tabs = st.tabs(["📋 Лента новостей", "➕ Добавить новость", "📊 Аналитика"])

# --- TAB 1: Лента ---
with tabs[0]:
    st.header("Последние новости")
    try:
        res = requests.get(f"{BACKEND_URL}/news", timeout=5)
        if res.status_code == 200:
            news_items = res.json()
            if not news_items:
                st.info("Новостей пока нет.")
            else:
                # Фильтр по категории
                categories = ["Все"] + sorted(list(set(n["category"] for n in news_items)))
                selected_cat = st.selectbox("Фильтр по категории", categories)
                
                for n in news_items:
                    if selected_cat != "Все" and n["category"] != selected_cat:
                        continue
                        
                    date_obj = datetime.fromisoformat(n["date"])
                    date_str = date_obj.strftime("%d.%m.%Y %H:%M")
                    
                    st.markdown(f"""
                    <div class="news-card">
                        <div class="news-title">{n['title']}</div>
                        <div class="news-meta">
                            <span class="category-badge">{n['category']}</span>
                            📅 {date_str}
                        </div>
                        <div class="news-content">{n['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Удалить noticia #{n['id']}", key=f"del_{n['id']}"):
                        requests.delete(f"{BACKEND_URL}/news/{n['id']}")
                        st.rerun()
        else:
            st.error("Ошибка при получении данных с сервера.")
    except Exception as e:
        st.error(f"Не удалось подключиться к Backend: {e}")

# --- TAB 2: Добавление ---
with tabs[1]:
    st.header("Опубликовать новость")
    with st.form("add_news_form"):
        title = st.text_input("Заголовок")
        content = st.text_area("Текст новости")
        category = st.selectbox("Категория", ["Общее", "IT", "HR", "Спорт", "Кухня", "Мероприятия"])
        submitted = st.form_submit_button("Опубликовать")
        
        if submitted:
            if not title or not content:
                st.error("Заполните все поля!")
            else:
                payload = {"title": title, "content": content, "category": category}
                try:
                    res = requests.post(f"{BACKEND_URL}/news", json=payload)
                    if res.status_code == 200:
                        st.success("Новость успешно опубликована!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Ошибка: {res.text}")
                except Exception as e:
                    st.error(f"Ошибка соединения: {e}")

# --- TAB 3: Аналитика ---
with tabs[2]:
    st.header("Статистика публикаций")
    try:
        res = requests.get(f"{BACKEND_URL}/news")
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("По категориям")
                    fig_cat = px.pie(df, names="category", hole=0.4)
                    st.plotly_chart(fig_cat, use_container_width=True)
                
                with col2:
                    st.subheader("По датам")
                    df['date'] = pd.to_datetime(df['date']).dt.date
                    df_dates = df.groupby('date').size().reset_index(name='count')
                    fig_time = px.line(df_dates, x='date', y='count', markers=True)
                    st.plotly_chart(fig_time, use_container_width=True)
            else:
                st.info("Нет данных для анализа.")
    except:
        st.error("Ошибка при загрузке аналитики.")
