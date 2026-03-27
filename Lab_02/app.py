import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Автоматически загружаем переменные из .env из корня проекта
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

DATA_PATH   = os.getenv("DATA_PATH", "/data/hr_data.csv")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/output/chart.png")

# Если файл .env найден, он переопределит дефолты выше.
# Если мы на Windows и в .env пути типа /data/..., поправим их для локального запуска:
if not os.path.exists(os.path.dirname(DATA_PATH)) and not DATA_PATH.startswith('/'):
    # Вероятно, запуск локальный, пробуем найти папку относительно скрипта
    DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'hr_data.csv'))
    OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'chart.png'))

print("=" * 60)
print("  HR & RETENTION ANALYTICS — Вариант 2")
print("=" * 60)

# Генерируем или загружаем данные
if not os.path.exists(DATA_PATH):
    print(f"[!] Файл {DATA_PATH} не найден. Работа в режиме генерации...")
    import numpy as np
    from datetime import datetime, timedelta
    np.random.seed(42)
    N = 100
    df = pd.DataFrame({
        "hire_date": [datetime(2023, 1, 1) + timedelta(days=i*7) for i in range(N)],
        "satisfaction_level": np.random.uniform(0.3, 0.9, N)
    })
else:
    df = pd.read_csv(DATA_PATH)
    print(f"\nДатасет загружен: {DATA_PATH}")

# Преобразование даты
df['hire_date'] = pd.to_datetime(df['hire_date'])

# Группировка: Средний уровень удовлетворенности по месяцам (Time Series)
time_series = df.resample('M', on='hire_date')['satisfaction_level'].mean().round(2)

print("\n── Динамика удовлетворенности сотрудников ────────────────")
print(time_series.tail(10).to_string())

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(time_series.index, time_series.values, marker='o', linestyle='-', color='#2c3e50', linewidth=2, markersize=8)
plt.title('Тренд удовлетворенности персонала (Вариант 2)', fontsize=14, pad=15)
plt.xlabel('Дата приема на работу (Месяц)', fontsize=12)
plt.ylabel('Средний Satisfaction Score', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()

# Сохранение результата
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=150)
plt.close()

print(f"\n[✓] Линейный график сохранен: {OUTPUT_PATH}")
print("=" * 60)
