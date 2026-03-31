import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import numpy as np

# Загрузка .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

DATA_PATH   = os.getenv("DATA_PATH", "/data/hr_data.csv")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/output/chart.png")

# Коррекция путей для локального запуска
if not os.path.exists(os.path.dirname(DATA_PATH)) and not DATA_PATH.startswith('/'):
    DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'hr_data.csv'))
    OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'chart.png'))

print("=" * 60)
print("  HR & RETENTION ANALYTICS — Вариант 2 (с линией тренда)")
print("=" * 60)

# Загрузка или генерация данных
if not os.path.exists(DATA_PATH):
    print(f"[!] Файл {DATA_PATH} не найден. Генерация тестовых данных...")
    
    from datetime import datetime, timedelta
    np.random.seed(42)
    N = 100

    df = pd.DataFrame({
        "hire_date": [datetime(2023, 1, 1) + timedelta(days=i * 7) for i in range(N)],
        "satisfaction_level": np.random.uniform(0.3, 0.9, N)
    })
else:
    df = pd.read_csv(DATA_PATH)
    print(f"\n[✓] Датасет загружен: {DATA_PATH}")

# Преобразование даты
df['hire_date'] = pd.to_datetime(df['hire_date'])

# Агрегация по месяцам
time_series = df.resample('M', on='hire_date')['satisfaction_level'].mean().round(3)

print("\n── Динамика удовлетворенности сотрудников ────────────────")
print(time_series.tail(10).to_string())

# =============================
# 📈 Построение графика
# =============================
plt.figure(figsize=(10, 6))

# Основной график
plt.plot(
    time_series.index,
    time_series.values,
    marker='o',
    linestyle='-',
    linewidth=2,
    markersize=6,
    label='Фактические значения'
)

# =============================
# 📊 Линия тренда (линейная регрессия)
# =============================
x = np.arange(len(time_series))
y = time_series.values

# Вычисление коэффициентов (y = ax + b)
coeffs = np.polyfit(x, y, 1)
trend_line = np.poly1d(coeffs)

# Построение линии тренда
plt.plot(
    time_series.index,
    trend_line(x),
    linestyle='--',
    linewidth=2,
    label='Линия тренда'
)

# =============================
# 📌 Оформление
# =============================
plt.title('Тренд удовлетворенности персонала (с линией тренда)', fontsize=14, pad=15)
plt.xlabel('Дата приема (Месяц)', fontsize=12)
plt.ylabel('Средний Satisfaction Score', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Сохранение графика
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=150)
plt.close()

# =============================
# 📊 Аналитика
# =============================
slope = coeffs[0]

print("\n── Анализ тренда ─────────────────────────────────────────")
print(f"Коэффициент тренда (наклон): {slope:.5f}")

if slope > 0:
    print("📈 Тренд: Удовлетворенность РАСТЕТ")
elif slope < 0:
    print("📉 Тренд: Удовлетворенность ПАДАЕТ")
else:
    print("➖ Тренд: Без изменений")

print(f"\n[✓] График сохранен: {OUTPUT_PATH}")
print("=" * 60)
